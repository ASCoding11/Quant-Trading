## Asian markets

Daily Yahoo data since 2005; directions chosen on 2006-2014, checked on 2015-2026. An Asian session on date D falls between the US sessions of D-1 and D. Opening prices Yahoo copied from the previous close are dropped (share per ticker in asia_data_quality.csv).

### 1. Lead-lag between the US and Asian indices

'gap' = previous close -> open (the news is absorbed here: descriptive); 'after the open' = open -> close (tradable: SPY at the auctions, Asian markets through index futures).

| market         | signal                                    | target                    | tradable   |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:---------------|:------------------------------------------|:--------------------------|:-----------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| Japan          | US close-to-close (D-1)                   | Japan: gap                | False      |          0.677 |      31.783 |        2205 |          0.619 |      33.238 |        2882 |
| Japan          | US close-to-close (D-1)                   | Japan: after the open     | True       |          0.287 |      13.478 |        2205 |          0.13  |       6.954 |        2882 |
| Japan          | US open-to-close (D-1)                    | Japan: after the open     | True       |          0.25  |      11.756 |        2205 |          0.141 |       7.56  |        2882 |
| Japan          | Japan close-to-close (D)                  | US: US gap                | False      |          0.284 |      13.464 |        2245 |          0.301 |      16.368 |        2949 |
| Japan          | Japan close-to-close (D)                  | US: US after the open     | True       |         -0.055 |      -2.612 |        2245 |         -0.025 |      -1.339 |        2949 |
| Japan          | Japan open-to-close (D)                   | US: US after the open     | True       |         -0.04  |      -1.881 |        2245 |          0.004 |       0.226 |        2949 |
| Hong Kong      | US close-to-close (D-1)                   | Hong Kong: gap            | False      |          0.709 |      33.398 |        2218 |          0.505 |      27.228 |        2904 |
| Hong Kong      | US close-to-close (D-1)                   | Hong Kong: after the open | True       |         -0.126 |      -5.953 |        2218 |         -0.086 |      -4.628 |        2904 |
| Hong Kong      | US open-to-close (D-1)                    | Hong Kong: after the open | True       |         -0.094 |      -4.407 |        2218 |         -0.054 |      -2.893 |        2904 |
| Hong Kong      | Hong Kong close-to-close (D)              | US: US gap                | False      |          0.403 |      19.081 |        2247 |          0.318 |      17.302 |        2953 |
| Hong Kong      | Hong Kong close-to-close (D)              | US: US after the open     | True       |          0.053 |       2.497 |        2247 |         -0.035 |      -1.908 |        2953 |
| Hong Kong      | Hong Kong open-to-close (D)               | US: US after the open     | True       |          0.159 |       7.55  |        2247 |         -0.006 |      -0.345 |        2953 |
| China          | US close-to-close (D-1)                   | China: gap                | False      |          0.535 |      25.004 |        2182 |          0.421 |      22.505 |        2864 |
| China          | US close-to-close (D-1)                   | China: after the open     | True       |         -0.071 |      -3.302 |        2182 |         -0.051 |      -2.737 |        2864 |
| China          | US open-to-close (D-1)                    | China: after the open     | True       |         -0.025 |      -1.167 |        2182 |         -0.017 |      -0.889 |        2864 |
| China          | China close-to-close (D)                  | US: US gap                | False      |          0.173 |       8.122 |        2206 |          0.207 |      11.17  |        2899 |
| China          | China close-to-close (D)                  | US: US after the open     | True       |         -0.015 |      -0.724 |        2206 |          0.002 |       0.127 |        2899 |
| China          | China open-to-close (D)                   | US: US after the open     | True       |          0.021 |       0.983 |        2206 |          0.01  |       0.528 |        2899 |
| Korea          | US close-to-close (D-1)                   | Korea: gap                | False      |          0.769 |      36.295 |        2230 |          0.574 |      30.803 |        2884 |
| Korea          | US close-to-close (D-1)                   | Korea: after the open     | True       |         -0.178 |      -8.421 |        2230 |         -0.058 |      -3.117 |        2884 |
| Korea          | US open-to-close (D-1)                    | Korea: after the open     | True       |         -0.155 |      -7.309 |        2230 |         -0.066 |      -3.52  |        2884 |
| Korea          | Korea close-to-close (D)                  | US: US gap                | False      |          0.356 |      16.882 |        2247 |          0.283 |      15.386 |        2946 |
| Korea          | Korea close-to-close (D)                  | US: US after the open     | True       |          0.035 |       1.674 |        2247 |         -0.033 |      -1.778 |        2946 |
| Korea          | Korea open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.493 |        2247 |         -0.007 |      -0.392 |        2946 |
| Taiwan         | US close-to-close (D-1)                   | Taiwan: gap               | False      |          0.734 |      34.612 |        2221 |          0.572 |      30.569 |        2860 |
| Taiwan         | US close-to-close (D-1)                   | Taiwan: after the open    | True       |         -0.177 |      -8.355 |        2221 |          0.214 |      11.419 |        2860 |
| Taiwan         | US open-to-close (D-1)                    | Taiwan: after the open    | True       |         -0.136 |      -6.42  |        2221 |          0.21  |      11.248 |        2860 |
| Taiwan         | Taiwan close-to-close (D)                 | US: US gap                | False      |          0.298 |      14.007 |        2216 |          0.283 |      15.292 |        2912 |
| Taiwan         | Taiwan close-to-close (D)                 | US: US after the open     | True       |         -0.01  |      -0.479 |        2216 |         -0.06  |      -3.256 |        2912 |
| Taiwan         | Taiwan open-to-close (D)                  | US: US after the open     | True       |          0.07  |       3.311 |        2216 |         -0.046 |      -2.462 |        2909 |
| Australia      | US close-to-close (D-1)                   | Australia: gap            | False      |          0.754 |      31.388 |        1732 |          0.44  |      12.638 |         825 |
| Australia      | US close-to-close (D-1)                   | Australia: after the open | True       |          0.445 |      18.537 |        1732 |          0.481 |      13.803 |         825 |
| Australia      | US open-to-close (D-1)                    | Australia: after the open | True       |          0.445 |      18.504 |        1732 |          0.449 |      12.891 |         825 |
| Australia      | Australia close-to-close (D)              | US: US gap                | False      |          0.3   |      14.21  |        2247 |          0.4   |      21.728 |        2953 |
| Australia      | Australia close-to-close (D)              | US: US after the open     | True       |          0.011 |       0.528 |        2247 |          0.02  |       1.112 |        2953 |
| Australia      | Australia open-to-close (D)               | US: US after the open     | True       |          0.046 |       2.008 |        1905 |         -0.017 |      -0.605 |        1244 |
| India          | US close-to-close (D-1)                   | India: gap                | False      |          0.621 |      29.118 |        2198 |          0.475 |      25.574 |        2904 |
| India          | US close-to-close (D-1)                   | India: after the open     | True       |         -0.062 |      -2.897 |        2198 |         -0.012 |      -0.623 |        2904 |
| India          | US open-to-close (D-1)                    | India: after the open     | True       |          0.034 |       1.577 |        2198 |          0.02  |       1.074 |        2904 |
| India          | India close-to-close (D)                  | US: US gap                | False      |          0.384 |      18.2   |        2247 |          0.394 |      21.42  |        2953 |
| India          | India close-to-close (D)                  | US: US after the open     | True       |          0.093 |       4.432 |        2247 |         -0.013 |      -0.693 |        2953 |
| India          | India open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.499 |        2247 |          0.013 |       0.712 |        2953 |
| Singapore      | US close-to-close (D-1)                   | Singapore: gap            | False      |          0.717 |      23.954 |        1117 |          0.608 |      33.042 |        2958 |
| Singapore      | US close-to-close (D-1)                   | Singapore: after the open | True       |         -0.076 |      -2.557 |        1117 |         -0.02  |      -1.09  |        2958 |
| Singapore      | US open-to-close (D-1)                    | Singapore: after the open | True       |         -0.029 |      -0.953 |        1117 |         -0.024 |      -1.28  |        2958 |
| Singapore      | Singapore close-to-close (D)              | US: US gap                | False      |          0.445 |      21.099 |        2247 |          0.363 |      19.73  |        2953 |
| Singapore      | Singapore close-to-close (D)              | US: US after the open     | True       |          0.048 |       2.277 |        2247 |         -0.044 |      -2.375 |        2953 |
| Singapore      | Singapore open-to-close (D)               | US: US after the open     | True       |          0.047 |       1.694 |        1301 |         -0.006 |      -0.318 |        2953 |
| Asia (average) | Asian markets' average close-to-close (D) | US gap                    | False      |          0.44  |      20.857 |        2247 |          0.447 |      24.301 |        2953 |
| Asia (average) | Asian markets' average close-to-close (D) | US after the open         | True       |          0.027 |       1.271 |        2247 |         -0.035 |      -1.884 |        2953 |

