## News and media vs stock moves: correlation scan

Every collected news / media dataset turned into per-stock daily features (dated by the first open after the information was public) and correlated with the stocks' moves (relative to the average stock); market-wide news themes against ETF returns. A = 2016/17-2021, B = 2022-2026. 'weaker half t' = the smaller |t| of the two halves (same sign required).

### Data collected

| dataset                      |    rows |   columns | first      | last       |   megabytes |
|:-----------------------------|--------:|----------:|:-----------|:-----------|------------:|
| gdelt_company_timelinevolraw |    3543 |       333 | 2017-01-01 | 2026-10-24 |         1.6 |
| gdelt_theme_timelinetone     |    3543 |        91 | 2017-01-01 | 2026-10-24 |         2.2 |
| gdelt_theme_timelinevolraw   |    3543 |        92 | 2017-01-01 | 2026-10-24 |         1.1 |
| gdelt_total_articles         |    3541 |         1 | 2017-01-01 | 2026-10-22 |         0.1 |
| hn_stories                   |  538374 |         6 |            |            |        35.6 |
| sec_filings                  | 1709772 |         4 |            |            |        23.5 |
| sec_phrase_hits              |  487004 |         6 |            |            |         6.3 |
| tv_theme_timelinevol         |    2841 |        92 | 2017-01-01 | 2024-10-11 |         1.5 |
| wiki_extra_pageviews         |    4131 |       137 | 2015-07-01 | 2026-10-21 |         0.8 |

### Per-stock features

1224 feature-target pairs. |t| > 2 over the whole period: 351 (about 61 expected by luck). Same sign and |t| > 2 in both halves: 191 (about 1.6 expected by luck).

#### Predict the next move (tradable)

