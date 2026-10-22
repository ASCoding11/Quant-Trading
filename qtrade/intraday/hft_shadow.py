"""Shadow high-frequency trader: simulated trades on live quotes, every one of them logged.

Nothing here touches the Alpaca account; Alpaca only supplies the live IEX quotes and
trades (its free real-time feed). The simulation is event-driven: every quote update and
trade is replayed in time order, decisions are made the moment the data arrives, and
every order reaches the market ``latency`` later (5 ms + up to 5 ms of random jitter by
default) - it executes at the price quoted *then*, not at the decision. Fees are 0 bp.

Strategies, on a handful of liquid stocks:

* ``imbalance_taker`` - when the book turns lopsided (|quote imbalance| >= 0.6: far more
  shares bid than offered, or the reverse), buy at the ask / sell at the bid; 30 s later
  get out the same way (also after the latency);
* ``market_maker`` - every 10 s, send one order to the best bid and one to the best ask,
  live for 10 s once they arrive; a resting order fills when a trade prints at its price
  or through it. Exits 30 s after the fill at the quoted price (``pnl_bp``) and, for
  reference, at the midquote (``pnl_mid_bp``);
* ``maker_with_signal`` - the same, quoting only the side the imbalance favours.

IEX's own book is thinner and wider than the national best bid and offer. With
``GOOGLE_SERVICE_ACCOUNT_JSON`` and ``HFT_SHEET_ID`` set, new trades and the per-strategy
summary go straight into the Google Sheet's "HFT trades" tab every few seconds.
"""
from __future__ import annotations

import json
import os
import random
import time
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd

from ..data.loader import to_alpaca
from ..utils import LOG

NY = "America/New_York"
QUOTES_URL = "https://data.alpaca.markets/v2/stocks/quotes"
TRADES_URL = "https://data.alpaca.markets/v2/stocks/trades"
SYMBOLS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "TSLA", "META", "AMD", "BAC"]
FEE_BP = 0.0                    # the sheet's assumption: no fees at all
LATENCY_MS = 5.0                # every order reaches the market this long after the decision ...
JITTER_MS = 5.0                 # ... plus a uniform random 0-5 ms
IMB_THRESHOLD = 0.6
MAX_SPREAD_BP = 25.0            # ignore broken / one-sided IEX quotes (e.g. a 328 bp TSLA quote on 2026-10-22)
HOLD_S = 30
MM_EVERY_S = 10
MM_WAIT_S = 10
COLUMNS = ["strategy", "symbol", "side", "decision_time", "entry_time", "entry_price", "exit_time", "exit_price",
           "pnl_bp", "pnl_mid_bp", "spread_bp", "imbalance", "latency_ms"]


class Book:
    """Latest IEX top of book for one symbol."""

    def __init__(self):
        self.bid = self.ask = np.nan
        self.bsize = self.asize = np.nan

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def ok(self) -> bool:
        return bool(np.isfinite(self.bid) and np.isfinite(self.ask) and self.ask > self.bid > 0
                    and self.bsize > 0 and self.asize > 0)

    @property
    def imbalance(self) -> float:
        return float((self.bsize - self.asize) / (self.bsize + self.asize)) if self.ok else np.nan

    @property
    def spread_bp(self) -> float:
        return float((self.ask - self.bid) / self.mid * 1e4) if self.ok else np.nan


