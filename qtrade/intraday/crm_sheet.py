"""CRM satellite tracker: the critical-raw-material satellite signals, run live in the sheet with
$0 allocated - not part of the $10,000 book.

``qtrade.research.crm_satellite`` tests whether satellite readings of smelters (MODIS thermal
anomalies, Sentinel-5P SO2 plumes) predict copper, nickel (PICK), palladium, platinum, aluminium
and rare-earth (REMX) prices. This tracker trades each source's weekly "level" signal on a
hypothetical $10,000 split equally between the legs (source x commodity), so the live record can be
compared with the study:

* each Friday (or the first run with no positions, or after a week without a rebalance) the
  satellite caches are refreshed and every leg goes long or short its instrument: direction from
  ``crm_rules.json`` (fixed on the study's training years) times the sign of the latest signal,
  which only uses satellite days older than the publication lag;
* every weekday after the close each open leg is marked to the latest daily close, and the day's
  P&L is logged in the "CRM tracker" tab, with the open legs beside the log.

Prices are Yahoo daily closes (continuous front-month futures; roll jumps included, as in the study).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from ..research import crm_satellite as C
from ..utils import LOG

TAB = "CRM tracker"
BOOK_USD = 10_000.0
LOG_HEADER = ["Date", "Day P&L $", "Day %", "Equity $", "Legs open", "Rebalanced", "Note"]
POS_HEADER = ["Source", "Commodity", "Instrument", "Signal", "Position", "Notional $", "Entry date", "Entry price",
              "Last mark", "Mark price", "Open P&L $"]


def latest_signals(sat_cache: Path, today: pd.Timestamp) -> dict[tuple[str, str], float]:
    """(source, commodity) -> the level signal as known on ``today`` (only satellite days before the lag)."""
    from ..data import satellite as S
    from ..data import sentinel5p as S5

    out: dict[tuple[str, str], float] = {}
    fr = pd.DatetimeIndex([today.normalize()])
    files = sorted(Path(sat_cache).glob("modis_*.parquet"))
    if files:
        act = C.activity(S.daily_by_site(pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)))
        lvl = C.signals(act, fr)[C.LEVEL].iloc[-1]
        out.update({("MODIS", c): float(v) for c, v in lvl.items()})
    files = sorted(Path(sat_cache).glob("s5p_*.parquet"))
    if files:
        raw = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        act5 = C.so2_activity(S5.daily_by_site(raw))
        lvl = C.so2_signals(act5, fr)[C.LEVEL_S5P].iloc[-1]
        out.update({("SO2", c): float(v) for c, v in lvl.items()})
    return out


def legs(rules: list[dict], sig: dict[tuple[str, str], float]) -> list[dict]:
    """Every rule leg with its target position (+1 / -1, or 0 when the signal is missing or zero)."""
    out = []
    for r in rules:
        v = sig.get((r["source"], r["commodity"]), np.nan)
        pos = int(r["direction"] * np.sign(v)) if np.isfinite(v) else 0
        out.append({"source": r["source"], "commodity": r["commodity"], "instrument": r["instrument"],
                    "signal": None if not np.isfinite(v) else round(v, 4), "position": pos})
    return out


def mark(positions: pd.DataFrame, close: pd.Series) -> tuple[pd.DataFrame, float]:
    """Mark each open leg from its last mark to ``close``; returns the updated legs and the P&L."""
    if positions.empty:
        return positions, 0.0
    p = positions.copy()
    px = p["Instrument"].map(close).astype(float)
    ok = px.notna() & (p["Mark price"].astype(float) > 0)
    pnl = np.where(ok, p["Position"].astype(float) * p["Notional $"].astype(float)
                   * (px / p["Mark price"].astype(float) - 1), 0.0)
    p["Open P&L $"] = p["Open P&L $"].astype(float) + pnl
    p.loc[ok, "Mark price"] = px[ok]
    return p, float(np.sum(pnl))


def open_legs(target: list[dict], close: pd.Series, equity: float, day: str) -> pd.DataFrame:
    live = [t for t in target if t["position"] != 0 and np.isfinite(close.get(t["instrument"], np.nan))]
    n = len(target) or 1
    rows = [[t["source"], t["commodity"], t["instrument"], t["signal"], t["position"], round(equity / n, 2), day,
             float(close[t["instrument"]]), day, float(close[t["instrument"]]), 0.0] for t in live]
    return pd.DataFrame(rows, columns=POS_HEADER)


def due_rebalance(day: pd.Timestamp, positions: pd.DataFrame, last_rebalance: str | None) -> bool:
    if positions.empty or not last_rebalance:
        return True
    return day.weekday() == 4 or (day - pd.Timestamp(last_rebalance)).days >= 7


class CrmSheet:
    def __init__(self, sheet_id: str, creds_json: str):
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account

        creds = service_account.Credentials.from_service_account_info(
            json.loads(creds_json), scopes=["https://www.googleapis.com/auth/spreadsheets"])
        self.s = AuthorizedSession(creds)
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
        meta = self.s.get(self.base, params={"fields": "sheets.properties.title"}, timeout=30).json()
        if TAB not in [x["properties"]["title"] for x in meta.get("sheets", [])]:
            self.s.post(f"{self.base}:batchUpdate", json={"requests": [{"addSheet": {"properties": {"title": TAB}}}]},
                        timeout=30).raise_for_status()

    def get(self, rng: str) -> list[list]:
        r = self.s.get(f"{self.base}/values/'{TAB}'!{rng}", params={"valueRenderOption": "UNFORMATTED_VALUE"},
                       timeout=60)
        r.raise_for_status()
        return r.json().get("values", [])

    def state(self) -> tuple[list[list], pd.DataFrame]:
        log = [r for r in self.get("A6:G100000") if r and r[0]]
        pos = [r + [""] * (len(POS_HEADER) - len(r)) for r in self.get("J6:T200") if r and r[0]]
        return log, pd.DataFrame(pos, columns=POS_HEADER) if pos else pd.DataFrame(columns=POS_HEADER)

    def write(self, status: str, log_row: list, n_log: int, positions: pd.DataFrame) -> None:
        title = ("CRM satellite tracker - $0 allocated, NOT part of the $10,000 book. Weekly long / short in copper, "
                 "nickel (PICK), palladium, platinum, aluminium and rare earths (REMX) from satellite readings of their "
                 "smelters (MODIS heat, Sentinel-5P SO2), direction from the crm_satellite study; marked daily at Yahoo "
                 "closes on a hypothetical $10,000.")
        self.s.post(f"{self.base}/values:batchClear", json={"ranges": [f"'{TAB}'!J6:T200"]}, timeout=30).raise_for_status()
        pos = positions.copy()
        for c in ("Notional $", "Mark price", "Entry price", "Open P&L $"):
            if c in pos:
                pos[c] = pd.to_numeric(pos[c], errors="coerce").round(4)
        data = [{"range": f"'{TAB}'!A1", "values": [[title]]}, {"range": f"'{TAB}'!A3", "values": [[status]]},
                {"range": f"'{TAB}'!A5:G5", "values": [LOG_HEADER]},
                {"range": f"'{TAB}'!A{6 + n_log}:G{6 + n_log}", "values": [log_row]},
                {"range": f"'{TAB}'!J5:T5", "values": [POS_HEADER]}]
        if len(pos):
            data.append({"range": f"'{TAB}'!J6:T{5 + len(pos)}",
                         "values": pos.astype(object).where(pos.notna(), "").values.tolist()})
        self.s.post(f"{self.base}/values:batchUpdate", json={"valueInputOption": "RAW", "data": data},
                    timeout=30).raise_for_status()


def closes(instruments: list[str], days: int = 20) -> pd.DataFrame:
    from ..data.loader import download_prices

    md = download_prices(instruments, start=f"{pd.Timestamp.now() - pd.Timedelta(days=days):%Y-%m-%d}")
    return md.close


def run(rules: list[dict], sat_cache: Path, dry_run: bool = False) -> dict:
    now = pd.Timestamp.now(tz="America/New_York")
    today = now.tz_localize(None).normalize()
    day = f"{today:%Y-%m-%d}"
    sheet = None if dry_run else CrmSheet(os.environ["HFT_SHEET_ID"], os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    log, positions = sheet.state() if sheet else ([], pd.DataFrame(columns=POS_HEADER))
    if log and str(log[-1][0])[:10] == day:
        return {"skipped": f"{day} already marked"}
    px = closes(sorted({r["instrument"] for r in rules}))
    px = px[px.index <= today]
    if px.empty or px.index[-1] < today:
        return {"skipped": f"no closes for {day} yet (market holiday or data late)"}
    close = px.iloc[-1]
    equity0 = float(log[-1][3]) if log else BOOK_USD
    positions, pnl = mark(positions, close)
    equity = equity0 + pnl
    last_reb = next((str(r[0])[:10] for r in reversed(log) if len(r) > 5 and r[5] == "yes"), None)
    note, reb = "", "no"
    if due_rebalance(today, positions, last_reb):
        target = legs(rules, latest_signals(sat_cache, today))
        if any(t["position"] for t in target):
            positions = open_legs(target, close, equity, day)
            reb = "yes"
            note = ", ".join(f"{t['source']} {t['commodity']} {'long' if t['position'] > 0 else 'short'}"
                             for t in target if t["position"]) or "all flat"
        else:
            note = "no satellite signal available - legs kept"
    row = [day, round(pnl, 2), round(100 * pnl / equity0, 4) if equity0 else 0.0, round(equity, 2), int(len(positions)),
           reb, note]
    since = equity - BOOK_USD
    status = (f"Updated {now:%Y-%m-%d %H:%M} New York - today ${pnl:+,.2f}, equity ${equity:,.2f} on the hypothetical "
              f"$10,000 (${since:+,.2f} since the start); {len(positions)} legs open"
              + ("; rebalanced today from the latest satellite readings." if reb == "yes" else "."))
    if sheet:
        sheet.write(status, row, len(log), positions)
    LOG.info("CRM tracker: %s", status)
    return {"day": day, "pnl": round(pnl, 2), "equity": round(equity, 2), "rebalanced": reb, "legs": len(positions)}


def main(argv=None):
    import argparse

    from ..utils import setup_logging

    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default="data/crm_rules.json", help="the study's directions (crm_rules.json)")
    ap.add_argument("--sat-cache", default="data/satellite")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    setup_logging()
    if pd.Timestamp.now(tz="America/New_York").weekday() >= 5:
        print({"skipped": "weekend"})
        return
    print(run(json.load(open(args.rules)), Path(args.sat_cache), dry_run=args.dry_run))


if __name__ == "__main__":
    main()
