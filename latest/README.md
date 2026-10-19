# Backtest results

| | |
|---|---|
| Period | 2003-12-19 to 2026-10-19 (22.8 years) |
| Stocks / signals | 1000 / 44 |
| Traded model | ensemble |
| Sharpe ratio | -0.37 |
| Annual return | -0.6% |
| Annual volatility | 1.7% |
| Max drawdown | -19.9% |
| Deflated Sharpe probability | 1.0% |
| Beta / correlation to market | -0.01 / -0.15 |
| Avg gross exposure | 0.79x |
| Annual turnover | 10x |
| Cost + borrow drag / yr | 0.9% |

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
| elastic_net  |   -0.225 |       -0.004 |     0.016 |         -0.183 |          8.788 |           0.006 |     0.012 |
| gbm          |   -0.232 |       -0.004 |     0.019 |         -0.154 |         11.927 |           0.009 |     0.012 |
| ensemble     |   -0.367 |       -0.006 |     0.017 |         -0.199 |          9.877 |           0.007 |     0.014 |
| regime_ridge |   -0.377 |       -0.006 |     0.017 |         -0.207 |          9.321 |           0.007 |     0.011 |
| ic_weighted  |   -0.41  |       -0.006 |     0.015 |         -0.165 |          6.121 |           0.004 |     0.009 |
| ridge        |   -0.411 |       -0.007 |     0.017 |         -0.221 |         10.005 |           0.007 |     0.013 |
| kernel_ridge |   -0.43  |       -0.007 |     0.017 |         -0.246 |         10.886 |           0.008 |     0.013 |

## Portfolio-construction diagnostics (same ensemble forecast)

| variant                        |   sharpe |   sharpe_1st_half |   sharpe_2nd_half |   ann_return |   ann_vol |   pre_cost_sharpe |   avg_gross |   ann_turnover |   cost_drag |
|:-------------------------------|---------:|------------------:|------------------:|-------------:|----------:|------------------:|------------:|---------------:|------------:|
| current config                 |   -0.367 |            -0.307 |            -0.502 |       -0.006 |     0.017 |             0.191 |       0.794 |          9.877 |       0.009 |
| frictionless                   |    1.875 |             2.927 |             1.058 |        0.101 |     0.054 |             1.875 |       1.988 |        506.379 |       0     |
| rank_weights                   |   -0.269 |            -0.206 |            -0.414 |       -0.005 |     0.019 |             0.244 |       0.77  |         11.611 |       0.01  |
| dollar_neutral_only            |   -0.163 |            -0.194 |            -0.131 |       -0.009 |     0.052 |            -0.03  |       0.596 |          8.363 |       0.007 |
| halflife=0 cost_aversion=0.0   |   -5.954 |            -7.849 |            -4.634 |       -0.172 |     0.029 |             1.877 |       1.012 |        255.808 |       0.226 |
| halflife=0 cost_aversion=0.25  |   -0.908 |            -0.802 |            -1.154 |       -0.023 |     0.025 |             1.395 |       0.852 |         65.702 |       0.058 |
| halflife=0 cost_aversion=0.5   |   -0.363 |            -0.198 |            -0.727 |       -0.008 |     0.021 |             0.854 |       0.85  |         29.067 |       0.026 |
| halflife=0 cost_aversion=1.0   |   -0.367 |            -0.307 |            -0.502 |       -0.006 |     0.017 |             0.191 |       0.794 |          9.877 |       0.009 |
| halflife=3 cost_aversion=0.0   |   -1.338 |            -1.4   |            -1.28  |       -0.038 |     0.028 |             1.344 |       1.154 |         79.334 |       0.076 |
| halflife=3 cost_aversion=0.25  |   -0.484 |            -0.343 |            -0.702 |       -0.015 |     0.031 |             1.143 |       1.179 |         52.123 |       0.05  |
| halflife=3 cost_aversion=0.5   |   -0.268 |            -0.125 |            -0.501 |       -0.008 |     0.029 |             1.025 |       1.124 |         38.812 |       0.037 |
| halflife=3 cost_aversion=1.0   |   -0.13  |             0.05  |            -0.445 |       -0.003 |     0.026 |             0.809 |       1.027 |         25.673 |       0.025 |
| halflife=7 cost_aversion=0.0   |   -0.597 |            -0.612 |            -0.587 |       -0.019 |     0.031 |             1.002 |       1.224 |         49.277 |       0.05  |
| halflife=7 cost_aversion=0.25  |   -0.196 |            -0.156 |            -0.258 |       -0.006 |     0.029 |             0.782 |       1.181 |         28.279 |       0.029 |
| halflife=7 cost_aversion=0.5   |   -0.139 |            -0.069 |            -0.251 |       -0.004 |     0.028 |             0.644 |       1.117 |         21.056 |       0.022 |
| halflife=7 cost_aversion=1.0   |   -0.12  |             0.057 |            -0.357 |       -0.004 |     0.029 |             0.526 |       1.339 |         18.344 |       0.019 |
| halflife=15 cost_aversion=0.0  |   -0.445 |            -0.472 |            -0.421 |       -0.013 |     0.029 |             0.718 |       1.219 |         31.408 |       0.034 |
| halflife=15 cost_aversion=0.25 |   -0.185 |            -0.179 |            -0.202 |       -0.005 |     0.028 |             0.503 |       1.172 |         17.16  |       0.019 |
| halflife=15 cost_aversion=0.5  |   -0.201 |            -0.171 |            -0.257 |       -0.005 |     0.026 |             0.354 |       1.098 |         12.766 |       0.015 |
| halflife=15 cost_aversion=1.0  |   -0.221 |            -0.209 |            -0.256 |       -0.005 |     0.024 |             0.199 |       0.972 |          8.411 |       0.01  |
| halflife=30 cost_aversion=0.0  |   -0.5   |            -0.537 |            -0.469 |       -0.014 |     0.028 |             0.467 |       1.208 |         23.373 |       0.027 |
| halflife=30 cost_aversion=0.25 |   -0.299 |            -0.283 |            -0.343 |       -0.008 |     0.027 |             0.266 |       1.142 |         12.163 |       0.015 |
| halflife=30 cost_aversion=0.5  |   -0.315 |            -0.323 |            -0.324 |       -0.008 |     0.026 |             0.145 |       1.067 |          9.162 |       0.012 |
| halflife=30 cost_aversion=1.0  |   -0.335 |            -0.359 |            -0.32  |       -0.008 |     0.024 |             0.021 |       0.926 |          6.112 |       0.008 |

