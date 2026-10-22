## Asian markets

Daily Yahoo data since 2005; directions chosen on 2006-2014, checked on 2015-2026. An Asian session on date D falls between the US sessions of D-1 and D. Opening prices Yahoo copied from the previous close are dropped (share per ticker in asia_data_quality.csv).

### 1. Lead-lag between the US and Asian indices

'gap' = previous close -> open (the news is absorbed here: descriptive); 'after the open' = open -> close. Each market twice: the index (whose first value of the day still holds yesterday's prices for stocks that haven't opened yet - Sydney opens in alphabetical groups over 10 minutes - so 'after the open' partly repeats the gap and looks predictable) and an index ETF, whose open is a price you could actually trade. Only the ETF rows count as tradable evidence; index futures also trade overnight, so their open has already absorbed the US day.

| market         | instrument   | signal                                    | target                    | tradable   |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:---------------|:-------------|:------------------------------------------|:--------------------------|:-----------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| Japan          | ^N225        | US close-to-close (D-1)                   | Japan: gap                | False      |          0.677 |      31.783 |        2205 |          0.619 |      33.238 |        2882 |
| Japan          | ^N225        | US close-to-close (D-1)                   | Japan: after the open     | True       |          0.287 |      13.478 |        2205 |          0.129 |       6.945 |        2882 |
| Japan          | ^N225        | US open-to-close (D-1)                    | Japan: after the open     | True       |          0.25  |      11.756 |        2205 |          0.141 |       7.552 |        2882 |
| Japan          | ^N225        | Japan close-to-close (D)                  | US: US gap                | False      |          0.284 |      13.464 |        2245 |          0.301 |      16.368 |        2949 |
| Japan          | ^N225        | Japan close-to-close (D)                  | US: US after the open     | True       |         -0.055 |      -2.612 |        2245 |         -0.025 |      -1.339 |        2949 |
| Japan          | ^N225        | Japan open-to-close (D)                   | US: US after the open     | True       |         -0.04  |      -1.881 |        2245 |          0.004 |       0.226 |        2949 |
| Hong Kong      | ^HSI         | US close-to-close (D-1)                   | Hong Kong: gap            | False      |          0.709 |      33.398 |        2218 |          0.505 |      27.228 |        2904 |
| Hong Kong      | ^HSI         | US close-to-close (D-1)                   | Hong Kong: after the open | True       |         -0.126 |      -5.953 |        2218 |         -0.086 |      -4.629 |        2904 |
| Hong Kong      | ^HSI         | US open-to-close (D-1)                    | Hong Kong: after the open | True       |         -0.094 |      -4.407 |        2218 |         -0.054 |      -2.894 |        2904 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D)              | US: US gap                | False      |          0.403 |      19.081 |        2247 |          0.318 |      17.302 |        2953 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D)              | US: US after the open     | True       |          0.053 |       2.497 |        2247 |         -0.035 |      -1.908 |        2953 |
| Hong Kong      | ^HSI         | Hong Kong open-to-close (D)               | US: US after the open     | True       |          0.159 |       7.55  |        2247 |         -0.006 |      -0.345 |        2953 |
| China          | 000001.SS    | US close-to-close (D-1)                   | China: gap                | False      |          0.535 |      25.004 |        2182 |          0.421 |      22.505 |        2864 |
| China          | 000001.SS    | US close-to-close (D-1)                   | China: after the open     | True       |         -0.071 |      -3.302 |        2182 |         -0.051 |      -2.741 |        2864 |
| China          | 000001.SS    | US open-to-close (D-1)                    | China: after the open     | True       |         -0.025 |      -1.167 |        2182 |         -0.017 |      -0.892 |        2864 |
| China          | 000001.SS    | China close-to-close (D)                  | US: US gap                | False      |          0.173 |       8.122 |        2206 |          0.207 |      11.17  |        2899 |
| China          | 000001.SS    | China close-to-close (D)                  | US: US after the open     | True       |         -0.015 |      -0.724 |        2206 |          0.002 |       0.127 |        2899 |
| China          | 000001.SS    | China open-to-close (D)                   | US: US after the open     | True       |          0.021 |       0.983 |        2206 |          0.01  |       0.528 |        2899 |
| Korea          | ^KS11        | US close-to-close (D-1)                   | Korea: gap                | False      |          0.769 |      36.295 |        2230 |          0.574 |      30.803 |        2884 |
| Korea          | ^KS11        | US close-to-close (D-1)                   | Korea: after the open     | True       |         -0.178 |      -8.421 |        2230 |         -0.058 |      -3.119 |        2884 |
| Korea          | ^KS11        | US open-to-close (D-1)                    | Korea: after the open     | True       |         -0.155 |      -7.309 |        2230 |         -0.066 |      -3.521 |        2884 |
| Korea          | ^KS11        | Korea close-to-close (D)                  | US: US gap                | False      |          0.356 |      16.882 |        2247 |          0.283 |      15.386 |        2946 |
| Korea          | ^KS11        | Korea close-to-close (D)                  | US: US after the open     | True       |          0.035 |       1.674 |        2247 |         -0.033 |      -1.778 |        2946 |
| Korea          | ^KS11        | Korea open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.493 |        2247 |         -0.007 |      -0.392 |        2946 |
| Taiwan         | ^TWII        | US close-to-close (D-1)                   | Taiwan: gap               | False      |          0.734 |      34.612 |        2221 |          0.572 |      30.569 |        2860 |
| Taiwan         | ^TWII        | US close-to-close (D-1)                   | Taiwan: after the open    | True       |         -0.177 |      -8.355 |        2221 |          0.213 |      11.41  |        2860 |
| Taiwan         | ^TWII        | US open-to-close (D-1)                    | Taiwan: after the open    | True       |         -0.136 |      -6.42  |        2221 |          0.21  |      11.241 |        2860 |
| Taiwan         | ^TWII        | Taiwan close-to-close (D)                 | US: US gap                | False      |          0.298 |      14.007 |        2216 |          0.283 |      15.292 |        2912 |
| Taiwan         | ^TWII        | Taiwan close-to-close (D)                 | US: US after the open     | True       |         -0.01  |      -0.479 |        2216 |         -0.06  |      -3.256 |        2912 |
| Taiwan         | ^TWII        | Taiwan open-to-close (D)                  | US: US after the open     | True       |          0.07  |       3.311 |        2216 |         -0.046 |      -2.462 |        2909 |
| Australia      | ^AXJO        | US close-to-close (D-1)                   | Australia: gap            | False      |          0.754 |      31.388 |        1732 |          0.44  |      12.638 |         825 |
| Australia      | ^AXJO        | US close-to-close (D-1)                   | Australia: after the open | True       |          0.445 |      18.537 |        1732 |          0.481 |      13.803 |         825 |
| Australia      | ^AXJO        | US open-to-close (D-1)                    | Australia: after the open | True       |          0.445 |      18.504 |        1732 |          0.449 |      12.891 |         825 |
| Australia      | ^AXJO        | Australia close-to-close (D)              | US: US gap                | False      |          0.3   |      14.21  |        2247 |          0.4   |      21.728 |        2953 |
| Australia      | ^AXJO        | Australia close-to-close (D)              | US: US after the open     | True       |          0.011 |       0.528 |        2247 |          0.02  |       1.112 |        2953 |
| Australia      | ^AXJO        | Australia open-to-close (D)               | US: US after the open     | True       |          0.046 |       2.008 |        1905 |         -0.017 |      -0.605 |        1244 |
| India          | ^BSESN       | US close-to-close (D-1)                   | India: gap                | False      |          0.621 |      29.118 |        2198 |          0.475 |      25.574 |        2904 |
| India          | ^BSESN       | US close-to-close (D-1)                   | India: after the open     | True       |         -0.062 |      -2.897 |        2198 |         -0.012 |      -0.623 |        2904 |
| India          | ^BSESN       | US open-to-close (D-1)                    | India: after the open     | True       |          0.034 |       1.577 |        2198 |          0.02  |       1.074 |        2904 |
| India          | ^BSESN       | India close-to-close (D)                  | US: US gap                | False      |          0.384 |      18.2   |        2247 |          0.394 |      21.42  |        2953 |
| India          | ^BSESN       | India close-to-close (D)                  | US: US after the open     | True       |          0.093 |       4.432 |        2247 |         -0.013 |      -0.693 |        2953 |
| India          | ^BSESN       | India open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.499 |        2247 |          0.013 |       0.712 |        2953 |
| Singapore      | ^STI         | US close-to-close (D-1)                   | Singapore: gap            | False      |          0.717 |      23.954 |        1117 |          0.608 |      33.042 |        2958 |
| Singapore      | ^STI         | US close-to-close (D-1)                   | Singapore: after the open | True       |         -0.076 |      -2.557 |        1117 |         -0.02  |      -1.092 |        2958 |
| Singapore      | ^STI         | US open-to-close (D-1)                    | Singapore: after the open | True       |         -0.029 |      -0.953 |        1117 |         -0.024 |      -1.281 |        2958 |
| Singapore      | ^STI         | Singapore close-to-close (D)              | US: US gap                | False      |          0.445 |      21.099 |        2247 |          0.363 |      19.73  |        2953 |
| Singapore      | ^STI         | Singapore close-to-close (D)              | US: US after the open     | True       |          0.048 |       2.277 |        2247 |         -0.044 |      -2.375 |        2953 |
| Singapore      | ^STI         | Singapore open-to-close (D)               | US: US after the open     | True       |          0.047 |       1.694 |        1301 |         -0.006 |      -0.318 |        2953 |
| Asia (average) | nan          | Asian markets' average close-to-close (D) | US gap                    | False      |          0.44  |      20.857 |        2247 |          0.447 |      24.301 |        2953 |
| Asia (average) | nan          | Asian markets' average close-to-close (D) | US after the open         | True       |          0.027 |       1.271 |        2247 |         -0.035 |      -1.884 |        2953 |
| Japan          | 1321.T       | US close-to-close (D-1)                   | Japan: gap                | False      |          0.729 |      11.128 |         233 |          0.038 |       1.45  |        1494 |
| Japan          | 1321.T       | US close-to-close (D-1)                   | Japan: after the open     | True       |         -0.04  |      -0.608 |         234 |         -0.109 |      -4.204 |        1494 |
| Japan          | 1321.T       | US open-to-close (D-1)                    | Japan: after the open     | True       |         -0.027 |      -0.413 |         234 |         -0.1   |      -3.858 |        1494 |
| Japan          | 1321.T       | Japan close-to-close (D)                  | US: US gap                | False      |          0.233 |       3.72  |         255 |          0.015 |       0.587 |        1595 |
| Japan          | 1321.T       | Japan close-to-close (D)                  | US: US after the open     | True       |          0.061 |       0.979 |         255 |         -0.008 |      -0.337 |        1595 |
| Japan          | 1321.T       | Japan open-to-close (D)                   | US: US after the open     | True       |          0.009 |       0.137 |         256 |          0.082 |       3.28  |        1595 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1)                   | Hong Kong: gap            | False      |          0.651 |      23.512 |        1303 |          0.531 |      27.436 |        2671 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1)                   | Hong Kong: after the open | True       |         -0.011 |      -0.403 |        1303 |         -0.029 |      -1.489 |        2671 |
| Hong Kong      | 2800.HK      | US open-to-close (D-1)                    | Hong Kong: after the open | True       |          0.057 |       2.062 |        1303 |         -0.02  |      -1.025 |        2671 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D)              | US: US gap                | False      |          0.399 |      16.693 |        1750 |          0.259 |      14.078 |        2953 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D)              | US: US after the open     | True       |          0.062 |       2.576 |        1750 |         -0.044 |      -2.375 |        2953 |
| Hong Kong      | 2800.HK      | Hong Kong open-to-close (D)               | US: US after the open     | True       |          0.047 |       1.812 |        1496 |         -0.005 |      -0.268 |        2943 |
| Australia      | STW.AX       | US close-to-close (D-1)                   | Australia: gap            | False      |          0.692 |      26.72  |        1491 |          0.674 |      36.534 |        2938 |
| Australia      | STW.AX       | US close-to-close (D-1)                   | Australia: after the open | True       |         -0.1   |      -3.864 |        1491 |         -0.2   |     -10.821 |        2938 |
| Australia      | STW.AX       | US open-to-close (D-1)                    | Australia: after the open | True       |         -0.079 |      -3.038 |        1491 |         -0.089 |      -4.848 |        2938 |
| Australia      | STW.AX       | Australia close-to-close (D)              | US: US gap                | False      |          0.324 |      13.538 |        1750 |          0.401 |      21.787 |        2953 |
| Australia      | STW.AX       | Australia close-to-close (D)              | US: US after the open     | True       |          0.061 |       2.534 |        1750 |          0.015 |       0.812 |        2953 |
| Australia      | STW.AX       | Australia open-to-close (D)               | US: US after the open     | True       |          0.178 |       6.876 |        1500 |          0.103 |       5.577 |        2953 |
| Korea          | 069500.KS    | US close-to-close (D-1)                   | Korea: gap                | False      |          0.744 |      27.956 |        1412 |          0.521 |      27.68  |        2827 |
| Korea          | 069500.KS    | US close-to-close (D-1)                   | Korea: after the open     | True       |         -0.036 |      -1.366 |        1413 |         -0.078 |      -4.134 |        2827 |
| Korea          | 069500.KS    | US open-to-close (D-1)                    | Korea: after the open     | True       |         -0.016 |      -0.587 |        1413 |         -0.074 |      -3.908 |        2827 |
| Korea          | 069500.KS    | Korea close-to-close (D)                  | US: US gap                | False      |          0.284 |      10.785 |        1438 |          0.276 |      14.973 |        2945 |
| Korea          | 069500.KS    | Korea close-to-close (D)                  | US: US after the open     | True       |          0.019 |       0.72  |        1438 |         -0.031 |      -1.687 |        2945 |
| Korea          | 069500.KS    | Korea open-to-close (D)                   | US: US after the open     | True       |          0.064 |       2.433 |        1439 |          0.003 |       0.172 |        2945 |
| Taiwan         | 0050.TW      | US close-to-close (D-1)                   | Taiwan: gap               | False      |          0.081 |       3.038 |        1397 |          0.564 |      29.556 |        2743 |
| Taiwan         | 0050.TW      | US close-to-close (D-1)                   | Taiwan: after the open    | True       |          0.087 |       3.255 |        1397 |         -0.038 |      -1.994 |        2743 |
| Taiwan         | 0050.TW      | US open-to-close (D-1)                    | Taiwan: after the open    | True       |          0.06  |       2.244 |        1397 |          0     |       0.007 |        2743 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D)                 | US: US gap                | False      |          0.096 |       3.678 |        1478 |          0.278 |      14.979 |        2912 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D)                 | US: US after the open     | True       |          0.033 |       1.267 |        1478 |         -0.058 |      -3.139 |        2912 |
| Taiwan         | 0050.TW      | Taiwan open-to-close (D)                  | US: US after the open     | True       |          0.001 |       0.045 |        1478 |         -0.037 |      -2.001 |        2909 |
| India          | NIFTYBEES.NS | US close-to-close (D-1)                   | India: gap                | False      |          0.198 |       6.992 |        1245 |          0.052 |       2.764 |        2804 |
| India          | NIFTYBEES.NS | US close-to-close (D-1)                   | India: after the open     | True       |         -0.045 |      -1.593 |        1246 |         -0.02  |      -1.081 |        2804 |
| India          | NIFTYBEES.NS | US open-to-close (D-1)                    | India: after the open     | True       |          0.017 |       0.603 |        1246 |         -0.027 |      -1.434 |        2804 |
| India          | NIFTYBEES.NS | India close-to-close (D)                  | US: US gap                | False      |          0.29  |      11.211 |        1499 |          0.061 |       3.31  |        2953 |
| India          | NIFTYBEES.NS | India close-to-close (D)                  | US: US after the open     | True       |          0.094 |       3.645 |        1499 |         -0.01  |      -0.521 |        2953 |
| India          | NIFTYBEES.NS | India open-to-close (D)                   | US: US after the open     | True       |          0.068 |       2.499 |        1338 |          0.011 |       0.595 |        2952 |
| Singapore      | ES3.SI       | US close-to-close (D-1)                   | Singapore: gap            | False      |          0.576 |      19.894 |        1194 |          0.549 |      28.522 |        2701 |
| Singapore      | ES3.SI       | US close-to-close (D-1)                   | Singapore: after the open | True       |          0.04  |       1.385 |        1194 |          0.083 |       4.312 |        2701 |
| Singapore      | ES3.SI       | US open-to-close (D-1)                    | Singapore: after the open | True       |          0.105 |       3.619 |        1194 |          0.076 |       3.943 |        2701 |
| Singapore      | ES3.SI       | Singapore close-to-close (D)              | US: US gap                | False      |          0.441 |      18.46  |        1750 |          0.368 |      19.99  |        2953 |
| Singapore      | ES3.SI       | Singapore close-to-close (D)              | US: US after the open     | True       |          0.02  |       0.837 |        1750 |         -0.045 |      -2.423 |        2953 |
| Singapore      | ES3.SI       | Singapore open-to-close (D)               | US: US after the open     | True       |          0.085 |       3.275 |        1495 |          0.005 |       0.29  |        2950 |
| China          | 510300.SS    | US close-to-close (D-1)                   | China: gap                | False      |          0.331 |       7.982 |         580 |          0.378 |      20.061 |        2819 |
| China          | 510300.SS    | US close-to-close (D-1)                   | China: after the open     | True       |         -0.004 |      -0.097 |         580 |         -0.014 |      -0.736 |        2819 |
| China          | 510300.SS    | US open-to-close (D-1)                    | China: after the open     | True       |          0.054 |       1.289 |         580 |         -0.001 |      -0.052 |        2819 |
| China          | 510300.SS    | China close-to-close (D)                  | US: US gap                | False      |          0.155 |       3.944 |         650 |          0.218 |      11.715 |        2899 |
| China          | 510300.SS    | China close-to-close (D)                  | US: US after the open     | True       |         -0.024 |      -0.6   |         650 |          0.01  |       0.532 |        2899 |
| China          | 510300.SS    | China open-to-close (D)                   | US: US after the open     | True       |         -0.041 |      -1.014 |         604 |          0.017 |       0.901 |        2899 |

