## News and media vs stock moves: correlation scan

Every collected news / media dataset turned into per-stock daily features (dated by the first open after the information was public) and correlated with the stocks' moves (relative to the average stock); market-wide news themes against ETF returns. A = 2016/17-2021, B = 2022-2026. 'weaker half t' = the smaller |t| of the two halves (same sign required).

### Data collected

(no media data yet)

### Per-stock features

420 feature-target pairs. |t| > 2 over the whole period: 139 (about 21 expected by luck). Same sign and |t| > 2 in both halves: 98 (about 0.5 expected by luck).

#### Predict the next move (tradable)

| source             | feature                        | target   |   names_per_day |    ic_A |     t_A |    ic_B |     t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:-------------------------------|:---------|----------------:|--------:|--------:|--------:|--------:|--------------:|--------------:|----------------:|
| benzinga_headlines | headline:buyback               | intraday |             0.7 |  0.006  |  5.1726 |  0.0045 |  3.3799 |       27.5383 |       25.8983 |          3.3799 |
| benzinga_headlines | headline:ceo_change            | intraday |             0.2 | -0.0053 | -3.3314 | -0.0079 | -4.425  |      -27.5231 |      -36.9915 |          3.3314 |
| benzinga_headlines | headline:ceo_change            | next_1d  |             0.2 | -0.0052 | -3.3137 | -0.0085 | -4.7542 |      -35.4094 |      -44.8853 |          3.3137 |
| benzinga_headlines | headline:buyback               | next_1d  |             0.7 |  0.0051 |  4.4419 |  0.0035 |  2.7128 |       24.9016 |       23.728  |          2.7128 |
| benzinga_headlines | headline:buyback:last_5d       | intraday |             3.3 |  0.0024 |  2.6442 |  0.0033 |  3.0138 |        7.833  |        9.9082 |          2.6442 |
| benzinga_headlines | headline:dividend_up           | next_1d  |             0.3 |  0.0034 |  2.1685 |  0.0032 |  2.2501 |        9.4588 |       18.6134 |          2.1685 |
| benzinga_headlines | headline:deal:last_5d          | intraday |            17.4 | -0.002  | -2.0087 | -0.0025 | -2.0515 |       -1.1708 |       -2.0439 |          2.0087 |
| benzinga_headlines | headline:dividend_up           | intraday |             0.3 |  0.0032 |  1.9693 |  0.004  |  2.8988 |        8.7293 |       18.9199 |          1.9693 |
| benzinga_headlines | headline:deal:last_5d          | next_1d  |            17.4 | -0.0018 | -1.8316 | -0.0021 | -1.7747 |       -1.0549 |       -2.117  |          1.7747 |
| benzinga_headlines | headline:halt                  | next_1d  |             0.2 | -0.0037 | -1.9204 | -0.0034 | -1.6416 |      -33.856  |      -21.7851 |          1.6416 |
| benzinga_headlines | headline:ceo_change:last_5d    | intraday |             1.1 | -0.0015 | -1.597  | -0.0026 | -2.2871 |       -5.7024 |      -11.4841 |          1.597  |
| benzinga_headlines | headline:ceo_change:last_5d    | next_1d  |             1.1 | -0.0014 | -1.4675 | -0.0025 | -2.2301 |       -5.4894 |      -11.4828 |          1.4675 |
| benzinga_headlines | headline:buyback:last_5d       | next_1d  |             3.3 |  0.0018 |  1.9787 |  0.0015 |  1.408  |        7.336  |        6.896  |          1.408  |
| wikipedia          | wiki_views:abnormal            | next_1d  |           144   |  0.0013 |  1.3512 |  0.0026 |  2.1935 |       -0.11   |        2.5464 |          1.3512 |
| wikipedia          | wiki_views:abnormal_5d         | next_1d  |           143.8 |  0.0016 |  1.6115 |  0.0014 |  1.2131 |        0.8053 |        1.3837 |          1.2131 |
| benzinga_headlines | headline:offering:last_5d      | intraday |             2.6 | -0.0016 | -1.7896 | -0.0012 | -1.1847 |       -2.5169 |       -1.8107 |          1.1847 |
| benzinga_headlines | headline:halt                  | intraday |             0.2 | -0.0041 | -2.1522 | -0.0024 | -1.1558 |      -30.1233 |      -10.1773 |          1.1558 |
| benzinga           | benzinga_solo_articles:level   | next_1d  |            49.7 |  0.0014 |  1.2447 |  0.0019 |  1.1427 |      nan      |      nan      |          1.1427 |
| benzinga_headlines | headline:options_activity      | next_1d  |             2.2 | -0.0021 | -1.9836 | -0.0013 | -1.0477 |       -0.4275 |        1.3718 |          1.0477 |
| benzinga_headlines | headline:pt_cut:last_5d        | next_1d  |            25.2 | -0.0014 | -1.1444 | -0.0019 | -0.9953 |       -1.202  |       -0.8794 |          0.9953 |
| benzinga_headlines | headline:miss:last_5d          | next_1d  |             9.9 | -0.0017 | -1.6717 | -0.0012 | -0.9868 |        1.5001 |       -3.2266 |          0.9868 |
| benzinga           | benzinga_solo_articles:spike   | next_1d  |            35   |  0.001  |  0.9772 |  0.0016 |  1.2389 |        0.9686 |        1.4602 |          0.9772 |
| benzinga_headlines | headline:buyback               | next_5d  |             0.7 |  0.0032 |  1.3297 |  0.0026 |  0.9719 |       42.7469 |       30.0597 |          0.9719 |
| benzinga_headlines | headline:lawsuit:last_5d       | next_5d  |             1.8 |  0.0034 |  1.4899 |  0.0025 |  0.8841 |       25.0641 |       10.0667 |          0.8841 |
| benzinga_headlines | headline:investigation:last_5d | next_5d  |             1.8 |  0.0019 |  0.848  |  0.0038 |  1.4463 |        3.4743 |       15.1703 |          0.848  |

