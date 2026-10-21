# Research results

## Data quality

Bars removed as bad prints: 0

(none)

Largest close-to-close moves after cleaning:

| date       | ticker   |   return |
|:-----------|:---------|---------:|
| 2020-11-20 | CHRD     |  257.333 |
| 2004-11-18 | WT       |   36.5   |
| 2012-02-06 | TGTX     |    5.667 |
| 2002-08-30 | ARWR     |    5     |
| 2002-10-02 | ARWR     |    3     |
| 2002-04-26 | ARWR     |    3     |
| 2002-05-30 | ARWR     |    3     |
| 2009-06-10 | JAZZ     |    2.098 |
| 2011-07-21 | TGTX     |    2     |
| 2003-04-22 | ARWR     |    2     |
| 2002-03-28 | ARWR     |    2     |
| 2012-10-03 | SRPT     |    1.997 |
| 2003-04-23 | SBRA     |    1.833 |
| 2000-09-21 | DAR      |    1.75  |
| 2000-01-19 | ARWR     |    1.727 |

Largest overnight moves after cleaning:

| date       | ticker   |   return |
|:-----------|:---------|---------:|
| 2020-11-20 | CHRD     |  225.25  |
| 2004-11-18 | WT       |    5     |
| 2002-08-30 | ARWR     |    5     |
| 2002-05-30 | ARWR     |    3     |
| 2002-10-02 | ARWR     |    3     |
| 2011-07-21 | TGTX     |    2     |
| 2002-03-28 | ARWR     |    2     |
| 2012-11-27 | ACAD     |    1.826 |
| 2003-06-13 | WT       |    1.8   |
| 2000-01-26 | ACHC     |    1.625 |
| 2001-09-17 | OSIS     |    1.41  |
| 2021-01-27 | GME      |    1.398 |
| 2002-02-19 | SNEX     |    1.234 |
| 2024-05-14 | GME      |    1.129 |
| 2012-07-24 | SRPT     |    1.127 |

Largest intraday moves after cleaning:

| date       | ticker   |   return |
|:-----------|:---------|---------:|
| 2004-11-18 | WT       |    5.25  |
| 2000-11-22 | ACHC     |    3.5   |
| 2012-02-06 | TGTX     |    3.286 |
| 2002-11-06 | WT       |    1.714 |
| 2002-04-26 | ARWR     |    1.667 |
| 2014-07-01 | LEU      |    1.423 |
| 2008-10-20 | CELH     |    1.333 |
| 2002-10-28 | WT       |    1.333 |
| 2003-06-09 | CCOI     |    1.26  |
| 2005-10-25 | AGX      |    1.228 |
| 2020-03-13 | CHRD     |    1.222 |
| 2003-07-07 | EHC      |    1.1   |
| 2021-02-24 | GME      |    1.052 |
| 2000-01-26 | THRM     |    1.05  |
| 2021-11-02 | CAR      |    1.049 |


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


## Model families on the same signals

Each refit yearly on the previous 5 years; out-of-sample IC of the 5-day forecast, and the break-even cost / net Sharpe of trading it in 2015-2026 (hl = smoothing half-life).

| model    |   ic5_2010_14 |   ic5_2015_26 |   years_positive |   hl0_breakeven_2nd |   hl0_net_sharpe_2nd |   hl5_breakeven_2nd |   hl5_net_sharpe_2nd |
|:---------|--------------:|--------------:|-----------------:|--------------------:|---------------------:|--------------------:|---------------------:|
| ridge    |        0.0124 |        0.0062 |           0.7143 |              1.6175 |              -1.1503 |              5.0576 |              -0.0851 |
| logistic |        0.0094 |        0.0053 |           0.6667 |              1.4457 |              -1.2269 |              2.5545 |              -0.2062 |
| huber    |        0.0115 |        0.0045 |           0.6667 |              1.4467 |              -1.2257 |              2.138  |              -0.2243 |
| mlp      |        0.0106 |        0.009  |           0.7143 |              1.5437 |              -1.9721 |              8.8158 |               0.1339 |

How similar are their forecasts? (correlation of predictions)

|          |   ridge |   logistic |   huber |   mlp |
|:---------|--------:|-----------:|--------:|------:|
| ridge    |    1    |       0.96 |    0.96 |  0.49 |
| logistic |    0.96 |       1    |    0.95 |  0.48 |
| huber    |    0.96 |       0.95 |    1    |  0.47 |
| mlp      |    0.49 |       0.48 |    0.47 |  1    |

### Gamma GLM for volatility

Next 21 days' realized residual volatility (log link, Gamma errors), fit on 2004-2014, vs. the 63-day rolling estimate the portfolio uses. QLIKE out of sample (lower is better):

|            |   QLIKE 2015-2026 |
|:-----------|------------------:|
| gamma_glm  |           -7.4032 |
| rolling_63 |           -7.3052 |

| feature           |   coef_per_sd |   vol_ratio_per_sd |
|:------------------|--------------:|-------------------:|
| log_var_5         |         0.181 |              1.095 |
| log_var_21        |        -0.056 |              0.972 |
| log_var_63        |         0.754 |              1.458 |
| log_abn_volume    |        -0.013 |              0.994 |
| log_mkt_var_21    |         0.056 |              1.029 |
| log_dollar_volume |        -0.038 |              0.981 |


