## Momentum flip (Nico's research_night): independent check

Same rule rebuilt on this repository's pipeline: momentum composite (mom_12_1, resid_mom, high_52w), 21-day rebalance staggered over all start days, short when the VIX (FRED, one-day publication lag) is above 20 at the rebalance, measured costs. Nico reported net Sharpe 0.67 / 0.74 / 0.22 (2006-14 / 2015-20 / 2021-26).

| variant                                |   sharpe_2006-14 |   sharpe_2015-20 |   sharpe_2021-26 |   sharpe_2017-26 |   return_2015_26 |   max_dd_2015_26 |
|:---------------------------------------|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|
| momentum flip, VIX 20 (staggered, net) |            0.671 |            0.74  |            0.232 |            0.498 |            0.037 |           -0.11  |
| gross (no costs)                       |            0.774 |            0.809 |            0.332 |            0.573 |            0.043 |           -0.11  |
| plain momentum, never flipped          |           -0.481 |           -0.25  |           -0.119 |           -0.189 |           -0.015 |           -0.349 |
| always short momentum                  |            0.355 |            0.172 |            0.035 |            0.113 |            0.009 |           -0.172 |
| threshold 16                           |            0.275 |            0.729 |            0.198 |            0.507 |            0.036 |           -0.129 |
| threshold 18                           |            0.459 |            0.763 |            0.12  |            0.466 |            0.034 |           -0.11  |
| threshold 22                           |            0.641 |            0.62  |            0.064 |            0.389 |            0.028 |           -0.11  |
| threshold 25                           |            0.47  |            0.456 |           -0.01  |            0.3   |            0.018 |           -0.115 |
| threshold 30                           |            0.247 |            0.162 |           -0.015 |            0.145 |            0.005 |           -0.168 |

### Survivorship: point-in-time universe with delisted stocks (2017-26, before costs)

Close-only signals (12-1 momentum + 52-week high) on both universes, same dates, so only the universe differs.

| universe                     | book           |   gross_sharpe_2017_26 |   gross_return_2017_26 |   gross_sharpe_2017_20 |   gross_sharpe_2021_26 |
|:-----------------------------|:---------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| survivors (today's universe) | flip VIX 20    |                  0.465 |                  0.035 |                  0.718 |                  0.244 |
| survivors (today's universe) | plain momentum |                 -0.241 |                 -0.021 |                 -0.337 |                 -0.166 |
| point-in-time incl. delisted | flip VIX 20    |                  0.525 |                  0.047 |                  0.656 |                  0.438 |
| point-in-time incl. delisted | plain momentum |                  0.282 |                  0.028 |                  0.082 |                  0.404 |

