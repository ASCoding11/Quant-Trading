## Volatility models (GARCH family)

QLIKE loss out of sample (2015-2026), parameters estimated on 2004-2014. Lower is better; differences of 0.01 are meaningful over thousands of days.

### Market (equal-weighted universe)

|            |   1-day |   21-day |
|:-----------|--------:|---------:|
| rolling_21 | -8.0976 |  -7.8205 |
| rolling_63 | -8.0348 |  -7.6647 |
| ewma       | -8.1354 |  -7.8406 |
| garch      | -8.1639 |  -7.9432 |
| gjr        | -8.1936 |  -7.9619 |
| garch_t    | -8.1629 |  -7.9382 |
| gjr_t      | -8.1941 |  -7.9584 |

Fitted parameters (g = extra reaction to down days; nu = tail thickness, lower = fatter):

|         |      a |      b |      g |       nu |   persistence |   half_life_days |
|:--------|-------:|-------:|-------:|---------:|--------------:|-----------------:|
| garch   | 0.0933 | 0.8949 | 0      | nan      |        0.9882 |          58.5217 |
| gjr     | 0      | 0.9054 | 0.1588 | nan      |        0.9848 |          45.3116 |
| garch_t | 0.0878 | 0.9022 | 0      |  13.1666 |        0.99   |          68.8384 |
| gjr_t   | 0      | 0.9078 | 0.1564 |  18.4467 |        0.986  |          49.1802 |

### Stock residual volatility (150 stocks)

Average QLIKE and how often each model was best for a stock:

|            |   mean_qlike |   best_for_n_stocks |
|:-----------|-------------:|--------------------:|
| ewma       |      -7.3983 |                   2 |
| garch      |      -7.5003 |                  34 |
| garch_t    |      -7.4978 |                  28 |
| gjr        |      -7.4994 |                  49 |
| gjr_t      |      -7.4974 |                  35 |
| rolling_21 |      -7.2614 |                   0 |
| rolling_63 |      -7.4156 |                   2 |

The portfolio currently sizes with rolling_63. A clearly lower loss for a GARCH variant means position sizes (and the vol target) would track risk better with it.

### Volatility-managed composite (net of costs)

The long-short composite (5-day smoothing), scaled each day by 1 / its forecast volatility (capped at 3x). If Sharpe rises, the strategy's own risk is forecastable and the vol target should use the better forecast.

| scaling    |   sharpe_1st |   max_dd_1st |   sharpe_2nd |   max_dd_2nd |
|:-----------|-------------:|-------------:|-------------:|-------------:|
| none       |        0.434 |       -0.149 |       -0.053 |       -0.211 |
| rolling_63 |        0.053 |       -0.17  |       -0.354 |       -0.172 |
| ewma       |       -0.064 |       -0.187 |       -0.434 |       -0.191 |
| garch      |       -0.021 |       -0.159 |       -0.441 |       -0.198 |
| gjr_t      |       -0.031 |       -0.166 |       -0.534 |       -0.219 |