#### Predict the size of the next move (volatility)

| source             | feature                            | target      |   names_per_day |    ic_A |      t_A |    ic_B |      t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:-----------------------------------|:------------|----------------:|--------:|---------:|--------:|---------:|--------------:|--------------:|----------------:|
| benzinga           | benzinga_articles:spike            | abs_next_1d |            40   |  0.0607 |  42.4928 |  0.0622 |  33.572  |       44.9453 |       48.6474 |         33.572  |
| benzinga           | benzinga_solo_articles:spike       | abs_next_1d |            35   |  0.0565 |  42.07   |  0.0535 |  30.9812 |       43.5025 |       41.9969 |         30.9812 |
| benzinga_headlines | headline:beat                      | abs_next_1d |             4.6 |  0.0425 |  30.7885 |  0.0656 |  35.4768 |      104.08   |      150.942  |         30.7885 |
| benzinga           | benzinga_articles:level            | abs_next_1d |            77.1 |  0.0501 |  33.5766 |  0.0584 |  29.4519 |      218.677  |      nan      |         29.4519 |
| benzinga           | benzinga_solo_articles:level       | abs_next_1d |            49.7 |  0.0537 |  39.1761 |  0.0502 |  27.683  |      nan      |      nan      |         27.683  |
| benzinga_headlines | headline:miss                      | abs_next_1d |             2.1 |  0.0371 |  27.6606 |  0.0505 |  32.0209 |      126.332  |      168.575  |         27.6606 |
| benzinga_headlines | headline:beat:last_5d              | abs_next_1d |            21.4 |  0.0282 |  25.8414 |  0.0482 |  31.9683 |       33.821  |       48.4409 |         25.8414 |
| benzinga_headlines | headline:miss:last_5d              | abs_next_1d |             9.9 |  0.025  |  24.1306 |  0.0339 |  27.6503 |       44.9913 |       50.6337 |         24.1306 |
| benzinga           | benzinga_solo_articles:abnormal    | abs_next_1d |           389.3 |  0.0371 |  25.3251 |  0.0425 |  22.481  |       22.5896 |       28.1983 |         22.481  |
| benzinga           | benzinga_articles:abnormal         | abs_next_1d |           393   |  0.0343 |  24.1455 |  0.0418 |  21.8209 |       24.789  |       32.1859 |         21.8209 |
| benzinga           | benzinga_articles:abnormal_5d      | abs_next_1d |           390   |  0.0335 |  27.9222 |  0.0336 |  21.2975 |       18.9668 |       21.6134 |         21.2975 |
| benzinga           | benzinga_solo_articles:abnormal_5d | abs_next_1d |           387.4 |  0.0367 |  31.6146 |  0.0291 |  18.8984 |       18.8059 |       18.5846 |         18.8984 |
| benzinga_headlines | headline:guidance_up               | abs_next_1d |             0.6 |  0.0298 |  20.0514 |  0.0344 |  18.7854 |      120.036  |      152.437  |         18.7854 |
| benzinga_headlines | headline:guidance_down             | abs_next_1d |             0.2 |  0.0309 |  16.8856 |  0.034  |  18.8892 |      188.223  |      217.839  |         16.8856 |
| benzinga_headlines | headline:pt_cut                    | abs_next_1d |             6.3 |  0.0168 |  15.934  |  0.0215 |  17.139  |       43.3686 |       26.8205 |         15.934  |
| benzinga_headlines | headline:pt_cut:last_5d            | abs_next_1d |            25.2 |  0.0163 |  15.2301 |  0.02   |  13.4074 |       20.0414 |       10.6732 |         13.4074 |
| wikipedia          | wiki_views:level                   | abs_next_1d |           143.2 | -0.0247 | -26.6081 | -0.0149 | -12.7717 |      nan      |      nan      |         12.7717 |
| benzinga_headlines | headline:buyback                   | abs_next_1d |             0.7 |  0.0132 |  12.6451 |  0.0152 |  12.9873 |       54.6411 |       68.0031 |         12.6451 |
| benzinga_headlines | headline:guidance_down:last_5d     | abs_next_1d |             1.1 |  0.0137 |  12.0283 |  0.0197 |  16.2257 |       55.2076 |       74.403  |         12.0283 |
| benzinga_headlines | headline:new_low:last_5d           | abs_next_1d |             5.7 |  0.0183 |  13.5683 |  0.0237 |  11.7002 |       39.0216 |       38.0193 |         11.7002 |
| benzinga_headlines | headline:downgrade                 | abs_next_1d |             5.5 |  0.0172 |  18.8351 |  0.0125 |  11.6965 |       28.9352 |       28.9841 |         11.6965 |
| benzinga_headlines | headline:halt:last_5d              | abs_next_1d |             1.1 |  0.0105 |  10.0423 |  0.0119 |  10.1617 |       72.1321 |       64.9338 |         10.0423 |
| benzinga_headlines | headline:guidance_up:last_5d       | abs_next_1d |             3   |  0.01   |   9.8592 |  0.0129 |  10.9232 |       26.4866 |       32.4032 |          9.8592 |
| benzinga_headlines | headline:short_report:last_5d      | abs_next_1d |             0.5 |  0.0137 |   9.8342 |  0.0173 |  11.9265 |       87.6977 |      110.479  |          9.8342 |
| wikipedia          | wiki_views:abnormal                | abs_next_1d |           144   |  0.0138 |  14.6076 |  0.0107 |   9.5014 |        8.0274 |       12.1489 |          9.5014 |

