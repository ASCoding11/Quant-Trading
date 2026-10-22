## Consumer companies around earnings

30535 earnings releases since 2016 (4490 from consumer companies by SIC code), traded with a market-on-close order before the release and a market-on-open exit after it. Signal directions from 2016-2020; 2021-2026 is the check. Coverage of each signal: wiki_attention 34%, wiki_yoy 33%, trends_yoy 8%, runup_20d 100%, last_reaction 97%.

### Rank correlation of each signal with the outcome

| universe      | signal         | outcome   |   ic_2016_20 |   n_2016_20 |   ic_2021_26 |   n_2021_26 |
|:--------------|:---------------|:----------|-------------:|------------:|-------------:|------------:|
| consumer      | wiki_attention | ann_ret   |       -0.07  |         663 |        0.005 |         931 |
| consumer      | wiki_attention | drift_5d  |        0.027 |         663 |        0.067 |         931 |
| consumer      | wiki_attention | drift_20d |        0.007 |         663 |        0.022 |         931 |
| consumer      | wiki_yoy       | ann_ret   |       -0.001 |         645 |       -0.013 |         926 |
| consumer      | wiki_yoy       | drift_5d  |        0.026 |         645 |       -0.009 |         926 |
| consumer      | wiki_yoy       | drift_20d |       -0.015 |         645 |       -0.057 |         926 |
| consumer      | trends_yoy     | ann_ret   |        0.052 |        1007 |        0.085 |        1325 |
| consumer      | trends_yoy     | drift_5d  |       -0.035 |        1007 |        0.014 |        1325 |
| consumer      | trends_yoy     | drift_20d |       -0     |        1007 |       -0.026 |        1325 |
| consumer      | runup_20d      | ann_ret   |        0.023 |        2098 |       -0.008 |        2390 |
| consumer      | runup_20d      | drift_5d  |       -0.068 |        2099 |       -0.053 |        2390 |
| consumer      | runup_20d      | drift_20d |       -0.038 |        2099 |       -0.067 |        2390 |
| consumer      | last_reaction  | ann_ret   |        0.057 |        1974 |        0.007 |        2378 |
| consumer      | last_reaction  | drift_5d  |       -0.065 |        1975 |        0.029 |        2378 |
| consumer      | last_reaction  | drift_20d |       -0.065 |        1975 |        0.04  |        2378 |
| all companies | wiki_attention | ann_ret   |        0.007 |        4112 |        0.02  |        6251 |
| all companies | wiki_attention | drift_5d  |        0.036 |        4112 |        0.021 |        6251 |
| all companies | wiki_attention | drift_20d |        0.044 |        4112 |        0.012 |        6251 |
| all companies | wiki_yoy       | ann_ret   |       -0.003 |        3964 |       -0.011 |        6188 |
| all companies | wiki_yoy       | drift_5d  |        0.009 |        3964 |       -0.022 |        6188 |
| all companies | wiki_yoy       | drift_20d |        0.007 |        3964 |       -0.031 |        6188 |
| all companies | trends_yoy     | ann_ret   |        0.052 |        1007 |        0.085 |        1325 |
| all companies | trends_yoy     | drift_5d  |       -0.035 |        1007 |        0.014 |        1325 |
| all companies | trends_yoy     | drift_20d |       -0     |        1007 |       -0.026 |        1325 |
| all companies | runup_20d      | ann_ret   |        0.01  |       14003 |       -0.004 |       16530 |
| all companies | runup_20d      | drift_5d  |       -0.024 |       14004 |       -0.005 |       16530 |
| all companies | runup_20d      | drift_20d |       -0     |       14004 |       -0.019 |       16529 |
| all companies | last_reaction  | ann_ret   |        0.025 |       13164 |        0.001 |       16464 |
| all companies | last_reaction  | drift_5d  |       -0.03  |       13165 |        0.007 |       16464 |
| all companies | last_reaction  | drift_20d |       -0.014 |       13165 |        0.01  |       16463 |

### Trading it (IBKR Lite: no commission; SEC/FINRA fees on sales; auction legs at 0 bp and 1 bp)

2% of capital per event; announcement trades are overnight (close -> next open). The post-earnings drift rows show the average event return and its t-statistic (entered at the open after the release).

