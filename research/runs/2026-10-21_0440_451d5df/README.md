# Research results

## Events: news types, novelty and index changes

### After each kind of news (market-relative, from the first open after the article)

t-stats average same-day events first, since they move together.

| event                |   events |   car_1d_bp |   t_1d |   car_5d_bp |   t_5d |   car_21d_bp |   t_21d |
|:---------------------|---------:|------------:|-------:|------------:|-------:|-------------:|--------:|
| buyback              |     4157 |       33.33 |   6.62 |       35.05 |   4.18 |        37    |    2.64 |
| analyst upgrade      |    38232 |        4.51 |   3.18 |        8.43 |   2.71 |        10.75 |    1.69 |
| merger / acquisition |    24644 |       -0.37 |  -0.21 |       -9.89 |  -2.55 |       -22.31 |   -3.19 |
| CEO change           |      581 |      -38.18 |  -2.82 |      -35.58 |  -1.49 |       -10.81 |   -0.26 |
| earnings beat        |    31192 |       -3.99 |  -0.93 |      -10.03 |  -1.42 |        -5.77 |   -0.52 |
| dividend raise       |     1886 |       17.8  |   3.18 |       14.19 |   1.36 |       -17.75 |   -0.99 |
| guidance raised      |      741 |       -8.82 |  -0.64 |      -23.34 |  -1.08 |       -58.83 |   -1.73 |
| lawsuit / probe      |     4502 |       -3.18 |  -0.74 |       13.69 |   1.08 |        76.42 |    3.62 |
| price target cut     |    41547 |       -0.7  |  -0.33 |        3.81 |   0.91 |        -0.12 |   -0.02 |
| guidance cut         |      296 |      -23.72 |  -0.79 |       30.38 |   0.75 |       -10.09 |   -0.13 |
| FDA / trial          |    10512 |       -1.5  |  -0.47 |       -4.02 |  -0.59 |       -13.36 |   -1.01 |
| share offering       |     4141 |       -7.2  |  -1.5  |        5.82 |   0.53 |        -1.43 |   -0.08 |
| price target raised  |    60860 |        1.54 |   0.83 |        0.92 |   0.24 |        -9.78 |   -1.39 |
| earnings miss        |    14292 |        1.22 |   0.2  |       -1.71 |  -0.17 |        12.96 |    0.88 |
| analyst downgrade    |    37199 |        0.66 |   0.36 |       -0.2  |  -0.05 |         1.16 |    0.17 |

### Novel vs. stale news: does the move continue?

continuation = return in the direction of the stock's move into the open after the news (positive = it keeps going, negative = it reverses).

| news                  |   horizon |   continuation_bp |     t |   days |
|:----------------------|----------:|------------------:|------:|-------:|
| novel (overlap < 30%) |         1 |             -1.15 | -1.98 |   2970 |
| novel (overlap < 30%) |         5 |             -2.06 | -1.47 |   2970 |
| novel (overlap < 30%) |        21 |             -4.57 | -1.71 |   2970 |
| stale (overlap > 70%) |         1 |             -4.53 | -2.2  |   2268 |
| stale (overlap > 70%) |         5 |             -6.29 | -1.34 |   2268 |
| stale (overlap > 70%) |        21 |            -22.4  | -2.64 |   2268 |


## Survivorship bias, signal by signal

14736 US stocks from Alpaca since 2016, 1954 of them no longer trading. Point-in-time universe: top 1,000 by dollar volume at each month end. Same signals, same dates (mid-2017 on), close-to-close.

|                             |   point-in-time (incl. delisted) |   survivors (current method) |   bias (survivor - pit) |
|:----------------------------|---------------------------------:|-----------------------------:|------------------------:|
| amihud (5d)                 |                          -0.011  |                       0.0029 |                  0.0139 |
| amihud (21d)                |                          -0.0241 |                       0.0148 |                  0.0389 |
| low_vol (5d)                |                           0.008  |                      -0.009  |                 -0.017  |
| low_vol (21d)               |                           0.0197 |                      -0.0214 |                 -0.0411 |
| max_effect (5d)             |                           0.0062 |                      -0.0037 |                 -0.0099 |
| max_effect (21d)            |                           0.0171 |                      -0.0111 |                 -0.0283 |
| mom_12_1 (5d)               |                           0.0272 |                       0.0102 |                 -0.017  |
| mom_12_1 (21d)              |                           0.0345 |                       0.0051 |                 -0.0295 |
| rev_1d (5d)                 |                           0.0109 |                       0.0123 |                  0.0014 |
| rev_1d (21d)                |                           0.0036 |                       0.0098 |                  0.0062 |
| rev_21d (5d)                |                           0.0052 |                       0.0159 |                  0.0107 |
| rev_21d (21d)               |                           0.0032 |                       0.0207 |                  0.0175 |
| rev_5d (5d)                 |                           0.0147 |                       0.0163 |                  0.0016 |
| rev_5d (21d)                |                           0.0048 |                       0.0148 |                  0.01   |
| size_proxy (illiquid) (5d)  |                          -0.0081 |                       0.0003 |                  0.0084 |
| size_proxy (illiquid) (21d) |                          -0.015  |                       0.0095 |                  0.0245 |

A large positive bias means the signal looks better on today's survivors than it would have been in real time.

