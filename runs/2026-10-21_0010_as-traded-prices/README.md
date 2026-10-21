# Backtest results

| | |
|---|---|
| Period | 2003-12-19 to 2026-10-20 (22.8 years) |
| Stocks / signals | 1000 / 44 |
| Traded model | ensemble |
| Sharpe ratio | 0.30 |
| Annual return | 11.0% |
| Annual volatility | 36.1% |
| Max drawdown | -25.0% |
| Deflated Sharpe probability | 99.7% |
| Beta / correlation to market | 0.05 / 0.03 |
| Avg gross exposure | 1.07x |
| Annual turnover | 79x |
| Cost + borrow drag / yr | 1.7% |

> **Read these results with care.** The universe is today's largest companies that have traded for 15+ years, tested over the past - so it never holds a company that later failed or shrank (survivorship and look-ahead bias). Expect live results to be weaker.
>
> Everything else is out-of-sample: signals use only past data, models are refit walk-forward, trades fill at the next day's open, and spread, market impact and borrow fees are charged.
>
> The **deflated Sharpe** is the probability the true Sharpe is above zero after correcting for having tried every model on this page. Below ~95% the edge is not statistically convincing.
>

![Growth of $1](charts/equity.png)

![Drawdown](charts/drawdown.png)

![Rolling Sharpe](charts/rolling_sharpe.png)

![Annual returns](charts/annual.png)

![Exposure](charts/exposure.png)

![HMM regimes](charts/regimes.png)

![Model comparison](charts/models.png)

## Models (same portfolio rules)

| model        |   sharpe |   ann_return |   ann_vol |   max_drawdown |   ann_turnover |   ann_cost_drag |   mean_ic |
|:-------------|---------:|-------------:|----------:|---------------:|---------------:|----------------:|----------:|
| gbm          |    0.428 |        0.029 |     0.068 |         -0.294 |         69.105 |           0.012 |     0.007 |
| ensemble     |    0.304 |        0.11  |     0.361 |         -0.25  |         78.721 |           0.015 |     0.008 |
| ridge        |    0.268 |        0.071 |     0.265 |         -0.328 |         62.261 |           0.011 |     0.005 |
| kernel_ridge |    0.265 |        0.061 |     0.232 |         -0.371 |         70.425 |           0.013 |     0.006 |
| regime_ridge |    0.249 |        0.089 |     0.359 |         -0.244 |         64.851 |           0.012 |     0.006 |
| elastic_net  |    0.243 |        0.021 |     0.086 |         -0.325 |         56.491 |           0.01  |     0.007 |
| ic_weighted  |    0.214 |        0.014 |     0.067 |         -0.301 |         79.889 |           0.014 |     0.009 |

## Portfolio-construction diagnostics (same ensemble forecast)

