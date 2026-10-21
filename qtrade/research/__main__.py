"""python -m qtrade.research --tasks quality,spreads,edge,hmm --out reports/research"""
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

from ..config import Config
from ..utils import LOG, setup_logging


def main(argv=None):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="quality,spreads,edge,hmm")
    ap.add_argument("--out", default="reports/research")
    ap.add_argument("--config")
    ap.add_argument("--synthetic", action="store_true", help="offline smoke test on a simulated market")
    args = ap.parse_args(argv)
    setup_logging()
    cfg = Config.load(args.config)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.synthetic:
        from ..data import make_market

        md, _ = make_market(n_stocks=150, n_days=3000, seed=1, start="2004-01-02")
        cfg.universe.min_dollar_volume = 0
    else:
        from ..cli import _market

        md = _market(cfg)
    from ..features.context import FeatureContext

    ctx = FeatureContext(md, cfg)
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    summary = {}
    for task in tasks:
        LOG.info("research task: %s", task)
        try:
            if task == "quality":
                from .data_quality import run
                summary[task] = run(md, ctx, out, cfg.data.cache_dir)
            elif task == "spreads":
                from .spreads import run
                summary[task] = run(md, ctx, out)
            elif task == "edge":
                from .edge import run
                summary[task] = run(md, ctx, out)
            elif task == "hmm":
                from .hmm_eval import run
                summary[task] = run(md, ctx, out, cfg)
        except Exception as exc:          # one failing study shouldn't lose the others
            LOG.exception("task %s failed", task)
            summary[task] = {"error": f"{type(exc).__name__}: {exc}"}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    parts = ["# Research results", ""]
    for name in ("data_quality", "spreads", "edge", "hmm"):
        p = out / f"{name}.md"
        if p.exists():
            parts.append(p.read_text())
    (out / "README.md").write_text("\n".join(parts))
    print(json.dumps(summary, indent=1, default=str)[:3000])


if __name__ == "__main__":
    main()