| source             | feature                          | target   |   names_per_day |    ic_A |     t_A |    ic_B |     t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:---------------------------------|:---------|----------------:|--------:|--------:|--------:|--------:|--------------:|--------------:|----------------:|
| benzinga_headlines | headline:buyback                 | intraday |             0.7 |  0.006  |  5.1725 |  0.0045 |  3.3799 |       27.5383 |       25.8983 |          3.3799 |
| benzinga_headlines | headline:ceo_change              | intraday |             0.2 | -0.0053 | -3.3313 | -0.0079 | -4.425  |      -27.5231 |      -36.9915 |          3.3313 |
| benzinga_headlines | headline:ceo_change              | next_1d  |             0.2 | -0.0052 | -3.3132 | -0.0085 | -4.7549 |      -35.4096 |      -44.8852 |          3.3132 |
| sec_filings        | sec_10q                          | next_1d  |             5.2 | -0.0033 | -3.2717 | -0.0046 | -3.4779 |       -7.1621 |      -12.5869 |          3.2717 |
| sec_filings        | sec_10q                          | intraday |             5.2 | -0.0028 | -2.7684 | -0.0048 | -3.5911 |       -6.1467 |       -9.2526 |          2.7684 |
| benzinga_headlines | headline:buyback                 | next_1d  |             0.7 |  0.0051 |  4.4403 |  0.0035 |  2.7062 |       24.9016 |       23.6227 |          2.7062 |
| benzinga_headlines | headline:buyback:last_5d         | intraday |             3.3 |  0.0024 |  2.6442 |  0.0033 |  3.021  |        7.833  |        9.9198 |          2.6442 |
| sec_filings        | sec_8k_5.02                      | intraday |             4.3 | -0.0018 | -2.2914 | -0.007  | -7.1043 |       -2.5742 |      -12.9967 |          2.2914 |
| sec_phrases        | 8k_says:tender offer:last_5d     | intraday |             3.6 | -0.0024 | -2.7282 | -0.0022 | -2.2818 |       -2.805  |       -2.7698 |          2.2818 |
| sec_filings        | sec_8k_5.02                      | next_1d  |             4.3 | -0.0017 | -2.1995 | -0.0062 | -6.422  |       -3.0311 |      -13.2729 |          2.1995 |
| benzinga_headlines | headline:dividend_up             | next_1d  |             0.3 |  0.0034 |  2.1674 |  0.0032 |  2.2501 |        9.4589 |       18.6133 |          2.1674 |
| benzinga_headlines | headline:deal:last_5d            | intraday |            17.4 | -0.002  | -2.0087 | -0.0025 | -2.1026 |       -1.1708 |       -2.0747 |          2.0087 |
| sec_phrases        | 8k_says:merger agreement:last_5d | intraday |             2.7 | -0.0019 | -2.0035 | -0.0041 | -4.2591 |       -2.4477 |       -8.6295 |          2.0035 |
| benzinga_headlines | headline:dividend_up             | intraday |             0.3 |  0.0032 |  1.9693 |  0.004  |  2.8701 |        8.7293 |       18.7751 |          1.9693 |
| sec_phrases        | 8k_says:merger agreement:last_5d | next_5d  |             2.7 | -0.0045 | -2.2004 | -0.004  | -1.937  |      -16.1188 |      -16.8317 |          1.937  |
| sec_filings        | sec_form144                      | next_1d  |             4.7 | -0.0031 | -1.8996 | -0.0051 | -3.7432 |       -5.064  |       -7.2552 |          1.8996 |
| sec_phrases        | 8k_says:merger agreement:last_5d | next_1d  |             2.7 | -0.0017 | -1.8468 | -0.0032 | -3.3331 |       -2.6201 |       -7.509  |          1.8468 |
| gdelt_news         | gdelt_news:level                 | next_20d |           102.5 |  0.0235 |  1.9492 |  0.0207 |  1.8035 |      nan      |      nan      |          1.8035 |
| gdelt_news         | gdelt_news:level                 | next_5d  |           102.5 |  0.0148 |  2.3575 |  0.0115 |  1.7994 |      nan      |      nan      |          1.7994 |
| sec_phrases        | 8k_says:tariffs:last_5d          | intraday |             7.5 | -0.0018 | -1.7972 | -0.0022 | -2.0354 |       -0.5976 |       -1.1342 |          1.7972 |
| benzinga_headlines | headline:deal:last_5d            | next_1d  |            17.4 | -0.0018 | -1.8332 | -0.0022 | -1.7895 |       -1.0549 |       -2.1381 |          1.7895 |
| gdelt_news         | gdelt_news:level                 | intraday |           102.5 |  0.0052 |  1.7659 |  0.006  |  2.0857 |      nan      |      nan      |          1.7659 |
| sec_phrases        | 8k_says:tariffs                  | intraday |             1.5 | -0.0031 | -2.387  | -0.0021 | -1.704  |       -0.9266 |       -4.6052 |          1.704  |
| gdelt_news         | gdelt_news:abnormal_5d           | next_20d |           115.4 | -0.0111 | -1.7033 | -0.0108 | -1.8127 |      -11.314  |      -14.8913 |          1.7033 |
| sec_phrases        | 8k_says:work stoppage:last_5d    | intraday |             0.9 | -0.0017 | -1.6627 | -0.0036 | -3.2773 |       -5.4836 |      -17.1152 |          1.6627 |

#### Predict the size of the next move (volatility)

