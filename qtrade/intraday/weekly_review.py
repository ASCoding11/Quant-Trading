"""Weekly review of the $10,000 sheet book: each sleeve's live record against its backtest.

Every Saturday (``.github/workflows/weekly-review.yml``) this reads the daily logs in the sheet,
computes each sleeve's live statistics and writes them to the "Weekly review" tab, with a verdict
from a rule fixed in advance (``config/review.json``), so the sleeves are not retuned on noise:

* the live annualised Sharpe ``S`` over ``n`` trading days is compared with the backtest Sharpe
  ``B`` of the same rule (0 bp fees, like the sheet). A Sharpe estimated from ``n`` days has a
  standard error of about ``sqrt(252 / n)``, so ``z = (S - B) * sqrt(n / 252)``;
* before ``min_days`` live days there is no verdict ("too early"), whatever the numbers;
* ``z <= cut_z`` (-2): **cut** - the live record is clearly worse than the backtest;
  ``z <= halve_z`` (-1): **halve**; otherwise **keep**. A sleeve already cut is reported as "off";
  the review does not re-enable it - that needs its backtest re-run on newer data first.

The review only proposes; the change itself (``config/sheet_book.json``) goes in by pull request.
The two $0 trackers (foreign HFT, CRM satellite) are listed for information - neither is in the book.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import LOG

TAB = "Weekly review"
REVIEW_FILE = Path(__file__).resolve().parents[2] / "config" / "review.json"
HEADER = ["Sleeve", "In book", "Live days", "P&L $", "Live Sharpe", "Backtest Sharpe", "z", "Days up",
          "Max drawdown $", "Verdict", "Why"]


# --- pure statistics -----------------------------------------------------------------------------
def stats(daily: pd.DataFrame) -> dict:
    """``daily``: one row per trading day with ``pnl`` (dollars) and ``ret`` (fraction of capital)."""
    n = len(daily)
    if n == 0:
        return {"days": 0, "pnl": 0.0, "sharpe": np.nan, "hit": np.nan, "max_dd": 0.0}
    r = daily["ret"].astype(float)
    sd = r.std(ddof=1) if n > 1 else np.nan
    cum = daily["pnl"].astype(float).cumsum()
    return {"days": n, "pnl": float(daily["pnl"].sum()),
            "sharpe": float(r.mean() / sd * np.sqrt(252)) if sd and np.isfinite(sd) and sd > 0 else np.nan,
            "hit": float((daily["pnl"] > 0).mean()), "max_dd": float((cum - cum.cummax().clip(lower=0)).min())}


def verdict(st: dict, backtest_sharpe: float | None, rule: dict, in_book: bool) -> tuple[str, float, str]:
    """(verdict, z, why) from the fixed rule."""
    if not in_book:
        return "off", np.nan, "already out of the book"
    if backtest_sharpe is None:
        return "info", np.nan, "$0 tracker, not in the book"
    n, s = st["days"], st["sharpe"]
    if not np.isfinite(s):
        return "too early", np.nan, f"{n} live days"
    z = (s - backtest_sharpe) * np.sqrt(n / 252)
    if n < rule["min_days"]:
        return "too early", z, f"{n} of {rule['min_days']} live days needed"
    if z <= rule["cut_z"]:
        return "cut", z, f"live Sharpe {s:.2f} vs backtest {backtest_sharpe:.2f}: z {z:.2f} <= {rule['cut_z']}"
    if z <= rule["halve_z"]:
        return "halve", z, f"live Sharpe {s:.2f} vs backtest {backtest_sharpe:.2f}: z {z:.2f} <= {rule['halve_z']}"
    return "keep", z, f"live Sharpe {s:.2f} vs backtest {backtest_sharpe:.2f}: z {z:.2f}"


# --- daily series from each tab's log ------------------------------------------------------------
def _num(x) -> pd.Series:
    return pd.to_numeric(pd.Series(x), errors="coerce")


def _frame(rows: list[list], width: int) -> pd.DataFrame:
    rows = [r + [""] * (width - len(r)) for r in rows if r and str(r[0])[:2] == "20"]
    return pd.DataFrame(rows, columns=range(width)) if rows else pd.DataFrame(columns=range(width))


def daily_flip(rows) -> pd.DataFrame:
    f = _frame(rows, 10)   # Date, VIX, Regime, Longs, Shorts, Gross, Day P&L $, Day %, Equity, Turnover
    return pd.DataFrame({"date": f[0], "pnl": _num(f[6]).values, "ret": _num(f[7]).values / 100}).dropna()


def daily_auction(rows, col: int) -> pd.DataFrame:
    """col 1 = the overnight book, 2 = the ADR book; returns as a fraction of the sleeve's capital."""
    f = _frame(rows, 11)   # Date, Overnight $, ADR $, Day $, Day %, Equity $, ..., Capital $
    pnl, eq, cap = _num(f[col]).values, _num(f[5]).values, _num(f[10]).values
    base = np.where(np.isfinite(eq), eq - _num(f[3]).values, cap)
    return pd.DataFrame({"date": f[0], "pnl": pnl, "ret": pnl / base}).dropna()


def daily_by_date(rows, pnl_col: int, base: float | pd.Series, width: int) -> pd.DataFrame:
    """Logs with several rows per day (foreign book passes, tracker trades): summed per date."""
    f = _frame(rows, width)
    d = pd.DataFrame({"date": f[0].astype(str).str[:10], "pnl": _num(f[pnl_col]).values}).dropna()
    d = d.groupby("date", as_index=False)["pnl"].sum()
    d["ret"] = d["pnl"] / base
    return d


