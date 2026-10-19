"""Full backtest: research pipeline -> every model through the same portfolio
rules -> overfitting-aware statistics -> HTML report and data files."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..config import Config
from ..data.market import MarketData
from ..pipeline import build_research
from ..utils import LOG
from .engine import run_backtest
from .metrics import deflated_sharpe, summarize
from .report import charts, write_markdown, write_report

BIAS_NOTES = [
    "<b>Read these results with care.</b> The universe is today's largest companies that have "
    "traded for 15+ years, tested over the past - so it never holds a company that later failed "
    "or shrank (survivorship and look-ahead bias). Expect live results to be weaker.",
    "Everything else is out-of-sample: signals use only past data, models are refit walk-forward, "
    "trades fill at the next day's open, and spread, market impact and borrow fees are charged.",
    "The <b>deflated Sharpe</b> is the probability the true Sharpe is above zero after "
    "correcting for having tried every model on this page. Below ~95% the edge is not "
    "statistically convincing.",
]


def run(md: MarketData, cfg: Config, out_dir: str | Path | None = None, synthetic: bool = False) -> dict:
    out_dir = Path(out_dir or cfg.report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    research = build_research(md, cfg)

    results, comparison, rows = {}, {}, []
    for name in research.wf.predictions:
        bt = run_backtest(research.ctx, research.prediction(name), research.fwd_ret, cfg,
                          name=name, record_weights=(name == cfg.model.trade_model))
        results[name] = bt
        comparison[name] = bt.returns
        s = summarize(bt.returns, bt.daily)
        rows.append({"model": name, "sharpe": s["sharpe"], "ann_return": s["ann_return"],
                     "ann_vol": s["ann_vol"], "max_drawdown": s["max_drawdown"],
                     "ann_turnover": s["ann_turnover"], "ann_cost_drag": s["ann_cost_drag"],
                     "mean_ic": float(np.nanmean(bt.ic.reindex(bt.daily.index)))})
    cmp_tbl = pd.DataFrame(rows).set_index("model").sort_values("sharpe", ascending=False)

    main = results[cfg.model.trade_model]
    bench = research.ctx.market_ret
    summary = summarize(main.returns, main.daily, benchmark=bench)
    summary["deflated_sharpe_prob"] = deflated_sharpe(main.returns, cmp_tbl["sharpe"].tolist())
    summary["n_models_tried"] = len(cmp_tbl)
    summary["n_signals"] = len(research.signal_names)
    summary["n_stocks"] = len(md.tickers)
    summary["model"] = main.name

    ic_table = research.signal_ic_table()
    imgs = charts(main, bench, research.regimes, comparison, ic_table,
                  research.wf.weights.get("ridge", []), research.signal_names)
    notes = list(BIAS_NOTES)
    if synthetic:
        notes = ["<b>Synthetic data.</b> This run used a simulated market with planted "
                 "patterns, to check that the machinery works. It says nothing about real markets."]
    path = write_report(main, summary, cmp_tbl, ic_table, imgs, cfg, out_dir, notes)
    write_markdown(summary, cmp_tbl, ic_table, imgs, out_dir, notes, cfg)

    main.daily.to_csv(out_dir / "daily.csv")
    cmp_tbl.to_csv(out_dir / "model_comparison.csv")
    ic_table.to_csv(out_dir / "signal_ic.csv", index=False)
    research.regimes.to_csv(out_dir / "regimes.csv")
    if main.weights is not None:
        last = main.weights.iloc[-1]
        last[last.abs() > 1e-6].sort_values().to_csv(out_dir / "latest_weights.csv", header=["weight"])
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    LOG.info("report written to %s", path)
    LOG.info("Sharpe %.2f | ann. return %.1f%% | max DD %.1f%% | deflated Sharpe prob %.1f%%",
             summary["sharpe"], summary["ann_return"] * 100, summary["max_drawdown"] * 100,
             summary["deflated_sharpe_prob"] * 100)
    return {"summary": summary, "comparison": cmp_tbl, "report": str(path), "research": research,
            "results": results}
