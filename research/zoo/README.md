# Model zoo: what forecasts best, and does it last?

252 fitted models, 1512 traded strategies (model x signal set x horizon x smoothing x universe), refit yearly on 5 years, costs from measured spreads. Period 1 = 2006-2014, period 2 = 2015-2026.

## Does picking the best in period 1 work in period 2?

* Rank correlation of net Sharpe between the periods: **0.58** (IC: -0.24).
* With 1512 strategies tried, the best period-1 Sharpe expected from pure luck is up to **2.21** (deflated-Sharpe hurdle; an upper bound, since the strategies overlap heavily).
* Top 1 by period 1: Sharpe 0.42 in period 1 -> **0.11** in period 2.
* Top 10 by period 1: Sharpe 0.35 in period 1 -> **0.14** in period 2.
* Top 50 by period 1: Sharpe 0.24 in period 1 -> **0.04** in period 2.
* Ensemble of the 10 best period-1 models (equal weight): IC 0.0053 -> **0.0019**; best single of them in period 2: 0.0064.

## Model families: results, pros and cons

| name          |   ic_1st |   ic_2nd |   net_sharpe_2nd_best |   net_sharpe_2nd_median |   breakeven_2nd_median |   years_positive | pros                                                    | cons                                                   |
|:--------------|---------:|---------:|----------------------:|------------------------:|-----------------------:|-----------------:|:--------------------------------------------------------|:-------------------------------------------------------|
| extra_trees   |   0.0055 |   0.011  |                0.2823 |                  0.018  |                 5.2669 |           0.7619 | Averages many random trees: low variance                | Coarse; slow on big data                               |
| gbm_shallow   |   0.0067 |   0.0102 |                0.4596 |                 -0.0721 |                 3.7322 |           0.7778 | Finds interactions (e.g. reversal x low volume); robust | Slower; harder to explain                              |
| ridge_1e6     |   0.0003 |   0.0092 |                0.2244 |                 -0.0357 |                 3.9675 |           0.7143 | Close to an equal-weighted blend                        | Barely learns anything                                 |
| gbm_deep      |   0.0077 |   0.0091 |                0.4632 |                 -0.0689 |                 3.5335 |           0.75   | Captures complex interactions                           | Overfits easily; slow                                  |
| pca15_ridge   |   0.0015 |   0.0083 |                0.2746 |                 -0.0592 |                 3.2958 |           0.6905 | Keeps more detail than PCA-5                            | Same issue; more components = more noise               |
| lasso         |   0.0007 |   0.0081 |                0.158  |                 -0.1179 |                 2.4666 |           0.6944 | Sparse, interpretable                                   | Arbitrary pick between near-duplicates                 |
| elastic_net   |   0.0007 |   0.0081 |                0.1583 |                 -0.1185 |                 2.5028 |           0.6944 | Drops useless signals                                   | Unstable choice among correlated signals               |
| sign_ic       |   0.008  |   0.0079 |                0.5222 |                 -0.1713 |                 2.6588 |           0.7795 | Nothing to overfit; transparent                         | Ignores how strong each signal is and their overlap    |
| ridge_100     |   0.0012 |   0.0075 |                0.2074 |                 -0.1254 |                 2.5817 |           0.6944 | Balanced shrinkage                                      | Linear only                                            |
| ridge_1       |   0.0008 |   0.0073 |                0.2109 |                 -0.1444 |                 2.5251 |           0.6944 | Handles correlated signals jointly                      | Nearly unpenalised: noisy weights                      |
| tstat_ic      |   0.0081 |   0.0072 |                0.5828 |                 -0.181  |                 2.3801 |           0.7863 | Weights by proven reliability; robust (Grinold)         | Ignores correlation between signals: double-counts     |
| kernel_rff    |   0.0059 |   0.0072 |                0.3861 |                 -0.114  |                 3.0418 |           0.7302 | Nonlinear at linear cost                                | Bandwidth chosen by rule of thumb, not tuned           |
| ridge_1e4     |   0.0007 |   0.0071 |                0.1449 |                 -0.131  |                 1.9636 |           0.6944 | Heavy shrinkage, stable weights                         | Can shrink away real edges                             |
| logistic      |   0.0008 |   0.0069 |                0.1041 |                 -0.1987 |                 1.5369 |           0.6786 | Direction model, less shrinkage                         | Same; more overfitting                                 |
| huber         |   0.0017 |   0.0069 |                0.1732 |                 -0.1857 |                 1.559  |           0.6786 | Downweights extreme returns                             | Slow; similar to ridge in practice                     |
| mlp_64        |   0.0059 |   0.0068 |                0.4033 |                 -0.186  |                 2.6626 |           0.7302 | More capacity                                           | More noise and overfitting risk                        |
| logistic_weak |   0.0009 |   0.0067 |                0.0967 |                 -0.1911 |                 1.4278 |           0.6786 | Only direction matters: robust to outliers              | Throws away magnitude                                  |
| pca5_ridge    |  -0.0004 |   0.0066 |                0.2903 |                 -0.0224 |                 4.4158 |           0.7063 | Strips redundancy between signals                       | First components follow variance, not predictive power |
| mlp_16        |   0.0052 |   0.0064 |                0.4635 |                 -0.1902 |                 2.0932 |           0.7262 | Smooth nonlinearity                                     | Random initialisation adds noise between refits        |
| best_single   |   0.0063 |   0.0062 |                0.1984 |                 -0.2188 |                 2.8552 |           0.746  | Simplest possible; easy to monitor                      | No diversification; chases last period's winner        |
| mlp_64_32     |   0.0058 |   0.0059 |                0.3404 |                 -0.2209 |                 1.9221 |           0.7222 | Deepest network                                         | Least stable; needs more data than a few years give    |