# --- the sheet -----------------------------------------------------------------------------------
class Sheet:
    def __init__(self, sheet_id: str, creds_json: str):
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account

        creds = service_account.Credentials.from_service_account_info(
            json.loads(creds_json), scopes=["https://www.googleapis.com/auth/spreadsheets"])
        self.s = AuthorizedSession(creds)
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"

    def get(self, tab: str, rng: str) -> list[list]:
        r = self.s.get(f"{self.base}/values/'{tab}'!{rng}", params={"valueRenderOption": "UNFORMATTED_VALUE"},
                       timeout=60)
        if r.status_code == 400:        # the tab doesn't exist
            return []
        r.raise_for_status()
        return r.json().get("values", [])

    def write(self, rows: list[list], status: str) -> None:
        meta = self.s.get(self.base, params={"fields": "sheets.properties.title"}, timeout=30).json()
        if TAB not in [x["properties"]["title"] for x in meta.get("sheets", [])]:
            self.s.post(f"{self.base}:batchUpdate", json={"requests": [{"addSheet": {"properties": {"title": TAB}}}]},
                        timeout=30).raise_for_status()
        history = [r for r in self.get(TAB, "A20:L5000") if r and r[0]]
        self.s.post(f"{self.base}/values:batchClear", json={"ranges": [f"'{TAB}'!A1:L19"]},
                    timeout=30).raise_for_status()
        title = ("Weekly review of the $10,000 book - each sleeve's live record against its backtest, with a verdict "
                 "from a rule fixed in advance (config/review.json): no verdict before the minimum number of live "
                 "days; then cut when the live Sharpe is more than 2 standard errors below the backtest, halve "
                 "between 1 and 2. Changes go in by pull request.")
        day = rows[0][0] if rows else ""
        data = [{"range": f"'{TAB}'!A1", "values": [[title]]}, {"range": f"'{TAB}'!A3", "values": [[status]]},
                {"range": f"'{TAB}'!A5:K5", "values": [HEADER]},
                {"range": f"'{TAB}'!A6:K{5 + len(rows)}", "values": [r[1:] for r in rows]},
                {"range": f"'{TAB}'!A19:L19", "values": [["Week of"] + HEADER]}]
        hist_rows = [] if any(str(h[0])[:10] == day for h in history) else [[day] + r[1:] for r in rows]
        if hist_rows:
            data.append({"range": f"'{TAB}'!A{20 + len(history)}:L{19 + len(history) + len(hist_rows)}",
                         "values": hist_rows})
        self.s.post(f"{self.base}/values:batchUpdate", json={"valueInputOption": "RAW", "data": data},
                    timeout=30).raise_for_status()


def review(sheet, book: dict, cfg: dict, today: str) -> list[list]:
    rule, bt = cfg["rule"], cfg["backtest_sharpe"]
    series = {
        "momentum_flip": daily_flip(sheet.get("Momentum flip", "A6:J5000")),
        "auction_overnight": daily_auction(auction := sheet.get("Auction book", "A6:K5000"), 1),
        "adr": daily_auction(auction, 2),
        "foreign": daily_by_date(sheet.get("Foreign book", "A6:H5000"), 1, book.get("foreign", 1.0) or 1.0, 8),
        "foreign_hft_tracker": daily_by_date(sheet.get("Foreign HFT tracker", "A6:K100000"), 10, 10_000.0, 11),
        "crm_tracker": daily_by_date(sheet.get("CRM tracker", "A6:G5000"), 1, 10_000.0, 7),
    }
    in_book = {"momentum_flip": book.get("momentum_flip", 0) > 0,
               "auction_overnight": book.get("auction", 0) > 0 and book.get("auction_overnight_weight", 1.0) > 0,
               "adr": book.get("auction", 0) > 0, "foreign": book.get("foreign", 0) > 0,
               "foreign_hft_tracker": True, "crm_tracker": True}
    rows = []
    for name, d in series.items():
        if name.endswith("_tracker"):
            d = d[d["pnl"] != 0] if name == "foreign_hft_tracker" else d   # days with trades only
        st = stats(d)
        v, z, why = verdict(st, bt.get(name), rule, in_book[name])
        rows.append([today, name, "yes" if bt.get(name) is not None and in_book[name] else "no", st["days"],
                     round(st["pnl"], 2), None if not np.isfinite(st["sharpe"]) else round(st["sharpe"], 2),
                     bt.get(name), None if not np.isfinite(z) else round(z, 2),
                     None if not np.isfinite(st["hit"]) else round(st["hit"], 2), round(st["max_dd"], 2), v, why])
    return [[x if x is not None else "" for x in r] for r in rows]


def run(dry_run: bool = False) -> list[list]:
    from .hft_shadow import book_split

    cfg = json.loads(REVIEW_FILE.read_text())
    today = f"{pd.Timestamp.now(tz='America/New_York'):%Y-%m-%d}"
    sheet = Sheet(os.environ["HFT_SHEET_ID"], os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    rows = review(sheet, book_split(), cfg, today)
    action = [f"{r[1]}: {r[10]}" for r in rows if r[10] in ("cut", "halve")]
    status = (f"Reviewed {today} - " + ("; ".join(action) + " (proposed; goes in by pull request)." if action
                                        else "no change: every sleeve in the book is 'keep' or 'too early'."))
    if not dry_run:
        sheet.write(rows, status)
    LOG.info("weekly review: %s", status)
    for r in rows:
        LOG.info("  %s", r[1:])
    return rows


def main(argv=None):
    import argparse

    from ..utils import setup_logging

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    setup_logging()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