#### Move together with the news (same window: descriptive, not tradable)

| source             | feature                      | target   |   names_per_day |    ic_A |      t_A |    ic_B |      t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:-----------------------------|:---------|----------------:|--------:|---------:|--------:|---------:|--------------:|--------------:|----------------:|
| benzinga           | benzinga:tone                | past_1d  |            30.3 |  0.1698 |  64.5857 |  0.1283 |  42.5224 |      165.991  |      133.32   |         42.5224 |
| benzinga_headlines | headline:upgrade             | past_1d  |             5.6 |  0.0346 |  31.2581 |  0.0378 |  31.7726 |       71.1815 |      107.115  |         31.2581 |
| benzinga_headlines | headline:downgrade           | past_1d  |             5.5 | -0.0323 | -27.3877 | -0.0321 | -25.2291 |      -72.6494 |     -109.827  |         25.2291 |
| benzinga           | benzinga:tone_change         | past_1d  |            32.4 |  0.0943 |  25.5099 |  0.0786 |  22.008  |       66.2775 |       67.9841 |         22.008  |
| benzinga_headlines | headline:pt_raised           | past_1d  |             9.2 |  0.0314 |  26.8096 |  0.0316 |  20.8219 |       91.7278 |       54.6579 |         20.8219 |
| benzinga_headlines | headline:pt_cut              | past_1d  |             6.3 | -0.0342 | -29.653  | -0.0284 | -18.9859 |     -145.53   |      -58.2788 |         18.9859 |
| benzinga_headlines | headline:miss                | past_1d  |             2.1 | -0.0252 | -17.5035 | -0.0307 | -19.159  |     -157.969  |     -183.675  |         17.5035 |
| benzinga_headlines | headline:deal                | past_1d  |             3.9 |  0.0246 |  24.8726 |  0.0178 |  15.2605 |       56.0799 |       50.1364 |         15.2605 |
| benzinga_headlines | headline:upgrade:last_5d     | past_1d  |            22.7 |  0.0171 |  16.1061 |  0.0163 |  13.8881 |       18.0992 |       21.9855 |         13.8881 |
| benzinga_headlines | headline:buyback             | past_1d  |             0.7 |  0.0155 |  12.8844 |  0.0214 |  15.9698 |       62.7212 |      106.774  |         12.8844 |
| benzinga_headlines | headline:downgrade:last_5d   | past_1d  |            22.1 | -0.0158 | -14.4675 | -0.0152 | -12.4252 |      -16.376  |      -24.8126 |         12.4252 |
| benzinga_headlines | headline:guidance_down       | past_1d  |             0.2 | -0.0299 | -13.9396 | -0.0275 | -12.1933 |     -331.817  |     -350.156  |         12.1933 |
| benzinga_headlines | headline:guidance_up         | past_1d  |             0.6 |  0.0227 |  13.5578 |  0.0231 |  11.3286 |      166.103  |      174.05   |         11.3286 |
| benzinga_headlines | headline:new_low             | past_1d  |             1.6 | -0.0252 | -11.4046 | -0.0357 | -10.9345 |      -96.7943 |     -126.748  |         10.9345 |
| benzinga_headlines | headline:beat                | past_1d  |             4.6 |  0.0162 |  12.0888 |  0.016  |  10.6534 |       65.933  |       60.2893 |         10.6534 |
| benzinga_headlines | headline:miss:last_5d        | past_1d  |             9.9 | -0.01   |  -9.1249 | -0.0129 | -10      |      -32.0727 |      -41.5047 |          9.1249 |
| benzinga           | benzinga_solo_articles:spike | past_1d  |            35   |  0.0135 |  12.4516 |  0.0115 |   8.8589 |        9.4718 |        7.9551 |          8.8589 |
| benzinga           | benzinga_articles:spike      | past_1d  |            40   |  0.0161 |  13.6504 |  0.0109 |   8.3339 |       10.7172 |        9.3049 |          8.3339 |
| benzinga_headlines | headline:buyback:last_5d     | past_1d  |             3.3 |  0.0072 |   7.4566 |  0.0095 |   8.4887 |       18.8853 |       26.1154 |          7.4566 |
| benzinga           | benzinga_solo_articles:level | past_1d  |            49.7 |  0.014  |  11.8972 |  0.0125 |   7.4227 |      nan      |      nan      |          7.4227 |
| benzinga_headlines | headline:pt_raised:last_5d   | past_1d  |            36.5 |  0.0143 |  11.0882 |  0.0151 |   7.3792 |       23.0344 |       11.7708 |          7.3792 |
| benzinga_headlines | headline:pt_cut:last_5d      | past_1d  |            25.2 | -0.0149 | -12.0373 | -0.0138 |  -7.1684 |      -34.0626 |      -13.7612 |          7.1684 |
| benzinga           | benzinga_articles:level      | past_1d  |            77.1 |  0.0172 |  11.6594 |  0.0128 |   6.7284 |       -9.5248 |      nan      |          6.7284 |
| benzinga_headlines | headline:new_high            | past_1d  |             3.7 |  0.0306 |  15.6554 |  0.013  |   6.6589 |       73.5652 |       71.4984 |          6.6589 |
| benzinga_headlines | headline:offering            | past_1d  |             0.6 | -0.0115 |  -9.1252 | -0.0083 |  -6.3692 |      -80.588  |      -59.5669 |          6.3692 |

