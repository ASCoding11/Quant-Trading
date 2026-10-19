"""Self-contained HTML backtest report (charts embedded as PNG) plus CSV/JSON."""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from .metrics import annual_returns, drawdown_series, monthly_table, rolling_sharpe  # noqa: E402

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
BENCH = "#9a9893"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold",
    "axes.titlesize": 10, "axes.titlecolor": INK, "axes.titlelocation": "left", "legend.frameon": False,
})


def _log_axis(ax) -> None:
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.2f}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def _png(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _fmt(v, kind="pct"):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "–"
    if kind == "pct":
        return f"{v * 100:.1f}%"
    if kind == "num":
        return f"{v:.2f}"
    return str(v)


def charts(res, benchmark: pd.Series, regimes: pd.DataFrame, comparison: dict[str, pd.Series],
           ic_table: pd.DataFrame, weights_hist: list, signal_names: list[str]) -> dict[str, str]:
    r = res.returns
    bench = benchmark.reindex(r.index).fillna(0)
    # scale the benchmark to the strategy's volatility so the curves are comparable
    bench_scaled = bench * (r.std() / bench.std() if bench.std() > 0 else 1)
    out = {}

    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot((1 + r).cumprod(), color=SERIES[0], lw=2, label="Strategy (net of costs)")
    ax.plot((1 + bench_scaled).cumprod(), color=BENCH, lw=1.5, label="Equal-weight universe, same vol")
    _log_axis(ax)
    ax.set_title("Growth of $1")
    ax.legend(loc="upper left")
    out["equity"] = _png(fig)

    fig, ax = plt.subplots(figsize=(9, 2.2))
    dd = drawdown_series(r)
    ax.fill_between(dd.index, dd.values, 0, color=SERIES[0], alpha=0.35, lw=0)
    ax.plot(dd, color=SERIES[0], lw=1)
    ax.set_title("Drawdown")
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    out["drawdown"] = _png(fig)

    fig, ax = plt.subplots(figsize=(9, 2.4))
    ax.plot(rolling_sharpe(r), color=SERIES[0], lw=1.5)
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("Rolling 1-year Sharpe ratio")
    out["rolling_sharpe"] = _png(fig)

    fig, ax = plt.subplots(figsize=(9, 2.6))
    ar = annual_returns(r)
    ax.bar(ar.index.astype(str), ar.values, color=SERIES[0], width=0.6)
    ax.axhline(0, color=MUTED, lw=1)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.set_title("Return by calendar year")
    ax.tick_params(axis="x", rotation=60)
    out["annual"] = _png(fig)

    fig, ax = plt.subplots(figsize=(9, 2.4))
    ax.plot(res.daily["gross"], color=SERIES[0], lw=1.2, label="Gross exposure")
    ax.plot(res.daily["net"], color=SERIES[1], lw=1.2, label="Net exposure")
    ax.set_title("Exposure (multiples of equity)")
    ax.legend(loc="upper left", ncol=2)
    out["exposure"] = _png(fig)

    # regimes: stacked filtered probabilities over the backtest window
    reg = regimes.reindex(r.index).ffill()
    fig, ax = plt.subplots(figsize=(9, 2.4))
    labels = {0: "Calm", 1: "Normal", 2: "Stressed"} if reg.shape[1] == 3 else {k: f"Regime {k}" for k in range(reg.shape[1])}
    ax.stackplot(reg.index, reg.T.values, colors=SERIES[: reg.shape[1]], alpha=0.85,
                 labels=[labels[k] for k in range(reg.shape[1])], lw=0)
    ax.set_ylim(0, 1)
    ax.set_title("Hidden Markov regime probabilities (filtered, no look-ahead)")
    ax.legend(loc="upper left", ncol=reg.shape[1])
    out["regimes"] = _png(fig)

    # model comparison
    fig, ax = plt.subplots(figsize=(9, 3.2))
    for i, (name, rr) in enumerate(comparison.items()):
        ax.plot((1 + rr).cumprod(), lw=2 if name == res.name else 1.2,
                color=SERIES[i % len(SERIES)], label=name)
    _log_axis(ax)
    ax.set_title("Every model, same portfolio rules (growth of $1)")
    ax.legend(loc="upper left", ncol=4)
    out["models"] = _png(fig)

    # signal ICs
    t = ic_table.sort_values("ic_ir")
    fig, ax = plt.subplots(figsize=(9, max(4, 0.2 * len(t))))
    colors = [SERIES[0] if v > 0 else SERIES[1] for v in t["ic_ir"]]
    ax.barh(t["signal"], t["ic_ir"], color=colors, height=0.7)
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_title("Signal information ratio (annualised mean IC / std IC)")
    ax.tick_params(axis="y", labelsize=8)
    out["signals"] = _png(fig)

    # ridge weights over time
    if weights_hist:
        dates = [d for d, _ in weights_hist]
        W = np.array([w for _, w in weights_hist])
        fig, ax = plt.subplots(figsize=(9, max(4, 0.2 * W.shape[1])))
        lim = np.nanmax(np.abs(W)) or 1
        im = ax.imshow(W.T, aspect="auto", cmap="RdBu_r", vmin=-lim, vmax=lim, interpolation="nearest")
        ax.set_yticks(range(W.shape[1]))
        ax.set_yticklabels(signal_names[: W.shape[1]], fontsize=7)
        step = max(1, len(dates) // 10)
        ax.set_xticks(range(0, len(dates), step))
        ax.set_xticklabels([str(d.year) for d in dates[::step]])
        ax.grid(False)
        ax.set_title("Ridge signal weights at each walk-forward refit")
        fig.colorbar(im, ax=ax, fraction=0.025)
        out["weights"] = _png(fig)
    return out


CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#0b0b0b;background:#fcfcfb;margin:0}
main{max-width:980px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:32px 0 8px}
.sub{color:#52514e;margin:0 0 20px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.tile{background:#f3f2ee;border-radius:8px;padding:10px 12px}.tile b{display:block;font-size:20px}
.tile span{color:#52514e;font-size:12px}
img{width:100%;height:auto;margin:6px 0}
table{border-collapse:collapse;width:100%;font-size:12px;margin:8px 0}
th,td{padding:4px 6px;border-bottom:1px solid #e6e5e0;text-align:right}th:first-child,td:first-child{text-align:left}
th{color:#52514e;font-weight:600}
.note{background:#fff7e6;border-left:3px solid #eda100;padding:10px 12px;border-radius:4px;color:#3a3936}
.scroll{overflow-x:auto}
"""


def write_report(res, summary: dict, comparison_tbl: pd.DataFrame, ic_table: pd.DataFrame,
                 imgs: dict[str, str], cfg, out_dir: str | Path, notes: list[str]) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    s = summary
    tiles = [
        ("Sharpe ratio", _fmt(s["sharpe"], "num")), ("Annual return", _fmt(s["ann_return"])),
        ("Annual volatility", _fmt(s["ann_vol"])), ("Max drawdown", _fmt(s["max_drawdown"])),
        ("Deflated Sharpe (prob.)", _fmt(s.get("deflated_sharpe_prob"))),
        ("Beta to market", _fmt(s.get("beta_to_market"), "num")),
        ("Avg gross exposure", f"{s.get('avg_gross', 0):.2f}x"),
        ("Cost drag / yr", _fmt(s.get("ann_cost_drag"))),
    ]
    tiles_html = "".join(f'<div class="tile"><b>{v}</b><span>{k}</span></div>' for k, v in tiles)
    mt = monthly_table(res.returns)
    mt_html = mt.map(lambda v: "" if pd.isna(v) else f"{v * 100:.1f}").to_html(classes="m", border=0)
    ic_html = ic_table.round(4).to_html(index=False, border=0)
    cmp_html = comparison_tbl.to_html(border=0, float_format=lambda v: f"{v:.3f}")
    notes_html = "".join(f"<p>{n}</p>" for n in notes)
    img = lambda k: f'<img alt="{k}" src="data:image/png;base64,{imgs[k]}">' if k in imgs else ""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Backtest Report</title><style>{CSS}</style></head><body><main>
<h1>Statistical-arbitrage backtest</h1>
<p class="sub">{s['start']} → {s['end']} · {s['years']:.1f} years · traded model: <b>{res.name}</b> ·
forecast horizon {cfg.model.horizon}d · costs and borrow included</p>
<div class="tiles">{tiles_html}</div>
<div class="note">{notes_html}</div>
<h2>Performance</h2>{img('equity')}{img('drawdown')}{img('rolling_sharpe')}{img('annual')}
<h2>Exposure and regimes</h2>{img('exposure')}{img('regimes')}
<h2>Model comparison</h2><p class="sub">Each model's forecasts run through identical portfolio and cost rules.
The deflated Sharpe corrects the chosen model for having tried all of these.</p>{img('models')}
<div class="scroll">{cmp_html}</div>
<h2>Signals</h2>{img('signals')}{img('weights')}
<div class="scroll">{ic_html}</div>
<h2>Monthly returns (%)</h2><div class="scroll">{mt_html}</div>
<h2>Configuration</h2><pre style="font-size:11px;white-space:pre-wrap">{json.dumps(cfg.to_dict(), indent=1)}</pre>
</main></body></html>"""
    path = out_dir / "report.html"
    path.write_text(html)
    return path
