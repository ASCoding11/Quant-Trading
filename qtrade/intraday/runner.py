"""Intraday backtest end to end: forecasts once, then the same forecasts traded
at several rebalance intervals, with and without costs."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..backtest.metrics import deflated_sharpe
from ..utils import LOG
from .bars import DayBars
from .strategy import ic_for_sizing, prepare, run_backtest

REBALANCE_GRID = [1, 3, 6, 12]          # bars: every 5, 15, 30, 60 minutes


def stats(daily: pd.DataFrame) -> dict:
    r = daily["ret"]
    sd = r.std()
    eq = (1 + r).cumprod()
    half = r.index[len(r) // 2] if len(r) else None
    sh = lambda x: float(x.mean() / x.std() * np.sqrt(252)) if len(x) > 2 and x.std() > 0 else float("nan")  # noqa: E731
    return {
        "start": str(r.index[0].date()), "end": str(r.index[-1].date()), "days": len(r),
        "sharpe": sh(r), "sharpe_pre_cost": sh(daily["pre_cost"]),
        "sharpe_1st_half": sh(r[r.index < half]), "sharpe_2nd_half": sh(r[r.index >= half]),
        "ann_return": float(r.mean() * 252), "ann_vol": float(sd * np.sqrt(252)),
        "ann_return_pre_cost": float(daily["pre_cost"].mean() * 252),
        "ann_cost": float(daily["cost"].mean() * 252),
        "max_drawdown": float((eq / eq.cummax() - 1).min()),
        "turnover_per_day": float(daily["turnover"].mean()),
        "avg_gross": float(daily["avg_gross"].mean()),
        "trades_per_day": float(daily["trades"].mean()),
        "edge_bp_per_dollar_traded": float(daily["pre_cost"].sum() / max(daily["turnover"].sum(), 1e-12) * 1e4),
        "cost_bp_per_dollar_traded": float(daily["cost"].sum() / max(daily["turnover"].sum(), 1e-12) * 1e4),
    }


def run(bars: DayBars, cfg, out_dir: str | Path) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    icfg = cfg.intraday
    hist, pred, log, final, daily_ic = prepare(bars, icfg)
    ic_size = ic_for_sizing(daily_ic)

    variants, results = [], {}
    for every in sorted(set(REBALANCE_GRID + [icfg.rebalance_every])):
        for fric in (False, True):
            c = copy.deepcopy(icfg)
            c.rebalance_every = every
            name = f"every {every * bars.bar_minutes} min" + (" (costs not charged)" if fric else "")
            daily = run_backtest(bars, hist, pred, c, ic_size, frictionless=fric)
            results[name] = daily
            variants.append({"variant": name, "rebalance_minutes": every * bars.bar_minutes,
                             "costs": not fric, **stats(daily)})
            LOG.info("%-28s Sharpe %.2f (pre-cost %.2f)", name, variants[-1]["sharpe"],
                     variants[-1]["sharpe_pre_cost"])
    for mult in (0.5, 2.0):                 # cost sensitivity at the configured interval
        c = copy.deepcopy(icfg)
        c.spread_tiers = [[t, b * mult] for t, b in icfg.spread_tiers]
        c.slippage_bps = icfg.slippage_bps * mult
        name = f"every {icfg.rebalance_every * bars.bar_minutes} min, costs x{mult:g}"
        daily = run_backtest(bars, hist, pred, c, ic_size)
        variants.append({"variant": name, "rebalance_minutes": icfg.rebalance_every * bars.bar_minutes,
                         "costs": True, **stats(daily)})
    vt = pd.DataFrame(variants).set_index("variant")

    main_name = f"every {icfg.rebalance_every * bars.bar_minutes} min"
    main = results[main_name]
    summary = stats(main) | {
        "variant": main_name, "n_stocks": len(bars.tickers), "bar_minutes": bars.bar_minutes,
        "mean_oos_ic": float(np.nanmean(daily_ic)),
        "deflated_sharpe_prob": float(deflated_sharpe(main["ret"], vt.loc[vt["costs"], "sharpe"].tolist())),
    }
    by_year = main.groupby(main.index.year).agg(
        ret=("ret", "sum"), pre_cost=("pre_cost", "sum"), cost=("cost", "sum"),
        sharpe=("ret", lambda r: r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan),
        turnover=("turnover", "mean"), oos_ic=("ic", "mean"))

    main.to_csv(out / "daily.csv")
    vt.to_csv(out / "variants.csv")
    by_year.to_csv(out / "by_year.csv")
    log.to_csv(out / "model_log.csv", index=False)
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    if final:
        final["config"] = {k: v for k, v in vars(icfg).items()}
        (out / "model.json").write_text(json.dumps(final, indent=1))
    _chart(results, out)
    _markdown(summary, vt, by_year, log, out)
    LOG.info("intraday report written to %s", out)
    return {"summary": summary, "variants": vt, "by_year": by_year, "daily": main, "model": final}


def _chart(results: dict, out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for name, d in results.items():
        if "not charged" in name:
            continue
        ax.plot((1 + d["ret"]).cumprod(), label=name, lw=1.2)
    ax.axhline(1, color="grey", lw=0.6)
    ax.set_title("Intraday reversal: growth of $1 after costs")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "equity.png", dpi=110)
    plt.close(fig)


def _markdown(summary: dict, vt: pd.DataFrame, by_year: pd.DataFrame, log: pd.DataFrame, out: Path) -> None:
    pct = lambda x: f"{x * 100:.1f}%"  # noqa: E731
    lines = [
        "# Intraday backtest", "",
        f"{summary['n_stocks']} stocks, {summary['bar_minutes']}-minute bars, "
        f"{summary['start']} to {summary['end']} ({summary['days']} sessions). "
        "Walk-forward ridge refit monthly; trades at the next bar's open; flat every night.", "",
        f"**{summary['variant']}: Sharpe {summary['sharpe']:.2f}** after costs "
        f"({summary['sharpe_pre_cost']:.2f} before), {pct(summary['ann_return'])}/yr, "
        f"max drawdown {pct(summary['max_drawdown'])}, deflated-Sharpe probability "
        f"{summary['deflated_sharpe_prob'] * 100:.0f}%. Edge {summary['edge_bp_per_dollar_traded']:.2f} bp "
        f"per dollar traded vs. cost {summary['cost_bp_per_dollar_traded']:.2f} bp. "
        f"Mean out-of-sample IC {summary['mean_oos_ic']:.4f}.", "",
        "![equity](equity.png)", "",
        "## Rebalance interval and costs", "",
        "| variant | Sharpe | pre-cost | 1st half | 2nd half | return/yr | cost/yr | turnover/day | trades/day |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for name, r in vt.iterrows():
        lines.append(f"| {name} | {r.sharpe:.2f} | {r.sharpe_pre_cost:.2f} | {r.sharpe_1st_half:.2f} | "
                     f"{r.sharpe_2nd_half:.2f} | {pct(r.ann_return)} | {pct(r.ann_cost)} | "
                     f"{r.turnover_per_day:.1f}x | {r.trades_per_day:.0f} |")
    lines += ["", "## By year", "", "| year | return | pre-cost | cost | Sharpe | turnover/day | OOS IC |",
              "|---|---|---|---|---|---|---|"]
    for y, r in by_year.iterrows():
        lines.append(f"| {y} | {pct(r.ret)} | {pct(r.pre_cost)} | {pct(r.cost)} | {r.sharpe:.2f} | "
                     f"{r.turnover:.1f}x | {r.oos_ic:.4f} |")
    if len(log):
        from .features import FEATURES

        last = log.iloc[-1]
        lines += ["", f"## Latest model ({last['month']})", "", "| feature | weight |", "|---|---|"]
        lines += [f"| {f} | {last[f]:+.4f} |" for f in FEATURES]
    (out / "README.md").write_text("\n".join(lines) + "\n")