## Signal sets

| set        |   ic_1st |   ic_2nd |   net_sharpe_2nd |
|:-----------|---------:|---------:|-----------------:|
| all        |   0.0078 |   0.0073 |          -0.117  |
| price      |   0.0081 |   0.0074 |          -0.1087 |
| price+fund |   0.0078 |   0.007  |          -0.1334 |
| reversal   |   0.0099 |   0.0062 |          -0.1852 |

## Forecast horizon

|   horizon |   ic_1st |   ic_2nd |   net_sharpe_1st |   net_sharpe_2nd |   turnover_2nd |
|----------:|---------:|---------:|-----------------:|-----------------:|---------------:|
|         1 |   0.0109 |   0.0071 |          -0.3857 |          -0.0741 |         0.1645 |
|         5 |   0.0083 |   0.0062 |          -0.3829 |          -0.1218 |         0.1767 |
|        21 |  -0.0114 |   0.0087 |          -0.5993 |          -0.1888 |         0.1655 |

## How to trade a forecast (median over models)

|                  |   net_sharpe_1st |   net_sharpe_2nd |   breakeven_bp_2nd |
|:-----------------|-----------------:|-----------------:|-------------------:|
| (0.0, 'all')     |           -1.487 |           -1.301 |              1.508 |
| (0.0, 'top300')  |           -0.491 |           -0.478 |              1.337 |
| (5.0, 'all')     |           -0.436 |           -0.177 |              3.704 |
| (5.0, 'top300')  |           -0.296 |           -0.053 |              2.574 |
| (20.0, 'all')    |           -0.408 |            0.056 |              9.338 |
| (20.0, 'top300') |           -0.37  |            0.01  |              4.219 |

## Strategies positive in both periods (ranked by the weaker period)

