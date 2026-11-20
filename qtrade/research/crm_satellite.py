"""Do satellite readings of critical-raw-material plants predict their futures?

Two satellite sources, the same test:

* MODIS daily thermal anomalies at ~25 smelters / refineries (``qtrade.data.satellite``), 2012 on;
* Sentinel-5P TROPOMI SO2 plumes over the same plants (``qtrade.data.sentinel5p``), May 2018 on -
  sulphide smelting vents SO2, so the plume tracks copper / nickel / PGM smelter throughput.

MODIS:
For each commodity, the activity index is the plants' summed fire radiative power (FRP) over the
last 28 days, as an anomaly against its own trailing year:

    anomaly = log(1 + FRP_28d) - log(1 + median of FRP_28d over the previous 365 days)

Publication lag: a MODIS day becomes usable here ``LAG_DAYS`` after it (the 8-day files appear on
the Planetary Computer a few days after the period ends), so the signal on Friday F only uses
satellite days up to F - LAG_DAYS.

SO2: per commodity, the day's mean plume enhancement (plume minus a 60-120 km background ring,
Dobson units) over its plants; the signal is its 28-day mean minus the median of that over the
previous year, using satellite days up to ``LAG_DAYS_S5P`` before the Friday (offline products appear
about 5 days after the overpass).

Trade: each Friday close, long or short the commodity's future by the sign of the signal (or of
its 4-week change), held to the next Friday close; the direction is fixed on the training years
(MODIS 2012-2019, SO2 2018-2022) and judged on the rest. ``crm_rules.json`` keeps each signal's
direction for the $0 tracker (``qtrade.intraday.crm_sheet``). Futures are Yahoo's continuous front months (roll jumps included - a small bias,
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
LAG_DAYS_S5P = 7
INSTRUMENT = {"copper": "HG=F", "nickel": "PICK", "pgm_palladium": "PA=F", "pgm_platinum": "PL=F",
              "aluminium": "ALI=F", "rare_earths": "REMX"}
TRAIN = ("2012-01-01", "2019-12-31")
TEST = ("2020-01-01", "2026-12-31")
TRAIN_S5P = ("2018-01-01", "2022-12-31")
TEST_S5P = ("2023-01-01", "2026-12-31")
LEVEL = "level (28d FRP vs its trailing year)"
LEVEL_S5P = "level (28d SO2 plume vs its trailing year)"


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


def so2_activity(daily: pd.DataFrame) -> pd.DataFrame:
    """Per commodity and calendar day: the mean SO2 enhancement (DU) over its plants seen that day (NaN = none seen)."""
    a = daily.groupby(["date", "commodity"])["so2_enh_du"].mean().unstack().sort_index()
    idx = pd.date_range(a.index.min(), a.index.max(), freq="D")
    return a.reindex(idx)


def so2_signals(act: pd.DataFrame, fridays: pd.DatetimeIndex, lag: int = LAG_DAYS_S5P) -> dict[str, pd.DataFrame]:
    """Like ``signals`` for the SO2 plume (a difference in DU, since the enhancement can be negative)."""
    m28 = act.rolling(28, min_periods=8).mean()
    base = m28.rolling(365, min_periods=150).median().shift(1)
    anom = m28 - base
    known = fridays - pd.Timedelta(days=lag)
    level = anom.reindex(known, method="ffill")
    level.index = fridays
    return {LEVEL_S5P: level, "4-week change of the SO2 level": level - level.shift(4)}


def weekly_returns(prices: pd.DataFrame, fridays: pd.DatetimeIndex) -> pd.DataFrame:
    """Friday close -> next Friday close."""
    p = prices.reindex(prices.index.union(fridays)).ffill().reindex(fridays)
    return p.shift(-1) / p - 1


def _sharpe(x: pd.Series) -> float:
    x = x.dropna()
    return float(x.mean() / x.std() * np.sqrt(52)) if len(x) > 20 and x.std() > 0 else np.nan


def evaluate(sig: pd.DataFrame, ret: pd.DataFrame, train: tuple = TRAIN, test: tuple = TEST) -> pd.DataFrame:
    rows = []
    for com, inst in INSTRUMENT.items():
        if com not in sig or inst not in ret:
            continue
        s, r = sig[com], ret[inst]
        ok = s.notna() & r.notna()
        s, r = s[ok], r[ok]
        tr, te = (s.index >= train[0]) & (s.index <= train[1]), (s.index >= test[0]) & (s.index <= test[1])
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


def _fridays(start, end, prices: pd.DataFrame, lag: int) -> pd.DatetimeIndex:
    return pd.date_range(max(start + pd.Timedelta(days=400), prices.index.min()),
                         min(end + pd.Timedelta(days=lag), prices.index.max()), freq="W-FRI")


def rules(res: pd.DataFrame) -> list[dict]:
    """Each level signal's direction (fixed on its training years) and its test record, for the tracker."""
    out = []
    for r in res[res["signal"].isin([LEVEL, LEVEL_S5P])].itertuples():
        out.append({"source": "SO2" if r.signal == LEVEL_S5P else "MODIS", "commodity": r.commodity,
                    "instrument": r.instrument, "direction": 1 if r.direction == "follow activity" else -1,
                    "sharpe_train": None if pd.isna(r.sharpe_train) else round(float(r.sharpe_train), 3),
                    "sharpe_test": None if pd.isna(r.sharpe_test) else round(float(r.sharpe_test), 3),
                    "t_test": None if pd.isna(r.t_test) else round(float(r.t_test), 3)})
    return out


