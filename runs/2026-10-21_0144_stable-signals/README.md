# Backtest results

| | |
|---|---|
| Period | 2003-12-19 to 2026-10-19 (22.8 years) |
| Stocks / signals | 1000 / 44 |
| Traded model | ensemble |
| Sharpe ratio | 0.35 |
| Annual return | 2.6% |
| Annual volatility | 7.3% |
| Max drawdown | -29.1% |
| Deflated Sharpe probability | 83.1% |
| Beta / correlation to market | 0.02 / 0.05 |
| Avg gross exposure | 0.94x |
| Annual turnover | 77x |
| Cost + borrow drag / yr | 1.6% |

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
| gbm          |    0.461 |        0.031 |     0.066 |         -0.302 |         75.765 |           0.013 |     0.005 |
| kernel_ridge |    0.405 |        0.028 |     0.069 |         -0.26  |         76.796 |           0.013 |     0.006 |
| ensemble     |    0.354 |        0.026 |     0.073 |         -0.291 |         77.018 |           0.013 |     0.007 |
| elastic_net  |    0.317 |        0.023 |     0.072 |         -0.349 |         70.514 |           0.012 |     0.004 |
| ridge        |    0.276 |        0.02  |     0.071 |         -0.304 |         74.192 |           0.013 |     0.007 |
| regime_ridge |    0.208 |        0.013 |     0.065 |         -0.227 |         69.431 |           0.012 |     0.007 |
| ic_weighted  |    0.144 |        0.01  |     0.072 |         -0.331 |         91.201 |           0.016 |     0.008 |

## Portfolio-construction diagnostics (same ensemble forecast)

| variant                        |   sharpe |   sharpe_1st_half |   sharpe_2nd_half |   ann_return |   ann_vol |   pre_cost_sharpe |   avg_gross |   ann_turnover |   cost_drag |
|:-------------------------------|---------:|------------------:|------------------:|-------------:|----------:|------------------:|------------:|---------------:|------------:|
| current config                 |    0.354 |             0.783 |            -0.199 |        0.026 |     0.073 |             0.568 |       0.944 |         77.018 |       0.016 |
| frictionless                   |    0.537 |             1.091 |            -0.089 |        0.045 |     0.085 |             0.537 |       1.151 |        102.403 |       0     |
| auction_costs (no spread)      |    0.354 |             0.783 |            -0.199 |        0.026 |     0.073 |             0.568 |       0.944 |         77.018 |       0.016 |
| quoted_spread_costs            |   -0.102 |             0.16  |            -0.434 |       -0.005 |     0.053 |             0.589 |       0.581 |         44.608 |       0.037 |
| rank_weights                   |    0.336 |             0.696 |            -0.184 |        0.027 |     0.079 |             0.538 |       0.939 |         76.038 |       0.016 |
| dollar_neutral_only            |    0.143 |             0.378 |            -0.124 |        0.014 |     0.101 |             0.256 |       0.836 |         55.267 |       0.011 |
| regime_ic                      |    0.291 |             0.69  |            -0.116 |        0.026 |     0.09  |             0.516 |       1.235 |         99.419 |       0.02  |
| regime_ic + edge_scaling       |    0.356 |             0.745 |            -0.097 |        0.022 |     0.062 |             0.59  |       0.868 |         73.482 |       0.015 |
| edge_scaling                   |    0.403 |             0.919 |            -0.171 |        0.024 |     0.059 |             0.619 |       0.759 |         63.39  |       0.013 |
| halflife=0 cost_aversion=0.0   |    0.415 |             0.953 |            -0.184 |        0.039 |     0.094 |             1.111 |       1.234 |        336.204 |       0.065 |
| halflife=0 cost_aversion=0.25  |    0.461 |             1.05  |            -0.192 |        0.043 |     0.093 |             1.116 |       1.19  |        312.758 |       0.061 |
| halflife=0 cost_aversion=0.5   |    0.485 |             1.077 |            -0.168 |        0.044 |     0.092 |             1.11  |       1.14  |        291.321 |       0.057 |
| halflife=0 cost_aversion=1.0   |    0.547 |             1.139 |            -0.1   |        0.048 |     0.088 |             1.134 |       1.065 |        260.944 |       0.052 |
| halflife=3 cost_aversion=0.0   |    0.366 |             0.775 |            -0.195 |        0.028 |     0.077 |             0.611 |       1.03  |         93.262 |       0.019 |
| halflife=3 cost_aversion=0.25  |    0.371 |             0.792 |            -0.206 |        0.028 |     0.076 |             0.606 |       1.014 |         87.958 |       0.018 |
| halflife=3 cost_aversion=0.5   |    0.387 |             0.804 |            -0.181 |        0.029 |     0.075 |             0.616 |       0.994 |         84.079 |       0.017 |
| halflife=3 cost_aversion=1.0   |    0.354 |             0.783 |            -0.199 |        0.026 |     0.073 |             0.568 |       0.944 |         77.018 |       0.016 |
| halflife=7 cost_aversion=0.0   |    0.138 |             0.472 |            -0.207 |        0.01  |     0.07  |             0.311 |       0.975 |         57.777 |       0.012 |
| halflife=7 cost_aversion=0.25  |    0.152 |             0.48  |            -0.194 |        0.01  |     0.069 |             0.323 |       0.961 |         55.583 |       0.012 |
| halflife=7 cost_aversion=0.5   |    0.165 |             0.447 |            -0.157 |        0.011 |     0.065 |             0.333 |       0.906 |         52.045 |       0.011 |
| halflife=7 cost_aversion=1.0   |    0.134 |             0.371 |            -0.15  |        0.009 |     0.066 |             0.294 |       0.882 |         49.549 |       0.011 |
| halflife=15 cost_aversion=0.0  |    0.214 |             0.411 |             0.071 |        0.021 |     0.097 |             0.343 |       1.306 |         54.669 |       0.013 |
| halflife=15 cost_aversion=0.25 |    0.219 |             0.406 |             0.082 |        0.021 |     0.096 |             0.346 |       1.297 |         53.11  |       0.012 |
| halflife=15 cost_aversion=0.5  |    0.202 |             0.397 |             0.061 |        0.019 |     0.096 |             0.326 |       1.279 |         51.623 |       0.012 |
| halflife=15 cost_aversion=1.0  |    0.205 |             0.392 |             0.069 |        0.019 |     0.095 |             0.327 |       1.246 |         49.571 |       0.011 |
| halflife=30 cost_aversion=0.0  |    0.109 |             0.185 |             0.039 |        0.007 |     0.06  |             0.218 |       0.81  |         27.389 |       0.007 |
| halflife=30 cost_aversion=0.25 |    0.113 |             0.199 |             0.037 |        0.007 |     0.06  |             0.221 |       0.807 |         26.817 |       0.006 |
| halflife=30 cost_aversion=0.5  |    0.113 |             0.197 |             0.039 |        0.007 |     0.06  |             0.22  |       0.801 |         26.381 |       0.006 |
| halflife=30 cost_aversion=1.0  |    0.094 |             0.199 |             0.005 |        0.006 |     0.061 |             0.197 |       0.801 |         25.944 |       0.006 |