| source             | feature                            | target      |   names_per_day |    ic_A |      t_A |    ic_B |      t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:-----------------------------------|:------------|----------------:|--------:|---------:|--------:|---------:|--------------:|--------------:|----------------:|
| benzinga           | benzinga_articles:spike            | abs_next_1d |            40   |  0.0607 |  42.4927 |  0.0621 |  33.5802 |       44.9453 |       48.6285 |         33.5802 |
| benzinga           | benzinga_solo_articles:spike       | abs_next_1d |            35   |  0.0565 |  42.0706 |  0.0535 |  30.9725 |       43.5025 |       41.9644 |         30.9725 |
| benzinga_headlines | headline:beat                      | abs_next_1d |             4.6 |  0.0425 |  30.7872 |  0.0656 |  35.477  |      104.08   |      150.948  |         30.7872 |
| benzinga           | benzinga_articles:level            | abs_next_1d |            77.2 |  0.0501 |  33.5764 |  0.0585 |  29.4886 |      218.677  |      nan      |         29.4886 |
| benzinga           | benzinga_solo_articles:level       | abs_next_1d |            49.7 |  0.0537 |  39.1763 |  0.0502 |  27.7038 |      nan      |      nan      |         27.7038 |
| benzinga_headlines | headline:miss                      | abs_next_1d |             2.1 |  0.0371 |  27.6612 |  0.0504 |  32.0081 |      126.332  |      168.443  |         27.6612 |
| benzinga_headlines | headline:beat:last_5d              | abs_next_1d |            21.4 |  0.0282 |  25.8422 |  0.0482 |  31.9771 |       33.821  |       48.4118 |         25.8422 |
| benzinga_headlines | headline:miss:last_5d              | abs_next_1d |             9.9 |  0.025  |  24.131  |  0.0338 |  27.6571 |       44.9913 |       50.5912 |         24.131  |
| wikipedia          | wiki_views:level                   | abs_next_1d |            36.4 |  0.0259 |  24.3424 |  0.0301 |  23.1782 |      nan      |      nan      |         23.1782 |
| benzinga           | benzinga_solo_articles:abnormal    | abs_next_1d |           389.4 |  0.0371 |  25.3269 |  0.0424 |  22.4685 |       22.5905 |       28.166  |         22.4685 |
| benzinga           | benzinga_articles:abnormal         | abs_next_1d |           393.1 |  0.0343 |  24.147  |  0.0418 |  21.8305 |       24.7841 |       32.1952 |         21.8305 |
| benzinga           | benzinga_articles:abnormal_5d      | abs_next_1d |           390.1 |  0.0335 |  27.9352 |  0.0336 |  21.3553 |       18.9538 |       21.6091 |         21.3553 |
| sec_filings        | sec_8k_7.01                        | abs_next_1d |             5.5 |  0.0215 |  25.5511 |  0.0224 |  20.1453 |       38.1598 |       42.6514 |         20.1453 |
| gdelt_news         | gdelt_news:level                   | abs_next_1d |           102.5 | -0.0599 | -31.2652 | -0.038  | -19.2422 |      nan      |      nan      |         19.2422 |
| benzinga           | benzinga_solo_articles:abnormal_5d | abs_next_1d |           387.4 |  0.0367 |  31.6118 |  0.0291 |  18.9105 |       18.8055 |       18.5603 |         18.9105 |
| benzinga_headlines | headline:guidance_up               | abs_next_1d |             0.6 |  0.0298 |  20.0505 |  0.0344 |  18.7852 |      120.036  |      152.437  |         18.7852 |
| sec_filings        | sec_10q                            | abs_next_1d |             5.2 |  0.0178 |  18.1458 |  0.026  |  18.4764 |       40.3886 |       62.0431 |         18.1458 |
| benzinga_headlines | headline:guidance_down             | abs_next_1d |             0.2 |  0.0309 |  16.8807 |  0.034  |  18.8891 |      188.223  |      217.839  |         16.8807 |
| gdelt_news         | gdelt_news:abnormal                | abs_next_1d |           115.6 |  0.0264 |  17.8353 |  0.0251 |  16.8511 |        6.9927 |       11.2738 |         16.8511 |
| sec_filings        | sec_424b:last_5d                   | abs_next_1d |             9.7 | -0.0159 | -16.4758 | -0.0228 | -19.032  |      -15.7018 |      -25.9026 |         16.4758 |
| sec_phrases        | 8k_says:tariffs                    | abs_next_1d |             1.5 |  0.0195 |  16.3501 |  0.0242 |  19.2153 |       60.9238 |       65.6683 |         16.3501 |
| benzinga_headlines | headline:pt_cut                    | abs_next_1d |             6.3 |  0.0168 |  15.9326 |  0.0215 |  17.1081 |       43.3686 |       26.7853 |         15.9326 |
| sec_phrases        | 8k_says:share repurchase program   | abs_next_1d |             1   |  0.018  |  15.7174 |  0.0209 |  16.9289 |       62.3136 |       72.2384 |         15.7174 |
| sec_phrases        | 8k_says:goodwill impairment        | abs_next_1d |             0.5 |  0.0171 |  13.6332 |  0.0209 |  15.851  |       80.4465 |       87.3818 |         13.6332 |
| benzinga_headlines | headline:pt_cut:last_5d            | abs_next_1d |            25.3 |  0.0163 |  15.228  |  0.0199 |  13.3945 |       20.0415 |       10.6569 |         13.3945 |

#### Move together with the news (same window: descriptive, not tradable)