Trading the sign of the signal on the 'after the open' leg (cost: 0 bp SPY auctions, 2 bp Asian futures round trip):

| market         | strategy                                             | direction   |   sharpe_2006_14 |   sharpe_2015_26 |   net_sharpe_2015_26 |   avg_bp_2015_26 |   cost_bp |
|:---------------|:-----------------------------------------------------|:------------|-----------------:|-----------------:|---------------------:|-----------------:|----------:|
| Japan          | US close-to-close (D-1) -> Japan after the open      | +           |            1.144 |            0.783 |                0.459 |            4.817 |         2 |
| Japan          | US open-to-close (D-1) -> Japan after the open       | +           |            1.339 |            0.794 |                0.469 |            4.888 |         2 |
| Japan          | Japan close-to-close (D) -> US US after the open     | +           |            0.156 |           -0.118 |               -0.118 |           -0.62  |         0 |
| Japan          | Japan open-to-close (D) -> US US after the open      | +           |            0.269 |            0.19  |                0.19  |            0.998 |         0 |
| Hong Kong      | US close-to-close (D-1) -> Hong Kong after the open  | -           |            1.096 |            0.852 |                0.54  |            5.445 |         2 |
| Hong Kong      | US open-to-close (D-1) -> Hong Kong after the open   | -           |            0.602 |            0.624 |                0.312 |            3.995 |         2 |
| Hong Kong      | Hong Kong close-to-close (D) -> US US after the open | +           |            0.273 |           -0.428 |               -0.428 |           -2.246 |         0 |
| Hong Kong      | Hong Kong open-to-close (D) -> US US after the open  | +           |            0.96  |            0.151 |                0.151 |            0.794 |         0 |
| China          | US close-to-close (D-1) -> China after the open      | -           |            0.024 |            0.154 |               -0.132 |            1.073 |         2 |
| China          | US open-to-close (D-1) -> China after the open       | +           |            0.315 |           -0.261 |               -0.547 |           -1.818 |         2 |
| China          | China close-to-close (D) -> US US after the open     | +           |            0.027 |           -0.182 |               -0.182 |           -0.956 |         0 |
| China          | China open-to-close (D) -> US US after the open      | -           |            0.116 |           -0.407 |               -0.407 |           -2.14  |         0 |
| Korea          | US close-to-close (D-1) -> Korea after the open      | -           |            1.471 |            0.552 |                0.261 |            3.784 |         2 |
| Korea          | US open-to-close (D-1) -> Korea after the open       | -           |            1.122 |            0.785 |                0.493 |            5.384 |         2 |
| Korea          | Korea close-to-close (D) -> US US after the open     | +           |            0.549 |           -0.245 |               -0.245 |           -1.285 |         0 |
| Korea          | Korea open-to-close (D) -> US US after the open      | +           |            0.718 |           -0.067 |               -0.067 |           -0.354 |         0 |
| Taiwan         | US close-to-close (D-1) -> Taiwan after the open     | -           |            1.744 |           -2.975 |               -3.349 |          -15.865 |         2 |
| Taiwan         | US open-to-close (D-1) -> Taiwan after the open      | -           |            0.762 |           -2.129 |               -2.5   |          -11.449 |         2 |
| Taiwan         | Taiwan close-to-close (D) -> US US after the open    | -           |            0.005 |           -0.059 |               -0.059 |           -0.309 |         0 |
| Taiwan         | Taiwan open-to-close (D) -> US US after the open     | +           |            0.759 |            0.151 |                0.151 |            0.797 |         0 |
| Australia      | US close-to-close (D-1) -> Australia after the open  | +           |            5.163 |            5.862 |                5.415 |           26.169 |         2 |
| Australia      | US open-to-close (D-1) -> Australia after the open   | +           |            5.002 |            5     |                4.559 |           22.701 |         2 |
| Australia      | Australia close-to-close (D) -> US US after the open | +           |            0.075 |           -0.062 |               -0.062 |           -0.323 |         0 |
| Australia      | Australia open-to-close (D) -> US US after the open  | +           |            0.442 |           -0.095 |               -0.095 |           -0.522 |         0 |
| India          | US close-to-close (D-1) -> India after the open      | +           |            0.238 |           -0.22  |               -0.589 |           -1.19  |         2 |
| India          | US open-to-close (D-1) -> India after the open       | +           |            1.102 |            0.263 |               -0.106 |            1.424 |         2 |
| India          | India close-to-close (D) -> US US after the open     | +           |            0.644 |           -0.002 |               -0.002 |           -0.009 |         0 |
| India          | India open-to-close (D) -> US US after the open      | +           |            0.807 |            0.017 |                0.017 |            0.091 |         0 |
| Singapore      | US close-to-close (D-1) -> Singapore after the open  | -           |            0.774 |            0.036 |               -0.479 |            0.139 |         2 |
| Singapore      | US open-to-close (D-1) -> Singapore after the open   | -           |            0.395 |            0.449 |               -0.067 |            1.742 |         2 |
| Singapore      | Singapore close-to-close (D) -> US US after the open | +           |            0.608 |           -0.414 |               -0.414 |           -2.17  |         0 |
| Singapore      | Singapore open-to-close (D) -> US US after the open  | +           |            0.265 |            0.03  |                0.03  |            0.16  |         0 |
| Asia (average) | Asia average (D) -> SPY open-to-close (D)            | +           |            0.592 |           -0.147 |               -0.147 |           -0.77  |         0 |