| variant                        |   sharpe |   sharpe_1st_half |   sharpe_2nd_half |   ann_return |   ann_vol |   pre_cost_sharpe |   avg_gross |   ann_turnover |   cost_drag |
|:-------------------------------|---------:|------------------:|------------------:|-------------:|----------:|------------------:|------------:|---------------:|------------:|
| current config                 |    0.304 |             0.439 |            -0.021 |        0.11  |     0.361 |             0.352 |       1.073 |         78.721 |       0.017 |
| frictionless                   |    0.359 |             0.498 |             0.098 |        0.142 |     0.397 |             0.359 |       1.368 |        111.884 |       0     |
| auction_costs (no spread)      |    0.304 |             0.439 |            -0.021 |        0.11  |     0.361 |             0.352 |       1.073 |         78.721 |       0.017 |
| quoted_spread_costs            |    0.189 |             0.338 |            -0.43  |        0.046 |     0.244 |             0.355 |       0.689 |         48.484 |       0.041 |
| rank_weights                   |    0.384 |             0.598 |            -0.078 |        0.067 |     0.176 |             0.474 |       0.973 |         71.522 |       0.016 |
| dollar_neutral_only            |    0.28  |             0.36  |             0.179 |        0.085 |     0.302 |             0.318 |       0.909 |         52.468 |       0.011 |
| halflife=0 cost_aversion=0.0   |    0.315 |             0.488 |            -0.24  |        0.133 |     0.424 |             0.483 |       1.286 |        326.02  |       0.071 |
| halflife=0 cost_aversion=0.25  |    0.331 |             0.519 |            -0.262 |        0.125 |     0.379 |             0.502 |       1.233 |        298.937 |       0.065 |
| halflife=0 cost_aversion=0.5   |    0.331 |             0.52  |            -0.274 |        0.125 |     0.379 |             0.49  |       1.175 |        276.33  |       0.06  |
| halflife=0 cost_aversion=1.0   |    0.335 |             0.528 |            -0.27  |        0.114 |     0.34  |             0.486 |       1.059 |        239.518 |       0.052 |
| halflife=3 cost_aversion=0.0   |    0.301 |             0.432 |            -0.011 |        0.123 |     0.408 |             0.355 |       1.207 |         99.41  |       0.022 |
| halflife=3 cost_aversion=0.25  |    0.299 |             0.429 |            -0.018 |        0.122 |     0.409 |             0.349 |       1.182 |         92.982 |       0.021 |
| halflife=3 cost_aversion=0.5   |    0.298 |             0.426 |             0     |        0.122 |     0.41  |             0.344 |       1.123 |         85.334 |       0.019 |
| halflife=3 cost_aversion=1.0   |    0.304 |             0.439 |            -0.021 |        0.11  |     0.361 |             0.352 |       1.073 |         78.721 |       0.017 |
| halflife=7 cost_aversion=0.0   |    0.251 |             0.368 |            -0.081 |        0.094 |     0.375 |             0.283 |       0.991 |         54.374 |       0.012 |
| halflife=7 cost_aversion=0.25  |    0.249 |             0.365 |            -0.08  |        0.094 |     0.377 |             0.28  |       0.98  |         51.977 |       0.012 |
| halflife=7 cost_aversion=0.5   |    0.255 |             0.361 |             0.021 |        0.097 |     0.378 |             0.286 |       0.983 |         50.973 |       0.011 |
| halflife=7 cost_aversion=1.0   |    0.25  |             0.351 |             0.04  |        0.095 |     0.379 |             0.278 |       0.945 |         47.714 |       0.011 |
| halflife=15 cost_aversion=0.0  |    0.257 |             0.369 |            -0.023 |        0.094 |     0.364 |             0.283 |       0.992 |         39.016 |       0.009 |
| halflife=15 cost_aversion=0.25 |    0.257 |             0.367 |            -0.002 |        0.094 |     0.367 |             0.282 |       1.003 |         38.788 |       0.009 |
| halflife=15 cost_aversion=0.5  |    0.257 |             0.367 |            -0.002 |        0.094 |     0.366 |             0.282 |       0.98  |         36.982 |       0.009 |
| halflife=15 cost_aversion=1.0  |    0.263 |             0.38  |            -0.026 |        0.097 |     0.367 |             0.289 |       1.027 |         37.538 |       0.009 |
| halflife=30 cost_aversion=0.0  |    0.278 |             0.45  |             0.093 |        0.017 |     0.062 |             0.385 |       0.825 |         27.151 |       0.007 |
| halflife=30 cost_aversion=0.25 |    0.244 |             0.439 |             0.098 |        0.018 |     0.074 |             0.343 |       0.933 |         29.827 |       0.007 |
| halflife=30 cost_aversion=0.5  |    0.239 |             0.426 |             0.1   |        0.018 |     0.074 |             0.337 |       0.926 |         29.176 |       0.007 |
| halflife=30 cost_aversion=1.0  |    0.241 |             0.421 |             0.108 |        0.018 |     0.074 |             0.337 |       0.914 |         28.347 |       0.007 |

## Signals (descriptive, full-sample rank IC)