class ShadowHFT:
    """Event-driven state machine. Feed it quotes and trades in time order; orders execute after
    the latency at the book prevailing then."""

    def __init__(self, symbols: list[str], latency_ms: float = LATENCY_MS, jitter_ms: float = JITTER_MS,
                 seed: int = 0):
        self.books = {s: Book() for s in symbols}
        self.latency_ms, self.jitter_ms = latency_ms, jitter_ms
        self.rng = random.Random(seed)
        self.pending: list[dict] = []              # market orders on their way (entries and exits)
        self.positions: list[dict] = []            # open positions waiting for their exit decision
        self.resting: list[dict] = []              # maker orders (live from ``live_at`` to ``expires``)
        self.closed: list[dict] = []
        self.last_mm: dict[str, pd.Timestamp] = defaultdict(lambda: pd.Timestamp(0, tz="UTC"))
        self.taker_busy_until: dict[str, pd.Timestamp] = defaultdict(lambda: pd.Timestamp(0, tz="UTC"))

    def _delay(self) -> pd.Timedelta:
        return pd.Timedelta(milliseconds=self.latency_ms + self.rng.uniform(0, self.jitter_ms))

    # --- time ------------------------------------------------------------------------------------
    def advance(self, t: pd.Timestamp) -> None:
        """Everything due strictly before ``t`` happens against the book as it stands (the book
        prevailing until the event at ``t``)."""
        while True:
            due = [(o["exec_at"], 0, i) for i, o in enumerate(self.pending) if o["exec_at"] < t] + \
                  [(p["exit_decide_at"], 1, i) for i, p in enumerate(self.positions) if p["exit_decide_at"] < t]
            if not due:
                break
            _, kind, i = min(due, key=lambda d: (d[0], d[1]))
            if kind == 0:
                self._execute(self.pending.pop(i))
            else:                                    # time to get out: send the exit order
                p = self.positions.pop(i)
                self.pending.append({**p, "kind": "exit", "exec_at": p["exit_decide_at"] + self._delay()})

    def _execute(self, o: dict) -> None:
        b = self.books[o["symbol"]]
        if not b.ok:
            return
        if o["kind"] == "entry":
            px = b.ask if o["side"] == "buy" else b.bid
            self.positions.append({**o, "entry_time": o["exec_at"], "entry_price": px,
                                   "exit_decide_at": o["exec_at"] + pd.Timedelta(seconds=HOLD_S)})
            return
        exit_px = b.bid if o["side"] == "buy" else b.ask
        d = 1.0 if o["side"] == "buy" else -1.0
        self.closed.append({"strategy": o["strategy"], "symbol": o["symbol"], "side": o["side"],
                            "decision_time": o["decision_time"], "entry_time": o["entry_time"],
                            "entry_price": o["entry_price"], "exit_time": o["exec_at"], "exit_price": exit_px,
                            "pnl_bp": d * (exit_px / o["entry_price"] - 1) * 1e4 - FEE_BP,
                            "pnl_mid_bp": d * (b.mid / o["entry_price"] - 1) * 1e4 - FEE_BP,
                            "spread_bp": o["spread_bp"], "imbalance": o["imbalance"],
                            "latency_ms": o["latency_ms"]})

    # --- inputs -----------------------------------------------------------------------------------
    def on_quote(self, sym: str, t: pd.Timestamp, bid: float, bsize: float, ask: float, asize: float) -> None:
        self.advance(t)
        b = self.books[sym]
        if not (bid > 0 and ask > bid and bsize > 0 and asize > 0):
            return
        b.bid, b.bsize, b.ask, b.asize = bid, bsize, ask, asize
        imb = b.imbalance
        if abs(imb) >= IMB_THRESHOLD and b.spread_bp <= MAX_SPREAD_BP and t >= self.taker_busy_until[sym]:
            delay = self._delay()
            self.pending.append({"kind": "entry", "strategy": "imbalance_taker", "symbol": sym,
                                 "side": "buy" if imb > 0 else "sell", "decision_time": t, "exec_at": t + delay,
                                 "spread_bp": b.spread_bp, "imbalance": imb,
                                 "latency_ms": delay.total_seconds() * 1e3})
            self.taker_busy_until[sym] = t + delay + pd.Timedelta(seconds=HOLD_S) + pd.Timedelta(seconds=1)

    def on_trade(self, sym: str, t: pd.Timestamp, price: float, size: float) -> None:
        self.advance(t)
        for o in list(self.resting):
            if o["symbol"] != sym or t < o["live_at"] or t > o["expires"]:
                continue
            if (o["side"] == "buy" and price <= o["price"]) or (o["side"] == "sell" and price >= o["price"]):
                self.resting.remove(o)
                self.positions.append({**o, "kind": "maker", "entry_time": t, "entry_price": o["price"],
                                       "exit_decide_at": t + pd.Timedelta(seconds=HOLD_S)})

    def step(self, now: pd.Timestamp) -> None:
        """Clock tick: run everything due, expire resting orders, send the next maker quotes."""
        self.advance(now)
        self.resting = [o for o in self.resting if o["expires"] >= now]
        for sym, b in self.books.items():
            if not b.ok or b.spread_bp > MAX_SPREAD_BP or now - self.last_mm[sym] < pd.Timedelta(seconds=MM_EVERY_S):
                continue
            self.last_mm[sym] = now
            imb = b.imbalance
            for side, px in (("buy", b.bid), ("sell", b.ask)):
                delay = self._delay()
                base = {"symbol": sym, "side": side, "price": px, "decision_time": now, "live_at": now + delay,
                        "expires": now + delay + pd.Timedelta(seconds=MM_WAIT_S), "spread_bp": b.spread_bp,
                        "imbalance": imb, "latency_ms": delay.total_seconds() * 1e3}
                self.resting.append({**base, "strategy": "market_maker"})
                if (side == "buy" and imb > 0) or (side == "sell" and imb < 0):
                    self.resting.append({**base, "strategy": "maker_with_signal"})

    def take_closed(self) -> pd.DataFrame:
        out, self.closed = self.closed, []
        return pd.DataFrame(out, columns=COLUMNS)


