"""Do satellite readings of critical-raw-material plants predict their futures?

Input: daily MODIS thermal anomalies at ~25 smelters / refineries (``qtrade.data.satellite``).
For each commodity, the activity index is the plants' summed fire radiative power (FRP) over the
last 28 days, as an anomaly against its own trailing year:

    anomaly = log(1 + FRP_28d) - log(1 + median of FRP_28d over the previous 365 days)

Publication lag: a MODIS day becomes usable here ``LAG_DAYS`` after it (the 8-day files appear on
the Planetary Computer a few days after the period ends), so the signal on Friday F only uses
satellite days up to F - LAG_DAYS.

Trade: each Friday close, long or short the commodity's future by the sign of the anomaly (or of
its 4-week change), held to the next Friday close; the direction is fixed on 2012-2019 and judged
on 2020-2026. Futures are Yahoo's continuous front months (roll jumps included - a small bias,
the same in both directions). Nickel has no free futures series: its signal is tested on the PICK
metals-miners ETF, as a proxy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..data.satellite import daily_by_site
from ..utils import LOG, setup_logging

LAG_DAYS = 12
INSTRUMENT = {"copper": "HG=F", "nickel": "PICK", "pgm_palladium": "PA=F", "pgm_platinum": "PL=F",
              "aluminium": "ALI=F", "rare_earths": "REMX"}
TRAIN = ("2012-01-01", "2019-12-31")
TEST = ("2020-01-01", "2026-12-31")


def activity(daily: pd.DataFrame) -> pd.DataFrame:
    """Daily FRP per commodity (sum over its sites), every calendar day (missing days = 0 fire)."""
    a = daily.groupby(["date", "commodity"])["frp_mw"].sum().unstack().sort_index()
    idx = pd.date_range(a.index.min(), a.index.max(), freq="D")
    return a.reindex(idx).fillna(0.0)


def signals(act: pd.DataFrame, fridays: pd.DatetimeIndex, lag: int = LAG_DAYS) -> dict[str, pd.DataFrame]:
    """Per signal name: a (Friday x commodity) frame using only satellite days <= Friday - lag."""
    s28 = act.rolling(28, min_periods=20).sum()
    base = s28.rolling(365, min_periods=180).median().shift(1)
    anom = np.log1p(s28) - np.log1p(base)
    known = fridays - pd.Timedelta(days=lag)
    level = anom.reindex(known, method="ffill")
    level.index = fridays
    change = level - level.shift(4)
    return {"level (28d FRP vs its trailing year)": level, "4-week change of the level": change}


def weekly_returns(prices: pd.DataFrame, fridays: pd.DatetimeIndex) -> pd.DataFrame:
    """Friday close -> next Friday close."""
    p = prices.reindex(prices.index.union(fridays)).ffill().reindex(fridays)
    return p.shift(-1) / p - 1


def _sharpe(x: pd.Series) -> float:
    x = x.dropna()
    return float(x.mean() / x.std() * np.sqrt(52)) if len(x) > 20 and x.std() > 0 else np.nan


def evaluate(sig: pd.DataFrame, ret: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for com, inst in INSTRUMENT.items():
        if com not in sig or inst not in ret:
            continue
        s, r = sig[com], ret[inst]
        ok = s.notna() & r.notna()
        s, r = s[ok], r[ok]
        tr, te = (s.index >= TRAIN[0]) & (s.index <= TRAIN[1]), (s.index >= TEST[0]) & (s.index <= TEST[1])
        pos = np.sign(s)
        d = np.sign((pos[tr] * r[tr]).mean()) if tr.sum() > 52 else np.nan
        d = d if np.isfinite(d) and d != 0 else 1.0
        pnl = d * pos * r
        row = {"commodity": com, "instrument": inst, "direction": "follow activity" if d > 0 else "fade activity",
               "weeks_train": int(tr.sum()), "weeks_test": int(te.sum())}
        for tag, m in (("train", tr), ("test", te)):
            c = np.corrcoef(s[m], r[m])[0, 1] if m.sum() > 20 else np.nan
            row.update({f"corr_{tag}": c, f"t_{tag}": c * np.sqrt(max(m.sum() - 2, 1)) / np.sqrt(max(1 - c * c, 1e-9))
                        if np.isfinite(c) else np.nan,
                        f"sharpe_{tag}": _sharpe(pnl[m]), f"hit_{tag}": float((pnl[m] > 0).mean()) if m.sum() else np.nan})
        rows.append(row)
    return pd.DataFrame(rows)


def coverage(daily: pd.DataFrame) -> pd.DataFrame:
    g = daily.groupby(["commodity", "site"])
    return pd.DataFrame({"days": g.size(), "days_with_fire": g["fire_pixels"].apply(lambda x: int((x > 0).sum())),
                         "share_days_with_fire": g["fire_pixels"].apply(lambda x: float((x > 0).mean())),
                         "mean_frp_mw": g["frp_mw"].mean()}).reset_index().sort_values(["commodity", "site"])


def run(sat_cache: Path, out: Path) -> dict:
    from ..data.loader import download_prices

    out.mkdir(parents=True, exist_ok=True)
    files = sorted(Path(sat_cache).glob("modis_*.parquet"))
    raw = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    daily = daily_by_site(raw)
    cov = coverage(daily)
    act = activity(daily)
    md = download_prices(list(INSTRUMENT.values()), start="2011-01-01")
    prices = md.close
    fridays = pd.date_range(max(act.index.min() + pd.Timedelta(days=400), prices.index.min()),
                            min(act.index.max() + pd.Timedelta(days=LAG_DAYS), prices.index.max()), freq="W-FRI")
    ret = weekly_returns(prices, fridays)
    tabs = []
    for name, sig in signals(act, fridays).items():
        t = evaluate(sig, ret)
        t.insert(0, "signal", name)
        tabs.append(t)
    res = pd.concat(tabs, ignore_index=True)
    res.to_csv(out / "crm_satellite_results.csv", index=False)
    cov.to_csv(out / "crm_satellite_coverage.csv", index=False)
    latest = {name: sig.iloc[-1].round(3).to_dict() for name, sig in signals(act, fridays).items()}
    lines = ["## Critical raw materials: satellite activity at smelters vs futures", "",
             f"MODIS daily thermal anomalies (Terra + Aqua, 1 km) at {daily['site'].nunique()} plants, "
             f"{daily['date'].min():%Y-%m-%d} to {daily['date'].max():%Y-%m-%d}. Signal on each Friday uses satellite "
             f"days up to {LAG_DAYS} days earlier (publication lag). Weekly futures returns, Friday close to Friday close; "
             f"direction fixed on {TRAIN[0][:4]}-{TRAIN[1][:4]}, judged on {TEST[0][:4]}-{TEST[1][:4]}. Nickel is tested on "
             "the PICK miners ETF (no free nickel futures series).", "",
             res.round(3).to_markdown(index=False), "",
             "### Detection by site (is the plant visible to MODIS?)", "",
             cov.round(3).to_markdown(index=False), "",
             "### Latest readings", "", "```", json.dumps(latest, indent=1, default=str), "```", ""]
    (out / "crm_satellite.md").write_text("\n".join(lines) + "\n")
    return {"results": res.round(3).to_dict(orient="records")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sat-cache", default="data/satellite")
    ap.add_argument("--out", default="reports/crm")
    args = ap.parse_args(argv)
    setup_logging()
    print(json.dumps(run(Path(args.sat_cache), Path(args.out)), indent=1, default=str))


if __name__ == "__main__":
    main()