| strategy                                        |   ic_1st |   ic_2nd |   net_sharpe_1st |   net_sharpe_2nd |   breakeven_bp_2nd |   turnover_2nd |
|:------------------------------------------------|---------:|---------:|-----------------:|-----------------:|-------------------:|---------------:|
| tstat_ic | reversal | h1 | hl5.0 | top300       |    0.01  |    0.01  |            0.308 |            0.583 |             22.469 |          0.171 |
| tstat_ic | reversal | h1 | hl20.0 | all         |    0.01  |    0.01  |            0.262 |            0.32  |             19.799 |          0.115 |
| ridge_1e6 | reversal | h1 | hl5.0 | top300      |    0.012 |    0.012 |            0.321 |            0.224 |              7.132 |          0.236 |
| sign_ic | reversal | h1 | hl5.0 | top300        |    0.01  |    0.01  |            0.219 |            0.522 |             25.482 |          0.136 |
| ridge_1e6 | reversal | h1 | hl20.0 | all        |    0.012 |    0.012 |            0.235 |            0.213 |             12.93  |          0.11  |
| ridge_1e6 | reversal | h1 | hl20.0 | top300     |    0.012 |    0.012 |            0.213 |            0.205 |              9.683 |          0.124 |
| best_single | price | h5 | hl20.0 | top300      |    0.007 |    0.007 |            0.232 |            0.198 |              7.486 |          0.154 |
| best_single | reversal | h5 | hl20.0 | top300   |    0.008 |    0.007 |            0.38  |            0.198 |              7.486 |          0.154 |
| best_single | reversal | h1 | hl20.0 | top300   |    0.01  |    0.008 |            0.375 |            0.18  |              5.813 |          0.239 |
| ridge_1e6 | reversal | h5 | hl20.0 | all        |    0.015 |    0.012 |            0.267 |            0.168 |             12.381 |          0.096 |
| ridge_1e6 | reversal | h5 | hl20.0 | top300     |    0.015 |    0.012 |            0.167 |            0.169 |              9.299 |          0.11  |
| tstat_ic | reversal | h1 | hl20.0 | top300      |    0.01  |    0.01  |            0.152 |            0.537 |             33.697 |          0.097 |
| best_single | price+fund | h5 | hl20.0 | top300 |    0.007 |    0.007 |            0.232 |            0.129 |              6.631 |          0.129 |
| sign_ic | reversal | h1 | hl20.0 | all          |    0.01  |    0.01  |            0.115 |            0.295 |             20.352 |          0.099 |
| best_single | reversal | h5 | hl5.0 | top300    |    0.008 |    0.007 |            0.416 |            0.108 |              4.691 |          0.292 |
| best_single | price | h5 | hl5.0 | top300       |    0.007 |    0.007 |            0.202 |            0.108 |              4.691 |          0.292 |
| sign_ic | reversal | h1 | hl20.0 | top300       |    0.01  |    0.01  |            0.096 |            0.508 |             37.566 |          0.082 |
| ridge_1e6 | reversal | h5 | hl5.0 | top300      |    0.015 |    0.012 |            0.327 |            0.09  |              5.251 |          0.213 |
| best_single | price+fund | h5 | hl5.0 | top300  |    0.007 |    0.007 |            0.202 |            0.074 |              4.489 |          0.239 |
| best_single | price | h1 | hl20.0 | top300      |    0.01  |    0.004 |            0.262 |            0.074 |              4.761 |          0.191 |
| best_single | reversal | h5 | hl20.0 | all      |    0.008 |    0.007 |            0.318 |            0.071 |              8.115 |          0.14  |
| best_single | price | h5 | hl20.0 | all         |    0.007 |    0.007 |            0.269 |            0.071 |              8.113 |          0.14  |
| pca5_ridge | reversal | h5 | hl5.0 | top300     |    0.01  |    0.008 |            0.283 |            0.054 |              4.576 |          0.237 |
| best_single | all | h1 | hl20.0 | top300        |    0.01  |    0.003 |            0.185 |            0.046 |              4.529 |          0.148 |
| sign_ic | reversal | h5 | hl20.0 | all          |    0.013 |    0.008 |            0.288 |            0.04  |              8.324 |          0.114 |

## Strongest and most consistent correlations with future returns

Full list: `best_correlations.csv`. Ranked by the IC in the *weaker* of the two periods; only entries with the same sign in both periods and a positive IC in at least 70% of years. Survivorship-prone = small/illiquid tilts that a universe of today's survivors flatters.