Trading the sign of the signal on the 'after the open' leg (cost: 0 bp for SPY at the auctions; 2 bp for an index (as if futures, flattering - see above); each ETF at its market's round trip):

| market         | instrument   | strategy                                             | direction   |   sharpe_2006_14 |   sharpe_2015_26 |   net_sharpe_2015_26 |   avg_bp_2015_26 |   cost_bp |
|:---------------|:-------------|:-----------------------------------------------------|:------------|-----------------:|-----------------:|---------------------:|-----------------:|----------:|
| Japan          | ^N225        | US close-to-close (D-1) -> Japan after the open      | +           |            1.144 |            0.779 |                0.455 |            4.794 |         2 |
| Japan          | ^N225        | US open-to-close (D-1) -> Japan after the open       | +           |            1.339 |            0.79  |                0.465 |            4.865 |         2 |
| Japan          | ^N225        | Japan close-to-close (D) -> US US after the open     | +           |            0.156 |           -0.118 |               -0.118 |           -0.62  |         0 |
| Japan          | ^N225        | Japan open-to-close (D) -> US US after the open      | +           |            0.269 |            0.19  |                0.19  |            0.998 |         0 |
| Hong Kong      | ^HSI         | US close-to-close (D-1) -> Hong Kong after the open  | -           |            1.096 |            0.853 |                0.54  |            5.45  |         2 |
| Hong Kong      | ^HSI         | US open-to-close (D-1) -> Hong Kong after the open   | -           |            0.602 |            0.625 |                0.313 |            4.001 |         2 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D) -> US US after the open | +           |            0.273 |           -0.428 |               -0.428 |           -2.246 |         0 |
| Hong Kong      | ^HSI         | Hong Kong open-to-close (D) -> US US after the open  | +           |            0.96  |            0.151 |                0.151 |            0.794 |         0 |
| China          | 000001.SS    | US close-to-close (D-1) -> China after the open      | -           |            0.024 |            0.157 |               -0.129 |            1.094 |         2 |
| China          | 000001.SS    | US open-to-close (D-1) -> China after the open       | +           |            0.315 |           -0.264 |               -0.55  |           -1.839 |         2 |
| China          | 000001.SS    | China close-to-close (D) -> US US after the open     | +           |            0.027 |           -0.182 |               -0.182 |           -0.956 |         0 |
| China          | 000001.SS    | China open-to-close (D) -> US US after the open      | -           |            0.116 |           -0.407 |               -0.407 |           -2.14  |         0 |
| Korea          | ^KS11        | US close-to-close (D-1) -> Korea after the open      | -           |            1.471 |            0.554 |                0.263 |            3.798 |         2 |
| Korea          | ^KS11        | US open-to-close (D-1) -> Korea after the open       | -           |            1.122 |            0.787 |                0.495 |            5.398 |         2 |
| Korea          | ^KS11        | Korea close-to-close (D) -> US US after the open     | +           |            0.549 |           -0.245 |               -0.245 |           -1.285 |         0 |
| Korea          | ^KS11        | Korea open-to-close (D) -> US US after the open      | +           |            0.718 |           -0.067 |               -0.067 |           -0.354 |         0 |
| Taiwan         | ^TWII        | US close-to-close (D-1) -> Taiwan after the open     | -           |            1.744 |           -2.97  |               -3.345 |          -15.849 |         2 |
| Taiwan         | ^TWII        | US open-to-close (D-1) -> Taiwan after the open      | -           |            0.762 |           -2.125 |               -2.496 |          -11.433 |         2 |
| Taiwan         | ^TWII        | Taiwan close-to-close (D) -> US US after the open    | -           |            0.005 |           -0.059 |               -0.059 |           -0.309 |         0 |
| Taiwan         | ^TWII        | Taiwan open-to-close (D) -> US US after the open     | +           |            0.759 |            0.151 |                0.151 |            0.797 |         0 |
| Australia      | ^AXJO        | US close-to-close (D-1) -> Australia after the open  | +           |            5.163 |            5.862 |                5.415 |           26.169 |         2 |
| Australia      | ^AXJO        | US open-to-close (D-1) -> Australia after the open   | +           |            5.002 |            5     |                4.559 |           22.701 |         2 |
| Australia      | ^AXJO        | Australia close-to-close (D) -> US US after the open | +           |            0.075 |           -0.062 |               -0.062 |           -0.323 |         0 |
| Australia      | ^AXJO        | Australia open-to-close (D) -> US US after the open  | +           |            0.442 |           -0.095 |               -0.095 |           -0.522 |         0 |
| India          | ^BSESN       | US close-to-close (D-1) -> India after the open      | +           |            0.238 |           -0.22  |               -0.589 |           -1.191 |         2 |
| India          | ^BSESN       | US open-to-close (D-1) -> India after the open       | +           |            1.102 |            0.263 |               -0.107 |            1.423 |         2 |
| India          | ^BSESN       | India close-to-close (D) -> US US after the open     | +           |            0.644 |           -0.002 |               -0.002 |           -0.009 |         0 |
| India          | ^BSESN       | India open-to-close (D) -> US US after the open      | +           |            0.807 |            0.017 |                0.017 |            0.091 |         0 |
| Singapore      | ^STI         | US close-to-close (D-1) -> Singapore after the open  | -           |            0.774 |            0.037 |               -0.478 |            0.144 |         2 |
| Singapore      | ^STI         | US open-to-close (D-1) -> Singapore after the open   | -           |            0.395 |            0.451 |               -0.065 |            1.747 |         2 |
| Singapore      | ^STI         | Singapore close-to-close (D) -> US US after the open | +           |            0.608 |           -0.414 |               -0.414 |           -2.17  |         0 |
| Singapore      | ^STI         | Singapore open-to-close (D) -> US US after the open  | +           |            0.265 |            0.03  |                0.03  |            0.16  |         0 |
| Asia (average) | nan          | Asia average (D) -> SPY open-to-close (D)            | +           |            0.592 |           -0.147 |               -0.147 |           -0.77  |         0 |
| Japan          | 1321.T       | US close-to-close (D-1) -> Japan after the open      | -           |            1.048 |            1.32  |               -0.349 |            7.894 |        10 |
| Japan          | 1321.T       | US open-to-close (D-1) -> Japan after the open       | -           |            0.424 |            1.09  |               -0.58  |            6.528 |        10 |
| Japan          | 1321.T       | Japan close-to-close (D) -> US US after the open     | +           |            0.588 |           -0.213 |               -0.213 |           -1.109 |         0 |
| Japan          | 1321.T       | Japan open-to-close (D) -> US US after the open      | +           |            0.438 |            0.495 |                0.495 |            2.59  |         0 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1) -> Hong Kong after the open  | +           |            0.161 |           -0.435 |               -2.071 |           -2.917 |        11 |
| Hong Kong      | 2800.HK      | US open-to-close (D-1) -> Hong Kong after the open   | +           |            1.131 |           -0.302 |               -1.941 |           -2.027 |        11 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D) -> US US after the open | +           |            0.193 |           -0.306 |               -0.306 |           -1.579 |         0 |
| Hong Kong      | 2800.HK      | Hong Kong open-to-close (D) -> US US after the open  | +           |            0.58  |            0.031 |                0.031 |            0.164 |         0 |
| Australia      | STW.AX       | US close-to-close (D-1) -> Australia after the open  | -           |            0.912 |            0.943 |               -2.651 |            4.192 |        16 |
| Australia      | STW.AX       | US open-to-close (D-1) -> Australia after the open   | -           |            0.5   |            0.707 |               -2.89  |            3.145 |        16 |
| Australia      | STW.AX       | Australia close-to-close (D) -> US US after the open | +           |            0.827 |           -0.041 |               -0.041 |           -0.214 |         0 |
| Australia      | STW.AX       | Australia open-to-close (D) -> US US after the open  | +           |            1.82  |            0.627 |                0.627 |            3.289 |         0 |
| Korea          | 069500.KS    | US close-to-close (D-1) -> Korea after the open      | -           |            0.118 |            0.723 |                0.004 |            5.019 |         5 |
| Korea          | 069500.KS    | US open-to-close (D-1) -> Korea after the open       | +           |            0.495 |           -0.875 |               -1.596 |           -6.075 |         5 |
| Korea          | 069500.KS    | Korea close-to-close (D) -> US US after the open     | +           |            0.313 |           -0.042 |               -0.042 |           -0.22  |         0 |
| Korea          | 069500.KS    | Korea open-to-close (D) -> US US after the open      | +           |            0.425 |            0.162 |                0.162 |            0.852 |         0 |
| Taiwan         | 0050.TW      | US close-to-close (D-1) -> Taiwan after the open     | +           |            0.713 |            0.567 |               -1.976 |            2.893 |        13 |
| Taiwan         | 0050.TW      | US open-to-close (D-1) -> Taiwan after the open      | +           |            0.771 |            0.062 |               -2.485 |            0.317 |        13 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D) -> US US after the open    | +           |            0.168 |           -0.192 |               -0.192 |           -0.996 |         0 |
| Taiwan         | 0050.TW      | Taiwan open-to-close (D) -> US US after the open     | +           |            0.808 |           -0.132 |               -0.132 |           -0.697 |         0 |
| India          | NIFTYBEES.NS | US close-to-close (D-1) -> India after the open      | -           |            0.271 |            0.75  |               -0.896 |           11.372 |        25 |
| India          | NIFTYBEES.NS | US open-to-close (D-1) -> India after the open       | +           |            0.291 |           -0.743 |               -2.388 |          -11.287 |        25 |
| India          | NIFTYBEES.NS | India close-to-close (D) -> US US after the open     | +           |            0.706 |            0.113 |                0.113 |            0.594 |         0 |
| India          | NIFTYBEES.NS | India open-to-close (D) -> US US after the open      | +           |            1.088 |           -0.307 |               -0.307 |           -1.613 |         0 |
| Singapore      | ES3.SI       | US close-to-close (D-1) -> Singapore after the open  | +           |            0.734 |            1.441 |               -2.246 |            6.243 |        16 |
| Singapore      | ES3.SI       | US open-to-close (D-1) -> Singapore after the open   | +           |            1.454 |            1.078 |               -2.605 |            4.683 |        16 |
| Singapore      | ES3.SI       | Singapore close-to-close (D) -> US US after the open | +           |            0.492 |           -0.261 |               -0.261 |           -1.337 |         0 |
| Singapore      | ES3.SI       | Singapore open-to-close (D) -> US US after the open  | +           |            0.826 |           -0.013 |               -0.013 |           -0.068 |         0 |
| China          | 510300.SS    | US close-to-close (D-1) -> China after the open      | -           |            0.085 |           -0.115 |               -0.878 |           -0.906 |         6 |
| China          | 510300.SS    | US open-to-close (D-1) -> China after the open       | +           |            0.715 |           -0.105 |               -0.868 |           -0.822 |         6 |
| China          | 510300.SS    | China close-to-close (D) -> US US after the open     | +           |            0.078 |           -0.004 |               -0.004 |           -0.022 |         0 |
| China          | 510300.SS    | China open-to-close (D) -> US US after the open      | -           |            0.273 |           -0.327 |               -0.327 |           -1.722 |         0 |