| universe      | strategy                | direction   |   events |   auction_slippage_bp |   sharpe_2016_20 |   annual_return_2016_20 |   avg_event_bp_2016_20 |   sharpe_2021_26 |   annual_return_2021_26 |   avg_event_bp_2021_26 |   t_2016_20 |   t_2021_26 |
|:--------------|:------------------------|:------------|---------:|----------------------:|-----------------:|------------------------:|-----------------------:|-----------------:|------------------------:|-----------------------:|------------:|------------:|
| consumer      | wiki_attention          | -           |     1585 |                     0 |            0.601 |                   0.007 |                 27.274 |            0.259 |                   0.004 |                 13.452 |     nan     |     nan     |
| consumer      | wiki_yoy                | -           |     1555 |                     0 |            0.263 |                   0.003 |                 12.027 |           -0.074 |                  -0.001 |                 -3.254 |     nan     |     nan     |
| consumer      | trends_yoy              | +           |     2311 |                     0 |            1.062 |                   0.015 |                 38.424 |            1.11  |                   0.019 |                 44.485 |     nan     |     nan     |
| consumer      | runup_20d               | +           |     4468 |                     0 |           -0.419 |                  -0.009 |                -10.769 |           -0.195 |                  -0.005 |                 -5.836 |     nan     |     nan     |
| consumer      | last_reaction           | +           |     4332 |                     0 |            0.607 |                   0.012 |                 16.454 |           -0.029 |                  -0.001 |                 -0.607 |     nan     |     nan     |
| consumer      | composite               | +           |     4483 |                     0 |            1.358 |                   0.029 |                 36.009 |            0.207 |                   0.005 |                  6.785 |     nan     |     nan     |
| consumer      | post-earnings drift 5d  | +           |     4488 |                     0 |          nan     |                 nan     |                -22.775 |          nan     |                 nan     |                -13.834 |      -1.668 |      -1.029 |
| consumer      | post-earnings drift 20d | +           |     4488 |                     0 |          nan     |                 nan     |                -28.604 |          nan     |                 nan     |                -26.415 |      -1.429 |      -1.343 |
| all companies | wiki_attention          | +           |    10350 |                     0 |           -0.421 |                  -0.011 |                 -6.299 |            0.057 |                   0.002 |                  1.299 |     nan     |     nan     |
| all companies | wiki_yoy                | -           |    10134 |                     0 |           -0.297 |                  -0.008 |                 -5.042 |           -0.094 |                  -0.003 |                 -1.201 |     nan     |     nan     |
| all companies | runup_20d               | +           |    30512 |                     0 |           -0.178 |                  -0.009 |                 -1.333 |            0.361 |                   0.023 |                  4.505 |     nan     |     nan     |
| all companies | last_reaction           | +           |    29607 |                     0 |            0.764 |                   0.037 |                  7.624 |            0.397 |                   0.024 |                  4.748 |     nan     |     nan     |
| all companies | composite               | +           |    30534 |                     0 |            0.115 |                   0.006 |                  1.406 |            0.056 |                   0.004 |                  0.969 |     nan     |     nan     |
| all companies | post-earnings drift 5d  | +           |    30533 |                     0 |          nan     |                 nan     |                 -0.256 |          nan     |                 nan     |                  9.417 |      -0.049 |       1.852 |
| all companies | post-earnings drift 20d | +           |    30533 |                     0 |          nan     |                 nan     |                 14.17  |          nan     |                 nan     |                 16.934 |       1.813 |       2.332 |
| consumer      | wiki_attention          | -           |     1585 |                     1 |            0.556 |                   0.006 |                 27.274 |            0.219 |                   0.003 |                 13.452 |     nan     |     nan     |
| consumer      | wiki_yoy                | -           |     1555 |                     1 |            0.218 |                   0.002 |                 12.027 |           -0.116 |                  -0.002 |                 -3.254 |     nan     |     nan     |
| consumer      | trends_yoy              | +           |     2311 |                     1 |            1.007 |                   0.014 |                 38.424 |            1.061 |                   0.018 |                 44.485 |     nan     |     nan     |
| consumer      | runup_20d               | +           |     4468 |                     1 |           -0.495 |                  -0.011 |                -10.769 |           -0.259 |                  -0.006 |                 -5.836 |     nan     |     nan     |
| consumer      | last_reaction           | +           |     4332 |                     1 |            0.532 |                   0.011 |                 16.454 |           -0.092 |                  -0.002 |                 -0.607 |     nan     |     nan     |
| consumer      | composite               | +           |     4483 |                     1 |            1.283 |                   0.027 |                 36.009 |            0.143 |                   0.004 |                  6.785 |     nan     |     nan     |
| consumer      | post-earnings drift 5d  | +           |     4488 |                     1 |          nan     |                 nan     |                -22.775 |          nan     |                 nan     |                -13.834 |      -1.668 |      -1.029 |
| consumer      | post-earnings drift 20d | +           |     4488 |                     1 |          nan     |                 nan     |                -28.604 |          nan     |                 nan     |                -26.415 |      -1.429 |      -1.343 |
| all companies | wiki_attention          | +           |    10350 |                     1 |           -0.548 |                  -0.014 |                 -6.299 |           -0.058 |                  -0.002 |                  1.299 |     nan     |     nan     |
| all companies | wiki_yoy                | -           |    10134 |                     1 |           -0.407 |                  -0.011 |                 -5.042 |           -0.219 |                  -0.007 |                 -1.201 |     nan     |     nan     |
| all companies | runup_20d               | +           |    30512 |                     1 |           -0.391 |                  -0.02  |                 -1.333 |            0.189 |                   0.012 |                  4.505 |     nan     |     nan     |
| all companies | last_reaction           | +           |    29607 |                     1 |            0.555 |                   0.027 |                  7.624 |            0.218 |                   0.013 |                  4.748 |     nan     |     nan     |
| all companies | composite               | +           |    30534 |                     1 |           -0.102 |                  -0.005 |                  1.406 |           -0.115 |                  -0.007 |                  0.969 |     nan     |     nan     |
| all companies | post-earnings drift 5d  | +           |    30533 |                     1 |          nan     |                 nan     |                 -0.256 |          nan     |                 nan     |                  9.417 |      -0.049 |       1.852 |
| all companies | post-earnings drift 20d | +           |    30533 |                     1 |          nan     |                 nan     |                 14.17  |          nan     |                 nan     |                 16.934 |       1.813 |       2.332 |

