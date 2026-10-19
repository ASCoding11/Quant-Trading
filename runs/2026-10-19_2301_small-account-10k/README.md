# Backtest results

| | |
|---|---|
| Period | 2003-12-19 to 2026-10-19 (22.8 years) |
| Stocks / signals | 1000 / 44 |
| Traded model | ensemble |
| Sharpe ratio | 0.41 |
| Annual return | 3.3% |
| Annual volatility | 8.0% |
| Max drawdown | -24.1% |
| Deflated Sharpe probability | 91.4% |
| Beta / correlation to market | 0.02 / 0.05 |
| Avg gross exposure | 1.06x |
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
| ensemble     |    0.414 |        0.033 |     0.08  |         -0.241 |         76.958 |           0.013 |     0.01  |
| regime_ridge |    0.213 |        0.015 |     0.072 |         -0.211 |         65.453 |           0.011 |     0.007 |
| kernel_ridge |    0.189 |        0.014 |     0.073 |         -0.322 |         66.24  |           0.011 |     0.008 |
| gbm          |    0.18  |        0.013 |     0.07  |         -0.289 |         70.541 |           0.012 |     0.01  |
| elastic_net  |    0.173 |        0.011 |     0.066 |         -0.387 |         55.808 |           0.01  |     0.008 |
| ic_weighted  |    0.163 |        0.012 |     0.071 |         -0.354 |         85.254 |           0.015 |     0.009 |
| ridge        |    0.15  |        0.011 |     0.07  |         -0.415 |         62.117 |           0.011 |     0.007 |

## Portfolio-construction diagnostics (same ensemble forecast)

| variant                        |   sharpe |   sharpe_1st_half |   sharpe_2nd_half |   ann_return |   ann_vol |   pre_cost_sharpe |   avg_gross |   ann_turnover |   cost_drag |
|:-------------------------------|---------:|------------------:|------------------:|-------------:|----------:|------------------:|------------:|---------------:|------------:|
| current config                 |    0.414 |             0.787 |             0.01  |        0.033 |     0.08  |             0.616 |       1.058 |         76.958 |       0.016 |
| frictionless                   |    0.534 |             0.982 |             0.064 |        0.046 |     0.085 |             0.534 |       1.176 |         94.285 |       0     |
| auction_costs (no spread)      |    0.414 |             0.787 |             0.01  |        0.033 |     0.08  |             0.616 |       1.058 |         76.958 |       0.016 |
| quoted_spread_costs            |   -0.088 |             0.115 |            -0.376 |       -0.005 |     0.061 |             0.57  |       0.668 |         46.215 |       0.04  |
| rank_weights                   |    0.36  |             0.807 |            -0.096 |        0.03  |     0.083 |             0.543 |       0.991 |         71.122 |       0.015 |
| dollar_neutral_only            |    0.184 |             0.145 |             0.224 |        0.021 |     0.116 |             0.273 |       0.872 |         49.366 |       0.01  |
| halflife=0 cost_aversion=0.0   |    0.476 |             1.165 |            -0.298 |        0.045 |     0.094 |             1.12  |       1.243 |        308.564 |       0.06  |
| halflife=0 cost_aversion=0.25  |    0.484 |             1.168 |            -0.232 |        0.046 |     0.095 |             1.096 |       1.241 |        294.62  |       0.058 |
| halflife=0 cost_aversion=0.5   |    0.488 |             1.166 |            -0.228 |        0.045 |     0.093 |             1.07  |       1.183 |        272.722 |       0.054 |
| halflife=0 cost_aversion=1.0   |    0.509 |             1.121 |            -0.097 |        0.046 |     0.09  |             1.046 |       1.104 |        244.3   |       0.048 |
| halflife=3 cost_aversion=0.0   |    0.385 |             0.803 |            -0.062 |        0.032 |     0.082 |             0.61  |       1.126 |         90.671 |       0.019 |
| halflife=3 cost_aversion=0.25  |    0.389 |             0.794 |            -0.044 |        0.032 |     0.082 |             0.606 |       1.114 |         86.02  |       0.018 |
| halflife=3 cost_aversion=0.5   |    0.39  |             0.794 |            -0.039 |        0.032 |     0.081 |             0.601 |       1.1   |         82.935 |       0.017 |
| halflife=3 cost_aversion=1.0   |    0.414 |             0.787 |             0.01  |        0.033 |     0.08  |             0.616 |       1.058 |         76.958 |       0.016 |
| halflife=7 cost_aversion=0.0   |    0.234 |             0.47  |            -0.048 |        0.018 |     0.075 |             0.393 |       1.023 |         55.652 |       0.012 |
| halflife=7 cost_aversion=0.25  |    0.254 |             0.481 |            -0.027 |        0.019 |     0.074 |             0.409 |       1.014 |         53.21  |       0.012 |
| halflife=7 cost_aversion=0.5   |    0.27  |             0.492 |            -0.002 |        0.02  |     0.075 |             0.422 |       1.019 |         52.477 |       0.011 |
| halflife=7 cost_aversion=1.0   |    0.236 |             0.425 |            -0.004 |        0.017 |     0.073 |             0.383 |       0.977 |         49.089 |       0.011 |
| halflife=15 cost_aversion=0.0  |    0.221 |             0.508 |            -0.043 |        0.019 |     0.087 |             0.347 |       1.181 |         47.15  |       0.011 |
| halflife=15 cost_aversion=0.25 |    0.22  |             0.495 |            -0.032 |        0.019 |     0.087 |             0.344 |       1.17  |         45.479 |       0.011 |
| halflife=15 cost_aversion=0.5  |    0.213 |             0.495 |            -0.046 |        0.018 |     0.086 |             0.335 |       1.162 |         44.437 |       0.01  |
| halflife=15 cost_aversion=1.0  |    0.224 |             0.49  |            -0.035 |        0.019 |     0.083 |             0.342 |       1.11  |         41.556 |       0.01  |
| halflife=30 cost_aversion=0.0  |    0.178 |             0.336 |             0.007 |        0.011 |     0.065 |             0.291 |       0.916 |         29.884 |       0.007 |
| halflife=30 cost_aversion=0.25 |    0.174 |             0.33  |             0.008 |        0.011 |     0.064 |             0.284 |       0.896 |         28.36  |       0.007 |
| halflife=30 cost_aversion=0.5  |    0.165 |             0.327 |            -0.008 |        0.011 |     0.064 |             0.273 |       0.891 |         27.638 |       0.007 |
| halflife=30 cost_aversion=1.0  |    0.191 |             0.418 |            -0.023 |        0.013 |     0.068 |             0.297 |       0.955 |         28.899 |       0.007 |