### 2. ADRs vs their home listings

Residual = the home listing's last session in dollars minus the ADR's opening gap. Pooled long / short book on Alpaca (market-on-open in, market-on-close out). Yahoo dates FX bars by their London / New York close, after the US open, so the clean variant uses the previous day's FX move; the same-day variant is shown only to measure how much the peek was worth:

| strategy                                     | variant                                        | direction   |   cost_bp_round_trip |   sharpe_2006_14 |   sharpe_2015_26 |   avg_bp_2015_26 |   adrs_per_day_2015_26 |
|:---------------------------------------------|:-----------------------------------------------|:------------|---------------------:|-----------------:|-----------------:|-----------------:|-----------------------:|
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    0 |            4.04  |            2.914 |            8.685 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    1 |            3.819 |            2.578 |            8.685 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    3 |            3.378 |            1.907 |            8.685 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    0 |            4.06  |            3.306 |            9.727 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    1 |            3.836 |            2.966 |            9.727 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    3 |            3.389 |            2.287 |            9.727 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    0 |            4.362 |            2.912 |            8.838 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    1 |            4.138 |            2.583 |            8.838 |                 32.667 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    3 |            3.69  |            1.924 |            8.838 |                 32.667 |

Per ADR (correlations):

| adr   | home         | signal                        | target               |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:------|:-------------|:------------------------------|:---------------------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| BABA  | 9988.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.061 |       2.536 |        1730 |
| BABA  | 9988.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.062 |       2.572 |        1730 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.019 |       0.783 |        1649 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.704 |      28.588 |        1648 |
| JD    | 9618.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.051 |       2.019 |        1583 |
| JD    | 9618.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.037 |       1.462 |        1583 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.11  |       4.258 |        1501 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.705 |      27.289 |        1500 |
| BIDU  | 9888.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.059 |       2.222 |        1397 |
| BIDU  | 9888.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.072 |       2.681 |        1397 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.052 |       1.837 |        1259 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.74  |      26.251 |        1258 |
| NTES  | 9999.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.031 |       1.252 |        1590 |
| NTES  | 9999.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.022 |      -0.877 |        1590 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.069 |       2.686 |        1520 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.66  |      25.737 |        1519 |
| TCOM  | 9961.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |         -0     |      -0     |        1364 |
| TCOM  | 9961.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.019 |      -0.688 |        1364 |
| TCOM  | 9961.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.254 |       9.048 |        1269 |
| TCOM  | 9961.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.629 |      22.383 |        1268 |
| BILI  | 9626.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.02  |       0.726 |        1360 |
| BILI  | 9626.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.042 |       1.565 |        1360 |
| BILI  | 9626.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.109 |       3.824 |        1233 |
| BILI  | 9626.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.763 |      26.779 |        1232 |
| LI    | 2015.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.024 |       0.852 |        1275 |
| LI    | 2015.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.025 |       0.91  |        1275 |
| LI    | 2015.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.048 |       1.594 |        1120 |
| LI    | 2015.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.721 |      24.132 |        1119 |
| NIO   | 9866.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.012 |       0.386 |        1100 |
| NIO   | 9866.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.003 |      -0.096 |        1100 |
| NIO   | 9866.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.123 |       3.84  |         982 |
| NIO   | 9866.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.787 |      24.662 |         981 |
| XPEV  | 9868.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.01  |       0.35  |        1294 |
| XPEV  | 9868.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.066 |       2.368 |        1294 |
| XPEV  | 9868.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.082 |       2.82  |        1180 |
| XPEV  | 9868.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.757 |      25.982 |        1179 |
| YUMC  | 9987.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.064 |       2.483 |        1523 |
| YUMC  | 9987.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.034 |       1.316 |        1523 |
| YUMC  | 9987.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.235 |       8.943 |        1449 |
| YUMC  | 9987.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.599 |      22.802 |        1448 |
| ZTO   | 2057.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.126 |       4.88  |        1498 |
| ZTO   | 2057.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.06  |       2.313 |        1498 |
| ZTO   | 2057.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.196 |       7.373 |        1416 |
| ZTO   | 2057.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.619 |      23.301 |        1415 |
| TME   | 1698.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |         -0.028 |      -0.882 |        1000 |
| TME   | 1698.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.031 |      -0.974 |        1000 |
| TME   | 1698.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.25  |       7.608 |         929 |
| TME   | 1698.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.736 |      22.415 |         928 |
| BEKE  | 2423.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.091 |       3.008 |        1101 |
| BEKE  | 2423.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.044 |      -1.445 |        1101 |
| BEKE  | 2423.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.169 |       5.474 |        1050 |
| BEKE  | 2423.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.6   |      19.422 |        1049 |
| HTHT  | 1179.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.074 |       2.886 |        1513 |
| HTHT  | 1179.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.049 |       1.89  |        1513 |
| HTHT  | 1179.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.283 |      10.694 |        1426 |
| HTHT  | 1179.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.618 |      23.327 |        1425 |
| WB    | 9898.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.033 |       1.123 |        1167 |
| WB    | 9898.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.009 |      -0.322 |        1167 |
| WB    | 9898.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.359 |      12.084 |        1134 |
| WB    | 9898.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.559 |      18.816 |        1133 |
| BZ    | 2076.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.03  |       0.935 |         942 |
| BZ    | 2076.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.011 |      -0.34  |         942 |
| BZ    | 2076.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.273 |       6.473 |         563 |
| BZ    | 2076.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.556 |      13.173 |         562 |
| SONY  | 6758.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.058 |       2.748 |        2224 |         -0.006 |      -0.345 |        2926 |
| SONY  | 6758.T       | home move (USD)               | ADR open-to-close    |          0.107 |       5.034 |        2224 |          0.013 |       0.694 |        2926 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: after its open |          0.205 |       9.476 |        2127 |         -0.015 |      -0.794 |        2841 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: gap            |          0.43  |      19.825 |        2127 |          0.541 |      28.839 |        2841 |
| TM    | 7203.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.108 |       5.113 |        2250 |          0     |       0.006 |        2954 |
| TM    | 7203.T       | home move (USD)               | ADR open-to-close    |          0.119 |       5.637 |        2250 |          0.043 |       2.355 |        2954 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: after its open |          0.21  |       9.537 |        2064 |         -0.025 |      -1.359 |        2860 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: gap            |          0.393 |      17.876 |        2064 |          0.491 |      26.28  |        2860 |
| HMC   | 7267.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.16  |       7.547 |        2221 |          0.009 |       0.483 |        2904 |
| HMC   | 7267.T       | home move (USD)               | ADR open-to-close    |          0.155 |       7.301 |        2221 |          0.04  |       2.147 |        2904 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: after its open |          0.269 |      12.331 |        2099 |          0.029 |       1.524 |        2841 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: gap            |          0.337 |      15.46  |        2099 |          0.462 |      24.6   |        2841 |
| MUFG  | 8306.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.23  |      10.527 |        2088 |          0.071 |       3.696 |        2709 |
| MUFG  | 8306.T       | home move (USD)               | ADR open-to-close    |          0.095 |       4.327 |        2088 |          0.073 |       3.781 |        2709 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: after its open |          0.156 |       6.899 |        1968 |         -0.042 |      -2.259 |        2855 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: gap            |          0.285 |      12.636 |        1968 |          0.445 |      23.768 |        2855 |
| SMFG  | 8316.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.191 |       7.245 |        1437 |          0.033 |       1.734 |        2759 |
| SMFG  | 8316.T       | home move (USD)               | ADR open-to-close    |          0.09  |       3.418 |        1437 |          0.047 |       2.479 |        2759 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: after its open |          0.133 |       5.078 |        1463 |         -0.038 |      -2.047 |        2843 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: gap            |          0.29  |      11.081 |        1463 |          0.417 |      22.237 |        2843 |
| MFG   | 8411.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.262 |      11.167 |        1823 |          0.079 |       3.944 |        2522 |
| MFG   | 8411.T       | home move (USD)               | ADR open-to-close    |          0.178 |       7.582 |        1824 |          0.047 |       2.373 |        2522 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: after its open |          0.157 |       6.395 |        1662 |         -0.024 |      -1.263 |        2797 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: gap            |          0.227 |       9.241 |        1662 |          0.378 |      20.004 |        2797 |
| NMR   | 8604.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.155 |       7.202 |        2145 |          0.07  |       3.584 |        2642 |
| NMR   | 8604.T       | home move (USD)               | ADR open-to-close    |          0.167 |       7.741 |        2145 |          0.123 |       6.312 |        2642 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: after its open |          0.125 |       5.716 |        2091 |         -0.004 |      -0.226 |        2852 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: gap            |          0.399 |      18.224 |        2091 |          0.415 |      22.159 |        2852 |
| TAK   | 4502.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.217 |       7.571 |        1220 |          0.182 |       9.781 |        2877 |
| TAK   | 4502.T       | home move (USD)               | ADR open-to-close    |          0.041 |       1.448 |        1221 |          0.119 |       6.38  |        2877 |
| TAK   | 4502.T       | ADR open-to-close (US day)    | home: after its open |          0.011 |       0.359 |        1139 |          0.055 |       2.944 |        2842 |
| TAK   | 4502.T       | ADR open-to-close (US day)    | home: gap            |          0.181 |       6.102 |        1139 |          0.33  |      17.608 |        2842 |
| IX    | 8591.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.243 |      11.485 |        2241 |          0.133 |       7.175 |        2928 |
| IX    | 8591.T       | home move (USD)               | ADR open-to-close    |          0.24  |      11.356 |        2241 |          0.145 |       7.862 |        2928 |
| IX    | 8591.T       | ADR open-to-close (US day)    | home: after its open |          0.141 |       6.489 |        2125 |         -0.014 |      -0.729 |        2849 |
| IX    | 8591.T       | ADR open-to-close (US day)    | home: gap            |          0.374 |      17.254 |        2125 |          0.434 |      23.151 |        2849 |
| KB    | 105560.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.051 |       2.435 |        2242 |          0.067 |       3.62  |        2919 |
| KB    | 105560.KS    | home move (USD)               | ADR open-to-close    |          0.163 |       7.71  |        2242 |          0.09  |       4.877 |        2919 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: after its open |         -0.049 |      -1.896 |        1485 |          0.035 |       1.815 |        2755 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: gap            |          0.633 |      24.399 |        1485 |          0.399 |      20.964 |        2755 |
| SHG   | 055550.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.085 |       4.022 |        2251 |          0.168 |       9.055 |        2914 |
| SHG   | 055550.KS    | home move (USD)               | ADR open-to-close    |          0.157 |       7.464 |        2251 |          0.116 |       6.258 |        2914 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: after its open |         -0.091 |      -4.223 |        2136 |          0.018 |       0.965 |        2758 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: gap            |          0.554 |      25.583 |        2136 |          0.382 |      20.062 |        2758 |
| PKX   | 005490.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.074 |       3.489 |        2251 |          0.043 |       2.327 |        2944 |
| PKX   | 005490.KS    | home move (USD)               | ADR open-to-close    |          0.16  |       7.575 |        2251 |          0.029 |       1.598 |        2944 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: after its open |          0.013 |       0.604 |        2109 |          0.041 |       2.132 |        2735 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: gap            |          0.673 |      30.916 |        2109 |          0.456 |      23.827 |        2735 |
| LPL   | 034220.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.163 |       7.59  |        2159 |          0.182 |       9.372 |        2666 |
| LPL   | 034220.KS    | home move (USD)               | ADR open-to-close    |          0.204 |       9.47  |        2159 |          0.178 |       9.187 |        2666 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: after its open |         -0.013 |      -0.581 |        2159 |          0.037 |       1.888 |        2615 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: gap            |          0.569 |      26.419 |        2159 |          0.394 |      20.172 |        2615 |
| KEP   | 015760.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.17  |       7.961 |        2196 |          0.12  |       6.386 |        2822 |
| KEP   | 015760.KS    | home move (USD)               | ADR open-to-close    |          0.208 |       9.738 |        2196 |          0.125 |       6.646 |        2822 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: after its open |         -0.007 |      -0.304 |        2131 |          0.005 |       0.276 |        2724 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: gap            |          0.472 |      21.768 |        2131 |          0.309 |      16.122 |        2724 |
| SKM   | 017670.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.276 |      12.962 |        2210 |          0.095 |       5.11  |        2898 |
| SKM   | 017670.KS    | home move (USD)               | ADR open-to-close    |          0.174 |       8.158 |        2210 |          0.09  |       4.861 |        2898 |
| SKM   | 017670.KS    | ADR open-to-close (US day)    | home: after its open |          0.031 |       1.406 |        2002 |          0.043 |       2.21  |        2667 |
| SKM   | 017670.KS    | ADR open-to-close (US day)    | home: gap            |          0.353 |      15.811 |        2002 |          0.343 |      17.694 |        2667 |
| KT    | 030200.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.185 |       8.668 |        2202 |          0.178 |       9.492 |        2840 |
| KT    | 030200.KS    | home move (USD)               | ADR open-to-close    |          0.199 |       9.32  |        2202 |          0.137 |       7.304 |        2840 |
| KT    | 030200.KS    | ADR open-to-close (US day)    | home: after its open |         -0.049 |      -2.271 |        2107 |          0.113 |       5.801 |        2657 |
| KT    | 030200.KS    | ADR open-to-close (US day)    | home: gap            |          0.426 |      19.542 |        2107 |          0.227 |      11.694 |        2657 |
| WF    | 316140.KS    | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.198 |       8.636 |        1899 |
| WF    | 316140.KS    | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.265 |      11.543 |        1899 |
| WF    | 316140.KS    | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.018 |       0.752 |        1715 |
| WF    | 316140.KS    | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.304 |      12.574 |        1714 |
| IBN   | ICICIBANK.NS | home move (USD) minus ADR gap | ADR open-to-close    |          0.08  |       3.786 |        2243 |          0.082 |       4.373 |        2864 |
| IBN   | ICICIBANK.NS | home move (USD)               | ADR open-to-close    |          0.177 |       8.368 |        2243 |          0.117 |       6.244 |        2864 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: after its open |          0.153 |       7.186 |        2210 |          0.03  |       1.597 |        2899 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: gap            |          0.434 |      20.417 |        2210 |          0.498 |      26.824 |        2899 |
| HDB   | HDFCBANK.NS  | home move (USD) minus ADR gap | ADR open-to-close    |          0.08  |       3.795 |        2256 |          0.112 |       6.08  |        2929 |
| HDB   | HDFCBANK.NS  | home move (USD)               | ADR open-to-close    |          0.126 |       6.006 |        2256 |          0.149 |       8.081 |        2929 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: after its open |          0.089 |       4.185 |        2209 |          0.005 |       0.247 |        2902 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: gap            |          0.474 |      22.28  |        2209 |          0.404 |      21.757 |        2902 |
| INFY  | INFY.NS      | home move (USD) minus ADR gap | ADR open-to-close    |          0.055 |       2.591 |        2238 |          0.039 |       2.108 |        2890 |
| INFY  | INFY.NS      | home move (USD)               | ADR open-to-close    |          0.112 |       5.299 |        2238 |          0.018 |       0.944 |        2890 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: after its open |          0.158 |       7.446 |        2209 |          0.099 |       5.324 |        2907 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: gap            |          0.403 |      18.925 |        2209 |          0.49  |      26.413 |        2907 |
| WIT   | WIPRO.NS     | home move (USD) minus ADR gap | ADR open-to-close    |          0.242 |      11.401 |        2225 |          0.084 |       4.362 |        2701 |
| WIT   | WIPRO.NS     | home move (USD)               | ADR open-to-close    |          0.132 |       6.217 |        2225 |          0.038 |       1.979 |        2701 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: after its open |          0.048 |       2.239 |        2206 |          0.028 |       1.515 |        2882 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: gap            |          0.32  |      15.02  |        2206 |          0.363 |      19.504 |        2882 |
| RDY   | DRREDDY.NS   | home move (USD) minus ADR gap | ADR open-to-close    |          0.194 |       9.167 |        2234 |          0.149 |       8.022 |        2915 |
| RDY   | DRREDDY.NS   | home move (USD)               | ADR open-to-close    |          0.083 |       3.943 |        2234 |          0.191 |      10.301 |        2915 |
| RDY   | DRREDDY.NS   | ADR open-to-close (US day)    | home: after its open |          0.078 |       3.679 |        2209 |          0.083 |       4.486 |        2901 |
| RDY   | DRREDDY.NS   | ADR open-to-close (US day)    | home: gap            |          0.298 |      14.009 |        2209 |          0.428 |      23.035 |        2901 |
| TSM   | 2330.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.12  |       5.605 |        2171 |         -0.037 |      -1.976 |        2899 |
| TSM   | 2330.TW      | home move (USD)               | ADR open-to-close    |          0.12  |       5.581 |        2171 |         -0.069 |      -3.708 |        2899 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: after its open |          0.189 |       8.469 |        2008 |         -0.015 |      -0.756 |        2559 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: gap            |          0.137 |       6.125 |        2008 |          0.558 |      28.23  |        2559 |
| UMC   | 2303.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.141 |       6.292 |        1991 |          0.115 |       5.882 |        2635 |
| UMC   | 2303.TW      | home move (USD)               | ADR open-to-close    |          0.131 |       5.865 |        1991 |          0.116 |       5.953 |        2635 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: after its open |          0.155 |       6.81  |        1934 |         -0.064 |      -3.257 |        2556 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: gap            |          0.096 |       4.206 |        1934 |          0.479 |      24.233 |        2556 |
| ASX   | 3711.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.354 |      16.218 |        2101 |          0.02  |       1.066 |        2772 |
| ASX   | 3711.TW      | home move (USD)               | ADR open-to-close    |          0.264 |      12.113 |        2101 |          0.068 |       3.585 |        2772 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: after its open |         -0.045 |      -2.04  |        2092 |          0.011 |       0.556 |        2648 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: gap            |          0.389 |      17.795 |        2092 |          0.499 |      25.681 |        2648 |
| CHT   | 2412.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.132 |       6.152 |        2182 |          0.146 |       7.768 |        2850 |
| CHT   | 2412.TW      | home move (USD)               | ADR open-to-close    |          0.08  |       3.736 |        2182 |          0.109 |       5.805 |        2850 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: after its open |         -0.05  |      -2.174 |        1901 |          0.016 |       0.714 |        1994 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: gap            |          0.213 |       9.277 |        1901 |          0.192 |       8.555 |        1994 |
| BHP   | BHP.AX       | home move (USD) minus ADR gap | ADR open-to-close    |          0.006 |       0.281 |        2251 |          0.073 |       3.984 |        2942 |
| BHP   | BHP.AX       | home move (USD)               | ADR open-to-close    |          0.027 |       1.29  |        2251 |          0.053 |       2.872 |        2942 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: after its open |         -0.005 |      -0.247 |        2234 |         -0.012 |      -0.666 |        2946 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: gap            |          0.614 |      29.029 |        2234 |          0.509 |      27.651 |        2946 |