### High frequency: the reaction day, from 10:00 to the close

Does the first half hour's move after a release continue or reverse? Entry at 10:00 pays the half-spread (x1, and x2 because spreads widen on earnings days) plus 0.5 bp; exit in the closing auction.

| universe      |   period | strategy                |   events |   ic_first30_vs_rest |   gross_bp |   net_bp_spread_x1 |   net_bp_spread_x2 |   t_gross |
|:--------------|---------:|:------------------------|---------:|---------------------:|-----------:|-------------------:|-------------------:|----------:|
| consumer      |  2016_20 | follow the first 30 min |     2038 |               -0.007 |     -1.472 |             -7.725 |            -13.478 |    -0.214 |
| consumer      |  2016_20 | fade the first 30 min   |     2038 |               -0.007 |      1.472 |             -4.78  |            -10.533 |     0.214 |
| consumer      |  2021_26 | follow the first 30 min |     2371 |               -0.003 |     -4.751 |            -10.299 |            -15.346 |    -0.771 |
| consumer      |  2021_26 | fade the first 30 min   |     2371 |               -0.003 |      4.751 |             -0.796 |             -5.843 |     0.771 |
| all companies |  2016_20 | follow the first 30 min |    13772 |               -0.018 |     -1.255 |             -8.825 |            -15.895 |    -0.5   |
| all companies |  2016_20 | fade the first 30 min   |    13772 |               -0.018 |      1.255 |             -6.315 |            -13.385 |     0.5   |
| all companies |  2021_26 | follow the first 30 min |    16383 |                0.005 |      2.669 |             -3.764 |             -9.697 |     1.14  |
| all companies |  2021_26 | fade the first 30 min   |    16383 |                0.005 |     -2.669 |             -9.102 |            -15.036 |    -1.14  |

