# Backtest results

| | |
|---|---|
| Period | 2003-12-19 to 2026-10-19 (22.8 years) |
| Stocks / signals | 1000 / 44 |
| Traded model | ensemble |
| Sharpe ratio | -0.14 |
| Annual return | -0.4% |
| Annual volatility | 2.9% |
| Max drawdown | -21.7% |
| Deflated Sharpe probability | 10.0% |
| Beta / correlation to market | 0.01 / 0.09 |
| Avg gross exposure | 1.03x |
| Annual turnover | 17x |
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
| gbm          |   -0.097 |       -0.002 |     0.024 |         -0.213 |         15.114 |           0.013 |     0.01  |
| ensemble     |   -0.139 |       -0.004 |     0.029 |         -0.217 |         16.725 |           0.014 |     0.01  |
| ic_weighted  |   -0.203 |       -0.005 |     0.025 |         -0.207 |         15.819 |           0.012 |     0.009 |
| regime_ridge |   -0.258 |       -0.006 |     0.023 |         -0.173 |         10.157 |           0.008 |     0.007 |
| kernel_ridge |   -0.279 |       -0.006 |     0.023 |         -0.236 |         11.491 |           0.01  |     0.008 |
| ridge        |   -0.305 |       -0.007 |     0.023 |         -0.237 |         11.422 |           0.01  |     0.007 |
| elastic_net  |   -0.35  |       -0.008 |     0.022 |         -0.284 |         10.721 |           0.009 |     0.008 |

## Portfolio-construction diagnostics (same ensemble forecast)

| variant                        |   sharpe |   sharpe_1st_half |   sharpe_2nd_half |   ann_return |   ann_vol |   pre_cost_sharpe |   avg_gross |   ann_turnover |   cost_drag |
|:-------------------------------|---------:|------------------:|------------------:|-------------:|----------:|------------------:|------------:|---------------:|------------:|
| current config                 |   -0.139 |             0.288 |            -0.581 |       -0.004 |     0.029 |             0.43  |       1.031 |         16.725 |       0.016 |
| frictionless                   |    0.826 |             1.938 |             0.019 |        0.037 |     0.045 |             0.826 |       1.767 |         89.23  |       0     |
| rank_weights                   |   -0.257 |             0.081 |            -0.701 |       -0.008 |     0.031 |             0.272 |       0.869 |         16.206 |       0.016 |
| dollar_neutral_only            |   -0.122 |            -0.169 |            -0.064 |       -0.008 |     0.066 |             0.051 |       0.796 |         12.052 |       0.011 |
| halflife=0 cost_aversion=0.0   |   -3.723 |            -4.943 |            -2.925 |       -0.106 |     0.028 |             1.527 |       0.986 |        167.008 |       0.149 |
| halflife=0 cost_aversion=0.25  |   -0.778 |            -0.648 |            -0.963 |       -0.023 |     0.029 |             1.309 |       0.978 |         67.591 |       0.061 |
| halflife=0 cost_aversion=0.5   |   -0.381 |            -0.2   |            -0.66  |       -0.009 |     0.025 |             0.889 |       0.836 |         35.579 |       0.031 |
| halflife=0 cost_aversion=1.0   |   -0.291 |            -0.216 |            -0.444 |       -0.006 |     0.02  |             0.359 |       0.661 |         14.867 |       0.013 |
| halflife=3 cost_aversion=0.0   |   -0.736 |            -0.533 |            -0.985 |       -0.023 |     0.031 |             1.012 |       1.123 |         54.328 |       0.054 |
| halflife=3 cost_aversion=0.25  |   -0.23  |             0.095 |            -0.637 |       -0.007 |     0.029 |             0.742 |       1.021 |         28.85  |       0.028 |
| halflife=3 cost_aversion=0.5   |   -0.153 |             0.164 |            -0.559 |       -0.004 |     0.027 |             0.585 |       0.929 |         20.546 |       0.02  |
| halflife=3 cost_aversion=1.0   |   -0.139 |             0.288 |            -0.581 |       -0.004 |     0.029 |             0.43  |       1.031 |         16.725 |       0.016 |
| halflife=7 cost_aversion=0.0   |   -0.469 |            -0.229 |            -0.782 |       -0.014 |     0.029 |             0.74  |       1.114 |         34.074 |       0.035 |
| halflife=7 cost_aversion=0.25  |   -0.226 |             0.134 |            -0.705 |       -0.007 |     0.031 |             0.715 |       1.298 |         27.691 |       0.029 |
| halflife=7 cost_aversion=0.5   |   -0.194 |             0.181 |            -0.635 |       -0.006 |     0.031 |             0.627 |       1.352 |         24.553 |       0.025 |
| halflife=7 cost_aversion=1.0   |   -0.157 |             0.239 |            -0.611 |       -0.005 |     0.029 |             0.477 |       1.214 |         17.765 |       0.019 |
| halflife=15 cost_aversion=0.0  |   -0.376 |            -0.157 |            -0.667 |       -0.01  |     0.028 |             0.571 |       1.095 |         24.247 |       0.026 |
| halflife=15 cost_aversion=0.25 |   -0.251 |            -0.04  |            -0.528 |       -0.007 |     0.027 |             0.458 |       1.049 |         17.338 |       0.019 |
| halflife=15 cost_aversion=0.5  |   -0.194 |             0.091 |            -0.587 |       -0.006 |     0.029 |             0.499 |       1.254 |         18.003 |       0.02  |
| halflife=15 cost_aversion=1.0  |   -0.169 |             0.155 |            -0.607 |       -0.005 |     0.028 |             0.411 |       1.172 |         14.198 |       0.016 |
| halflife=30 cost_aversion=0.0  |   -0.412 |            -0.304 |            -0.562 |       -0.011 |     0.027 |             0.351 |       1.051 |         18.006 |       0.021 |
| halflife=30 cost_aversion=0.25 |   -0.276 |            -0.156 |            -0.439 |       -0.007 |     0.027 |             0.301 |       1.016 |         12.88  |       0.016 |
| halflife=30 cost_aversion=0.5  |   -0.251 |            -0.142 |            -0.397 |       -0.007 |     0.026 |             0.258 |       0.983 |         10.949 |       0.013 |
| halflife=30 cost_aversion=1.0  |   -0.222 |            -0.078 |            -0.431 |       -0.006 |     0.028 |             0.261 |       1.117 |         10.609 |       0.013 |

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