def run(sat_cache: Path, out: Path) -> dict:
    from ..data import sentinel5p as S5
    from ..data.loader import download_prices

    out.mkdir(parents=True, exist_ok=True)
    md = download_prices(list(INSTRUMENT.values()), start="2011-01-01")
    prices = md.close
    tabs, latest, cover = [], {}, []

    files = sorted(Path(sat_cache).glob("modis_*.parquet"))
    if files:
        daily = daily_by_site(pd.concat([pd.read_parquet(f) for f in files], ignore_index=True))
        cov = coverage(daily)
        cov.insert(0, "source", "MODIS")
        cover.append(cov)
        act = activity(daily)
        fr = _fridays(act.index.min(), act.index.max(), prices, LAG_DAYS)
        ret = weekly_returns(prices, fr)
        for name, sig in signals(act, fr).items():
            t = evaluate(sig, ret)
            t.insert(0, "signal", name)
            t.insert(0, "source", "MODIS")
            tabs.append(t)
            latest[f"MODIS {name}"] = sig.iloc[-1].round(3).to_dict()

    files = sorted(Path(sat_cache).glob("s5p_*.parquet"))
    if files:
        raw = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        d5 = S5.daily_by_site(raw)
        g = raw.groupby(["commodity", "site"])
        cov = pd.DataFrame({"days": d5.groupby(["commodity", "site"]).size(),
                            "overpasses": g.size(),
                            "mean_enh_du": d5.groupby(["commodity", "site"])["so2_enh_du"].mean()}).reset_index()
        cov.insert(0, "source", "SO2")
        cover.append(cov)
        act5 = so2_activity(d5)
        fr = _fridays(act5.index.min(), act5.index.max(), prices, LAG_DAYS_S5P)
        ret = weekly_returns(prices, fr)
        for name, sig in so2_signals(act5, fr).items():
            t = evaluate(sig, ret, TRAIN_S5P, TEST_S5P)
            t.insert(0, "signal", name)
            t.insert(0, "source", "SO2")
            tabs.append(t)
            latest[f"SO2 {name}"] = sig.iloc[-1].round(3).to_dict()

    res = pd.concat(tabs, ignore_index=True)
    cov = pd.concat(cover, ignore_index=True)
    res.to_csv(out / "crm_satellite_results.csv", index=False)
    cov.to_csv(out / "crm_satellite_coverage.csv", index=False)
    (out / "crm_rules.json").write_text(json.dumps(rules(res), indent=1))
    lines = ["## Critical raw materials: satellite activity at smelters vs futures", "",
             f"MODIS: daily thermal anomalies (Terra + Aqua, 1 km); signal uses satellite days up to {LAG_DAYS} days "
             f"before each Friday; direction fixed on {TRAIN[0][:4]}-{TRAIN[1][:4]}, judged on {TEST[0][:4]}-{TEST[1][:4]}.",
             f"SO2: Sentinel-5P TROPOMI plume minus background ring (DU); lag {LAG_DAYS_S5P} days; direction fixed on "
             f"{TRAIN_S5P[0][:4]}-{TRAIN_S5P[1][:4]}, judged on {TEST_S5P[0][:4]}-{TEST_S5P[1][:4]}.",
             "Weekly futures returns, Friday close to Friday close. Nickel is tested on the PICK miners ETF, rare earths "
             "on REMX (no free futures series).", "",
             res.round(3).to_markdown(index=False), "",
             "### Coverage by site", "", cov.round(3).to_markdown(index=False), "",
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