## Signals (descriptive, full-sample rank IC)

| signal              | family         |   mean_ic |   ic_ir |   t_stat |   hit_rate |   ic_regime_0 |   ic_regime_1 |   ic_regime_2 |
|:--------------------|:---------------|----------:|--------:|---------:|-----------:|--------------:|--------------:|--------------:|
| resid_rev_1d        | mean_reversion |    0.0097 |  2.685  |  13.586  |     0.5663 |        0.0083 |        0.0117 |        0.0109 |
| peer_gap            | structure      |    0.0132 |  2.3062 |  11.6966 |     0.5565 |        0.0091 |        0.0141 |        0.0181 |
| resid_rev_5d        | mean_reversion |    0.0097 |  2.218  |  11.2228 |     0.5569 |        0.0056 |        0.0111 |        0.0144 |
| low_volume_rev      | mean_reversion |    0.0181 |  1.9504 |   9.9012 |     0.5397 |        0.0123 |        0.0156 |        0.0262 |
| rev_5d              | mean_reversion |    0.0182 |  1.9489 |   9.8932 |     0.538  |        0.0123 |        0.0157 |        0.0263 |
| ou_sscore           | mean_reversion |    0.0072 |  1.903  |   9.6151 |     0.5417 |        0.0039 |        0.0036 |        0.0122 |
| bollinger_z         | mean_reversion |    0.0139 |  1.6464 |   8.358  |     0.533  |        0.0073 |        0.0063 |        0.0242 |
| rev_1d              | mean_reversion |    0.0145 |  1.5986 |   8.115  |     0.5382 |        0.012  |        0.013  |        0.0182 |
| close_location      | microstructure |    0.0103 |  1.5768 |   8.0045 |     0.5339 |        0.0055 |        0.0136 |        0.0155 |
| intraday_rev        | mean_reversion |    0.0119 |  1.4233 |   7.2254 |     0.5333 |        0.0105 |        0.0108 |        0.014  |
| rsi_14              | mean_reversion |    0.0129 |  1.4157 |   7.1868 |     0.5239 |        0.0068 |        0.0033 |        0.0232 |
| vol_price_corr      | volume         |    0.007  |  1.3338 |   6.7711 |     0.5326 |        0.0053 |        0.0105 |        0.0081 |
| rev_21d             | mean_reversion |    0.0128 |  1.3104 |   6.6521 |     0.5288 |        0.0078 |        0.0028 |        0.0218 |
| resid_mom           | momentum       |    0.0094 |  1.2287 |   6.1487 |     0.5514 |        0.0117 |        0.0181 |        0.0042 |
| intraday_rev_21     | momentum       |    0.0107 |  1.1655 |   5.9168 |     0.5299 |        0.0057 |        0.0056 |        0.0185 |
| same_month          | seasonality    |    0.0073 |  1.0942 |   5.4402 |     0.5458 |        0.0066 |        0.0217 |        0.0043 |
| mom_12_1            | momentum       |    0.0106 |  0.8669 |   4.3965 |     0.5374 |        0.0141 |        0.0237 |        0.0027 |
| overnight_rev       | mean_reversion |    0.0065 |  0.7311 |   3.7113 |     0.5208 |        0.0033 |        0.006  |        0.0108 |
| weekday_seasonality | seasonality    |    0.0028 |  0.666  |   3.3435 |     0.5249 |        0.0033 |        0.0057 |        0.0013 |
| size_proxy          | volume         |    0.005  |  0.638  |   3.239  |     0.5211 |        0.0051 |        0.0006 |        0.006  |
| neg_skew            | volatility     |    0.0028 |  0.537  |   2.7258 |     0.5003 |        0.0043 |        0.0022 |        0.0011 |
| amihud              | volume         |    0.005  |  0.5322 |   2.7018 |     0.5149 |        0.0021 |        0.0001 |        0.0098 |
| autocorr_signal     | structure      |    0.0019 |  0.4319 |   2.1924 |     0.5046 |       -0      |       -0.002  |        0.0055 |
| turn_of_month       | seasonality    |    0.0059 |  0.3321 |   1.6856 |     0.5065 |        0.01   |       -0.0023 |        0.003  |
| mom_6_1             | momentum       |    0.0036 |  0.3225 |   1.6374 |     0.5325 |        0.0015 |        0.0217 |        0.0014 |
| turnover_trend      | volume         |    0.0022 |  0.3198 |   1.6234 |     0.4909 |       -0.001  |       -0.0106 |        0.0098 |
| gk_ratio            | microstructure |    0.0016 |  0.2699 |   1.37   |     0.4955 |       -0.0026 |        0.0056 |        0.006  |
| range_vol_ratio     | microstructure |    0.0013 |  0.2253 |   1.1437 |     0.5205 |        0.0023 |        0.0026 |       -0.0004 |
| max_effect          | volatility     |    0.0019 |  0.1546 |   0.7847 |     0.5017 |        0.0073 |        0.0049 |       -0.0059 |
| market_corr         | structure      |    0.0016 |  0.1401 |   0.7111 |     0.5037 |        0.0123 |        0.0034 |       -0.0124 |
| bab                 | volatility     |   -0.0002 | -0.0089 |  -0.0453 |     0.4937 |        0.0137 |        0.0019 |       -0.0182 |
| low_vol             | volatility     |   -0.0014 | -0.0881 |  -0.4475 |     0.4915 |        0.0087 |       -0.0039 |       -0.0134 |
| idio_vol            | volatility     |   -0.001  | -0.0885 |  -0.4476 |     0.4922 |        0.0034 |        0.004  |       -0.008  |
| cs_spread           | microstructure |   -0.0018 | -0.1642 |  -0.8337 |     0.502  |       -0.0069 |       -0.0058 |        0.0058 |
| high_52w            | momentum       |   -0.0048 | -0.3593 |  -1.8242 |     0.5048 |        0.0042 |        0.0121 |       -0.0207 |
| vol_of_vol          | volatility     |   -0.0023 | -0.4433 |  -2.2503 |     0.4894 |       -0.0029 |        0.0024 |       -0.0028 |
| abn_volume          | volume         |   -0.0021 | -0.5004 |  -2.54   |     0.4932 |       -0.0024 |        0.0001 |       -0.0023 |
| trend_quality       | momentum       |   -0.007  | -0.6857 |  -3.4809 |     0.4969 |       -0.0039 |        0.008  |       -0.015  |
| overnight_mom       | momentum       |   -0.0049 | -0.6971 |  -3.5387 |     0.4952 |       -0.0031 |        0.0051 |       -0.0098 |
| cluster_mom         | momentum       |   -0.0082 | -0.777  |  -3.9408 |     0.4858 |       -0.0048 |       -0.0006 |       -0.0146 |
| peer_lead           | structure      |   -0.0084 | -0.8212 |  -4.1648 |     0.486  |       -0.0062 |       -0.0047 |       -0.0123 |
| kalman_trend        | structure      |   -0.0092 | -0.9709 |  -4.9285 |     0.4857 |       -0.0061 |        0.0033 |       -0.0165 |
| mom_accel           | momentum       |   -0.0094 | -1.034  |  -5.2491 |     0.4861 |       -0.0054 |       -0.0039 |       -0.016  |
| downside_beta       | volatility     |   -0.0205 | -1.1989 |  -2.467  |     0.478  |       -0.0227 |       -0.0368 |       -0.0152 |

![signals](charts/signals.png)

![weights](charts/weights.png)

Full interactive-free report with monthly table and config: `report.html` (download and open).