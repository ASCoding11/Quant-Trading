"""Shadow high-frequency trader: simulated trades on live quotes, every one of them logged.

Real high-frequency trading needs colocation and direct exchange feeds; Alpaca's API
is ~100 ms+ away and its paper simulator fills at will. So nothing here touches the
account. During market hours it pulls every IEX quote update and trade (Alpaca's free
real-time feed) for a handful of liquid stocks every two seconds and runs three
simulated strategies, logging each trade with its prices and P&L:

* ``imbalance_taker`` - when the book is lopsided (|quote imbalance| >= 0.6: e.g. far
  more shares bid than offered), buy at the ask / sell at the bid, and get out 30 s
  later crossing the spread again;
* ``market_maker`` - every 10 s, rest one order at the best bid and one at the best
  ask for 10 s. A resting order fills only if a trade prints *through* it (so the
  queue ahead of it must have been used up - conservative). Exits 30 s later crossing
  the spread (``pnl_bp``) and, for reference, marked at the midquote (``pnl_mid_bp``);
* ``maker_with_signal`` - the same, quoting only the side the imbalance favours.

Costs: no commission (IBKR Lite / Alpaca), the SEC fee on sales (0.278 bp). IEX's own
book is thinner and wider than the national best bid and offer, so spreads here are
conservative.
"""
from __future__ import annotations

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
SEC_FEE_BP = 0.278
IMB_THRESHOLD = 0.6
HOLD_S = 30
MM_EVERY_S = 10
MM_WAIT_S = 10
COLUMNS = ["strategy", "symbol", "side", "entry_time", "entry_price", "exit_time", "exit_price", "pnl_bp",
           "pnl_mid_bp", "spread_bp", "imbalance"]


class Book:
    """Latest IEX top of book and recent trades for one symbol."""

    def __init__(self):
        self.bid = self.ask = np.nan
        self.bsize = self.asize = np.nan
        self.trades: deque = deque(maxlen=5000)       # (time, price, size)

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
    """Pure state machine: feed it quotes and trades, it opens and closes simulated trades."""

    def __init__(self, symbols: list[str]):
        self.books = {s: Book() for s in symbols}
        self.open: list[dict] = []                 # taker positions waiting for their exit time
        self.resting: list[dict] = []              # maker orders waiting for a fill
        self.held: list[dict] = []                 # filled maker orders waiting for their exit
        self.closed: list[dict] = []
        self.last_mm: dict[str, pd.Timestamp] = defaultdict(lambda: pd.Timestamp(0, tz="UTC"))
        self.last_taker: dict[str, pd.Timestamp] = defaultdict(lambda: pd.Timestamp(0, tz="UTC"))

    # --- inputs -----------------------------------------------------------------------------------
    def on_quote(self, sym: str, t: pd.Timestamp, bid: float, bsize: float, ask: float, asize: float) -> None:
        b = self.books[sym]
        if bid > 0 and ask > bid and bsize > 0 and asize > 0:
            b.bid, b.bsize, b.ask, b.asize = bid, bsize, ask, asize

    def on_trade(self, sym: str, t: pd.Timestamp, price: float, size: float) -> None:
        self.books[sym].trades.append((t, price, size))
        for o in list(self.resting):                 # a trade through a resting order fills it
            if o["symbol"] != sym or t <= o["placed"] or t > o["expires"]:
                continue
            if (o["side"] == "buy" and price < o["price"]) or (o["side"] == "sell" and price > o["price"]):
                self.resting.remove(o)
                self.held.append({**o, "entry_time": t, "exit_due": t + pd.Timedelta(seconds=HOLD_S)})

    # --- decisions --------------------------------------------------------------------------------
    def step(self, now: pd.Timestamp) -> None:
        self.resting = [o for o in self.resting if o["expires"] >= now]
        for sym, b in self.books.items():
            if not b.ok:
                continue
            imb = b.imbalance
            # taker on a lopsided book, at most one position per symbol at a time
            if abs(imb) >= IMB_THRESHOLD and now - self.last_taker[sym] >= pd.Timedelta(seconds=HOLD_S):
                side = "buy" if imb > 0 else "sell"
                self.open.append({"strategy": "imbalance_taker", "symbol": sym, "side": side,
                                  "entry_time": now, "entry_price": b.ask if side == "buy" else b.bid,
                                  "exit_due": now + pd.Timedelta(seconds=HOLD_S), "spread_bp": b.spread_bp,
                                  "imbalance": imb})
                self.last_taker[sym] = now
            # market making every 10 s
            if now - self.last_mm[sym] >= pd.Timedelta(seconds=MM_EVERY_S):
                self.last_mm[sym] = now
                exp = now + pd.Timedelta(seconds=MM_WAIT_S)
                for side, px in (("buy", b.bid), ("sell", b.ask)):
                    base = {"symbol": sym, "side": side, "price": px, "entry_price": px, "placed": now,
                            "expires": exp, "spread_bp": b.spread_bp, "imbalance": imb}
                    self.resting.append({**base, "strategy": "market_maker"})
                    if (side == "buy" and imb > 0) or (side == "sell" and imb < 0):
                        self.resting.append({**base, "strategy": "maker_with_signal"})
        for pos in [p for p in self.open + self.held if p["exit_due"] <= now]:
            b = self.books[pos["symbol"]]
            if not b.ok:
                continue
            exit_px = b.bid if pos["side"] == "buy" else b.ask        # get out crossing the spread
            d = 1.0 if pos["side"] == "buy" else -1.0
            pnl = d * (exit_px / pos["entry_price"] - 1) * 1e4 - SEC_FEE_BP / 2
            pnl_mid = d * (b.mid / pos["entry_price"] - 1) * 1e4 - SEC_FEE_BP / 2
            self.closed.append({"strategy": pos["strategy"], "symbol": pos["symbol"], "side": pos["side"],
                                "entry_time": pos["entry_time"], "entry_price": pos["entry_price"],
                                "exit_time": now, "exit_price": exit_px, "pnl_bp": pnl, "pnl_mid_bp": pnl_mid,
                                "spread_bp": pos["spread_bp"], "imbalance": pos["imbalance"]})
            (self.open if pos in self.open else self.held).remove(pos)

    def take_closed(self) -> pd.DataFrame:
        out, self.closed = self.closed, []
        return pd.DataFrame(out, columns=COLUMNS)


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
        poll_s: float = 2.0) -> Path | None:
    """Trade in the shadow until ``minutes`` have passed or the market closes; returns the trade log."""
    from ..data.intraday import AlpacaBars

    symbols = symbols or SYMBOLS
    client = AlpacaBars(feed="iex", per_minute=90)      # leaves headroom for the auction trader's calls
    hft = ShadowHFT(symbols)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"hft_trades_{pd.Timestamp.now(tz=NY):%Y%m%d_%H%M}.csv"
    stop = time.time() + minutes * 60
    last = pd.Timestamp.now(tz="UTC") - pd.Timedelta(seconds=5)
    n = 0
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
            n += len(done)
        last = now
        time.sleep(max(0.0, poll_s - (pd.Timestamp.now(tz="UTC") - now).total_seconds()))
    LOG.info("shadow HFT: %d simulated trades logged to %s", n, path)
    return path if path.exists() else None


def summary(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    g = trades.groupby("strategy")
    return pd.DataFrame({"trades": g.size(), "avg_pnl_bp": g["pnl_bp"].mean(), "avg_pnl_mid_bp": g["pnl_mid_bp"].mean(),
                         "hit_rate": g["pnl_bp"].apply(lambda x: (x > 0).mean()),
                         "avg_spread_bp": g["spread_bp"].mean()}).reset_index()


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