#### As the live trader can run it (Alpaca bars, 2016-20 picks the direction, 2021-26 checks)

The backtest's reference price is the official open, which isn't known when market-on-open orders must be in (9:28). Executable versions: the last pre-market trade before 9:25 on the free IEX feed (market-on-open in), or entering at 9:35 with market orders (paying the spread).

| variant                                                                        | direction   |   cost_bp_round_trip |   sharpe_2016_20 |   sharpe_2021_26 |   avg_bp_2021_26 |   adrs_per_day_2021_26 |
|:-------------------------------------------------------------------------------|:------------|---------------------:|-----------------:|-----------------:|-----------------:|-----------------------:|
| official open (backtest reference; not executable at the open)                 | +           |                    0 |            3.406 |            2.022 |            7.046 |                 39.502 |
| official open (backtest reference; not executable at the open)                 | +           |                    1 |            2.98  |            1.735 |            7.046 |                 39.502 |
| official open (backtest reference; not executable at the open)                 | +           |                    3 |            2.129 |            1.161 |            7.046 |                 39.502 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | +           |                    0 |            3.879 |            2.177 |            7.57  |                 39.502 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | +           |                    1 |            3.443 |            1.89  |            7.57  |                 39.502 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | +           |                    3 |            2.57  |            1.314 |            7.57  |                 39.502 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | -           |                    0 |          nan     |           -0.477 |           -6.136 |                  2.383 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | -           |                    1 |          nan     |           -0.555 |           -6.136 |                  2.383 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | -           |                    3 |          nan     |           -0.71  |           -6.136 |                  2.383 |
| official open -> enter 9:35 with market orders                                 | +           |                    3 |           -0.669 |           -0.269 |            2.132 |                 39.461 |
| official open -> enter 9:35 with market orders                                 | +           |                    6 |           -2.053 |           -1.199 |            2.132 |                 39.461 |
| official open -> enter 9:35 with market orders                                 | +           |                   10 |           -3.898 |           -2.439 |            2.132 |                 39.461 |