# -----------------------------------------------------------------------------
# Google Sheet (optional): the trade log every few seconds
# -----------------------------------------------------------------------------
class SheetWriter:
    """Appends trades to the 'HFT trades' tab and rewrites its summary, through a service account."""

    TAB = "HFT trades"

    def __init__(self, sheet_id: str, creds_json: str):
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account

        creds = service_account.Credentials.from_service_account_info(
            json.loads(creds_json), scopes=["https://www.googleapis.com/auth/spreadsheets"])
        self.s = AuthorizedSession(creds)
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"

    @staticmethod
    def _rows(trades: pd.DataFrame) -> list[list]:
        def ny(ts):
            return pd.Timestamp(ts).tz_convert(NY).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return [[r.strategy, r.symbol, r.side, ny(r.entry_time), round(float(r.entry_price), 4), ny(r.exit_time),
                 round(float(r.exit_price), 4), round(float(r.pnl_bp), 3), round(float(r.pnl_mid_bp), 3),
                 round(float(r.spread_bp), 3), round(float(r.imbalance), 3), round(float(r.latency_ms), 2)]
                for r in trades.itertuples()]

    def append(self, trades: pd.DataFrame) -> None:
        if trades.empty:
            return
        r = self.s.post(f"{self.base}/values/'{self.TAB}'!A6:L:append",
                        params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
                        json={"values": self._rows(trades)}, timeout=30)
        r.raise_for_status()

    def status(self, text: str, summary_rows: list[list]) -> None:
        data = [{"range": f"'{self.TAB}'!A3", "values": [[text]]},
                {"range": f"'{self.TAB}'!N4:S{4 + len(summary_rows)}", "values": summary_rows}]
        r = self.s.post(f"{self.base}/values:batchUpdate", json={"valueInputOption": "RAW", "data": data}, timeout=30)
        r.raise_for_status()