### 2. ADRs vs their home listings

Residual = the home listing's last session in dollars minus the ADR's opening gap. Pooled long / short book on Alpaca (market-on-open in, market-on-close out):

| strategy                                               | direction   |   cost_bp_round_trip |   sharpe_2006_14 |   sharpe_2015_26 |   avg_bp_2015_26 |   adrs_per_day_2015_26 |
|:-------------------------------------------------------|:------------|---------------------:|-----------------:|-----------------:|-----------------:|-----------------------:|
| ADRs: trade the home-vs-gap residual, MOO in / MOC out | +           |                    0 |            3.899 |            2.637 |             7.96 |                 22.056 |
| ADRs: trade the home-vs-gap residual, MOO in / MOC out | +           |                    1 |            3.692 |            2.306 |             7.96 |                 22.056 |
| ADRs: trade the home-vs-gap residual, MOO in / MOC out | +           |                    3 |            3.276 |            1.643 |             7.96 |                 22.056 |

Per ADR (correlations):

| adr   | home         | signal                        | target               |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:------|:-------------|:------------------------------|:---------------------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| TSM   | 2330.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.133 |       6.2   |        2171 |         -0.025 |      -1.36  |        2899 |
| TSM   | 2330.TW      | home move (USD)               | ADR open-to-close    |          0.13  |       6.045 |        2171 |         -0.057 |      -3.043 |        2899 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: after its open |          0.189 |       8.469 |        2008 |         -0.015 |      -0.758 |        2559 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: gap            |          0.137 |       6.125 |        2008 |          0.558 |      28.23  |        2559 |
| UMC   | 2303.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.157 |       6.992 |        1991 |          0.12  |       6.156 |        2635 |
| UMC   | 2303.TW      | home move (USD)               | ADR open-to-close    |          0.144 |       6.419 |        1991 |          0.121 |       6.222 |        2635 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: after its open |          0.155 |       6.81  |        1934 |         -0.064 |      -3.258 |        2556 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: gap            |          0.096 |       4.206 |        1934 |          0.479 |      24.233 |        2556 |
| ASX   | 3711.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.374 |      17.155 |        2101 |          0.02  |       1.031 |        2772 |
| ASX   | 3711.TW      | home move (USD)               | ADR open-to-close    |          0.279 |      12.799 |        2101 |          0.067 |       3.506 |        2772 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: after its open |         -0.045 |      -2.04  |        2092 |          0.011 |       0.558 |        2648 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: gap            |          0.389 |      17.795 |        2092 |          0.499 |      25.681 |        2648 |
| CHT   | 2412.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.14  |       6.556 |        2182 |          0.162 |       8.653 |        2850 |
| CHT   | 2412.TW      | home move (USD)               | ADR open-to-close    |          0.088 |       4.104 |        2182 |          0.121 |       6.44  |        2850 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: after its open |         -0.05  |      -2.174 |        1901 |          0.016 |       0.717 |        1994 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: gap            |          0.213 |       9.277 |        1901 |          0.192 |       8.555 |        1994 |
| SONY  | 6758.T       | home move (USD) minus ADR gap | ADR open-to-close    |         -0.029 |      -1.383 |        2224 |          0.011 |       0.596 |        2926 |
| SONY  | 6758.T       | home move (USD)               | ADR open-to-close    |          0.033 |       1.533 |        2224 |          0.027 |       1.479 |        2926 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: after its open |          0.206 |       9.492 |        2126 |         -0.015 |      -0.794 |        2841 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: gap            |          0.43  |      19.828 |        2126 |          0.541 |      28.839 |        2841 |
| TM    | 7203.T       | home move (USD) minus ADR gap | ADR open-to-close    |         -0.065 |      -3.086 |        2250 |          0.016 |       0.846 |        2954 |
| TM    | 7203.T       | home move (USD)               | ADR open-to-close    |         -0.025 |      -1.167 |        2250 |          0.058 |       3.157 |        2954 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: after its open |          0.214 |       9.734 |        2065 |         -0.025 |      -1.351 |        2861 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: gap            |          0.392 |      17.831 |        2065 |          0.491 |      26.28  |        2861 |
| HMC   | 7267.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.054 |       2.541 |        2221 |          0.015 |       0.819 |        2904 |
| HMC   | 7267.T       | home move (USD)               | ADR open-to-close    |          0.074 |       3.494 |        2221 |          0.047 |       2.524 |        2904 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: after its open |          0.269 |      12.331 |        2099 |          0.028 |       1.517 |        2841 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: gap            |          0.337 |      15.46  |        2099 |          0.462 |      24.6   |        2841 |
| MUFG  | 8306.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.118 |       5.381 |        2088 |          0.092 |       4.797 |        2709 |
| MUFG  | 8306.T       | home move (USD)               | ADR open-to-close    |          0.013 |       0.616 |        2088 |          0.086 |       4.497 |        2709 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: after its open |          0.155 |       6.895 |        1967 |         -0.042 |      -2.258 |        2855 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: gap            |          0.285 |      12.633 |        1967 |          0.445 |      23.768 |        2855 |
| SMFG  | 8316.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.144 |       5.455 |        1437 |          0.063 |       3.287 |        2759 |
| SMFG  | 8316.T       | home move (USD)               | ADR open-to-close    |          0.057 |       2.165 |        1437 |          0.068 |       3.596 |        2759 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: after its open |          0.133 |       5.078 |        1463 |         -0.038 |      -2.046 |        2843 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: gap            |          0.29  |      11.081 |        1463 |          0.417 |      22.237 |        2843 |
| MFG   | 8411.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.101 |       4.297 |        1823 |          0.126 |       6.353 |        2522 |
| MFG   | 8411.T       | home move (USD)               | ADR open-to-close    |          0.056 |       2.373 |        1824 |          0.079 |       3.982 |        2522 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: after its open |          0.157 |       6.395 |        1662 |         -0.024 |      -1.263 |        2797 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: gap            |          0.227 |       9.241 |        1662 |          0.378 |      20.004 |        2797 |
| NMR   | 8604.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.047 |       2.191 |        2145 |          0.084 |       4.327 |        2642 |
| NMR   | 8604.T       | home move (USD)               | ADR open-to-close    |          0.083 |       3.858 |        2145 |          0.136 |       6.994 |        2642 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: after its open |          0.125 |       5.716 |        2091 |         -0.004 |      -0.229 |        2852 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: gap            |          0.399 |      18.224 |        2091 |          0.415 |      22.159 |        2852 |
| BABA  | 9988.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.06  |       2.513 |        1730 |
| BABA  | 9988.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.061 |       2.555 |        1730 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.019 |       0.781 |        1649 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.704 |      28.588 |        1648 |
| JD    | 9618.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.051 |       2.013 |        1583 |
| JD    | 9618.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.037 |       1.458 |        1583 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.11  |       4.263 |        1501 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.705 |      27.289 |        1500 |
| BIDU  | 9888.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.059 |       2.223 |        1397 |
| BIDU  | 9888.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.072 |       2.682 |        1397 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.052 |       1.833 |        1259 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.74  |      26.251 |        1258 |
| NTES  | 9999.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.031 |       1.251 |        1590 |
| NTES  | 9999.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.022 |      -0.878 |        1590 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.069 |       2.685 |        1520 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.66  |      25.737 |        1519 |
| KB    | 105560.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.093 |       4.4   |        2242 |          0.03  |       1.642 |        2919 |
| KB    | 105560.KS    | home move (USD)               | ADR open-to-close    |          0.188 |       8.915 |        2242 |          0.064 |       3.444 |        2919 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: after its open |         -0.049 |      -1.896 |        1485 |          0.035 |       1.814 |        2755 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: gap            |          0.633 |      24.399 |        1485 |          0.399 |      20.964 |        2755 |
| SHG   | 055550.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.118 |       5.583 |        2251 |          0.141 |       7.593 |        2914 |
| SHG   | 055550.KS    | home move (USD)               | ADR open-to-close    |          0.169 |       8.004 |        2251 |          0.099 |       5.355 |        2914 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: after its open |         -0.091 |      -4.223 |        2136 |          0.018 |       0.957 |        2757 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: gap            |          0.554 |      25.583 |        2136 |          0.382 |      20.06  |        2757 |
| PKX   | 005490.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.125 |       5.912 |        2251 |          0.022 |       1.214 |        2944 |
| PKX   | 005490.KS    | home move (USD)               | ADR open-to-close    |          0.19  |       9.027 |        2251 |          0.016 |       0.862 |        2944 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: after its open |          0.013 |       0.604 |        2109 |          0.041 |       2.122 |        2735 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: gap            |          0.673 |      30.916 |        2109 |          0.456 |      23.827 |        2735 |
| LPL   | 034220.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.204 |       9.457 |        2159 |          0.164 |       8.448 |        2666 |
| LPL   | 034220.KS    | home move (USD)               | ADR open-to-close    |          0.222 |      10.297 |        2159 |          0.169 |       8.728 |        2666 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: after its open |         -0.013 |      -0.581 |        2159 |          0.037 |       1.895 |        2615 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: gap            |          0.569 |      26.419 |        2159 |          0.394 |      20.172 |        2615 |
| KEP   | 015760.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.238 |      11.14  |        2196 |          0.094 |       4.986 |        2822 |
| KEP   | 015760.KS    | home move (USD)               | ADR open-to-close    |          0.241 |      11.309 |        2196 |          0.109 |       5.796 |        2822 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: after its open |         -0.007 |      -0.304 |        2131 |          0.005 |       0.28  |        2724 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: gap            |          0.472 |      21.768 |        2131 |          0.309 |      16.122 |        2724 |
| IBN   | ICICIBANK.NS | home move (USD) minus ADR gap | ADR open-to-close    |          0.085 |       4.009 |        2243 |          0.081 |       4.359 |        2864 |
| IBN   | ICICIBANK.NS | home move (USD)               | ADR open-to-close    |          0.175 |       8.287 |        2243 |          0.116 |       6.227 |        2864 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: after its open |          0.153 |       7.186 |        2210 |          0.03  |       1.594 |        2899 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: gap            |          0.434 |      20.417 |        2210 |          0.498 |      26.824 |        2899 |
| HDB   | HDFCBANK.NS  | home move (USD) minus ADR gap | ADR open-to-close    |          0.084 |       3.97  |        2256 |          0.109 |       5.906 |        2929 |
| HDB   | HDFCBANK.NS  | home move (USD)               | ADR open-to-close    |          0.125 |       5.945 |        2256 |          0.147 |       7.93  |        2929 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: after its open |          0.089 |       4.185 |        2209 |          0.005 |       0.246 |        2902 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: gap            |          0.474 |      22.28  |        2209 |          0.404 |      21.757 |        2902 |
| INFY  | INFY.NS      | home move (USD) minus ADR gap | ADR open-to-close    |          0.059 |       2.768 |        2238 |          0.03  |       1.631 |        2890 |
| INFY  | INFY.NS      | home move (USD)               | ADR open-to-close    |          0.113 |       5.331 |        2238 |          0.011 |       0.582 |        2890 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: after its open |          0.158 |       7.446 |        2209 |          0.099 |       5.354 |        2907 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: gap            |          0.403 |      18.925 |        2209 |          0.49  |      26.413 |        2907 |
| WIT   | WIPRO.NS     | home move (USD) minus ADR gap | ADR open-to-close    |          0.237 |      11.195 |        2225 |          0.083 |       4.334 |        2701 |
| WIT   | WIPRO.NS     | home move (USD)               | ADR open-to-close    |          0.124 |       5.855 |        2225 |          0.038 |       1.996 |        2701 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: after its open |          0.048 |       2.239 |        2206 |          0.029 |       1.545 |        2882 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: gap            |          0.32  |      15.02  |        2206 |          0.363 |      19.504 |        2882 |
| BHP   | BHP.AX       | home move (USD) minus ADR gap | ADR open-to-close    |          0.152 |       7.224 |        2251 |          0.048 |       2.6   |        2942 |
| BHP   | BHP.AX       | home move (USD)               | ADR open-to-close    |          0.162 |       7.662 |        2251 |          0.028 |       1.511 |        2942 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: after its open |         -0.005 |      -0.247 |        2234 |         -0.012 |      -0.669 |        2946 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: gap            |          0.614 |      29.029 |        2234 |          0.509 |      27.651 |        2946 |

