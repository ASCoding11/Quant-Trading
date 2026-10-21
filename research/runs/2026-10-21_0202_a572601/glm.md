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