| source             | feature                      | target   |   names_per_day |    ic_A |      t_A |    ic_B |      t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:-----------------------------|:---------|----------------:|--------:|---------:|--------:|---------:|--------------:|--------------:|----------------:|
| benzinga           | benzinga:tone                | past_1d  |            30.3 |  0.1698 |  64.5872 |  0.1283 |  42.5424 |      165.991  |      133.256  |         42.5424 |
| benzinga_headlines | headline:upgrade             | past_1d  |             5.6 |  0.0346 |  31.2572 |  0.0378 |  31.8018 |       71.1815 |      107.156  |         31.2572 |
| benzinga_headlines | headline:downgrade           | past_1d  |             5.5 | -0.0323 | -27.3886 | -0.0321 | -25.2289 |      -72.6494 |     -109.827  |         25.2289 |
| benzinga           | benzinga:tone_change         | past_1d  |            32.4 |  0.0943 |  25.509  |  0.0785 |  22.0175 |       66.2776 |       67.941  |         22.0175 |
| benzinga_headlines | headline:pt_raised           | past_1d  |             9.2 |  0.0314 |  26.8099 |  0.0316 |  20.8473 |       91.7278 |       54.6464 |         20.8473 |
| benzinga_headlines | headline:pt_cut              | past_1d  |             6.3 | -0.0342 | -29.6522 | -0.0284 | -19.0062 |     -145.53   |      -58.2475 |         19.0062 |
| benzinga_headlines | headline:miss                | past_1d  |             2.1 | -0.0252 | -17.5026 | -0.0307 | -19.186  |     -157.969  |     -183.588  |         17.5026 |
| benzinga_headlines | headline:deal                | past_1d  |             3.9 |  0.0246 |  24.8706 |  0.0178 |  15.3004 |       56.08   |       50.226  |         15.3004 |
| benzinga_headlines | headline:upgrade:last_5d     | past_1d  |            22.7 |  0.0171 |  16.1041 |  0.0163 |  13.8591 |       18.0992 |       21.9312 |         13.8591 |
| benzinga_headlines | headline:buyback             | past_1d  |             0.7 |  0.0155 |  12.8852 |  0.0214 |  15.9689 |       62.7212 |      106.774  |         12.8852 |
| benzinga_headlines | headline:downgrade:last_5d   | past_1d  |            22.1 | -0.0158 | -14.4691 | -0.0152 | -12.4217 |      -16.376  |      -24.761  |         12.4217 |
| benzinga_headlines | headline:guidance_down       | past_1d  |             0.2 | -0.0299 | -13.9394 | -0.0275 | -12.1936 |     -331.817  |     -350.156  |         12.1936 |
| benzinga_headlines | headline:guidance_up         | past_1d  |             0.6 |  0.0227 |  13.558  |  0.0231 |  11.3285 |      166.103  |      174.05   |         11.3285 |
| benzinga_headlines | headline:new_low             | past_1d  |             1.6 | -0.0252 | -11.4038 | -0.0357 | -10.9343 |      -96.7944 |     -126.748  |         10.9343 |
| benzinga_headlines | headline:beat                | past_1d  |             4.6 |  0.0162 |  12.0906 |  0.0159 |  10.609  |       65.933  |       60.0732 |         10.609  |
| benzinga_headlines | headline:miss:last_5d        | past_1d  |             9.9 | -0.01   |  -9.1246 | -0.0129 | -10.0318 |      -32.0727 |      -41.5181 |          9.1246 |
| benzinga           | benzinga_solo_articles:spike | past_1d  |            35   |  0.0135 |  12.4539 |  0.0115 |   8.8512 |        9.4718 |        7.9498 |          8.8512 |
| benzinga           | benzinga_articles:spike      | past_1d  |            40   |  0.0161 |  13.6517 |  0.0109 |   8.297  |       10.7172 |        9.2791 |          8.297  |
| benzinga_headlines | headline:buyback:last_5d     | past_1d  |             3.3 |  0.0072 |   7.456  |  0.0095 |   8.5002 |       18.8853 |       26.1538 |          7.456  |
| benzinga           | benzinga_solo_articles:level | past_1d  |            49.7 |  0.014  |  11.8995 |  0.0124 |   7.4232 |      nan      |      nan      |          7.4232 |
| benzinga_headlines | headline:pt_raised:last_5d   | past_1d  |            36.5 |  0.0143 |  11.0875 |  0.0152 |   7.4183 |       23.0344 |       11.807  |          7.4183 |
| benzinga_headlines | headline:pt_cut:last_5d      | past_1d  |            25.3 | -0.0149 | -12.0372 | -0.0138 |  -7.1796 |      -34.0626 |      -13.7561 |          7.1796 |
| benzinga           | benzinga_articles:level      | past_1d  |            77.2 |  0.0172 |  11.6601 |  0.0128 |   6.7146 |       -9.5248 |      nan      |          6.7146 |
| benzinga_headlines | headline:new_high            | past_1d  |             3.7 |  0.0306 |  15.6544 |  0.013  |   6.6963 |       73.5652 |       71.6183 |          6.6963 |
| benzinga_headlines | headline:offering            | past_1d  |             0.6 | -0.0115 |  -9.1256 | -0.0083 |  -6.3428 |      -80.5881 |      -59.3643 |          6.3428 |