| what   | name                           |   horizon_days |   ic_2006_14 |   ic_2015_26 |   t_2006_14 |   t_2015_26 |   years_positive | survivorship_prone   |
|:-------|:-------------------------------|---------------:|-------------:|-------------:|------------:|------------:|-----------------:|:---------------------|
| pair   | rev_5d + downside_beta         |              5 |       0.0205 |       0.0181 |      3.7463 |    nan      |           0.8519 | False                |
| pair   | low_volume_rev + downside_beta |              5 |       0.0216 |       0.0174 |      3.898  |    nan      |           0.8519 | True                 |
| pair   | rev_1d + rev_21d               |              5 |       0.0178 |       0.0168 |      3.4318 |    nan      |           0.8889 | False                |
| signal | bollinger_z                    |             21 |       0.0212 |       0.0164 |      2.4608 |      1.537  |           0.7778 | False                |
| pair   | rev_5d + rev_21d               |              5 |       0.0189 |       0.0161 |      3.5792 |    nan      |           0.8519 | False                |
| pair   | rev_5d + resid_mom             |              5 |       0.0199 |       0.016  |      4.2746 |    nan      |           0.8148 | False                |
| pair   | bollinger_z + resid_mom        |              5 |       0.016  |       0.016  |      3.9971 |    nan      |           0.8889 | False                |
| pair   | rsi_14 + downside_beta         |              5 |       0.0159 |       0.0168 |      2.9933 |    nan      |           0.8148 | False                |
| pair   | rev_21d + low_volume_rev       |              5 |       0.0199 |       0.0159 |      3.7147 |    nan      |           0.8519 | True                 |
| signal | rev_21d                        |             21 |       0.0158 |       0.0174 |      1.4932 |      1.4738 |           0.7037 | False                |
| pair   | mom_12_1 + high_52w            |              5 |       0.0171 |       0.0158 |      2.6971 |    nan      |           0.8519 | False                |
| pair   | rev_5d + cluster_mom           |              5 |       0.0161 |       0.0158 |      2.6526 |    nan      |           0.7778 | False                |
| pair   | rev_1d + downside_beta         |              5 |       0.0155 |       0.0167 |      2.9396 |    nan      |           0.8519 | False                |
| pair   | low_volume_rev + resid_mom     |              5 |       0.0209 |       0.0155 |      4.3951 |    nan      |           0.8519 | True                 |
| pair   | rev_21d + intraday_rev         |              5 |       0.0163 |       0.0154 |      3.182  |    nan      |           0.8519 | False                |
| pair   | low_volume_rev + cluster_mom   |              5 |       0.017  |       0.0154 |      2.775  |    nan      |           0.8519 | True                 |
| pair   | rev_1d + resid_mom             |              5 |       0.0163 |       0.0153 |      3.5449 |    nan      |           0.8519 | False                |
| pair   | bollinger_z + downside_beta    |              5 |       0.0152 |       0.018  |      3.1003 |    nan      |           0.8519 | False                |
| pair   | rev_21d + peer_gap             |              5 |       0.0153 |       0.0151 |      3.3381 |    nan      |           0.8519 | False                |
| pair   | rev_21d + mom_12_1             |              5 |       0.0151 |       0.0153 |      2.6759 |    nan      |           0.7778 | False                |
| pair   | rev_5d + mom_accel             |              5 |       0.0198 |       0.0151 |      3.8556 |    nan      |           0.8889 | False                |
| pair   | rev_21d + bollinger_z          |              5 |       0.0157 |       0.015  |      3.0608 |    nan      |           0.8889 | False                |
| pair   | rsi_14 + resid_mom             |              5 |       0.0168 |       0.015  |      4.111  |    nan      |           0.9259 | False                |
| pair   | rev_1d + bollinger_z           |              5 |       0.0198 |       0.015  |      4.2881 |    nan      |           0.9259 | False                |
| pair   | rev_1d + mom_accel             |              5 |       0.0178 |       0.015  |      3.5758 |    nan      |           0.8889 | False                |
| pair   | rev_1d + rev_5d                |              5 |       0.0222 |       0.0148 |      4.4388 |    nan      |           0.9259 | False                |
| signal | low_volume_rev                 |             21 |       0.0147 |       0.0151 |      1.4399 |      1.2706 |           0.7778 | True                 |
| pair   | low_volume_rev + mom_accel     |              5 |       0.0208 |       0.0147 |      3.9934 |    nan      |           0.8889 | True                 |
| pair   | rev_5d + mom_12_1              |              5 |       0.0224 |       0.0147 |      3.7975 |    nan      |           0.8148 | False                |
| pair   | bollinger_z + mom_12_1         |              5 |       0.0188 |       0.0147 |      3.4143 |    nan      |           0.7778 | False                |
| pair   | rev_1d + intraday_rev_21       |              5 |       0.017  |       0.0146 |      3.3088 |    nan      |           0.8519 | False                |
| pair   | rev_5d + bollinger_z           |              5 |       0.0208 |       0.0146 |      4.3755 |    nan      |           0.8889 | False                |
| pair   | resid_mom + peer_gap           |              5 |       0.0147 |       0.0144 |      4.0457 |    nan      |           0.8148 | False                |
| pair   | rev_1d + rsi_14                |              5 |       0.0207 |       0.0144 |      4.2981 |    nan      |           0.8889 | False                |
| pair   | rev_1d + mom_12_1              |              5 |       0.02   |       0.0144 |      3.4161 |    nan      |           0.8148 | False                |
| pair   | rev_1d + low_volume_rev        |              5 |       0.023  |       0.0144 |      4.5366 |    nan      |           0.9259 | True                 |
| pair   | bollinger_z + mom_accel        |              5 |       0.0165 |       0.0144 |      3.3357 |    nan      |           0.8519 | False                |
| pair   | rev_5d + overnight_mom         |              5 |       0.0171 |       0.0143 |      3.9451 |    nan      |           0.8889 | False                |
| pair   | low_volume_rev + mom_12_1      |              5 |       0.0234 |       0.0142 |      3.9283 |    nan      |           0.8148 | True                 |
| pair   | bollinger_z + low_volume_rev   |              5 |       0.0215 |       0.0142 |      4.4896 |    nan      |           0.9259 | True                 |

