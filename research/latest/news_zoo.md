## News and media vs stock moves: correlation scan

Every collected news / media dataset turned into per-stock daily features (dated by the first open after the information was public) and correlated with the stocks' moves (relative to the average stock); market-wide news themes against ETF returns. A = 2016/17-2021, B = 2022-2026. 'weaker half t' = the smaller |t| of the two halves (same sign required).

### Data collected

| dataset                    |    rows |   columns | first      | last       |   megabytes |
|:---------------------------|--------:|----------:|:-----------|:-----------|------------:|
| gdelt_theme_timelinevolraw |    3541 |        21 | 2017-01-01 | 2026-10-22 |         0.3 |
| gdelt_total_articles       |    3541 |         1 | 2017-01-01 | 2026-10-22 |         0.1 |
| hn_stories                 |  538065 |         6 |            |            |        33.1 |
| sec_filings                | 1709772 |         4 |            |            |        23.5 |
| sec_phrase_hits            |  486597 |         6 |            |            |         8.5 |
| wiki_extra_pageviews       |    4131 |       137 | 2015-07-01 | 2026-10-21 |         0.8 |

### Per-stock features

1200 feature-target pairs. |t| > 2 over the whole period: 340 (about 60 expected by luck). Same sign and |t| > 2 in both halves: 186 (about 1.6 expected by luck).

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
| sec_phrases        | 8k_says:tender offer:last_5d     | intraday |             3.6 | -0.0024 | -2.7282 | -0.0023 | -2.2965 |       -2.805  |       -2.9223 |          2.2965 |
| sec_filings        | sec_8k_5.02                      | intraday |             4.3 | -0.0018 | -2.2914 | -0.007  | -7.1043 |       -2.5742 |      -12.9967 |          2.2914 |
| sec_filings        | sec_8k_5.02                      | next_1d  |             4.3 | -0.0017 | -2.1995 | -0.0062 | -6.422  |       -3.0311 |      -13.2729 |          2.1995 |
| benzinga_headlines | headline:dividend_up             | next_1d  |             0.3 |  0.0034 |  2.1674 |  0.0032 |  2.2501 |        9.4589 |       18.6133 |          2.1674 |
| benzinga_headlines | headline:deal:last_5d            | intraday |            17.4 | -0.002  | -2.0087 | -0.0025 | -2.1026 |       -1.1708 |       -2.0747 |          2.0087 |
| benzinga_headlines | headline:dividend_up             | intraday |             0.3 |  0.0032 |  1.9693 |  0.004  |  2.8701 |        8.7293 |       18.7751 |          1.9693 |
| sec_phrases        | 8k_says:merger agreement:last_5d | intraday |             2.7 | -0.0018 | -1.9547 | -0.0042 | -4.3057 |       -2.4029 |       -8.8537 |          1.9547 |
| sec_filings        | sec_form144                      | next_1d  |             4.7 | -0.0031 | -1.8996 | -0.0051 | -3.7432 |       -5.064  |       -7.2552 |          1.8996 |
| sec_phrases        | 8k_says:merger agreement:last_5d | next_5d  |             2.7 | -0.0044 | -2.1836 | -0.0038 | -1.8248 |      -16.0643 |      -15.0054 |          1.8248 |
| sec_phrases        | 8k_says:merger agreement:last_5d | next_1d  |             2.7 | -0.0017 | -1.8043 | -0.0033 | -3.3776 |       -2.5825 |       -7.7265 |          1.8043 |
| sec_phrases        | 8k_says:tariffs:last_5d          | intraday |             7.5 | -0.0018 | -1.7972 | -0.0022 | -2.0428 |       -0.5976 |       -1.1299 |          1.7972 |
| benzinga_headlines | headline:deal:last_5d            | next_1d  |            17.4 | -0.0018 | -1.8332 | -0.0022 | -1.7895 |       -1.0549 |       -2.1381 |          1.7895 |
| sec_phrases        | 8k_says:tariffs                  | intraday |             1.5 | -0.0031 | -2.387  | -0.0021 | -1.7014 |       -0.9266 |       -4.6331 |          1.7014 |
| sec_phrases        | 8k_says:work stoppage:last_5d    | intraday |             0.9 | -0.0017 | -1.6627 | -0.0036 | -3.2902 |       -5.4836 |      -17.1565 |          1.6627 |
| sec_filings        | sec_13g:last_5d                  | next_1d  |            23.4 | -0.0015 | -1.672  | -0.0024 | -1.6426 |       -1.656  |       -2.3642 |          1.6426 |
| benzinga_headlines | headline:halt                    | next_1d  |             0.2 | -0.0037 | -1.9201 | -0.0034 | -1.6418 |      -33.8559 |      -21.7852 |          1.6418 |
| sec_filings        | sec_10q:last_5d                  | intraday |            26   | -0.0024 | -2.5206 | -0.002  | -1.6268 |       -1.022  |       -0.4801 |          1.6268 |
| sec_filings        | sec_10q:last_5d                  | next_1d  |            26   | -0.0032 | -3.4404 | -0.002  | -1.6071 |       -1.9758 |       -1.5342 |          1.6071 |