| signal              | family         |   mean_ic |   ic_ir |   t_stat |   hit_rate |   ic_regime_0 |   ic_regime_1 |   ic_regime_2 |
|:--------------------|:---------------|----------:|--------:|---------:|-----------:|--------------:|--------------:|--------------:|
| resid_rev_1d        | mean_reversion |    0.0097 |  2.6792 |  13.5575 |     0.5644 |        0.0081 |        0.0081 |        0.0121 |
| peer_gap            | structure      |    0.0129 |  2.2675 |  11.5011 |     0.5519 |        0.0081 |        0.0154 |        0.0172 |
| resid_rev_5d        | mean_reversion |    0.0097 |  2.2131 |  11.1993 |     0.557  |        0.0049 |        0.0112 |        0.0144 |
| low_volume_rev      | mean_reversion |    0.0181 |  1.9413 |   9.8557 |     0.5396 |        0.0118 |        0.0215 |        0.0236 |
| rev_5d              | mean_reversion |    0.0181 |  1.9379 |   9.8385 |     0.5378 |        0.0119 |        0.0212 |        0.0238 |
| ou_sscore           | mean_reversion |    0.0072 |  1.8979 |   9.5897 |     0.5431 |        0.0036 |        0.0054 |        0.0118 |
| bollinger_z         | mean_reversion |    0.0138 |  1.6375 |   8.3132 |     0.5332 |        0.007  |        0.0203 |        0.0187 |
| rev_1d              | mean_reversion |    0.0144 |  1.5903 |   8.0734 |     0.5386 |        0.0118 |        0.0098 |        0.0192 |
| close_location      | microstructure |    0.0103 |  1.5758 |   7.9999 |     0.5336 |        0.0052 |        0.0116 |        0.0154 |
| intraday_rev        | mean_reversion |    0.0118 |  1.4168 |   7.1927 |     0.533  |        0.0106 |        0.0084 |        0.0146 |
| rsi_14              | mean_reversion |    0.0128 |  1.4088 |   7.1522 |     0.5238 |        0.0062 |        0.0164 |        0.0188 |
| vol_price_corr      | volume         |    0.007  |  1.3287 |   6.7457 |     0.5327 |        0.0054 |        0.0136 |        0.006  |
| rev_21d             | mean_reversion |    0.0127 |  1.306  |   6.6302 |     0.5292 |        0.0067 |        0.0163 |        0.018  |
| resid_mom           | momentum       |    0.0093 |  1.2168 |   6.0897 |     0.5513 |        0.0125 |        0.0092 |        0.0059 |
| intraday_rev_21     | momentum       |    0.0107 |  1.1651 |   5.9149 |     0.5295 |        0.004  |        0.0202 |        0.0144 |
| same_month          | seasonality    |    0.0073 |  1.0929 |   5.4339 |     0.5462 |        0.007  |        0.0122 |        0.0057 |
| mom_12_1            | momentum       |    0.0106 |  0.8638 |   4.3811 |     0.538  |        0.0153 |        0.0152 |        0.0035 |
| overnight_rev       | mean_reversion |    0.0065 |  0.723  |   3.6707 |     0.5204 |        0.0026 |        0.0045 |        0.0116 |
| weekday_seasonality | seasonality    |    0.0027 |  0.656  |   3.2937 |     0.5243 |        0.0035 |        0.0023 |        0.002  |
| size_proxy          | volume         |    0.005  |  0.6381 |   3.2397 |     0.5207 |        0.006  |       -0.0011 |        0.0063 |
| neg_skew            | volatility     |    0.0028 |  0.5425 |   2.7543 |     0.5004 |        0.0048 |        0.0035 |        0.0004 |
| amihud              | volume         |    0.0049 |  0.5276 |   2.6787 |     0.5149 |        0.0024 |        0.0014 |        0.0091 |
| autocorr_signal     | structure      |    0.0019 |  0.4264 |   2.1647 |     0.503  |       -0.0006 |       -0.0001 |        0.0054 |
| turn_of_month       | seasonality    |    0.006  |  0.3382 |   1.7169 |     0.5073 |        0.0138 |       -0.0186 |        0.0073 |
| mom_6_1             | momentum       |    0.0036 |  0.3208 |   1.6288 |     0.5323 |        0.0038 |        0.0073 |        0.0019 |
| turnover_trend      | volume         |    0.0021 |  0.3073 |   1.56   |     0.4902 |       -0.0025 |        0.0005 |        0.0079 |
| gk_ratio            | microstructure |    0.0016 |  0.2593 |   1.3165 |     0.495  |       -0.0049 |        0.0105 |        0.0052 |
| range_vol_ratio     | microstructure |    0.0012 |  0.2194 |   1.114  |     0.521  |        0.0003 |        0.0037 |        0.0012 |
| max_effect          | volatility     |    0.0019 |  0.1585 |   0.8045 |     0.5018 |        0.0091 |       -0.0029 |       -0.0042 |
| market_corr         | structure      |    0.0016 |  0.1403 |   0.7125 |     0.5036 |        0.0154 |       -0.0038 |       -0.0117 |
| bab                 | volatility     |   -0      | -0.0018 |  -0.0093 |     0.4939 |        0.0163 |       -0.0153 |       -0.0121 |
| idio_vol            | volatility     |   -0.0009 | -0.0777 |  -0.3928 |     0.4926 |        0.004  |       -0.0062 |       -0.0042 |
| low_vol             | volatility     |   -0.0012 | -0.0781 |  -0.3966 |     0.4921 |        0.0102 |       -0.0106 |       -0.0101 |
| cs_spread           | microstructure |   -0.0019 | -0.1693 |  -0.8594 |     0.5019 |       -0.0068 |       -0.0011 |        0.0034 |
| high_52w            | momentum       |   -0.0047 | -0.3555 |  -1.8046 |     0.5044 |        0.0063 |       -0.0086 |       -0.0155 |
| vol_of_vol          | volatility     |   -0.0023 | -0.4363 |  -2.2152 |     0.4893 |       -0.003  |       -0.0035 |       -0.001  |
| abn_volume          | volume         |   -0.002  | -0.4826 |  -2.4501 |     0.4931 |       -0.0007 |       -0.0027 |       -0.0032 |
| trend_quality       | momentum       |   -0.0069 | -0.6783 |  -3.4436 |     0.497  |       -0.0021 |       -0.0053 |       -0.013  |
| overnight_mom       | momentum       |   -0.0048 | -0.6922 |  -3.5142 |     0.4958 |       -0.0049 |        0.0063 |       -0.0093 |
| peer_lead           | structure      |   -0.0082 | -0.8012 |  -4.0639 |     0.4811 |       -0.0059 |       -0.0021 |       -0.0133 |
| cluster_mom         | momentum       |   -0.0097 | -0.9202 |  -4.6675 |     0.4833 |       -0.0052 |       -0.0168 |       -0.0119 |
| kalman_trend        | structure      |   -0.0092 | -0.9707 |  -4.9279 |     0.4865 |       -0.0052 |       -0.0095 |       -0.0135 |
| mom_accel           | momentum       |   -0.0093 | -1.023  |  -5.1935 |     0.4887 |       -0.004  |       -0.0132 |       -0.0137 |
| downside_beta       | volatility     |   -0.0233 | -1.3639 |  -2.772  |     0.4745 |       -0.0341 |       -0.0543 |        0.006  |

![signals](charts/signals.png)

![weights](charts/weights.png)

Full interactive-free report with monthly table and config: `report.html` (download and open).