### Market-wide news themes vs ETFs

28542 theme-asset-horizon pairs; same sign and |t| > 2 in both halves: 17 (about 37.1 expected by luck).

#### Predictive (from the next close on)

| feature                                  | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:-----------------------------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| news_tone:volatility                     | ^VIX    | next_5d   |   0.143  |  2.2687 |   0.215  |  3.3032 |          2.2687 |
| 8k_says:FDA approval                     | HYG     | next_1d   |  -0.0599 | -2.3118 |  -0.0645 | -2.2401 |          2.2401 |
| news_share:unemployment                  | USO     | next_1d   |  -0.0887 | -3.1212 |  -0.0613 | -2.1108 |          2.1108 |
| tv_airtime:sanctions                     | USO     | next_1d   |   0.0618 |  2.1748 |   0.0775 |  2.049  |          2.049  |
| news_tone_change:artificial intelligence | HYG     | next_1d   |  -0.0574 | -2.029  |  -0.0614 | -2.1134 |          2.029  |
| news_tone_change:artificial intelligence | XLB     | next_1d   |  -0.062  | -2.1898 |  -0.0577 | -1.9859 |          1.9859 |
| tv_airtime:acquisition                   | USO     | next_1d   |   0.0754 |  2.6533 |   0.0749 |  1.9789 |          1.9789 |
| 8k_says:tender offer                     | UUP     | next_1d   |   0.0692 |  2.6719 |   0.0562 |  1.952  |          1.952  |
| news_tone_change:consumer confidence     | XLI     | next_1d   |   0.0547 |  1.9319 |   0.0749 |  2.5762 |          1.9319 |
| news_tone_change:Iran                    | IWM     | next_1d   |   0.0531 |  1.8763 |   0.0583 |  2.0069 |          1.8763 |
| news_tone:artificial intelligence        | QQQ     | next_1d   |  -0.0581 | -2.0613 |  -0.0545 | -1.8744 |          1.8744 |
| tv_airtime:stimulus                      | XLU     | next_1d   |  -0.0532 | -1.8729 |  -0.0753 | -1.9904 |          1.8729 |
| news_tone:jobs report                    | ^VIX    | next_5d   |   0.1175 |  1.863  |   0.1237 |  1.9009 |          1.863  |
| news_share:volatility                    | ^VIX    | next_5d   |  -0.1159 | -1.8236 |  -0.1542 | -2.3686 |          1.8236 |
| 8k_says:complete response letter         | HYG     | next_1d   |  -0.0471 | -1.817  |  -0.0639 | -2.2203 |          1.817  |
| tv_airtime:antitrust                     | XLK     | next_1d   |   0.085  |  2.9937 |   0.0685 |  1.81   |          1.81   |
| news_tone:rate hike                      | ^VIX    | next_5d   |   0.1113 |  1.7662 |   0.1523 |  2.339  |          1.7662 |
| 8k_says:class action                     | HYG     | next_1d   |  -0.0598 | -2.3081 |  -0.0508 | -1.7659 |          1.7659 |
| news_share:meme stock                    | TLT     | next_1d   |  -0.0777 | -2.7334 |  -0.0508 | -1.7474 |          1.7474 |
| news_share:rate hike                     | XLB     | next_1d   |  -0.0528 | -1.8592 |  -0.0508 | -1.7473 |          1.7473 |
| news_tone:inflation                      | ^VIX    | next_1d   |   0.0491 |  1.7412 |   0.0679 |  2.3349 |          1.7412 |
| news_tone_change:artificial intelligence | ^VIX    | next_1d   |   0.0556 |  1.9642 |   0.0502 |  1.7257 |          1.7257 |
| tv_airtime:Federal Reserve               | XLF     | next_1d   |  -0.0604 | -2.1259 |  -0.0649 | -1.7155 |          1.7155 |
| news_tone_change:electric vehicle        | UUP     | next_1d   |  -0.0486 | -1.7154 |  -0.0512 | -1.7602 |          1.7154 |
| news_share:rate hike                     | HYG     | next_1d   |  -0.0487 | -1.7149 |  -0.0671 | -2.3074 |          1.7149 |