#### Predict the size of the next move (volatility)

| source             | feature                             | target      |   names_per_day |    ic_A |      t_A |    ic_B |      t_B |   spread_bp_A |   spread_bp_B |   weaker_half_t |
|:-------------------|:------------------------------------|:------------|----------------:|--------:|---------:|--------:|---------:|--------------:|--------------:|----------------:|
| benzinga           | benzinga_articles:spike             | abs_next_1d |            40   |  0.0607 |  42.4927 |  0.0621 |  33.5802 |       44.9453 |       48.6285 |         33.5802 |
| benzinga           | benzinga_solo_articles:spike        | abs_next_1d |            35   |  0.0565 |  42.0706 |  0.0535 |  30.9725 |       43.5025 |       41.9644 |         30.9725 |
| benzinga_headlines | headline:beat                       | abs_next_1d |             4.6 |  0.0425 |  30.7872 |  0.0656 |  35.477  |      104.08   |      150.948  |         30.7872 |
| benzinga           | benzinga_articles:level             | abs_next_1d |            77.2 |  0.0501 |  33.5764 |  0.0585 |  29.4886 |      218.677  |      nan      |         29.4886 |
| benzinga           | benzinga_solo_articles:level        | abs_next_1d |            49.7 |  0.0537 |  39.1763 |  0.0502 |  27.7038 |      nan      |      nan      |         27.7038 |
| benzinga_headlines | headline:miss                       | abs_next_1d |             2.1 |  0.0371 |  27.6612 |  0.0504 |  32.0081 |      126.332  |      168.443  |         27.6612 |
| benzinga_headlines | headline:beat:last_5d               | abs_next_1d |            21.4 |  0.0282 |  25.8422 |  0.0482 |  31.9771 |       33.821  |       48.4118 |         25.8422 |
| benzinga_headlines | headline:miss:last_5d               | abs_next_1d |             9.9 |  0.025  |  24.131  |  0.0338 |  27.6571 |       44.9913 |       50.5912 |         24.131  |
| wikipedia          | wiki_views:level                    | abs_next_1d |            36.4 |  0.0259 |  24.3424 |  0.0301 |  23.1782 |      nan      |      nan      |         23.1782 |
| benzinga           | benzinga_solo_articles:abnormal     | abs_next_1d |           389.4 |  0.0371 |  25.3265 |  0.0424 |  22.4674 |       22.5897 |       28.1715 |         22.4674 |
| benzinga           | benzinga_articles:abnormal          | abs_next_1d |           393.1 |  0.0343 |  24.1463 |  0.0418 |  21.8263 |       24.789  |       32.1775 |         21.8263 |
| benzinga           | benzinga_articles:abnormal_5d       | abs_next_1d |           390.1 |  0.0335 |  27.9216 |  0.0336 |  21.3203 |       18.9668 |       21.5907 |         21.3203 |
| sec_filings        | sec_8k_7.01                         | abs_next_1d |             5.5 |  0.0215 |  25.5511 |  0.0224 |  20.1453 |       38.1598 |       42.6514 |         20.1453 |
| benzinga           | benzinga_solo_articles:abnormal_5d  | abs_next_1d |           387.4 |  0.0367 |  31.6152 |  0.0291 |  18.9052 |       18.8059 |       18.5678 |         18.9052 |
| benzinga_headlines | headline:guidance_up                | abs_next_1d |             0.6 |  0.0298 |  20.0505 |  0.0344 |  18.7852 |      120.036  |      152.437  |         18.7852 |
| sec_filings        | sec_10q                             | abs_next_1d |             5.2 |  0.0178 |  18.1458 |  0.026  |  18.4764 |       40.3886 |       62.0431 |         18.1458 |
| benzinga_headlines | headline:guidance_down              | abs_next_1d |             0.2 |  0.0309 |  16.8807 |  0.034  |  18.8891 |      188.223  |      217.839  |         16.8807 |
| sec_filings        | sec_424b:last_5d                    | abs_next_1d |             9.7 | -0.0159 | -16.4758 | -0.0228 | -19.032  |      -15.7018 |      -25.9026 |         16.4758 |
| sec_phrases        | 8k_says:tariffs                     | abs_next_1d |             1.5 |  0.0195 |  16.3501 |  0.0242 |  19.1964 |       60.9238 |       65.6136 |         16.3501 |
| benzinga_headlines | headline:pt_cut                     | abs_next_1d |             6.3 |  0.0168 |  15.9326 |  0.0215 |  17.1081 |       43.3686 |       26.7853 |         15.9326 |
| sec_phrases        | 8k_says:share repurchase program    | abs_next_1d |             1   |  0.018  |  15.7174 |  0.0209 |  16.9289 |       62.3136 |       72.2384 |         15.7174 |
| sec_phrases        | 8k_says:goodwill impairment         | abs_next_1d |             0.5 |  0.0171 |  13.6332 |  0.0209 |  15.851  |       80.4465 |       87.3818 |         13.6332 |
| benzinga_headlines | headline:pt_cut:last_5d             | abs_next_1d |            25.3 |  0.0163 |  15.228  |  0.0199 |  13.3945 |       20.0415 |       10.6569 |         13.3945 |
| sec_phrases        | 8k_says:goodwill impairment:last_5d | abs_next_1d |             2.6 |  0.0123 |  13.2563 |  0.0147 |  14.3804 |       34.4592 |       38.0907 |         13.2563 |
| sec_filings        | sec_8k_7.01:last_5d                 | abs_next_1d |            26.2 |  0.0164 |  19.7639 |  0.0138 |  13.1444 |       12.0614 |       10.3149 |         13.1444 |

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