By market:

| variant                                                                        | market    |   adrs | direction   |   sharpe_2016_20 |   sharpe_2021_26 |   avg_bp_2021_26 |
|:-------------------------------------------------------------------------------|:----------|-------:|:------------|-----------------:|-----------------:|-----------------:|
| official open (backtest reference; not executable at the open)                 | Australia |      1 | +           |            0.892 |            0.862 |            6.423 |
| official open (backtest reference; not executable at the open)                 | China     |     16 | +           |            2.118 |            0.899 |            6.624 |
| official open (backtest reference; not executable at the open)                 | India     |      5 | +           |            2.131 |            2.849 |           10.868 |
| official open (backtest reference; not executable at the open)                 | Japan     |     10 | +           |            1.376 |            0.746 |            3.063 |
| official open (backtest reference; not executable at the open)                 | Korea     |      8 | +           |            3.229 |            2.844 |           11.751 |
| official open (backtest reference; not executable at the open)                 | Taiwan    |      4 | +           |            2.852 |            0.51  |            3.325 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | Australia |      1 | +           |            0.102 |            0.364 |            2.715 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | China     |     16 | +           |            0.816 |            0.56  |            4.26  |
| pre-market price before 9:25 -> market-on-open (else the last close)           | India     |      5 | +           |            1.976 |            3.218 |           13.12  |
| pre-market price before 9:25 -> market-on-open (else the last close)           | Japan     |     10 | +           |            2.506 |            1.528 |            5.828 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | Korea     |      8 | +           |            3.823 |            2.738 |           10.844 |
| pre-market price before 9:25 -> market-on-open (else the last close)           | Taiwan    |      4 | +           |            2.481 |            1.508 |            9.45  |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | Australia |      1 | -           |          nan     |          nan     |          -25.254 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | China     |     15 | -           |          nan     |           -0.302 |           -4.75  |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | India     |      5 | +           |          nan     |          nan     |           37.212 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | Japan     |     10 | +           |          nan     |           -0.229 |           -1.527 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | Korea     |      7 | +           |          nan     |          nan     |           48.566 |
| pre-market price before 9:25 -> market-on-open (names with a pre-market trade) | Taiwan    |      4 | -           |          nan     |           -0.866 |          -10.455 |
| official open -> enter 9:35 with market orders                                 | Australia |      1 | +           |            0.604 |            0.957 |            6.709 |
| official open -> enter 9:35 with market orders                                 | China     |     16 | -           |           -0.775 |           -0.308 |           -2.052 |
| official open -> enter 9:35 with market orders                                 | India     |      5 | +           |            0.326 |            1.692 |            5.942 |
| official open -> enter 9:35 with market orders                                 | Japan     |     10 | +           |            0.215 |           -0.148 |           -0.568 |
| official open -> enter 9:35 with market orders                                 | Korea     |      8 | +           |            0.884 |            1.123 |            4.352 |
| official open -> enter 9:35 with market orders                                 | Taiwan    |      4 | +           |            0.43  |           -0.387 |           -2.375 |