#### Same day (descriptive)

| feature                            | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:-----------------------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| hacker_news:stories                | ^VIX    | same_day  |   0.1101 |  4.2532 |   0.0993 |  3.4505 |          3.4505 |
| news_share:volatility              | ^VIX    | same_day  |  -0.0846 | -2.9765 |  -0.1276 | -4.3938 |          2.9765 |
| news_share:acquisition             | HYG     | same_day  |   0.0824 |  2.8979 |   0.0774 |  2.6655 |          2.6655 |
| news_share:antitrust               | ^VIX    | same_day  |  -0.0935 | -3.2901 |  -0.0756 | -2.6033 |          2.6033 |
| news_share:acquisition             | ^VIX    | same_day  |  -0.1084 | -3.8149 |  -0.0739 | -2.5436 |          2.5436 |
| news_share:regulation              | ^VIX    | same_day  |  -0.0672 | -2.3655 |  -0.0678 | -2.3322 |          2.3322 |
| news_share:artificial intelligence | ^VIX    | same_day  |  -0.07   | -2.4618 |  -0.0639 | -2.1982 |          2.1982 |
| news_tone:rate hike                | ^VIX    | same_day  |   0.0652 |  2.3141 |   0.0635 |  2.1874 |          2.1874 |
| news_share:cryptocurrency          | UUP     | same_day  |  -0.0738 | -2.5983 |  -0.062  | -2.1336 |          2.1336 |
| news_tone:bull market              | ^VIX    | same_day  |   0.059  |  2.0928 |   0.1014 |  3.4892 |          2.0928 |
| news_tone_change:downgrade         | XLU     | same_day  |   0.0592 |  2.0925 |   0.0782 |  2.6933 |          2.0925 |
| news_tone_change:acquisition       | HYG     | same_day  |   0.0574 |  2.0273 |   0.0699 |  2.4055 |          2.0273 |
| news_tone:volatility               | ^VIX    | same_day  |   0.0553 |  1.9621 |   0.0823 |  2.834  |          1.9621 |
| tv_airtime:stock market crash      | XLU     | same_day  |  -0.0557 | -1.9608 |  -0.097  | -2.5659 |          1.9608 |
| news_tone:Taiwan                   | IWM     | same_day  |   0.0603 |  2.1381 |   0.057  |  1.9607 |          1.9607 |
| tv_airtime:drought                 | IWM     | same_day  |   0.066  |  2.3236 |   0.0739 |  1.9536 |          1.9536 |
| news_tone:downgrade                | XLU     | same_day  |   0.0544 |  1.93   |   0.0681 |  2.3432 |          1.93   |
| 8k_says:data breach                | USO     | same_day  |   0.0622 |  2.3972 |   0.0552 |  1.9175 |          1.9175 |
| tv_airtime:tax cut                 | IWM     | same_day  |  -0.0584 | -2.0569 |  -0.0718 | -1.8979 |          1.8979 |
| news_tone:Taiwan                   | XLI     | same_day  |   0.0609 |  2.1588 |   0.0551 |  1.8964 |          1.8964 |
| news_tone:Federal Reserve          | ^VIX    | same_day  |   0.0531 |  1.8849 |   0.0662 |  2.2779 |          1.8849 |
| news_share:bankruptcy              | ^VIX    | same_day  |  -0.0535 | -1.8817 |  -0.0571 | -1.9644 |          1.8817 |
| news_tone:Taiwan                   | XLF     | same_day  |   0.0696 |  2.4675 |   0.0547 |  1.8816 |          1.8816 |
| tv_airtime:cryptocurrency          | GLD     | same_day  |   0.058  |  2.0415 |   0.0711 |  1.8796 |          1.8796 |
| news_share:acquisition             | XLB     | same_day  |   0.0533 |  1.8766 |   0.055  |  1.8936 |          1.8766 |