### 3. Strategies inside each Asian market (long top fifth / short bottom fifth)

| market    | strategy                                                            | direction   |   stocks |   sharpe_2006_14 |   sharpe_2015_26 |   annual_return_2015_26 |   net_sharpe_2015_26 |   net_annual_return_2015_26 |   round_trip_cost_bp | on_ibkr   |   bad_open_share |
|:----------|:--------------------------------------------------------------------|:------------|---------:|-----------------:|-----------------:|------------------------:|---------------------:|----------------------------:|---------------------:|:----------|-----------------:|
| Japan     | overnight persistence (21d overnight sum; close in, open out)       | +           |       40 |            0.517 |            0.788 |                   0.052 |               -3.001 |                      -0.2   |                   10 | True      |            0.038 |
| Japan     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       40 |            0.092 |            1.126 |                   0.071 |               -2.844 |                      -0.181 |                   10 | True      |            0.038 |
| Japan     | 1-day reversal (against today's close-to-close; close to close)     | -           |       40 |            0.509 |           -0.232 |                  -0.024 |               -2.119 |                      -0.221 |                   10 | True      |            0.038 |
| Japan     | 5-day reversal (close to close)                                     | +           |       40 |            0.635 |            0.131 |                   0.014 |               -0.693 |                      -0.076 |                   10 | True      |            0.038 |
| Hong Kong | overnight persistence (21d overnight sum; close in, open out)       | +           |       35 |            4.122 |            3.785 |                   0.224 |               -9.835 |                      -0.582 |                   32 | True      |            0.071 |
| Hong Kong | end-of-day fade (against today's open-to-close; close in, open out) | +           |       35 |            1.25  |           -1.271 |                  -0.077 |              -14.53  |                      -0.884 |                   32 | True      |            0.071 |
| Hong Kong | 1-day reversal (against today's close-to-close; close to close)     | -           |       35 |            1.924 |            0.284 |                   0.032 |               -5.161 |                      -0.588 |                   32 | True      |            0.071 |
| Hong Kong | 5-day reversal (close to close)                                     | -           |       35 |            0.016 |            0.265 |                   0.032 |               -2.048 |                      -0.251 |                   32 | True      |            0.071 |
| Korea     | overnight persistence (21d overnight sum; close in, open out)       | +           |       28 |            4.223 |            3.124 |                   0.203 |               -5.789 |                      -0.376 |                   23 | False     |            0.07  |
| Korea     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       28 |            2.257 |            1.735 |                   0.124 |               -6.38  |                      -0.456 |                   23 | False     |            0.07  |
| Korea     | 1-day reversal (against today's close-to-close; close to close)     | -           |       28 |            2.492 |           -1.967 |                  -0.254 |               -5.537 |                      -0.716 |                   23 | False     |            0.07  |
| Korea     | 5-day reversal (close to close)                                     | +           |       28 |            1.5   |            1.138 |                   0.162 |               -0.372 |                      -0.053 |                   23 | False     |            0.07  |
| Taiwan    | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.002 |            4.775 |                   0.278 |               -9.508 |                      -0.554 |                   33 | False     |            0.103 |
| Taiwan    | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            1.39  |            0.938 |                   0.057 |              -12.825 |                      -0.775 |                   33 | False     |            0.103 |
| Taiwan    | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.339 |           -1.868 |                  -0.19  |               -8.309 |                      -0.848 |                   33 | False     |            0.103 |
| Taiwan    | 5-day reversal (close to close)                                     | +           |       30 |            2.238 |            0.813 |                   0.088 |               -2.081 |                      -0.225 |                   33 | False     |            0.103 |
| Australia | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            2.556 |            1.832 |                   0.111 |               -4.811 |                      -0.292 |                   16 | True      |            0.038 |
| Australia | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            0.498 |           -0.755 |                  -0.046 |               -7.439 |                      -0.449 |                   16 | True      |            0.038 |
| Australia | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.433 |            0.633 |                   0.065 |               -2.379 |                      -0.245 |                   16 | True      |            0.038 |
| Australia | 5-day reversal (close to close)                                     | +           |       30 |            0.639 |            0.267 |                   0.028 |               -1.122 |                      -0.117 |                   16 | True      |            0.038 |
| India     | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.675 |            4.545 |                   0.155 |              -13.982 |                      -0.475 |                   25 | False     |            0.014 |
| India     | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            3.319 |            0.599 |                   0.023 |              -15.748 |                      -0.607 |                   25 | False     |            0.014 |
| India     | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.835 |           -0.832 |                  -0.077 |               -6.26  |                      -0.58  |                   25 | False     |            0.014 |
| India     | 5-day reversal (close to close)                                     | +           |       30 |            1.182 |            0.879 |                   0.086 |               -1.52  |                      -0.149 |                   25 | False     |            0.014 |

Costs used (round trip at the auctions):

| market    |   round_trip_cost_bp | on_ibkr   | what                                                                          |
|:----------|---------------------:|:----------|:------------------------------------------------------------------------------|
| Japan     |                   10 | True      | 0.05% commission each side, no stamp duty                                     |
| Hong Kong |                   32 | True      | 0.05% commission + 0.1% stamp duty each side (0.13% Aug 2021-Nov 2023) + fees |
| Australia |                   16 | True      | 0.08% commission each side, no stamp duty                                     |
| Korea     |                   23 | False     | securities transaction tax ~0.18-0.25% on sales + broker fees; not on IBKR    |
| Taiwan    |                   33 | False     | 0.3% transaction tax on sales + broker fees; not on IBKR                      |
| India     |                   25 | False     | 0.1% STT each side + fees; not open to non-resident IBKR accounts             |
| US        |                    0 | True      | IBKR Lite / Alpaca: no commission; SEC + TAF fees under 0.3 bp                |

