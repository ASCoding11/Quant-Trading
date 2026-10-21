# Research backlog

Ideas queued for the overnight research loop. Each wave is pushed as a commit
with a `[zoo: ...]` / `[research: ...]` tag, runs in GitHub Actions on real
data, and adds its results to `research/zoo/best_correlations.csv` on the
`results` branch. Ticked = pushed.

## Signals (ideas lab, `qtrade/research/ideas.py`)

- [x] **Wave 1**: momentum variants (vol-scaled, frog-in-the-pan, consistency,
  peer-relative, time-series), trend shape (MA gap, MACD, distance from high),
  volatility change, skewness, co-skewness, illiquidity change, OBV divergence,
  fundamentals (earnings/revenue growth, ROE, leverage, net issuance, R&D, cash)
- [ ] **Wave 2**: seasonality (stock's same-calendar-month return over 1-10
  years, weekday, pre-holiday), overnight momentum (overnight returns persist),
  52-week low, nominal price level, volume-spike continuation vs reversal,
  earnings-surprise revisions (change in SUE), sector leader -> follower lead-lag
- [ ] **Wave 3**: interactions found to stick (momentum x 52-week high,
  reversal x momentum, reversal x HMM stress) as single signals; rank and
  nonlinear transforms of the best signals; signal decay-adjusted blends

## Models (model zoo, `qtrade/research/zoo.py`)

- [x] 21 base families x 4 signal sets x 1/5/21 days
- [x] 13 more families (random forest, robust/early-stopped boosting, PLS,
  Bayesian ridge, SVR, kernel bandwidths, decayed/expanding/regime ridge,
  stacking) and a 63-day horizon for all
- [ ] Other targets: factor-residual returns, volatility-scaled returns,
  top/bottom-decile classification
- [ ] Feature engineering: sticky pairs and the best ideas as inputs; two-stage
  lasso-selection then boosting

## Strategies (`qtrade/research/strategies.py`)

- [x] Market timing, cross-asset trend/risk parity, sector momentum, stock
  factors, pairs, earnings premium
- [ ] Sector- and beta-neutral factor books; momentum crash protection
  (volatility-scaled momentum); ETF pair trades; a risk-parity blend of the
  momentum and reversal books
- [ ] Intraday (5-minute data): opening drive, last-half-hour momentum,
  overnight-intraday reversal