4047 theme-asset-horizon pairs; same sign and |t| > 2 in both halves: 2 (about 5.3 expected by luck).

#### Predictive (from the next close on)

| feature                          | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:---------------------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| 8k_says:FDA approval             | HYG     | next_1d   |  -0.0599 | -2.3118 |  -0.0644 | -2.2348 |          2.2348 |
| 8k_says:tender offer             | UUP     | next_1d   |   0.0692 |  2.6719 |   0.0565 |  1.9591 |          1.9591 |
| 8k_says:complete response letter | HYG     | next_1d   |  -0.0471 | -1.8169 |  -0.0644 | -2.2326 |          1.8169 |
| 8k_says:class action             | HYG     | next_1d   |  -0.0598 | -2.3081 |  -0.0508 | -1.7618 |          1.7618 |
| 8k_says:preliminary results      | HYG     | next_1d   |  -0.0643 | -2.4791 |  -0.047  | -1.6323 |          1.6323 |
| 8k_says:going concern            | TLT     | next_1d   |  -0.0411 | -1.5858 |  -0.0603 | -2.0931 |          1.5858 |
| 8k_says:Department of Justice    | HYG     | next_1d   |  -0.0713 | -2.7525 |  -0.0442 | -1.5342 |          1.5342 |
| 8k_says:work stoppage            | GLD     | next_1d   |  -0.0435 | -1.6791 |  -0.0437 | -1.5163 |          1.5163 |
| news_share:inflation             | HYG     | next_1d   |  -0.043  | -1.5128 |  -0.0504 | -1.7334 |          1.5128 |
| 8k_says:work stoppage            | UUP     | next_1d   |   0.0615 |  2.3758 |   0.0433 |  1.5028 |          1.5028 |
| 8k_says:merger agreement         | HYG     | next_1d   |  -0.0385 | -1.4861 |  -0.0581 | -2.0169 |          1.4861 |
| 8k_says:covenant waiver          | HYG     | next_1d   |  -0.0385 | -1.4779 |  -0.0655 | -2.271  |          1.4779 |
| 8k_says:preliminary results      | HYG     | next_5d   |  -0.1047 | -1.8069 |  -0.089  | -1.3789 |          1.3789 |
| news_share:election              | GLD     | next_5d   |  -0.0869 | -1.3672 |  -0.11   | -1.6885 |          1.3672 |
| news_share:government shutdown   | GLD     | next_5d   |   0.0893 |  1.4056 |   0.088  |  1.352  |          1.352  |
| news_share:impeachment           | TLT     | next_1d   |  -0.0381 | -1.3398 |  -0.056  | -1.9266 |          1.3398 |
| 8k_says:material weakness        | HYG     | next_1d   |  -0.0419 | -1.6175 |  -0.0386 | -1.3386 |          1.3386 |
| 8k_says:subpoena                 | TLT     | next_1d   |  -0.0337 | -1.2998 |  -0.0544 | -1.8876 |          1.2998 |
| 8k_says:tender offer             | HYG     | next_1d   |  -0.0336 | -1.2985 |  -0.0749 | -2.5995 |          1.2985 |
| 8k_says:special dividend         | XLP     | next_1d   |   0.0335 |  1.2945 |   0.0378 |  1.3121 |          1.2945 |
| news_share:debt ceiling          | XLP     | next_1d   |  -0.0407 | -1.2644 |  -0.0516 | -1.7727 |          1.2644 |
| news_share:terrorist attack      | GLD     | next_1d   |   0.0459 |  1.6167 |   0.0365 |  1.2546 |          1.2546 |
| 8k_says:FDA approval             | XLY     | next_5d   |  -0.0833 | -1.4372 |  -0.08   | -1.2391 |          1.2391 |
| news_share:coronavirus           | TLT     | next_20d  |   0.2283 |  1.796  |   0.1825 |  1.2246 |          1.2246 |
| news_share:government shutdown   | GLD     | next_1d   |   0.0605 |  2.1286 |   0.0354 |  1.2183 |          1.2183 |