## Signals (descriptive, full-sample rank IC)

| signal              | family         |   mean_ic |   ic_ir |   t_stat |   hit_rate |   ic_regime_0 |   ic_regime_1 |   ic_regime_2 |
|:--------------------|:---------------|----------:|--------:|---------:|-----------:|--------------:|--------------:|--------------:|
| resid_rev_1d        | mean_reversion |    0.011  |  2.6032 |  13.1762 |     0.5669 |        0.011  |        0.0076 |        0.0123 |
| resid_rev_5d        | mean_reversion |    0.0065 |  1.4459 |   7.3187 |     0.5381 |        0.0047 |        0.0077 |        0.0081 |
| peer_gap            | structure      |    0.0083 |  1.3847 |   7.0248 |     0.5338 |        0.0074 |        0.0101 |        0.0086 |
| rev_1d              | mean_reversion |    0.0123 |  1.2951 |   6.5763 |     0.548  |        0.0136 |        0.0061 |        0.0133 |
| intraday_rev        | mean_reversion |    0.0104 |  1.2021 |   6.1041 |     0.5359 |        0.0109 |        0.0066 |        0.0115 |
| rev_5d              | mean_reversion |    0.0109 |  1.1131 |   5.6525 |     0.5269 |        0.0097 |        0.0108 |        0.0122 |
| low_volume_rev      | mean_reversion |    0.0107 |  1.1064 |   5.6182 |     0.5259 |        0.0099 |        0.0108 |        0.0117 |
| resid_mom           | momentum       |    0.0078 |  1.0862 |   5.4372 |     0.5411 |        0.0092 |        0.0085 |        0.006  |
| autocorr_signal     | structure      |    0.0046 |  1.0352 |   5.2566 |     0.5317 |        0.0023 |        0.0023 |        0.0081 |
| ou_sscore           | mean_reversion |    0.0033 |  0.894  |   4.5181 |     0.5203 |        0.0018 |        0.0043 |        0.0047 |
| mom_12_1            | momentum       |    0.01   |  0.8506 |   4.3149 |     0.5329 |        0.0134 |        0.0134 |        0.0047 |
| bollinger_z         | mean_reversion |    0.0072 |  0.838  |   4.2551 |     0.5148 |        0.0052 |        0.0096 |        0.0085 |
| vol_price_corr      | volume         |    0.0042 |  0.7929 |   4.0262 |     0.5139 |        0.0032 |        0.0095 |        0.0031 |
| close_location      | microstructure |    0.005  |  0.7295 |   3.7042 |     0.5179 |        0.0038 |        0.0021 |        0.0074 |
| mom_6_1             | momentum       |    0.007  |  0.6478 |   3.2897 |     0.5292 |        0.0081 |        0.0076 |        0.0056 |
| rsi_14              | mean_reversion |    0.0058 |  0.6315 |   3.2066 |     0.508  |        0.004  |        0.0076 |        0.0071 |
| same_month          | seasonality    |    0.0041 |  0.6213 |   3.09   |     0.5184 |        0.0045 |        0.0063 |        0.0028 |
| rev_21d             | mean_reversion |    0.006  |  0.6159 |   3.1273 |     0.5125 |        0.0048 |        0.0092 |        0.0061 |
| intraday_rev_21     | momentum       |    0.0054 |  0.5966 |   3.0297 |     0.5066 |        0.0042 |        0.0103 |        0.0047 |
| weekday_seasonality | seasonality    |    0.0024 |  0.5611 |   2.818  |     0.5217 |        0.0015 |        0.0039 |        0.0026 |
| max_effect          | volatility     |    0.0055 |  0.4588 |   2.3297 |     0.5005 |        0.0065 |        0.0029 |        0.0055 |
| overnight_rev       | mean_reversion |    0.0043 |  0.4524 |   2.2975 |     0.5192 |        0.0047 |       -0.001  |        0.0058 |
| neg_skew            | volatility     |    0.0023 |  0.4502 |   2.2863 |     0.5078 |        0.003  |        0.0038 |        0.0009 |
| idio_vol            | volatility     |    0.0045 |  0.387  |   1.9571 |     0.5012 |        0.0041 |        0.0002 |        0.0068 |
| low_vol             | volatility     |    0.005  |  0.3271 |   1.6608 |     0.5002 |        0.0069 |       -0.0009 |        0.0053 |
| bab                 | volatility     |    0.0048 |  0.274  |   1.3914 |     0.5011 |        0.009  |       -0.004  |        0.0036 |
| size_proxy          | volume         |    0.0021 |  0.2665 |   1.3533 |     0.5008 |        0.0038 |       -0.0029 |        0.0024 |
| high_52w            | momentum       |    0.0032 |  0.2545 |   1.2925 |     0.5168 |        0.006  |        0.0012 |        0.0009 |
| range_vol_ratio     | microstructure |    0.0014 |  0.2482 |   1.2606 |     0.5137 |       -0.0003 |        0.002  |        0.0031 |
| turn_of_month       | seasonality    |    0.003  |  0.1697 |   0.8615 |     0.5015 |        0.0065 |       -0.0125 |        0.0053 |
| market_corr         | structure      |    0.0009 |  0.0817 |   0.415  |     0.5037 |        0.0062 |       -0.0011 |       -0.0041 |
| amihud              | volume         |    0.0005 |  0.0551 |   0.28   |     0.4963 |        0.0012 |       -0.0025 |        0.001  |
| trend_quality       | momentum       |   -0      | -0.0011 |  -0.0058 |     0.5106 |        0.001  |        0.0021 |       -0.002  |
| vol_of_vol          | volatility     |   -0      | -0.0082 |  -0.0414 |     0.5068 |       -0.0012 |        0.0008 |        0.0009 |
| gk_ratio            | microstructure |   -0.0004 | -0.0695 |  -0.353  |     0.4948 |       -0.0025 |        0.0031 |        0.0004 |
| abn_volume          | volume         |   -0.0005 | -0.1043 |  -0.5297 |     0.4946 |        0.0002 |       -0.0014 |       -0.0008 |
| kalman_trend        | structure      |   -0.0012 | -0.1264 |  -0.642  |     0.4957 |       -0.0001 |       -0.0037 |       -0.0013 |
| turnover_trend      | volume         |   -0.001  | -0.1452 |  -0.7375 |     0.4883 |       -0.0037 |       -0.0014 |        0.0023 |
| overnight_mom       | momentum       |   -0.0018 | -0.246  |  -1.2489 |     0.4945 |       -0.0011 |        0.0009 |       -0.0037 |
| cluster_mom         | momentum       |   -0.0037 | -0.3534 |  -1.793  |     0.4955 |       -0.0028 |       -0.0085 |       -0.0028 |
| peer_lead           | structure      |   -0.0045 | -0.4364 |  -2.2138 |     0.4857 |       -0.0058 |        0.0011 |       -0.0053 |
| cs_spread           | microstructure |   -0.0051 | -0.4563 |  -2.3173 |     0.4932 |       -0.0057 |       -0.0031 |       -0.0052 |
| downside_beta       | volatility     |   -0.0089 | -0.5229 |  -1.0749 |     0.4854 |       -0.0146 |       -0.0277 |        0.0091 |
| mom_accel           | momentum       |   -0.0047 | -0.5313 |  -2.698  |     0.4931 |       -0.0043 |       -0.0031 |       -0.0059 |

![signals](charts/signals.png)

![weights](charts/weights.png)

Full interactive-free report with monthly table and config: `report.html` (download and open).