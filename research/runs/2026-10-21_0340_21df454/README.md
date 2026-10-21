# Research results

## Events: news types, novelty and index changes

### After each kind of news (market-relative, from the first open after the article)

t-stats average same-day events first, since they move together.

| event                |   events |   car_1d_bp |   t_1d |   car_5d_bp |   t_5d |   car_21d_bp |   t_21d |
|:---------------------|---------:|------------:|-------:|------------:|-------:|-------------:|--------:|
| analyst upgrade      |    38232 |       76.68 |  31.75 |       80.6  |  22.01 |        82.91 |   12.29 |
| analyst downgrade    |    37199 |      -80.07 | -27.18 |      -80.93 | -18.4  |       -79.57 |  -11.02 |
| earnings miss        |    14292 |     -160.02 | -17.06 |     -162.96 | -13.53 |      -148.29 |   -9.09 |
| merger / acquisition |    24644 |       53.47 |  20.06 |       43.95 |  11.16 |        31.52 |    4.41 |
| price target cut     |    41547 |      -61.31 | -15.94 |      -56.79 | -11.05 |       -60.73 |   -6.91 |
| buyback              |     4157 |      106.76 |  12.31 |      108.49 |  10    |       110.44 |    7.16 |
| price target raised  |    60860 |       43.79 |  12.52 |       43.17 |   8.74 |        32.47 |    4.32 |
| earnings beat        |    31192 |       60.41 |   8.61 |       54.36 |   6.08 |        58.63 |    4.76 |
| share offering       |     4141 |      -77.2  | -10.55 |      -64.19 |  -5.22 |       -71.43 |   -3.74 |
| guidance raised      |      741 |      159.83 |   6.77 |      145.31 |   5.13 |       109.81 |    2.77 |
| dividend raise       |     1886 |       54.11 |   6.24 |       50.5  |   4.01 |        18.56 |    0.97 |
| guidance cut         |      296 |     -243.77 |  -5.31 |     -189.67 |  -3.66 |      -230.15 |   -2.71 |
| CEO change           |      581 |     -102.14 |  -4.3  |      -99.54 |  -3.2  |       -74.77 |   -1.77 |
| FDA / trial          |    10512 |        8.75 |   1.61 |        6.24 |   0.79 |        -3.11 |   -0.22 |
| lawsuit / probe      |     4502 |      -12.08 |  -1.99 |        4.8  |   0.37 |        67.52 |    3.14 |

### Novel vs. stale news: does the move continue?

continuation = return in the direction of the stock's move into the open after the news (positive = it keeps going, negative = it reverses).

| news                  |   horizon |   continuation_bp |     t |   days |
|:----------------------|----------:|------------------:|------:|-------:|
| novel (overlap < 30%) |         1 |             -0.45 | -0.56 |   2970 |
| novel (overlap < 30%) |         5 |             -1.87 | -1.19 |   2970 |
| novel (overlap < 30%) |        21 |             -7.3  | -2.68 |   2970 |
| stale (overlap > 70%) |         1 |              0.46 |  0.22 |   2268 |
| stale (overlap > 70%) |         5 |             -5.64 | -1.19 |   2268 |
| stale (overlap > 70%) |        21 |              4.87 |  0.57 |   2268 |