def summary(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    g = trades.groupby("strategy")
    return pd.DataFrame({"trades": g.size(), "avg_pnl_bp": g["pnl_bp"].mean(), "avg_pnl_mid_bp": g["pnl_mid_bp"].mean(),
                         "hit_rate": g["pnl_bp"].apply(lambda x: (x > 0).mean()),
                         "avg_latency_ms": g["latency_ms"].mean()}).reset_index()


def _summary_rows(all_trades: pd.DataFrame) -> list[list]:
    head = [["Strategy", "Trades", "Avg P&L bp", "Avg P&L mid bp", "Hit rate", "Avg latency ms"]]
    s = summary(all_trades)
    return head + [[r.strategy, int(r.trades), round(r.avg_pnl_bp, 3), round(r.avg_pnl_mid_bp, 3),
                    round(r.hit_rate, 3), round(r.avg_latency_ms, 2)] for r in s.itertuples()]


def _pull(client, url: str, key: str, symbols: list[str], start: pd.Timestamp, end: pd.Timestamp) -> dict:
    params = {"symbols": ",".join(to_alpaca(s) for s in symbols), "start": start.isoformat(),
              "end": end.isoformat(), "limit": 10000, "feed": "iex", "sort": "asc"}
    out: dict[str, list] = defaultdict(list)
    for _ in range(10):
        data = client._get(params, url)
        for sym, rows in (data.get(key) or {}).items():
            out[sym] += rows
        token = data.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    return out


def run(minutes: float, out_dir: str | Path = "logs/hft", symbols: list[str] | None = None,
        poll_s: float = 1.0, sheet_every_s: float = 5.0) -> Path | None:
    """Trade in the shadow until ``minutes`` have passed or the market closes; returns the trade log."""
    from ..data.intraday import AlpacaBars

    symbols = symbols or SYMBOLS
    client = AlpacaBars(feed="iex", per_minute=140)     # leaves headroom for other data calls
    hft = ShadowHFT(symbols, seed=int(time.time()))
    sheet = None
    if os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON") and os.environ.get("HFT_SHEET_ID"):
        try:
            sheet = SheetWriter(os.environ["HFT_SHEET_ID"], os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
            LOG.info("shadow HFT: writing to the Google Sheet every %.0f s", sheet_every_s)
        except Exception as exc:
            LOG.warning("Google Sheet unavailable (%s) - log file only", exc.__class__.__name__)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"hft_trades_{pd.Timestamp.now(tz=NY):%Y%m%d_%H%M}.csv"
    stop = time.time() + minutes * 60
    last = pd.Timestamp.now(tz="UTC") - pd.Timedelta(seconds=5)
    unsent, everything = [], []
    last_sheet = 0.0
    while time.time() < stop:
        now_ny = pd.Timestamp.now(tz=NY)
        hm = now_ny.hour * 60 + now_ny.minute
        if now_ny.weekday() >= 5 or hm >= 16 * 60:
            break
        if hm < 9 * 60 + 31:                            # skip the opening auction's aftermath
            time.sleep(10)
            last = pd.Timestamp.now(tz="UTC") - pd.Timedelta(seconds=5)
            continue
        now = pd.Timestamp.now(tz="UTC")
        try:
            quotes = _pull(client, QUOTES_URL, "quotes", symbols, last, now)
            trades = _pull(client, TRADES_URL, "trades", symbols, last, now)
        except Exception as exc:
            LOG.warning("shadow HFT poll failed: %s", exc)
            time.sleep(poll_s)
            continue
        events = []
        for sym, rows in quotes.items():
            events += [(pd.Timestamp(q["t"]), 0, sym, q) for q in rows]
        for sym, rows in trades.items():
            events += [(pd.Timestamp(r["t"]), 1, sym, r) for r in rows]
        for t, kind, sym, r in sorted(events, key=lambda e: (e[0], e[1])):
            sym = sym.replace(".", "-")
            if sym not in hft.books:
                continue
            if kind == 0:
                hft.on_quote(sym, t, r.get("bp", 0), r.get("bs", 0), r.get("ap", 0), r.get("as", 0))
            else:
                hft.on_trade(sym, t, r.get("p", 0), r.get("s", 0))
        hft.step(now)
        done = hft.take_closed()
        if len(done):
            done.to_csv(path, mode="a", header=not path.exists(), index=False)
            unsent.append(done)
            everything.append(done)
        if sheet is not None and time.time() - last_sheet >= sheet_every_s:
            last_sheet = time.time()
            try:
                new = pd.concat(unsent, ignore_index=True) if unsent else pd.DataFrame(columns=COLUMNS)
                sheet.append(new)
                unsent = []
                total = pd.concat(everything, ignore_index=True) if everything else pd.DataFrame(columns=COLUMNS)
                sheet.status(f"Live - last update {pd.Timestamp.now(tz=NY):%Y-%m-%d %H:%M:%S} New York - "
                             f"{len(total)} trades this run", _summary_rows(total))
            except Exception as exc:
                LOG.warning("Google Sheet update failed: %s", exc)
        last = now
        time.sleep(max(0.0, poll_s - (pd.Timestamp.now(tz="UTC") - now).total_seconds()))
    n = sum(len(d) for d in everything)
    LOG.info("shadow HFT: %d simulated trades logged to %s", n, path)
    return path if path.exists() else None


def main(argv=None):
    import argparse

    from ..utils import setup_logging

    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=330)
    ap.add_argument("--out", default="logs/hft")
    args = ap.parse_args(argv)
    setup_logging()
    p = run(args.minutes, args.out)
    if p is not None:
        print(summary(pd.read_csv(p)).to_string(index=False))


if __name__ == "__main__":
    main()