### Market-wide news themes vs ETFs

71 theme-asset-horizon pairs; same sign and |t| > 2 in both halves: 0 (about 0.1 expected by luck).

#### Predictive (from the next close on)

| feature               | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:----------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| benzinga:all_articles | USO     | next_1d   |  -0.0396 | -1.6061 |  -0.0139 | -0.4838 |          0.4838 |
| benzinga:all_articles | XLY     | next_20d  |  -0.0618 | -0.5594 |  -0.0609 | -0.4685 |          0.4685 |
| benzinga:all_articles | GLD     | next_20d  |  -0.0818 | -0.7407 |  -0.058  | -0.4466 |          0.4466 |
| benzinga:all_articles | UUP     | next_1d   |   0.0442 |  1.7894 |   0.0111 |  0.3836 |          0.3836 |
| benzinga:all_articles | HYG     | next_1d   |  -0.0405 | -1.6418 |  -0.0109 | -0.3795 |          0.3795 |
| benzinga:all_articles | GLD     | next_1d   |  -0.0225 | -0.9099 |  -0.0075 | -0.2586 |          0.2586 |
| benzinga:all_articles | TLT     | next_1d   |  -0.0057 | -0.2321 |  -0.0072 | -0.2503 |          0.2321 |
| benzinga:all_articles | HYG     | next_20d  |  -0.0521 | -0.4721 |  -0.0287 | -0.2209 |          0.2209 |
| benzinga:all_articles | IWM     | next_1d   |   0.0047 |  0.1915 |   0.0163 |  0.5643 |          0.1915 |
| benzinga:all_articles | TLT     | next_20d  |   0.0208 |  0.188  |   0.0645 |  0.4968 |          0.188  |
| benzinga:all_articles | XLV     | next_5d   |  -0.0168 | -0.3037 |  -0.0114 | -0.1767 |          0.1767 |
| benzinga:all_articles | ^VIX    | next_1d   |   0.0173 |  0.7017 |   0.0043 |  0.1502 |          0.1502 |
| benzinga:all_articles | XLB     | next_20d  |   0.0381 |  0.3455 |   0.0171 |  0.1319 |          0.1319 |
| benzinga:all_articles | XLI     | next_20d  |   0.025  |  0.2266 |   0.0165 |  0.1271 |          0.1271 |
| benzinga:all_articles | HYG     | next_5d   |  -0.0669 | -1.2119 |  -0.0041 | -0.0633 |          0.0633 |
| benzinga:all_articles | UUP     | next_20d  |   0.0717 |  0.6495 |   0.0072 |  0.0556 |          0.0556 |
| benzinga:all_articles | USO     | next_5d   |  -0.0658 | -1.1919 |  -0.0016 | -0.0251 |          0.0251 |
| benzinga:all_articles | SPY     | next_20d  |  -0.0071 | -0.0639 |  -0.0026 | -0.0198 |          0.0198 |
| benzinga:all_articles | QQQ     | next_20d  |  -0.0342 | -0.3094 |  -0.0026 | -0.0197 |          0.0197 |
| benzinga:all_articles | GLD     | next_5d   |  -0.0486 | -0.8806 |  -0.0005 | -0.0072 |          0.0072 |

#### Same day (descriptive)

| feature               | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:----------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| benzinga:all_articles | ^VIX    | same_day  |  -0.0082 | -0.3304 |  -0.0247 | -0.8581 |          0.3304 |