#### Same day (descriptive)

| feature                          | asset   | horizon   |   corr_A |     t_A |   corr_B |     t_B |   weaker_half_t |
|:---------------------------------|:--------|:----------|---------:|--------:|---------:|--------:|----------------:|
| hacker_news:stories              | ^VIX    | same_day  |   0.1101 |  4.2532 |   0.1003 |  3.4819 |          3.4819 |
| news_share:bankruptcy            | ^VIX    | same_day  |  -0.0535 | -1.8817 |  -0.058  | -1.9954 |          1.8817 |
| 8k_says:data breach              | USO     | same_day  |   0.0622 |  2.3972 |   0.0538 |  1.8667 |          1.8667 |
| 8k_says:going concern            | TLT     | same_day  |  -0.0478 | -1.8452 |  -0.0663 | -2.3026 |          1.8452 |
| news_share:layoffs               | GLD     | same_day  |   0.0637 |  1.9801 |   0.0701 |  1.7969 |          1.7969 |
| 8k_says:class action             | HYG     | same_day  |  -0.0764 | -2.9497 |  -0.0511 | -1.7741 |          1.7741 |
| hacker_news:stories              | HYG     | same_day  |  -0.0455 | -1.7564 |  -0.0869 | -3.0158 |          1.7564 |
| 8k_says:cybersecurity incident   | XLE     | same_day  |   0.052  |  2.0055 |   0.0504 |  1.7507 |          1.7507 |
| 8k_says:reverse stock split      | UUP     | same_day  |   0.0604 |  2.3332 |   0.0501 |  1.739  |          1.739  |
| 8k_says:going concern            | XLE     | same_day  |   0.0489 |  1.886  |   0.0487 |  1.6913 |          1.6913 |
| 8k_says:complete response letter | HYG     | same_day  |  -0.0491 | -1.8951 |  -0.0436 | -1.5106 |          1.5106 |
| 8k_says:tender offer             | UUP     | same_day  |   0.0387 |  1.4955 |   0.0554 |  1.9219 |          1.4955 |
| news_share:layoffs               | XLP     | same_day  |   0.0502 |  1.562  |   0.0578 |  1.4816 |          1.4816 |
| 8k_says:subpoena                 | TLT     | same_day  |  -0.0378 | -1.4584 |  -0.0732 | -2.5396 |          1.4584 |
| 8k_says:tender offer             | HYG     | same_day  |  -0.0356 | -1.3756 |  -0.0538 | -1.8661 |          1.3756 |
| 8k_says:merger agreement         | HYG     | same_day  |  -0.0337 | -1.3011 |  -0.0442 | -1.5342 |          1.3011 |
| news_share:layoffs               | XLI     | same_day  |   0.054  |  1.6778 |   0.0505 |  1.2955 |          1.2955 |
| 8k_says:restatement              | UUP     | same_day  |   0.0519 |  2.0046 |   0.0368 |  1.2768 |          1.2768 |
| hacker_news:stories              | XLB     | same_day  |  -0.0327 | -1.2629 |  -0.0424 | -1.4734 |          1.2629 |
| 8k_says:material weakness        | HYG     | same_day  |  -0.0615 | -2.3755 |  -0.0358 | -1.2442 |          1.2442 |
| 8k_says:merger agreement         | TLT     | same_day  |  -0.031  | -1.1959 |  -0.041  | -1.4221 |          1.1959 |
| news_share:hurricane             | XLE     | same_day  |   0.034  |  1.1948 |   0.0466 |  1.6014 |          1.1948 |
| 8k_says:FDA approval             | HYG     | same_day  |  -0.0527 | -2.0343 |  -0.0344 | -1.1939 |          1.1939 |
| news_share:inflation             | ^VIX    | same_day  |  -0.0414 | -1.4555 |  -0.0344 | -1.1818 |          1.1818 |
| 8k_says:covenant waiver          | HYG     | same_day  |  -0.0459 | -1.7612 |  -0.033  | -1.1441 |          1.1441 |

