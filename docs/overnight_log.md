# Overnight research log

Running notes from the overnight research loop: what was launched, what came
back, and what it means. Newest first. Full results: `research/` on the
`results` branch.

## 2026-10-21 03:50 UTC: everything not yet covered is now launched

Built, tested on synthetic data, and pushed to run on real data:
- **Public data loaders:** FRED macro, S&P 500 changes, FINRA daily short volume, SEC insider trades, every US stock incl. delisted (Alpaca)
- **Ideas wave 2:** short volume (level and change), insider net and cluster buying, filing delays, correlation-network momentum, calendar-month seasonality, overnight momentum, 52-week low, nominal price, volume-spike continuation, earnings-surprise revisions
- **Ideas wave 3:** daily signals from 5-minute bars (realized skewness and kurtosis, jump share, first/last half hour, realized-vol ratio)
- **Survivorship study:** point-in-time top-1000 incl. delisted stocks vs today's survivors, 2017-2026
- **Events:** 15 headline-classified news types, novel vs stale news, S&P 500 additions/removals
- **Strategies wave 2:** ~30-ETF trend following, volatility premium, sector seasonality, macro timing of market and momentum, momentum crash protection, Ledoit-Wolf optimisation across strategies, capacity to $1B, open vs close execution
- **Model zoo:** sequence models on raw histories; online IC-weighted ensemble; disagreement-sized ensemble

Still open in the backlog: sector/beta-neutral factor books, ETF pair trades, intraday strategies, other training targets, interaction signals as features.
Not possible with free data: options, analyst revisions, borrow fees, supply chains.

## 2026-10-21 03:00 UTC: loop started

Launched:
- model zoo, wave 1: 21 families x 4 signal sets x 1/5/21 days (12 jobs)
- model zoo, wave 2: 13 more families at 1/5/21/63 days + all families at 63 days (8 jobs)
- ideas lab, wave 1: 20 new signals (momentum variants, trend shape, volatility, liquidity, fundamentals) at 1/5/21/63 days
- strategy zoo (rerun after a bug fix): ~20 non-reversal strategies and a diversified book

Findings so far:
- Strongest tradable signal pair: 12-month momentum + 52-week high. Net Sharpe 0.49 (2004-14) / 0.59 (2015-26), break-even 39-46 bp (~10x cost).
- Real spreads match the cost model (1.6 bp for liquid names; 5-8x wider at the open).
- Reversal IC is 2-3x larger in HMM-stressed markets, but trading only then doesn't add net profit.
- GARCH beats the rolling window for stock volatility (146/150 stocks), but scaling the whole book by volatility hurts.
- Jumps cluster (variance/mean 24); jump storms are predictable (7-day half-life); no-news up-jumps reverse twice as much as news-driven ones.