## Signals (descriptive, full-sample rank IC)

| signal              | family         |   mean_ic |   ic_ir |   t_stat |   hit_rate |   ic_regime_0 |   ic_regime_1 |   ic_regime_2 |
|:--------------------|:---------------|----------:|--------:|---------:|-----------:|--------------:|--------------:|--------------:|
| resid_rev_1d        | mean_reversion |    0.0098 |  2.6297 |  13.3064 |     0.5665 |        0.0084 |        0.0082 |        0.0119 |
| peer_gap            | structure      |    0.0133 |  2.2833 |  11.58   |     0.5491 |        0.0093 |        0.0138 |        0.0176 |
| resid_rev_5d        | mean_reversion |    0.0097 |  2.1656 |  10.9579 |     0.5547 |        0.0053 |        0.0108 |        0.0143 |
| rev_5d              | mean_reversion |    0.0181 |  1.9117 |   9.7046 |     0.5345 |        0.0123 |        0.0195 |        0.0241 |
| low_volume_rev      | mean_reversion |    0.018  |  1.9085 |   9.6882 |     0.5353 |        0.0123 |        0.0195 |        0.0238 |
| ou_sscore           | mean_reversion |    0.0073 |  1.8794 |   9.4956 |     0.5388 |        0.0033 |        0.0055 |        0.0124 |
| bollinger_z         | mean_reversion |    0.0142 |  1.6575 |   8.4143 |     0.5283 |        0.0078 |        0.0185 |        0.0195 |
| rev_1d              | mean_reversion |    0.0144 |  1.563  |   7.9342 |     0.536  |        0.0119 |        0.0097 |        0.019  |
| close_location      | microstructure |    0.0099 |  1.4906 |   7.5671 |     0.5277 |        0.005  |        0.01   |        0.0153 |
| rsi_14              | mean_reversion |    0.013  |  1.4101 |   7.158  |     0.5209 |        0.0067 |        0.015  |        0.0194 |
| intraday_rev        | mean_reversion |    0.0116 |  1.3749 |   6.9796 |     0.5342 |        0.0105 |        0.0081 |        0.0143 |
| vol_price_corr      | volume         |    0.0071 |  1.324  |   6.721  |     0.5306 |        0.0053 |        0.0133 |        0.0067 |
| rev_21d             | mean_reversion |    0.0126 |  1.2783 |   6.489  |     0.5297 |        0.0067 |        0.0144 |        0.0186 |
| resid_mom           | momentum       |    0.0091 |  1.1835 |   5.9229 |     0.5519 |        0.0118 |        0.0087 |        0.0065 |
| intraday_rev_21     | momentum       |    0.0101 |  1.0844 |   5.5049 |     0.5202 |        0.0037 |        0.0179 |        0.0142 |
| same_month          | seasonality    |    0.007  |  1.0292 |   5.117  |     0.5417 |        0.0066 |        0.0132 |        0.005  |
| mom_12_1            | momentum       |    0.0112 |  0.8941 |   4.5342 |     0.5417 |        0.0159 |        0.0157 |        0.004  |
| overnight_rev       | mean_reversion |    0.0068 |  0.7533 |   3.8241 |     0.5202 |        0.0033 |        0.0048 |        0.0116 |
| size_proxy          | volume         |    0.0049 |  0.6435 |   3.2665 |     0.5179 |        0.0061 |        0.0003 |        0.0053 |
| neg_skew            | volatility     |    0.0034 |  0.6331 |   3.214  |     0.504  |        0.0051 |        0.005  |        0.0007 |
| weekday_seasonality | seasonality    |    0.0026 |  0.6199 |   3.1123 |     0.5253 |        0.0033 |        0.0019 |        0.0022 |
| amihud              | volume         |    0.0045 |  0.4955 |   2.5155 |     0.5168 |        0.0017 |        0.0032 |        0.0082 |
| autocorr_signal     | structure      |    0.0019 |  0.4081 |   2.0717 |     0.5034 |       -0.0007 |       -0      |        0.0055 |
| turn_of_month       | seasonality    |    0.0071 |  0.3918 |   1.9889 |     0.5099 |        0.0146 |       -0.0186 |        0.0091 |
| turnover_trend      | volume         |    0.0025 |  0.3473 |   1.7631 |     0.4905 |       -0.0024 |        0.0008 |        0.0086 |
| mom_6_1             | momentum       |    0.0038 |  0.3312 |   1.6813 |     0.5311 |        0.0041 |        0.0069 |        0.0022 |
| gk_ratio            | microstructure |    0.0018 |  0.2834 |   1.4387 |     0.4977 |       -0.0048 |        0.0116 |        0.0051 |
| max_effect          | volatility     |    0.0034 |  0.2823 |   1.4329 |     0.5025 |        0.011  |       -0.0035 |       -0.0023 |
| range_vol_ratio     | microstructure |    0.0012 |  0.2146 |   1.0894 |     0.5222 |        0.0001 |        0.004  |        0.0014 |
| bab                 | volatility     |    0.0013 |  0.0713 |   0.362  |     0.4968 |        0.0183 |       -0.0154 |       -0.011  |
| idio_vol            | volatility     |    0.0008 |  0.0712 |   0.36   |     0.493  |        0.0064 |       -0.0059 |       -0.0026 |
| market_corr         | structure      |    0.0006 |  0.0549 |   0.2787 |     0.4965 |        0.0144 |       -0.0043 |       -0.0127 |
| low_vol             | volatility     |    0.0005 |  0.0293 |   0.149  |     0.4934 |        0.0127 |       -0.0111 |       -0.0086 |
| high_52w            | momentum       |   -0.0033 | -0.2457 |  -1.2475 |     0.5111 |        0.0084 |       -0.008  |       -0.0145 |
| cs_spread           | microstructure |   -0.0034 | -0.3033 |  -1.5398 |     0.4986 |       -0.0087 |       -0.0007 |        0.0015 |
| vol_of_vol          | volatility     |   -0.0018 | -0.3339 |  -1.6951 |     0.4923 |       -0.0029 |       -0.0024 |       -0.0002 |
| abn_volume          | volume         |   -0.0025 | -0.573  |  -2.909  |     0.4895 |       -0.0013 |       -0.0035 |       -0.0033 |
| trend_quality       | momentum       |   -0.0069 | -0.6629 |  -3.3653 |     0.4948 |       -0.0019 |       -0.0055 |       -0.0129 |
| overnight_mom       | momentum       |   -0.0053 | -0.7475 |  -3.7947 |     0.4946 |       -0.0051 |        0.0056 |       -0.0101 |
| peer_lead           | structure      |   -0.0081 | -0.7799 |  -3.9553 |     0.4816 |       -0.0052 |       -0.0043 |       -0.0128 |
| cluster_mom         | momentum       |   -0.0084 | -0.7867 |  -3.9898 |     0.4866 |       -0.0034 |       -0.0161 |       -0.0109 |
| kalman_trend        | structure      |   -0.009  | -0.9361 |  -4.752  |     0.4866 |       -0.0048 |       -0.0085 |       -0.0139 |
| mom_accel           | momentum       |   -0.0097 | -1.0566 |  -5.3639 |     0.4869 |       -0.0047 |       -0.0139 |       -0.0137 |
| downside_beta       | volatility     |   -0.0226 | -1.3121 |  -2.6974 |     0.4751 |       -0.0349 |       -0.0517 |        0.0067 |

![signals](charts/signals.png)

![weights](charts/weights.png)

Full interactive-free report with monthly table and config: `report.html` (download and open).