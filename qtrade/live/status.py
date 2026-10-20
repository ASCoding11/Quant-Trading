"""Daily paper-account report: P&L, exposure, positions, today's fills.

Returns are reported two ways:
* on the account (Alpaca paper accounts start at $100,000), and
* on the capital the strategy actually trades (``live.max_capital``, $10k in
  the small-account config) - the meaningful number for judging the model.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ..config import Config
from ..data.loader import to_yahoo
from ..utils import LOG


def _f(x, default=0.0) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def spy_day_return() -> float | None:
    """SPY's return today (IEX feed, free plan) for comparison; None if unavailable."""
    try:
        from ..data.intraday import AlpacaBars

        c = AlpacaBars(per_minute=50)
        snap = c._get({"feed": "iex"}, url="https://data.alpaca.markets/v2/stocks/SPY/snapshot")
        today, prev = snap.get("dailyBar") or {}, snap.get("prevDailyBar") or {}
        return _f(today.get("c")) / _f(prev.get("c")) - 1 if prev.get("c") else None
    except Exception as exc:  # comparison only
        LOG.warning("SPY comparison unavailable: %s", exc)
        return None


def account_status(client, cfg: Config) -> dict:
    acct = client.get("/account")
    positions = client.get("/positions") or []
    equity, last = _f(acct.get("equity")), _f(acct.get("last_equity"))
    capital = min(equity, cfg.live.max_capital or equity) * cfg.live.capital_fraction
    pnl = equity - last

    rows = [{
        "symbol": to_yahoo(p["symbol"]), "side": p.get("side"), "qty": _f(p.get("qty")),
        "market_value": _f(p.get("market_value")), "avg_entry": _f(p.get("avg_entry_price")),
        "price": _f(p.get("current_price")), "pnl_today": _f(p.get("unrealized_intraday_pl")),
        "pnl_total": _f(p.get("unrealized_pl")),
    } for p in positions]
    pos = pd.DataFrame(rows, columns=["symbol", "side", "qty", "market_value", "avg_entry", "price",
                                      "pnl_today", "pnl_total"])

    midnight = pd.Timestamp.now(tz="America/New_York").normalize()
    orders = client.get("/orders", {"status": "all", "after": midnight.isoformat(), "limit": 500}) or []
    filled = [o for o in orders if o.get("status") == "filled"]

    long_v = pos.loc[pos["market_value"] > 0, "market_value"].sum()
    short_v = -pos.loc[pos["market_value"] < 0, "market_value"].sum()
    spy = spy_day_return()
    status = {
        "date": str(midnight.date()),
        "time": pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d %H:%M %Z"),
        "equity": round(equity, 2), "last_equity": round(last, 2),
        "day_pnl": round(pnl, 2),
        "strategy_capital": round(capital, 2),
        "day_return_on_capital": round(pnl / capital, 6) if capital else None,
        "day_return_on_account": round(pnl / last, 6) if last else None,
        "spy_day_return": round(spy, 6) if spy is not None else None,
        "long_names": int((pos["market_value"] > 0).sum()), "short_names": int((pos["market_value"] < 0).sum()),
        "long_value": round(long_v, 2), "short_value": round(short_v, 2),
        "gross_on_capital": round((long_v + short_v) / capital, 3) if capital else None,
        "net_on_capital": round((long_v - short_v) / capital, 3) if capital else None,
        "orders_today": len(orders), "filled_today": len(filled),
        "unrealized_pnl_total": round(pos["pnl_total"].sum(), 2),
    }
    by_pnl = pos.sort_values("pnl_today")
    status["best_today"] = by_pnl.tail(5)[::-1][["symbol", "side", "pnl_today"]].to_dict("records")
    status["worst_today"] = by_pnl.head(5)[["symbol", "side", "pnl_today"]].to_dict("records")
    return status, pos


def run_status(cfg: Config, out_dir: str | Path = "logs/status") -> dict:
    from .alpaca_trader import _client

    client = _client()
    if client is None:
        raise SystemExit("Set ALPACA_API_KEY and ALPACA_SECRET_KEY to read the paper account.")
    status, pos = account_status(client, cfg)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest.json").write_text(json.dumps(status, indent=2))
    pos.to_csv(out / "positions.csv", index=False)
    return status


def summary_line(s: dict) -> str:
    pct = lambda v: "n/a" if v is None else f"{v * 100:+.2f}%"
    return (f"{s['time']}: day P&L ${s['day_pnl']:+,.2f} = {pct(s['day_return_on_capital'])} on "
            f"${s['strategy_capital']:,.0f} traded ({pct(s['day_return_on_account'])} on the "
            f"${s['last_equity']:,.0f} account); SPY {pct(s['spy_day_return'])}. "
            f"{s['long_names']} long / {s['short_names']} short, gross {s['gross_on_capital']}x, "
            f"net {s['net_on_capital']}x; {s['filled_today']} orders filled today.")
