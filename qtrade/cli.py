"""Command line interface.

    python -m qtrade universe            # pick the top-1000, 15-year-history universe
    python -m qtrade download            # download / refresh daily prices
    python -m qtrade backtest            # full walk-forward backtest + HTML report
    python -m qtrade demo                # same pipeline on a synthetic market (offline)
    python -m qtrade paper               # paper-trading dry run (prints orders)
    python -m qtrade paper --send        # actually place orders on Alpaca paper
    python -m qtrade signals             # list every signal in the library
"""
from __future__ import annotations

import argparse
import os
import sys
import warnings

import pandas as pd

from .config import Config
from .utils import LOG, setup_logging


def _cfg(args) -> Config:
    overrides: dict = {}
    if getattr(args, "size", None):
        overrides.setdefault("universe", {})["size"] = args.size
    if getattr(args, "years", None):
        overrides.setdefault("universe", {})["min_history_years"] = args.years
    if getattr(args, "start", None):
        overrides.setdefault("data", {})["start"] = args.start
    if getattr(args, "end", None):
        overrides.setdefault("data", {})["end"] = args.end
    if getattr(args, "models", None):
        ms = args.models.split(",")
        overrides["model"] = {"models": ms, "ensemble": [m for m in ms if m != "elastic_net"] or ms}
    if getattr(args, "horizon", None):
        overrides.setdefault("model", {})["horizon"] = args.horizon
    return Config.load(args.config, overrides)


def cmd_universe(args):
    from .data import build_universe, save_universe

    cfg = _cfg(args)
    u = cfg.universe
    uni = build_universe(u.size, u.min_history_years, u.candidate_source, u.universe_file,
                         start=cfg.data.start, batch_size=cfg.data.batch_size)
    path = save_universe(uni, cfg.data.cache_dir)
    print(f"Saved {len(uni)} companies to {path}")
    print(uni.head(15).to_string(index=False))


def _market(cfg):
    from .data import build_universe, get_market_data, load_universe, save_universe

    uni = load_universe(cfg.data.cache_dir)
    if uni is None:
        u = cfg.universe
        uni = build_universe(u.size, u.min_history_years, u.candidate_source, u.universe_file,
                             start=cfg.data.start, batch_size=cfg.data.batch_size)
        save_universe(uni, cfg.data.cache_dir)
    tickers = uni["ticker"].head(cfg.universe.size).tolist()
    return get_market_data(tickers, cfg.data.start, cfg.data.end, cfg.data.cache_dir, cfg.data.batch_size)


def cmd_download(args):
    cfg = _cfg(args)
    md = _market(cfg)
    print(f"{len(md.tickers)} tickers, {md.dates[0].date()} -> {md.dates[-1].date()}")


def cmd_backtest(args):
    from .backtest.runner import run

    cfg = _cfg(args)
    md = _market(cfg)
    out = run(md, cfg, args.out)
    _print_result(out)


def cmd_demo(args):
    from .backtest.runner import run
    from .data import make_market

    cfg = _cfg(args)
    cfg.universe.min_dollar_volume = 0
    md, _ = make_market(n_stocks=args.stocks, n_days=args.days, seed=args.seed)
    out = run(md, cfg, args.out or "reports/demo", synthetic=True)
    _print_result(out)


def cmd_paper(args):
    from .live.alpaca_trader import run_paper

    cfg = _cfg(args)
    run_paper(cfg, dry_run=not args.send)


def cmd_signals(args):
    from .signals import list_signals

    with pd.option_context("display.max_colwidth", 90, "display.width", 160):
        print(list_signals().to_string(index=False))


def _print_result(out):
    s = out["summary"]
    print("\n" + "=" * 64)
    print(f" {s['start']} -> {s['end']}   model: {s['model']}   stocks: {s['n_stocks']}")
    print(f" Sharpe {s['sharpe']:.2f} | return {s['ann_return']*100:.1f}%/yr | vol {s['ann_vol']*100:.1f}% "
          f"| max DD {s['max_drawdown']*100:.1f}%")
    print(f" deflated-Sharpe probability {s['deflated_sharpe_prob']*100:.0f}% over {s['n_models_tried']} models")
    print("=" * 64)
    print(out["comparison"].round(3).to_string())
    print(f"\nReport: {out['report']}")


def main(argv=None):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    ap = argparse.ArgumentParser(prog="qtrade", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="YAML config file (default: built-in defaults)")
    ap.add_argument("--log", default="INFO")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--size", type=int, help="number of companies (default 1000)")
        p.add_argument("--years", type=float, help="minimum years of history (default 15)")
        p.add_argument("--start", help="first date of data, e.g. 2000-01-01")
        p.add_argument("--end", help="last date of data")
        p.add_argument("--models", help="comma list: ridge,elastic_net,regime_ridge,kernel_ridge,gbm,ic_weighted")
        p.add_argument("--horizon", type=int, help="forecast horizon in days (default 5)")
        return p

    common(sub.add_parser("universe", help="select the trading universe")).set_defaults(fn=cmd_universe)
    common(sub.add_parser("download", help="download daily prices")).set_defaults(fn=cmd_download)
    p = common(sub.add_parser("backtest", help="run the full backtest"))
    p.add_argument("--out", help="report directory (default reports/)")
    p.set_defaults(fn=cmd_backtest)
    p = common(sub.add_parser("demo", help="run on a synthetic market (no internet needed)"))
    p.add_argument("--stocks", type=int, default=200)
    p.add_argument("--days", type=int, default=2520)
    p.add_argument("--seed", type=int, default=3)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_demo)
    p = common(sub.add_parser("paper", help="paper trade on Alpaca"))
    p.add_argument("--send", action="store_true", help="really submit orders (paper account)")
    p.set_defaults(fn=cmd_paper)
    sub.add_parser("signals", help="list the signal library").set_defaults(fn=cmd_signals)

    args = ap.parse_args(argv)
    setup_logging(args.log)
    LOG.debug("args: %s", args)
    try:
        args.fn(args)
    except (Exception, SystemExit) as exc:
        if isinstance(exc, SystemExit) and exc.code in (0, None):
            raise
        if os.environ.get("GITHUB_ACTIONS"):
            # surfaces as an annotation on the run page, readable without opening logs
            msg = str(exc).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::error title=qtrade {args.cmd} failed::{type(exc).__name__}: {msg}", flush=True)
        raise
    return 0


if __name__ == "__main__":
    sys.exit(main())