### 3. Strategies inside each Asian market (long top fifth / short bottom fifth)

| market    | strategy                                                            | direction   |   stocks |   sharpe_2006_14 |   sharpe_2015_26 |   annual_return_2015_26 |   net_sharpe_2015_26 |   net_annual_return_2015_26 |   round_trip_cost_bp | on_ibkr   |   bad_open_share |
|:----------|:--------------------------------------------------------------------|:------------|---------:|-----------------:|-----------------:|------------------------:|---------------------:|----------------------------:|---------------------:|:----------|-----------------:|
| Japan     | overnight persistence (21d overnight sum; close in, open out)       | +           |       40 |            0.517 |            0.788 |                   0.052 |               -3.001 |                      -0.2   |                   10 | True      |            0.038 |
| Japan     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       40 |            0.1   |            1.125 |                   0.071 |               -2.845 |                      -0.181 |                   10 | True      |            0.038 |
| Japan     | 1-day reversal (against today's close-to-close; close to close)     | -           |       40 |            0.498 |           -0.231 |                  -0.024 |               -2.118 |                      -0.221 |                   10 | True      |            0.038 |
| Japan     | 5-day reversal (close to close)                                     | +           |       40 |            0.639 |            0.13  |                   0.014 |               -0.694 |                      -0.076 |                   10 | True      |            0.038 |
| Hong Kong | overnight persistence (21d overnight sum; close in, open out)       | +           |       35 |            4.122 |            3.785 |                   0.224 |               -9.835 |                      -0.582 |                   32 | True      |            0.071 |
| Hong Kong | end-of-day fade (against today's open-to-close; close in, open out) | +           |       35 |            1.251 |           -1.27  |                  -0.077 |              -14.529 |                      -0.884 |                   32 | True      |            0.071 |
| Hong Kong | 1-day reversal (against today's close-to-close; close to close)     | -           |       35 |            1.915 |            0.284 |                   0.032 |               -5.16  |                      -0.588 |                   32 | True      |            0.071 |
| Hong Kong | 5-day reversal (close to close)                                     | -           |       35 |            0.004 |            0.268 |                   0.033 |               -2.044 |                      -0.25  |                   32 | True      |            0.071 |
| Korea     | overnight persistence (21d overnight sum; close in, open out)       | +           |       28 |            4.223 |            3.127 |                   0.203 |               -5.785 |                      -0.376 |                   23 | False     |            0.07  |
| Korea     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       28 |            2.256 |            1.737 |                   0.124 |               -6.378 |                      -0.456 |                   23 | False     |            0.07  |
| Korea     | 1-day reversal (against today's close-to-close; close to close)     | -           |       28 |            2.489 |           -1.964 |                  -0.254 |               -5.533 |                      -0.715 |                   23 | False     |            0.07  |
| Korea     | 5-day reversal (close to close)                                     | +           |       28 |            1.506 |            1.138 |                   0.162 |               -0.371 |                      -0.053 |                   23 | False     |            0.07  |
| Taiwan    | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.002 |            4.775 |                   0.278 |               -9.508 |                      -0.554 |                   33 | False     |            0.103 |
| Taiwan    | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            1.39  |            0.938 |                   0.057 |              -12.824 |                      -0.775 |                   33 | False     |            0.103 |
| Taiwan    | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.339 |           -1.868 |                  -0.19  |               -8.311 |                      -0.848 |                   33 | False     |            0.103 |
| Taiwan    | 5-day reversal (close to close)                                     | +           |       30 |            2.252 |            0.823 |                   0.089 |               -2.073 |                      -0.224 |                   33 | False     |            0.103 |
| Australia | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            2.556 |            1.832 |                   0.111 |               -4.811 |                      -0.292 |                   16 | True      |            0.038 |
| Australia | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            0.498 |           -0.754 |                  -0.045 |               -7.439 |                      -0.449 |                   16 | True      |            0.038 |
| Australia | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.434 |            0.632 |                   0.065 |               -2.38  |                      -0.245 |                   16 | True      |            0.038 |
| Australia | 5-day reversal (close to close)                                     | +           |       30 |            0.643 |            0.264 |                   0.027 |               -1.126 |                      -0.117 |                   16 | True      |            0.038 |
| India     | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.675 |            4.546 |                   0.155 |              -13.981 |                      -0.475 |                   25 | False     |            0.014 |
| India     | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            3.319 |            0.601 |                   0.023 |              -15.748 |                      -0.607 |                   25 | False     |            0.014 |
| India     | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.835 |           -0.84  |                  -0.078 |               -6.271 |                      -0.581 |                   25 | False     |            0.014 |
| India     | 5-day reversal (close to close)                                     | +           |       30 |            1.182 |            0.886 |                   0.086 |               -1.514 |                      -0.148 |                   25 | False     |            0.014 |

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

