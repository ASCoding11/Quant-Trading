"""Live auction trader: the overnight strategies, traded only in the auctions.

Every trading day, on Alpaca paper:

* **close phase** (about 15:45 New York): compute the two signals from live
  prices - against the 15:15 -> 15:45 move (``last30_fade``) and the past
  month's overnight returns (``overnight_persistence``) - build the long/short
  book (top / bottom fifth, equal capital per strategy), add the earnings leg
  (``last_reaction``, ``earnings_live``: names reporting tonight, long or short
  by their previous release's reaction) and send **market-on-close** orders
  before Alpaca's 15:50 cutoff;
* **open phase** (before 9:28 the next morning): send **market-on-open**
  orders that close every position, so the account is flat all day;
* **report**: each phase compares the previous auction's fills with the
  official open / close prices, which measures the real cost of trading this
  way (the backtest assumes 0 bp).

Auction orders fill at the official auction price, so they pay no spread; that
is why these strategies are the only ones whose edge survives.
The signal formulas are shared with the backtest (``slice_sim``), and the
strategy directions are the ones the backtest fixed on 2016-2020.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from ..data.intraday import AlpacaBars, bars_to_frame
from ..live.alpaca_trader import _account_state, _client, plan_orders
from ..utils import LOG
from .earnings_live import earnings_weights
from .slice_sim import _weights, last30_signal, overnight_signal

NY = "America/New_York"
CLOSE_CUTOFF = (15, 49)          # Alpaca rejects market-on-close orders from 15:50
OPEN_CUTOFF = (9, 27)            # ... and market-on-open orders from 9:28


def _now() -> pd.Timestamp:
    return pd.Timestamp.now(tz=NY)


def _fetch(data: AlpacaBars, symbols, timeframe, start, end, feed) -> dict[str, pd.DataFrame]:
    old = data.feed
    data.feed = feed
    try:
        out = {}
        for i in range(0, len(symbols), 200):
            got = data.bars(symbols[i:i + 200], timeframe, start.isoformat(), end.isoformat())
            out.update({s: bars_to_frame(rows, regular_hours=timeframe != "1Day") for s, rows in got.items() if rows})
        return out
    finally:
        data.feed = old


def build_book(today_5min: dict[str, pd.DataFrame], daily: dict[str, pd.DataFrame], tickers: list[str],
               signs: dict, acfg, today: pd.Timestamp, shortable: set | None = None,
               reactions: dict[str, float] | None = None) -> dict:
    """Target weights (fractions of capital), the prices used and the raw signals.

    ``today_5min``: today's 5-minute bars per ticker (New York index);
    ``daily``: daily bars with official open/close for the last ~30 sessions including today
    (today's bar only needs its open);
    ``reactions``: for names reporting earnings tonight, their previous release's reaction
    (the ``last_reaction`` leg, added on top of the other strategies)."""
    N = len(tickers)
    p1515, p1545 = np.full(N, np.nan), np.full(N, np.nan)
    t1515 = today.tz_localize(NY) + pd.Timedelta(hours=15, minutes=10)     # the bar that closes at 15:15
    t1545 = today.tz_localize(NY) + pd.Timedelta(hours=15, minutes=40)     # ... and at 15:45
    for i, t in enumerate(tickers):
        f = today_5min.get(t)
        if f is None or f.empty:
            continue
        upto = f[f.index <= t1515]
        if len(upto):
            p1515[i] = float(upto["close"].iloc[-1])
        upto = f[f.index <= t1545]
        if len(upto):
            p1545[i] = float(upto["close"].iloc[-1])
    sessions = sorted({d for f in daily.values() for d in f.index.normalize()})
    sessions = [d for d in sessions if d.tz_localize(None) <= today][-22:]
    opens = np.full((len(sessions), N), np.nan)
    closes = np.full((len(sessions), N), np.nan)
    for i, t in enumerate(tickers):
        f = daily.get(t)
        if f is None or f.empty:
            continue
        g = f.copy()
        g.index = g.index.normalize()
        g = g[~g.index.duplicated(keep="last")].reindex(sessions)
        opens[:, i] = g["open"].to_numpy()
        closes[:, i] = g["close"].to_numpy()
    prev_closes = np.vstack([np.full((1, N), np.nan), closes[:-1]])
    sig = {"last30_fade": signs.get("last30_fade", 1.0) * last30_signal(p1515, p1545),
           "overnight_persistence": signs.get("overnight_persistence", 1.0) * overnight_signal(opens, prev_closes)}
    ok = np.isfinite(p1545) & (p1545 > 0)
    w = np.zeros(N)
    used = []
    for s in acfg.strategies:
        if s not in sig:
            continue
        x = sig[s][ok]
        informative = np.isfinite(x) & (np.abs(x) > 1e-12)
        # a flat or missing signal (prices not printed yet, a data gap) would rank ties at random
        if len(x) == 0 or informative.mean() < 0.5:
            LOG.warning("%s: only %d of %d stocks have a signal today - leaving it out", s,
                        int(informative.sum()), len(x))
            continue
        used.append(s)
    for s in used:
        w += _weights(sig[s], ok & np.isfinite(sig[s]), acfg.frac) * acfg.gross / max(len(used), 1)
    if "last_reaction" in acfg.strategies and reactions:
        e = earnings_weights(tickers, reactions, ok, signs.get("last_reaction", 1.0), acfg.earnings_per_event,
                             acfg.earnings_max_gross)
        if np.abs(e).sum() > 0:
            w += e
            used.append("last_reaction")
    if shortable is not None:
        w[(w < 0) & ~np.array([t in shortable for t in tickers])] = 0.0
    return {"weights": dict(zip(tickers, w)), "prices": dict(zip(tickers, p1545)), "signals": sig,
            "n_priced": int(ok.sum()), "strategies": used}


def _submit(client, orders, tif: str) -> list[str]:
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.trading.requests import MarketOrderRequest

    from ..data import to_alpaca

    t = {"cls": TimeInForce.CLS, "opg": TimeInForce.OPG, "day": TimeInForce.DAY}[tif]
    ids = []
    for o in sorted(orders, key=lambda o: o.side != "sell"):
        try:
            r = client.submit_order(MarketOrderRequest(
                symbol=to_alpaca(o.symbol), qty=o.qty,
                side=OrderSide.BUY if o.side == "buy" else OrderSide.SELL, time_in_force=t))
            ids.append(str(r.id))
        except Exception as exc:       # one rejected symbol must not stop the rest
            LOG.warning("order %s %d %s rejected: %s", o.side, o.qty, o.symbol, exc)
    return ids


def _sent_today(client, tif: str) -> bool:
    """True if orders with this time-in-force were submitted since midnight New York time."""
    midnight = _now().normalize().isoformat()
    for status in ("open", "closed"):
        orders = client.get("/orders", {"status": status, "after": midnight, "limit": 500})
        if any(o.get("time_in_force") == tif for o in orders):
            return True
    return False


def _wait_until(target: pd.Timestamp) -> None:
    while (left := (target - _now()).total_seconds()) > 0:
        time.sleep(min(left, 60))


def _earnings_reactions(data: AlpacaBars, acfg, tickers: list[str], today: pd.Timestamp) -> dict[str, float]:
    """Last reactions of the names reporting tonight; {} (and a warning) if any source fails."""
    from .earnings_live import last_reactions, releases_tonight

    try:
        names = [t for t in releases_tonight(today) if t in set(tickers)]
        if not names:
            LOG.info("last_reaction: no releases tonight among the traded names")
            return {}
        start = today.tz_localize(NY) - pd.Timedelta(days=150)       # back past the previous quarter's release
        hist = _fetch(data, names + ["SPY"], "1Day", start, _now() - pd.Timedelta(minutes=16), "sip")
        if "SPY" not in hist:
            return {}
        stop = _now().normalize() + pd.Timedelta(hours=15, minutes=44)
        r = last_reactions(names, _now(), hist, hist["SPY"], deadline=stop if _now() < stop else None)
        LOG.info("last_reaction: %d releases tonight, %d with a previous reaction (%d up, %d down)", len(names),
                 len(r), sum(v > 0 for v in r.values()), sum(v < 0 for v in r.values()))
        return r
    except Exception as exc:
        LOG.warning("last_reaction leg skipped today: %s", exc)
        return {}


def run_close(cfg, tickers: list[str], signs: dict, dry_run: bool = True, out_dir: str | Path = "logs") -> dict:
    """Send the evening book as market-on-close orders."""
    acfg = cfg.auction
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = _client()
    if client is None and not dry_run:
        raise SystemExit("Set ALPACA_API_KEY and ALPACA_SECRET_KEY to place paper orders.")
    clock = client.get_clock() if client else None
    now = _now()
    today = now.tz_localize(None).normalize()
    live = clock is not None and clock.is_open
    cutoff = now.normalize() + pd.Timedelta(hours=CLOSE_CUTOFF[0], minutes=CLOSE_CUTOFF[1])
    if live and not dry_run and _sent_today(client, "cls"):
        LOG.info("market-on-close orders were already sent today (an earlier run) - nothing to do")
        return {"status": "already sent"}
    data = AlpacaBars(feed=acfg.feed)
    reactions = None
    if live:
        close_time = pd.Timestamp(clock.next_close).tz_convert(NY)
        if close_time.hour < 16:
            LOG.info("early close today (%s): market-on-close timing differs - skipping", close_time)
            return {"status": "early close"}
        # the earnings leg needs no prices from today: look it up before the 15:45 rush
        if "last_reaction" in acfg.strategies:
            reactions = _earnings_reactions(data, acfg, tickers, today)
        if dry_run:
            LOG.info("dry run during the session: building the book from prices so far")
        else:
            _wait_until(now.normalize() + pd.Timedelta(hours=15, minutes=45, seconds=20))
        if not dry_run and _sent_today(client, "cls"):      # another run got there while this one waited
            LOG.info("market-on-close orders were sent by another run - nothing to do")
            return {"status": "already sent"}
        if not dry_run and _now() > cutoff:
            LOG.warning("too late for market-on-close orders (%s) - skipping today", _now().strftime("%H:%M"))
            return {"status": "missed cutoff"}
    elif not dry_run:
        LOG.info("market is closed - nothing to do")
        return {"status": "closed"}
    if not live:                                    # dry run outside hours: replay the last session
        probe = _fetch(data, tickers[:5], "1Day", now - pd.Timedelta(days=10), now - pd.Timedelta(minutes=20), "sip")
        today = max(f.index.max() for f in probe.values()).tz_convert(NY).tz_localize(None).normalize()
    start = today.tz_localize(NY) + pd.Timedelta(hours=9, minutes=30)
    today_5 = _fetch(data, tickers, "5Min", start, min(_now(), start + pd.Timedelta(hours=6, minutes=30)), acfg.feed)
    # daily bars through today (the consolidated tape allows data older than 15 minutes)
    daily = _fetch(data, tickers, "1Day", today.tz_localize(NY) - pd.Timedelta(days=45),
                   _now() - pd.Timedelta(minutes=16), "sip")
    if client is not None:
        equity, pos_qty, pos_val, shortable, tradable, _ = _account_state(client)
    else:
        equity, pos_qty, pos_val, shortable, tradable = 100_000.0, {}, {}, None, None
    capital = acfg.capital or min(equity * cfg.live.capital_fraction, cfg.live.max_capital or equity)
    if reactions is None and "last_reaction" in acfg.strategies:      # dry run outside hours
        reactions = _earnings_reactions(data, acfg, tickers, today)
    book = build_book(today_5, daily, tickers, signs, acfg, today, shortable, reactions)
    tw = {t: w for t, w in book["weights"].items() if abs(w) > 1e-9 and (tradable is None or t in tradable)}
    prices = {t: p for t, p in book["prices"].items() if np.isfinite(p)}
    pos = {t: q for t, q in pos_qty.items() if t in set(tickers)}
    orders, targets = plan_orders(tw, prices, capital, pos, shortable, acfg.min_order_value)
    stamp = _now().strftime("%Y%m%d_%H%M")
    pd.DataFrame([o.__dict__ | {"notional": o.notional} for o in orders]).to_csv(out / f"auction_close_{stamp}.csv",
                                                                                  index=False)
    LOG.info("close book for %s: %d priced, %d long, %d short, gross $%.0f on capital $%.0f -> %d MOC orders",
             today.date(), book["n_priced"], sum(v > 0 for v in targets.values()), sum(v < 0 for v in targets.values()),
             sum(abs(q) * prices.get(t, 0) for t, q in targets.items()), capital, len(orders))
    ids = []
    if live and not dry_run and orders:
        ids = _submit(client, orders, "cls")
        LOG.info("submitted %d market-on-close orders", len(ids))
    elif orders:
        LOG.info("dry run - first orders:\n%s", pd.DataFrame([o.__dict__ for o in orders]).head(10).to_string(index=False))
    return {"status": "done", "orders": len(orders), "submitted": len(ids), "capital": capital}


def run_open(cfg, dry_run: bool = True, out_dir: str | Path = "logs") -> dict:
    """Close every position at the open: market-on-open orders before 9:28, market orders if later."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = _client()
    if client is None:
        if not dry_run:
            raise SystemExit("Set ALPACA_API_KEY and ALPACA_SECRET_KEY to place paper orders.")
        LOG.info("no Alpaca keys: nothing to flatten")
        return {"status": "no account"}
    clock = client.get_clock()
    now = _now()
    cutoff = now.normalize() + pd.Timedelta(hours=OPEN_CUTOFF[0], minutes=OPEN_CUTOFF[1])
    if clock.is_open:
        tif = "day"
        LOG.warning("market already open - closing with regular market orders (these pay the spread)")
    elif now < cutoff and pd.Timestamp(clock.next_open).tz_convert(NY).normalize() == now.normalize():
        tif = "opg"
    else:
        LOG.info("not a pre-open window (next open %s) - nothing to do", clock.next_open)
        return {"status": "outside window"}
    open_orders = client.get("/orders", {"status": "open", "limit": 500})
    if any(o.get("time_in_force") == "opg" for o in open_orders):
        LOG.info("market-on-open orders already queued - nothing to do")
        return {"status": "already queued"}
    _, pos_qty, _, _, _, _ = _account_state(client)
    from ..live.alpaca_trader import PlannedOrder

    orders = [PlannedOrder(t, "sell" if q > 0 else "buy", abs(q), float("nan"), "flatten")
              for t, q in pos_qty.items() if q != 0]
    pd.DataFrame([o.__dict__ for o in orders]).to_csv(out / f"auction_open_{_now():%Y%m%d_%H%M}.csv", index=False)
    LOG.info("%d positions to close at the open (%s orders)", len(orders), tif.upper())
    ids = _submit(client, orders, tif) if (orders and not dry_run) else []
    return {"status": "done", "orders": len(orders), "submitted": len(ids)}


def run_keeper(cfg, tickers: list[str], signs: dict, hours: float = 5.4, dry_run: bool = True,
               out_dir: str | Path = "logs") -> dict:
    """Stay up for ``hours`` and act at the right moments instead of trusting a scheduler.

    GitHub starts scheduled workflows hours late on busy days, which missed the first
    market-on-close window. The keeper polls the clock every 30 seconds:

    * 9:00-9:27 on a trading day: queue market-on-open orders that close everything;
    * 9:31-10:30: if positions are still open (the open phase was missed or rejected),
      close them with market orders;
    * 15:40-15:49: build the book and send market-on-close orders (``run_close`` waits
      until 15:45 and skips if today's orders were already sent).

    Each action runs at most once per day per keeper, and every action is itself guarded
    against repeats, so overlapping or restarted keepers can't double-trade."""
    client = _client()
    if client is None:
        raise SystemExit("Set ALPACA_API_KEY and ALPACA_SECRET_KEY to run the keeper.")
    end = time.time() + hours * 3600
    done: dict[str, pd.Timestamp] = {}
    actions = []
    LOG.info("keeper up for %.1f hours (until %s New York)", hours,
             (_now() + pd.Timedelta(hours=hours)).strftime("%a %H:%M"))
    while time.time() < end:
        now = _now()
        today = now.normalize()
        hm = now.hour * 60 + now.minute
        try:
            clock = client.get_clock()
            opens_today = pd.Timestamp(clock.next_open).tz_convert(NY).normalize() == today
            trading_day = clock.is_open or opens_today
            if trading_day and 9 * 60 <= hm < 9 * 60 + 27 and done.get("open") != today:
                done["open"] = today
                fill_report(days=4, out_dir=out_dir)
                actions.append(("open", str(now), run_open(cfg, dry_run=dry_run, out_dir=out_dir)))
            elif clock.is_open and 9 * 60 + 31 <= hm < 10 * 60 + 30 and done.get("late") != today:
                done["late"] = today
                pos = _account_state(client)[1]
                if any(q != 0 for q in pos.values()):
                    LOG.warning("%d positions still open after the open - closing them", sum(q != 0 for q in pos.values()))
                    actions.append(("late flatten", str(now), run_open(cfg, dry_run=dry_run, out_dir=out_dir)))
            elif clock.is_open and 15 * 60 + 40 <= hm < 15 * 60 + 49 and done.get("close") != today:
                done["close"] = today
                fill_report(days=4, out_dir=out_dir)
                actions.append(("close", str(now), run_close(cfg, tickers, signs, dry_run=dry_run, out_dir=out_dir)))
        except Exception as exc:                  # keep the keeper alive through one bad poll
            LOG.warning("keeper poll failed: %s", exc)
        time.sleep(30)
    LOG.info("keeper done: %s", actions or "no actions in this window")
    return {"status": "done", "actions": actions}


def fill_report(days: int = 5, out_dir: str | Path = "logs") -> pd.DataFrame:
    """Auction fills of the last ``days`` days vs. the official open / close (bp, + = cost)."""
    client = _client()
    if client is None:
        return pd.DataFrame()
    after = (_now() - pd.Timedelta(days=days)).isoformat()
    rows, cursor = [], after
    for _ in range(50):
        raw = client.get("/orders", {"status": "closed", "after": cursor, "limit": 500, "direction": "asc"})
        rows += [o for o in raw if o.get("filled_at") and o.get("time_in_force") in ("cls", "opg")]
        if len(raw) < 500:
            break
        cursor = raw[-1]["submitted_at"]
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame([{"symbol": o["symbol"], "side": o["side"], "tif": o["time_in_force"],
                        "qty": float(o["filled_qty"]), "fill": float(o["filled_avg_price"]),
                        "filled_at": pd.Timestamp(o["filled_at"]).tz_convert(NY)} for o in rows]).drop_duplicates()
    df["date"] = df["filled_at"].dt.tz_localize(None).dt.normalize()
    data = AlpacaBars(feed="sip")
    data.adjustment = "raw"                       # compare with the prices actually printed
    syms = sorted(df["symbol"].unique())
    daily = _fetch(data, syms, "1Day", df["date"].min().tz_localize(NY) - pd.Timedelta(days=1),
                   _now() - pd.Timedelta(minutes=16), "sip")
    off = []
    for _, r in df.iterrows():
        f = daily.get(r["symbol"])
        px = np.nan
        if f is not None and len(f):
            g = f[f.index.tz_convert(NY).tz_localize(None).normalize() == r["date"]]
            if len(g):
                px = float(g["close" if r["tif"] == "cls" else "open"].iloc[-1])
        off.append(px)
    df["official"] = off
    sign = np.where(df["side"] == "buy", 1.0, -1.0)
    df["cost_bp"] = sign * (df["fill"] / df["official"] - 1) * 1e4
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"auction_fills_{_now():%Y%m%d_%H%M}.csv", index=False)
    v = df["qty"] * df["fill"]
    ok = df["cost_bp"].notna()
    for tif, g in df[ok].groupby("tif"):
        w = (g["qty"] * g["fill"])
        LOG.info("%s fills: %d, cost vs official %s: mean %.2f bp, value-weighted %.2f bp, median %.2f bp",
                 tif.upper(), len(g), "close" if tif == "cls" else "open", g["cost_bp"].mean(),
                 float((g["cost_bp"] * w).sum() / w.sum()), g["cost_bp"].median())
    LOG.info("all auction fills: value-weighted cost %.2f bp over $%.0f",
             float((df.loc[ok, "cost_bp"] * v[ok]).sum() / max(v[ok].sum(), 1e-9)), float(v[ok].sum()))
    return df


def load_inputs(tickers_file: str | Path, signs_file: str | Path | None) -> tuple[list[str], dict]:
    t = json.loads(Path(tickers_file).read_text())
    tickers = t["tickers"] if isinstance(t, dict) else list(t)
    signs = {"last30_fade": 1.0, "overnight_persistence": 1.0, "last_reaction": 1.0}
    if signs_file and Path(signs_file).exists():
        signs |= json.loads(Path(signs_file).read_text())
    LOG.info("auction trader: %d tickers, directions %s", len(tickers), signs)
    return tickers, signs
