## Asian markets

Daily Yahoo data since 2005; directions chosen on 2006-2014, checked on 2015-2026. An Asian session on date D falls between the US sessions of D-1 and D. Opening prices Yahoo copied from the previous close are dropped (share per ticker in asia_data_quality.csv).

### 1. Lead-lag between the US and Asian indices

'gap' = previous close -> open (the news is absorbed here: descriptive); 'after the open' = open -> close. Each market twice: the index (whose first value of the day still holds yesterday's prices for stocks that haven't opened yet - Sydney opens in alphabetical groups over 10 minutes - so 'after the open' partly repeats the gap and looks predictable) and an index ETF, whose open is a price you could actually trade. Only the ETF rows count as tradable evidence; index futures also trade overnight, so their open has already absorbed the US day.

| market         | instrument   | signal                                    | target                    | tradable   |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:---------------|:-------------|:------------------------------------------|:--------------------------|:-----------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| Japan          | ^N225        | US close-to-close (D-1)                   | Japan: gap                | False      |          0.677 |      31.783 |        2205 |          0.619 |      33.238 |        2882 |
| Japan          | ^N225        | US close-to-close (D-1)                   | Japan: after the open     | True       |          0.287 |      13.478 |        2205 |          0.13  |       6.954 |        2882 |
| Japan          | ^N225        | US open-to-close (D-1)                    | Japan: after the open     | True       |          0.25  |      11.756 |        2205 |          0.141 |       7.559 |        2882 |
| Japan          | ^N225        | Japan close-to-close (D)                  | US: US gap                | False      |          0.284 |      13.464 |        2245 |          0.301 |      16.368 |        2949 |
| Japan          | ^N225        | Japan close-to-close (D)                  | US: US after the open     | True       |         -0.055 |      -2.612 |        2245 |         -0.025 |      -1.339 |        2949 |
| Japan          | ^N225        | Japan open-to-close (D)                   | US: US after the open     | True       |         -0.04  |      -1.881 |        2245 |          0.004 |       0.226 |        2949 |
| Hong Kong      | ^HSI         | US close-to-close (D-1)                   | Hong Kong: gap            | False      |          0.709 |      33.398 |        2218 |          0.505 |      27.228 |        2904 |
| Hong Kong      | ^HSI         | US close-to-close (D-1)                   | Hong Kong: after the open | True       |         -0.126 |      -5.953 |        2218 |         -0.086 |      -4.628 |        2904 |
| Hong Kong      | ^HSI         | US open-to-close (D-1)                    | Hong Kong: after the open | True       |         -0.094 |      -4.407 |        2218 |         -0.054 |      -2.893 |        2904 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D)              | US: US gap                | False      |          0.403 |      19.081 |        2247 |          0.318 |      17.302 |        2953 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D)              | US: US after the open     | True       |          0.053 |       2.497 |        2247 |         -0.035 |      -1.908 |        2953 |
| Hong Kong      | ^HSI         | Hong Kong open-to-close (D)               | US: US after the open     | True       |          0.159 |       7.55  |        2247 |         -0.006 |      -0.345 |        2953 |
| China          | 000001.SS    | US close-to-close (D-1)                   | China: gap                | False      |          0.535 |      25.004 |        2182 |          0.421 |      22.505 |        2864 |
| China          | 000001.SS    | US close-to-close (D-1)                   | China: after the open     | True       |         -0.071 |      -3.302 |        2182 |         -0.051 |      -2.739 |        2864 |
| China          | 000001.SS    | US open-to-close (D-1)                    | China: after the open     | True       |         -0.025 |      -1.167 |        2182 |         -0.017 |      -0.89  |        2864 |
| China          | 000001.SS    | China close-to-close (D)                  | US: US gap                | False      |          0.173 |       8.122 |        2206 |          0.207 |      11.17  |        2899 |
| China          | 000001.SS    | China close-to-close (D)                  | US: US after the open     | True       |         -0.015 |      -0.724 |        2206 |          0.002 |       0.127 |        2899 |
| China          | 000001.SS    | China open-to-close (D)                   | US: US after the open     | True       |          0.021 |       0.983 |        2206 |          0.01  |       0.528 |        2899 |
| Korea          | ^KS11        | US close-to-close (D-1)                   | Korea: gap                | False      |          0.769 |      36.295 |        2230 |          0.574 |      30.803 |        2884 |
| Korea          | ^KS11        | US close-to-close (D-1)                   | Korea: after the open     | True       |         -0.178 |      -8.421 |        2230 |         -0.058 |      -3.118 |        2884 |
| Korea          | ^KS11        | US open-to-close (D-1)                    | Korea: after the open     | True       |         -0.155 |      -7.309 |        2230 |         -0.066 |      -3.521 |        2884 |
| Korea          | ^KS11        | Korea close-to-close (D)                  | US: US gap                | False      |          0.356 |      16.882 |        2247 |          0.283 |      15.386 |        2946 |
| Korea          | ^KS11        | Korea close-to-close (D)                  | US: US after the open     | True       |          0.035 |       1.674 |        2247 |         -0.033 |      -1.778 |        2946 |
| Korea          | ^KS11        | Korea open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.493 |        2247 |         -0.007 |      -0.392 |        2946 |
| Taiwan         | ^TWII        | US close-to-close (D-1)                   | Taiwan: gap               | False      |          0.734 |      34.612 |        2221 |          0.572 |      30.569 |        2860 |
| Taiwan         | ^TWII        | US close-to-close (D-1)                   | Taiwan: after the open    | True       |         -0.177 |      -8.355 |        2221 |          0.213 |      11.416 |        2860 |
| Taiwan         | ^TWII        | US open-to-close (D-1)                    | Taiwan: after the open    | True       |         -0.136 |      -6.42  |        2221 |          0.21  |      11.246 |        2860 |
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
| India          | ^BSESN       | US close-to-close (D-1)                   | India: after the open     | True       |         -0.062 |      -2.897 |        2198 |         -0.011 |      -0.619 |        2904 |
| India          | ^BSESN       | US open-to-close (D-1)                    | India: after the open     | True       |          0.034 |       1.577 |        2198 |          0.02  |       1.077 |        2904 |
| India          | ^BSESN       | India close-to-close (D)                  | US: US gap                | False      |          0.384 |      18.2   |        2247 |          0.394 |      21.42  |        2953 |
| India          | ^BSESN       | India close-to-close (D)                  | US: US after the open     | True       |          0.093 |       4.432 |        2247 |         -0.013 |      -0.693 |        2953 |
| India          | ^BSESN       | India open-to-close (D)                   | US: US after the open     | True       |          0.116 |       5.499 |        2247 |          0.013 |       0.712 |        2953 |
| Singapore      | ^STI         | US close-to-close (D-1)                   | Singapore: gap            | False      |          0.717 |      23.954 |        1117 |          0.608 |      33.042 |        2958 |
| Singapore      | ^STI         | US close-to-close (D-1)                   | Singapore: after the open | True       |         -0.076 |      -2.557 |        1117 |         -0.02  |      -1.089 |        2958 |
| Singapore      | ^STI         | US open-to-close (D-1)                    | Singapore: after the open | True       |         -0.029 |      -0.953 |        1117 |         -0.024 |      -1.28  |        2958 |
| Singapore      | ^STI         | Singapore close-to-close (D)              | US: US gap                | False      |          0.445 |      21.099 |        2247 |          0.363 |      19.73  |        2953 |
| Singapore      | ^STI         | Singapore close-to-close (D)              | US: US after the open     | True       |          0.048 |       2.277 |        2247 |         -0.044 |      -2.375 |        2953 |
| Singapore      | ^STI         | Singapore open-to-close (D)               | US: US after the open     | True       |          0.047 |       1.694 |        1301 |         -0.006 |      -0.318 |        2953 |
| Asia (average) | nan          | Asian markets' average close-to-close (D) | US gap                    | False      |          0.44  |      20.857 |        2247 |          0.447 |      24.301 |        2953 |
| Asia (average) | nan          | Asian markets' average close-to-close (D) | US after the open         | True       |          0.027 |       1.271 |        2247 |         -0.035 |      -1.884 |        2953 |
| Japan          | 1321.T       | US close-to-close (D-1)                   | Japan: gap                | False      |          0.729 |      11.128 |         233 |          0.038 |       1.45  |        1494 |
| Japan          | 1321.T       | US close-to-close (D-1)                   | Japan: after the open     | True       |         -0.04  |      -0.608 |         234 |         -0.109 |      -4.202 |        1494 |
| Japan          | 1321.T       | US open-to-close (D-1)                    | Japan: after the open     | True       |         -0.027 |      -0.413 |         234 |         -0.1   |      -3.857 |        1494 |
| Japan          | 1321.T       | Japan close-to-close (D)                  | US: US gap                | False      |          0.233 |       3.721 |         255 |          0.015 |       0.587 |        1595 |
| Japan          | 1321.T       | Japan close-to-close (D)                  | US: US after the open     | True       |          0.061 |       0.979 |         255 |         -0.008 |      -0.337 |        1595 |
| Japan          | 1321.T       | Japan open-to-close (D)                   | US: US after the open     | True       |          0.009 |       0.137 |         256 |          0.082 |       3.28  |        1595 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1)                   | Hong Kong: gap            | False      |          0.651 |      23.512 |        1303 |          0.53  |      27.412 |        2670 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1)                   | Hong Kong: after the open | True       |         -0.011 |      -0.403 |        1303 |         -0.029 |      -1.478 |        2670 |
| Hong Kong      | 2800.HK      | US open-to-close (D-1)                    | Hong Kong: after the open | True       |          0.057 |       2.062 |        1303 |         -0.019 |      -1.007 |        2670 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D)              | US: US gap                | False      |          0.399 |      16.693 |        1750 |          0.259 |      14.075 |        2953 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D)              | US: US after the open     | True       |          0.062 |       2.576 |        1750 |         -0.044 |      -2.376 |        2953 |
| Hong Kong      | 2800.HK      | Hong Kong open-to-close (D)               | US: US after the open     | True       |          0.047 |       1.812 |        1496 |         -0.005 |      -0.263 |        2943 |
| Australia      | STW.AX       | US close-to-close (D-1)                   | Australia: gap            | False      |          0.692 |      26.72  |        1491 |          0.674 |      36.534 |        2938 |
| Australia      | STW.AX       | US close-to-close (D-1)                   | Australia: after the open | True       |         -0.1   |      -3.864 |        1491 |         -0.2   |     -10.821 |        2938 |
| Australia      | STW.AX       | US open-to-close (D-1)                    | Australia: after the open | True       |         -0.079 |      -3.038 |        1491 |         -0.089 |      -4.849 |        2938 |
| Australia      | STW.AX       | Australia close-to-close (D)              | US: US gap                | False      |          0.324 |      13.537 |        1750 |          0.401 |      21.787 |        2953 |
| Australia      | STW.AX       | Australia close-to-close (D)              | US: US after the open     | True       |          0.061 |       2.534 |        1750 |          0.015 |       0.812 |        2953 |
| Australia      | STW.AX       | Australia open-to-close (D)               | US: US after the open     | True       |          0.178 |       6.876 |        1500 |          0.103 |       5.577 |        2953 |
| Korea          | 069500.KS    | US close-to-close (D-1)                   | Korea: gap                | False      |          0.744 |      27.956 |        1412 |          0.521 |      27.68  |        2827 |
| Korea          | 069500.KS    | US close-to-close (D-1)                   | Korea: after the open     | True       |         -0.036 |      -1.366 |        1413 |         -0.078 |      -4.133 |        2827 |
| Korea          | 069500.KS    | US open-to-close (D-1)                    | Korea: after the open     | True       |         -0.016 |      -0.587 |        1413 |         -0.074 |      -3.908 |        2827 |
| Korea          | 069500.KS    | Korea close-to-close (D)                  | US: US gap                | False      |          0.284 |      10.785 |        1438 |          0.276 |      14.973 |        2945 |
| Korea          | 069500.KS    | Korea close-to-close (D)                  | US: US after the open     | True       |          0.019 |       0.72  |        1438 |         -0.031 |      -1.687 |        2945 |
| Korea          | 069500.KS    | Korea open-to-close (D)                   | US: US after the open     | True       |          0.064 |       2.433 |        1439 |          0.003 |       0.172 |        2945 |
| Taiwan         | 0050.TW      | US close-to-close (D-1)                   | Taiwan: gap               | False      |          0.081 |       3.038 |        1397 |          0.564 |      29.546 |        2741 |
| Taiwan         | 0050.TW      | US close-to-close (D-1)                   | Taiwan: after the open    | True       |          0.087 |       3.255 |        1397 |         -0.038 |      -1.986 |        2741 |
| Taiwan         | 0050.TW      | US open-to-close (D-1)                    | Taiwan: after the open    | True       |          0.06  |       2.244 |        1397 |          0     |       0.017 |        2741 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D)                 | US: US gap                | False      |          0.096 |       3.678 |        1478 |          0.277 |      14.97  |        2912 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D)                 | US: US after the open     | True       |          0.033 |       1.267 |        1478 |         -0.058 |      -3.146 |        2912 |
| Taiwan         | 0050.TW      | Taiwan open-to-close (D)                  | US: US after the open     | True       |          0.001 |       0.045 |        1478 |         -0.037 |      -2     |        2909 |
| India          | NIFTYBEES.NS | US close-to-close (D-1)                   | India: gap                | False      |          0.198 |       6.992 |        1245 |          0.052 |       2.761 |        2803 |
| India          | NIFTYBEES.NS | US close-to-close (D-1)                   | India: after the open     | True       |         -0.045 |      -1.593 |        1246 |         -0.02  |      -1.075 |        2803 |
| India          | NIFTYBEES.NS | US open-to-close (D-1)                    | India: after the open     | True       |          0.017 |       0.603 |        1246 |         -0.027 |      -1.425 |        2803 |
| India          | NIFTYBEES.NS | India close-to-close (D)                  | US: US gap                | False      |          0.29  |      11.211 |        1499 |          0.061 |       3.31  |        2953 |
| India          | NIFTYBEES.NS | India close-to-close (D)                  | US: US after the open     | True       |          0.094 |       3.645 |        1499 |         -0.01  |      -0.521 |        2953 |
| India          | NIFTYBEES.NS | India open-to-close (D)                   | US: US after the open     | True       |          0.068 |       2.499 |        1338 |          0.011 |       0.598 |        2952 |
| Singapore      | ES3.SI       | US close-to-close (D-1)                   | Singapore: gap            | False      |          0.576 |      19.894 |        1194 |          0.549 |      28.525 |        2700 |
| Singapore      | ES3.SI       | US close-to-close (D-1)                   | Singapore: after the open | True       |          0.04  |       1.385 |        1194 |          0.083 |       4.316 |        2700 |
| Singapore      | ES3.SI       | US open-to-close (D-1)                    | Singapore: after the open | True       |          0.105 |       3.619 |        1194 |          0.076 |       3.946 |        2700 |
| Singapore      | ES3.SI       | Singapore close-to-close (D)              | US: US gap                | False      |          0.441 |      18.46  |        1750 |          0.368 |      19.987 |        2953 |
| Singapore      | ES3.SI       | Singapore close-to-close (D)              | US: US after the open     | True       |          0.02  |       0.837 |        1750 |         -0.045 |      -2.427 |        2953 |
| Singapore      | ES3.SI       | Singapore open-to-close (D)               | US: US after the open     | True       |          0.085 |       3.275 |        1495 |          0.005 |       0.288 |        2950 |
| China          | 510300.SS    | US close-to-close (D-1)                   | China: gap                | False      |          0.331 |       7.982 |         580 |          0.378 |      20.044 |        2819 |
| China          | 510300.SS    | US close-to-close (D-1)                   | China: after the open     | True       |         -0.004 |      -0.097 |         580 |         -0.014 |      -0.741 |        2819 |
| China          | 510300.SS    | US open-to-close (D-1)                    | China: after the open     | True       |          0.054 |       1.289 |         580 |         -0.001 |      -0.05  |        2819 |
| China          | 510300.SS    | China close-to-close (D)                  | US: US gap                | False      |          0.155 |       3.944 |         650 |          0.218 |      11.717 |        2899 |
| China          | 510300.SS    | China close-to-close (D)                  | US: US after the open     | True       |         -0.024 |      -0.6   |         650 |          0.01  |       0.533 |        2899 |
| China          | 510300.SS    | China open-to-close (D)                   | US: US after the open     | True       |         -0.041 |      -1.014 |         604 |          0.017 |       0.905 |        2899 |

Trading the sign of the signal on the 'after the open' leg (cost: 0 bp for SPY at the auctions; 2 bp for an index (as if futures, flattering - see above); each ETF at its market's round trip):

| market         | instrument   | strategy                                             | direction   |   sharpe_2006_14 |   sharpe_2015_26 |   net_sharpe_2015_26 |   avg_bp_2015_26 |   cost_bp |
|:---------------|:-------------|:-----------------------------------------------------|:------------|-----------------:|-----------------:|---------------------:|-----------------:|----------:|
| Japan          | ^N225        | US close-to-close (D-1) -> Japan after the open      | +           |            1.144 |            0.783 |                0.459 |            4.816 |         2 |
| Japan          | ^N225        | US open-to-close (D-1) -> Japan after the open       | +           |            1.339 |            0.794 |                0.469 |            4.887 |         2 |
| Japan          | ^N225        | Japan close-to-close (D) -> US US after the open     | +           |            0.156 |           -0.118 |               -0.118 |           -0.62  |         0 |
| Japan          | ^N225        | Japan open-to-close (D) -> US US after the open      | +           |            0.269 |            0.19  |                0.19  |            0.998 |         0 |
| Hong Kong      | ^HSI         | US close-to-close (D-1) -> Hong Kong after the open  | -           |            1.096 |            0.852 |                0.54  |            5.444 |         2 |
| Hong Kong      | ^HSI         | US open-to-close (D-1) -> Hong Kong after the open   | -           |            0.602 |            0.624 |                0.312 |            3.995 |         2 |
| Hong Kong      | ^HSI         | Hong Kong close-to-close (D) -> US US after the open | +           |            0.273 |           -0.428 |               -0.428 |           -2.246 |         0 |
| Hong Kong      | ^HSI         | Hong Kong open-to-close (D) -> US US after the open  | +           |            0.96  |            0.151 |                0.151 |            0.794 |         0 |
| China          | 000001.SS    | US close-to-close (D-1) -> China after the open      | -           |            0.024 |            0.155 |               -0.131 |            1.083 |         2 |
| China          | 000001.SS    | US open-to-close (D-1) -> China after the open       | +           |            0.315 |           -0.262 |               -0.549 |           -1.828 |         2 |
| China          | 000001.SS    | China close-to-close (D) -> US US after the open     | +           |            0.027 |           -0.182 |               -0.182 |           -0.956 |         0 |
| China          | 000001.SS    | China open-to-close (D) -> US US after the open      | -           |            0.116 |           -0.407 |               -0.407 |           -2.14  |         0 |
| Korea          | ^KS11        | US close-to-close (D-1) -> Korea after the open      | -           |            1.471 |            0.553 |                0.262 |            3.794 |         2 |
| Korea          | ^KS11        | US open-to-close (D-1) -> Korea after the open       | -           |            1.122 |            0.786 |                0.495 |            5.394 |         2 |
| Korea          | ^KS11        | Korea close-to-close (D) -> US US after the open     | +           |            0.549 |           -0.245 |               -0.245 |           -1.285 |         0 |
| Korea          | ^KS11        | Korea open-to-close (D) -> US US after the open      | +           |            0.718 |           -0.067 |               -0.067 |           -0.354 |         0 |
| Taiwan         | ^TWII        | US close-to-close (D-1) -> Taiwan after the open     | -           |            1.744 |           -2.973 |               -3.347 |          -15.859 |         2 |
| Taiwan         | ^TWII        | US open-to-close (D-1) -> Taiwan after the open      | -           |            0.762 |           -2.127 |               -2.499 |          -11.443 |         2 |
| Taiwan         | ^TWII        | Taiwan close-to-close (D) -> US US after the open    | -           |            0.005 |           -0.059 |               -0.059 |           -0.309 |         0 |
| Taiwan         | ^TWII        | Taiwan open-to-close (D) -> US US after the open     | +           |            0.759 |            0.151 |                0.151 |            0.797 |         0 |
| Australia      | ^AXJO        | US close-to-close (D-1) -> Australia after the open  | +           |            5.163 |            5.862 |                5.415 |           26.169 |         2 |
| Australia      | ^AXJO        | US open-to-close (D-1) -> Australia after the open   | +           |            5.002 |            5     |                4.559 |           22.701 |         2 |
| Australia      | ^AXJO        | Australia close-to-close (D) -> US US after the open | +           |            0.075 |           -0.062 |               -0.062 |           -0.323 |         0 |
| Australia      | ^AXJO        | Australia open-to-close (D) -> US US after the open  | +           |            0.442 |           -0.095 |               -0.095 |           -0.522 |         0 |
| India          | ^BSESN       | US close-to-close (D-1) -> India after the open      | +           |            0.238 |           -0.217 |               -0.586 |           -1.176 |         2 |
| India          | ^BSESN       | US open-to-close (D-1) -> India after the open       | +           |            1.102 |            0.266 |               -0.104 |            1.438 |         2 |
| India          | ^BSESN       | India close-to-close (D) -> US US after the open     | +           |            0.644 |           -0.002 |               -0.002 |           -0.009 |         0 |
| India          | ^BSESN       | India open-to-close (D) -> US US after the open      | +           |            0.807 |            0.017 |                0.017 |            0.091 |         0 |
| Singapore      | ^STI         | US close-to-close (D-1) -> Singapore after the open  | -           |            0.774 |            0.035 |               -0.479 |            0.137 |         2 |
| Singapore      | ^STI         | US open-to-close (D-1) -> Singapore after the open   | -           |            0.395 |            0.449 |               -0.067 |            1.74  |         2 |
| Singapore      | ^STI         | Singapore close-to-close (D) -> US US after the open | +           |            0.608 |           -0.414 |               -0.414 |           -2.17  |         0 |
| Singapore      | ^STI         | Singapore open-to-close (D) -> US US after the open  | +           |            0.265 |            0.03  |                0.03  |            0.16  |         0 |
| Asia (average) | nan          | Asia average (D) -> SPY open-to-close (D)            | +           |            0.592 |           -0.147 |               -0.147 |           -0.77  |         0 |
| Japan          | 1321.T       | US close-to-close (D-1) -> Japan after the open      | -           |            1.048 |            1.317 |               -0.353 |            7.868 |        10 |
| Japan          | 1321.T       | US open-to-close (D-1) -> Japan after the open       | -           |            0.424 |            1.086 |               -0.584 |            6.503 |        10 |
| Japan          | 1321.T       | Japan close-to-close (D) -> US US after the open     | +           |            0.588 |           -0.213 |               -0.213 |           -1.109 |         0 |
| Japan          | 1321.T       | Japan open-to-close (D) -> US US after the open      | +           |            0.438 |            0.495 |                0.495 |            2.59  |         0 |
| Hong Kong      | 2800.HK      | US close-to-close (D-1) -> Hong Kong after the open  | +           |            0.161 |           -0.423 |               -2.061 |           -2.838 |        11 |
| Hong Kong      | 2800.HK      | US open-to-close (D-1) -> Hong Kong after the open   | +           |            1.131 |           -0.291 |               -1.931 |           -1.948 |        11 |
| Hong Kong      | 2800.HK      | Hong Kong close-to-close (D) -> US US after the open | +           |            0.193 |           -0.303 |               -0.303 |           -1.562 |         0 |
| Hong Kong      | 2800.HK      | Hong Kong open-to-close (D) -> US US after the open  | +           |            0.58  |            0.031 |                0.031 |            0.164 |         0 |
| Australia      | STW.AX       | US close-to-close (D-1) -> Australia after the open  | -           |            0.912 |            0.944 |               -2.651 |            4.194 |        16 |
| Australia      | STW.AX       | US open-to-close (D-1) -> Australia after the open   | -           |            0.5   |            0.708 |               -2.89  |            3.147 |        16 |
| Australia      | STW.AX       | Australia close-to-close (D) -> US US after the open | +           |            0.827 |           -0.041 |               -0.041 |           -0.214 |         0 |
| Australia      | STW.AX       | Australia open-to-close (D) -> US US after the open  | +           |            1.82  |            0.627 |                0.627 |            3.289 |         0 |
| Korea          | 069500.KS    | US close-to-close (D-1) -> Korea after the open      | -           |            0.118 |            0.722 |                0.003 |            5.013 |         5 |
| Korea          | 069500.KS    | US open-to-close (D-1) -> Korea after the open       | +           |            0.495 |           -0.875 |               -1.595 |           -6.069 |         5 |
| Korea          | 069500.KS    | Korea close-to-close (D) -> US US after the open     | +           |            0.313 |           -0.042 |               -0.042 |           -0.22  |         0 |
| Korea          | 069500.KS    | Korea open-to-close (D) -> US US after the open      | +           |            0.425 |            0.162 |                0.162 |            0.852 |         0 |
| Taiwan         | 0050.TW      | US close-to-close (D-1) -> Taiwan after the open     | +           |            0.713 |            0.579 |               -1.965 |            2.95  |        13 |
| Taiwan         | 0050.TW      | US open-to-close (D-1) -> Taiwan after the open      | +           |            0.771 |            0.073 |               -2.474 |            0.372 |        13 |
| Taiwan         | 0050.TW      | Taiwan close-to-close (D) -> US US after the open    | +           |            0.168 |           -0.195 |               -0.195 |           -1.013 |         0 |
| Taiwan         | 0050.TW      | Taiwan open-to-close (D) -> US US after the open     | +           |            0.808 |           -0.132 |               -0.132 |           -0.697 |         0 |
| India          | NIFTYBEES.NS | US close-to-close (D-1) -> India after the open      | -           |            0.271 |            0.744 |               -0.902 |           11.273 |        25 |
| India          | NIFTYBEES.NS | US open-to-close (D-1) -> India after the open       | +           |            0.291 |           -0.736 |               -2.382 |          -11.188 |        25 |
| India          | NIFTYBEES.NS | India close-to-close (D) -> US US after the open     | +           |            0.706 |            0.113 |                0.113 |            0.594 |         0 |
| India          | NIFTYBEES.NS | India open-to-close (D) -> US US after the open      | +           |            1.088 |           -0.307 |               -0.307 |           -1.613 |         0 |
| Singapore      | ES3.SI       | US close-to-close (D-1) -> Singapore after the open  | +           |            0.734 |            1.446 |               -2.241 |            6.264 |        16 |
| Singapore      | ES3.SI       | US open-to-close (D-1) -> Singapore after the open   | +           |            1.454 |            1.082 |               -2.6   |            4.703 |        16 |
| Singapore      | ES3.SI       | Singapore close-to-close (D) -> US US after the open | +           |            0.492 |           -0.264 |               -0.264 |           -1.354 |         0 |
| Singapore      | ES3.SI       | Singapore open-to-close (D) -> US US after the open  | +           |            0.826 |           -0.013 |               -0.013 |           -0.068 |         0 |
| China          | 510300.SS    | US close-to-close (D-1) -> China after the open      | -           |            0.085 |           -0.114 |               -0.876 |           -0.896 |         6 |
| China          | 510300.SS    | US open-to-close (D-1) -> China after the open       | +           |            0.715 |           -0.106 |               -0.87  |           -0.832 |         6 |
| China          | 510300.SS    | China close-to-close (D) -> US US after the open     | +           |            0.078 |           -0.004 |               -0.004 |           -0.022 |         0 |
| China          | 510300.SS    | China open-to-close (D) -> US US after the open      | -           |            0.273 |           -0.327 |               -0.327 |           -1.722 |         0 |

### 2. ADRs vs their home listings

Residual = the home listing's last session in dollars minus the ADR's opening gap. Pooled long / short book on Alpaca (market-on-open in, market-on-close out). Yahoo dates FX bars by their London / New York close, after the US open, so the clean variant uses the previous day's FX move; the same-day variant is shown only to measure how much the peek was worth:

| strategy                                     | variant                                        | direction   |   cost_bp_round_trip |   sharpe_2006_14 |   sharpe_2015_26 |   avg_bp_2015_26 |   adrs_per_day_2015_26 |
|:---------------------------------------------|:-----------------------------------------------|:------------|---------------------:|-----------------:|-----------------:|-----------------:|-----------------------:|
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    0 |            3.555 |            2.643 |            7.797 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    1 |            3.352 |            2.304 |            7.797 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | FX lagged a day (clean)                        | +           |                    3 |            2.944 |            1.626 |            7.797 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    0 |            3.607 |            3.087 |            9.003 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    1 |            3.4   |            2.744 |            9.003 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | no FX (home move in local currency)            | +           |                    3 |            2.986 |            2.058 |            9.003 |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    0 |            3.897 |            2.637 |            7.96  |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    1 |            3.689 |            2.306 |            7.96  |                 22.056 |
| ADRs: home-vs-gap residual, MOO in / MOC out | same-day FX (peeks: shown for comparison only) | +           |                    3 |            3.273 |            1.643 |            7.96  |                 22.056 |

Per ADR (correlations):

| adr   | home         | signal                        | target               |   corr_2006_14 |   t_2006_14 |   n_2006_14 |   corr_2015_26 |   t_2015_26 |   n_2015_26 |
|:------|:-------------|:------------------------------|:---------------------|---------------:|------------:|------------:|---------------:|------------:|------------:|
| TSM   | 2330.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.12  |       5.605 |        2171 |         -0.037 |      -1.976 |        2899 |
| TSM   | 2330.TW      | home move (USD)               | ADR open-to-close    |          0.12  |       5.581 |        2171 |         -0.069 |      -3.708 |        2899 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: after its open |          0.189 |       8.469 |        2008 |         -0.015 |      -0.757 |        2559 |
| TSM   | 2330.TW      | ADR open-to-close (US day)    | home: gap            |          0.137 |       6.125 |        2008 |          0.558 |      28.23  |        2559 |
| UMC   | 2303.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.141 |       6.292 |        1991 |          0.115 |       5.882 |        2635 |
| UMC   | 2303.TW      | home move (USD)               | ADR open-to-close    |          0.131 |       5.865 |        1991 |          0.116 |       5.953 |        2635 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: after its open |          0.155 |       6.81  |        1934 |         -0.064 |      -3.257 |        2556 |
| UMC   | 2303.TW      | ADR open-to-close (US day)    | home: gap            |          0.096 |       4.206 |        1934 |          0.479 |      24.233 |        2556 |
| ASX   | 3711.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.354 |      16.218 |        2101 |          0.02  |       1.066 |        2772 |
| ASX   | 3711.TW      | home move (USD)               | ADR open-to-close    |          0.264 |      12.113 |        2101 |          0.068 |       3.585 |        2772 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: after its open |         -0.045 |      -2.04  |        2092 |          0.011 |       0.559 |        2648 |
| ASX   | 3711.TW      | ADR open-to-close (US day)    | home: gap            |          0.389 |      17.795 |        2092 |          0.499 |      25.681 |        2648 |
| CHT   | 2412.TW      | home move (USD) minus ADR gap | ADR open-to-close    |          0.132 |       6.152 |        2182 |          0.146 |       7.768 |        2850 |
| CHT   | 2412.TW      | home move (USD)               | ADR open-to-close    |          0.08  |       3.736 |        2182 |          0.109 |       5.805 |        2850 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: after its open |         -0.05  |      -2.174 |        1901 |          0.016 |       0.714 |        1994 |
| CHT   | 2412.TW      | ADR open-to-close (US day)    | home: gap            |          0.213 |       9.277 |        1901 |          0.192 |       8.555 |        1994 |
| SONY  | 6758.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.058 |       2.748 |        2224 |         -0.006 |      -0.345 |        2926 |
| SONY  | 6758.T       | home move (USD)               | ADR open-to-close    |          0.107 |       5.034 |        2224 |          0.013 |       0.694 |        2926 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: after its open |          0.205 |       9.476 |        2127 |         -0.015 |      -0.795 |        2841 |
| SONY  | 6758.T       | ADR open-to-close (US day)    | home: gap            |          0.43  |      19.825 |        2127 |          0.541 |      28.839 |        2841 |
| TM    | 7203.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.108 |       5.113 |        2250 |          0     |       0.006 |        2954 |
| TM    | 7203.T       | home move (USD)               | ADR open-to-close    |          0.119 |       5.637 |        2250 |          0.043 |       2.355 |        2954 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: after its open |          0.214 |       9.734 |        2065 |         -0.025 |      -1.353 |        2861 |
| TM    | 7203.T       | ADR open-to-close (US day)    | home: gap            |          0.392 |      17.831 |        2065 |          0.491 |      26.28  |        2861 |
| HMC   | 7267.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.16  |       7.547 |        2221 |          0.009 |       0.483 |        2904 |
| HMC   | 7267.T       | home move (USD)               | ADR open-to-close    |          0.155 |       7.301 |        2221 |          0.04  |       2.147 |        2904 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: after its open |          0.269 |      12.331 |        2099 |          0.028 |       1.515 |        2841 |
| HMC   | 7267.T       | ADR open-to-close (US day)    | home: gap            |          0.337 |      15.46  |        2099 |          0.462 |      24.6   |        2841 |
| MUFG  | 8306.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.23  |      10.527 |        2088 |          0.071 |       3.696 |        2709 |
| MUFG  | 8306.T       | home move (USD)               | ADR open-to-close    |          0.095 |       4.327 |        2088 |          0.073 |       3.781 |        2709 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: after its open |          0.156 |       6.899 |        1968 |         -0.042 |      -2.261 |        2855 |
| MUFG  | 8306.T       | ADR open-to-close (US day)    | home: gap            |          0.285 |      12.636 |        1968 |          0.445 |      23.768 |        2855 |
| SMFG  | 8316.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.191 |       7.245 |        1437 |          0.033 |       1.734 |        2759 |
| SMFG  | 8316.T       | home move (USD)               | ADR open-to-close    |          0.09  |       3.418 |        1437 |          0.047 |       2.479 |        2759 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: after its open |          0.133 |       5.078 |        1463 |         -0.038 |      -2.049 |        2843 |
| SMFG  | 8316.T       | ADR open-to-close (US day)    | home: gap            |          0.29  |      11.082 |        1463 |          0.417 |      22.237 |        2843 |
| MFG   | 8411.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.262 |      11.167 |        1823 |          0.079 |       3.944 |        2522 |
| MFG   | 8411.T       | home move (USD)               | ADR open-to-close    |          0.178 |       7.582 |        1824 |          0.047 |       2.373 |        2522 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: after its open |          0.157 |       6.381 |        1661 |         -0.024 |      -1.265 |        2797 |
| MFG   | 8411.T       | ADR open-to-close (US day)    | home: gap            |          0.227 |       9.24  |        1661 |          0.378 |      20.004 |        2797 |
| NMR   | 8604.T       | home move (USD) minus ADR gap | ADR open-to-close    |          0.155 |       7.202 |        2145 |          0.07  |       3.584 |        2642 |
| NMR   | 8604.T       | home move (USD)               | ADR open-to-close    |          0.167 |       7.741 |        2145 |          0.123 |       6.312 |        2642 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: after its open |          0.125 |       5.716 |        2091 |         -0.004 |      -0.23  |        2852 |
| NMR   | 8604.T       | ADR open-to-close (US day)    | home: gap            |          0.399 |      18.224 |        2091 |          0.415 |      22.159 |        2852 |
| BABA  | 9988.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.061 |       2.536 |        1730 |
| BABA  | 9988.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.062 |       2.572 |        1730 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.019 |       0.776 |        1649 |
| BABA  | 9988.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.704 |      28.588 |        1648 |
| JD    | 9618.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.051 |       2.019 |        1583 |
| JD    | 9618.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.037 |       1.462 |        1583 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.11  |       4.261 |        1501 |
| JD    | 9618.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.705 |      27.289 |        1500 |
| BIDU  | 9888.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.059 |       2.222 |        1397 |
| BIDU  | 9888.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |          0.072 |       2.681 |        1397 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.052 |       1.833 |        1259 |
| BIDU  | 9888.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.74  |      26.251 |        1258 |
| NTES  | 9999.HK      | home move (USD) minus ADR gap | ADR open-to-close    |        nan     |     nan     |           0 |          0.031 |       1.252 |        1590 |
| NTES  | 9999.HK      | home move (USD)               | ADR open-to-close    |        nan     |     nan     |           0 |         -0.022 |      -0.877 |        1590 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: after its open |        nan     |     nan     |           0 |          0.069 |       2.685 |        1520 |
| NTES  | 9999.HK      | ADR open-to-close (US day)    | home: gap            |        nan     |     nan     |           0 |          0.66  |      25.737 |        1519 |
| KB    | 105560.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.051 |       2.435 |        2242 |          0.067 |       3.62  |        2919 |
| KB    | 105560.KS    | home move (USD)               | ADR open-to-close    |          0.163 |       7.71  |        2242 |          0.09  |       4.877 |        2919 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: after its open |         -0.049 |      -1.896 |        1485 |          0.035 |       1.814 |        2755 |
| KB    | 105560.KS    | ADR open-to-close (US day)    | home: gap            |          0.633 |      24.399 |        1485 |          0.399 |      20.964 |        2755 |
| SHG   | 055550.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.085 |       4.022 |        2251 |          0.168 |       9.055 |        2914 |
| SHG   | 055550.KS    | home move (USD)               | ADR open-to-close    |          0.157 |       7.464 |        2251 |          0.116 |       6.258 |        2914 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: after its open |         -0.091 |      -4.223 |        2136 |          0.018 |       0.96  |        2758 |
| SHG   | 055550.KS    | ADR open-to-close (US day)    | home: gap            |          0.554 |      25.583 |        2136 |          0.382 |      20.062 |        2758 |
| PKX   | 005490.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.074 |       3.489 |        2251 |          0.043 |       2.327 |        2944 |
| PKX   | 005490.KS    | home move (USD)               | ADR open-to-close    |          0.16  |       7.575 |        2251 |          0.029 |       1.598 |        2944 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: after its open |          0.013 |       0.604 |        2109 |          0.041 |       2.126 |        2735 |
| PKX   | 005490.KS    | ADR open-to-close (US day)    | home: gap            |          0.673 |      30.916 |        2109 |          0.456 |      23.827 |        2735 |
| LPL   | 034220.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.163 |       7.59  |        2159 |          0.182 |       9.372 |        2666 |
| LPL   | 034220.KS    | home move (USD)               | ADR open-to-close    |          0.204 |       9.47  |        2159 |          0.178 |       9.187 |        2666 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: after its open |         -0.013 |      -0.581 |        2159 |          0.037 |       1.886 |        2615 |
| LPL   | 034220.KS    | ADR open-to-close (US day)    | home: gap            |          0.569 |      26.419 |        2159 |          0.394 |      20.172 |        2615 |
| KEP   | 015760.KS    | home move (USD) minus ADR gap | ADR open-to-close    |          0.17  |       7.961 |        2196 |          0.12  |       6.386 |        2822 |
| KEP   | 015760.KS    | home move (USD)               | ADR open-to-close    |          0.208 |       9.738 |        2196 |          0.125 |       6.646 |        2822 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: after its open |         -0.007 |      -0.304 |        2131 |          0.005 |       0.278 |        2724 |
| KEP   | 015760.KS    | ADR open-to-close (US day)    | home: gap            |          0.472 |      21.768 |        2131 |          0.309 |      16.122 |        2724 |
| IBN   | ICICIBANK.NS | home move (USD) minus ADR gap | ADR open-to-close    |          0.08  |       3.786 |        2243 |          0.082 |       4.373 |        2864 |
| IBN   | ICICIBANK.NS | home move (USD)               | ADR open-to-close    |          0.177 |       8.368 |        2243 |          0.117 |       6.244 |        2864 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: after its open |          0.153 |       7.186 |        2210 |          0.03  |       1.596 |        2899 |
| IBN   | ICICIBANK.NS | ADR open-to-close (US day)    | home: gap            |          0.434 |      20.417 |        2210 |          0.498 |      26.824 |        2899 |
| HDB   | HDFCBANK.NS  | home move (USD) minus ADR gap | ADR open-to-close    |          0.08  |       3.795 |        2256 |          0.112 |       6.08  |        2929 |
| HDB   | HDFCBANK.NS  | home move (USD)               | ADR open-to-close    |          0.126 |       6.006 |        2256 |          0.149 |       8.081 |        2929 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: after its open |          0.089 |       4.185 |        2209 |          0.005 |       0.244 |        2902 |
| HDB   | HDFCBANK.NS  | ADR open-to-close (US day)    | home: gap            |          0.474 |      22.28  |        2209 |          0.404 |      21.757 |        2902 |
| INFY  | INFY.NS      | home move (USD) minus ADR gap | ADR open-to-close    |          0.055 |       2.591 |        2238 |          0.039 |       2.108 |        2890 |
| INFY  | INFY.NS      | home move (USD)               | ADR open-to-close    |          0.112 |       5.299 |        2238 |          0.018 |       0.944 |        2890 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: after its open |          0.158 |       7.446 |        2209 |          0.099 |       5.341 |        2907 |
| INFY  | INFY.NS      | ADR open-to-close (US day)    | home: gap            |          0.403 |      18.925 |        2209 |          0.49  |      26.413 |        2907 |
| WIT   | WIPRO.NS     | home move (USD) minus ADR gap | ADR open-to-close    |          0.242 |      11.401 |        2225 |          0.084 |       4.362 |        2701 |
| WIT   | WIPRO.NS     | home move (USD)               | ADR open-to-close    |          0.132 |       6.217 |        2225 |          0.038 |       1.979 |        2701 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: after its open |          0.048 |       2.239 |        2206 |          0.029 |       1.533 |        2882 |
| WIT   | WIPRO.NS     | ADR open-to-close (US day)    | home: gap            |          0.32  |      15.02  |        2206 |          0.363 |      19.504 |        2882 |
| BHP   | BHP.AX       | home move (USD) minus ADR gap | ADR open-to-close    |          0.006 |       0.281 |        2251 |          0.073 |       3.984 |        2942 |
| BHP   | BHP.AX       | home move (USD)               | ADR open-to-close    |          0.027 |       1.29  |        2251 |          0.053 |       2.872 |        2942 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: after its open |         -0.005 |      -0.247 |        2234 |         -0.012 |      -0.669 |        2946 |
| BHP   | BHP.AX       | ADR open-to-close (US day)    | home: gap            |          0.614 |      29.029 |        2234 |          0.509 |      27.651 |        2946 |

### 3. Strategies inside each Asian market (long top fifth / short bottom fifth)

| market    | strategy                                                            | direction   |   stocks |   sharpe_2006_14 |   sharpe_2015_26 |   annual_return_2015_26 |   net_sharpe_2015_26 |   net_annual_return_2015_26 |   round_trip_cost_bp | on_ibkr   |   bad_open_share |
|:----------|:--------------------------------------------------------------------|:------------|---------:|-----------------:|-----------------:|------------------------:|---------------------:|----------------------------:|---------------------:|:----------|-----------------:|
| Japan     | overnight persistence (21d overnight sum; close in, open out)       | +           |       40 |            0.518 |            0.788 |                   0.052 |               -3.001 |                      -0.2   |                   10 | True      |            0.038 |
| Japan     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       40 |            0.1   |            1.128 |                   0.072 |               -2.842 |                      -0.18  |                   10 | True      |            0.038 |
| Japan     | 1-day reversal (against today's close-to-close; close to close)     | -           |       40 |            0.514 |           -0.229 |                  -0.024 |               -2.116 |                      -0.221 |                   10 | True      |            0.038 |
| Japan     | 5-day reversal (close to close)                                     | +           |       40 |            0.638 |            0.133 |                   0.015 |               -0.692 |                      -0.076 |                   10 | True      |            0.038 |
| Hong Kong | overnight persistence (21d overnight sum; close in, open out)       | +           |       35 |            4.122 |            3.785 |                   0.224 |               -9.835 |                      -0.582 |                   32 | True      |            0.071 |
| Hong Kong | end-of-day fade (against today's open-to-close; close in, open out) | +           |       35 |            1.251 |           -1.272 |                  -0.077 |              -14.53  |                      -0.884 |                   32 | True      |            0.071 |
| Hong Kong | 1-day reversal (against today's close-to-close; close to close)     | -           |       35 |            1.918 |            0.285 |                   0.032 |               -5.159 |                      -0.588 |                   32 | True      |            0.071 |
| Hong Kong | 5-day reversal (close to close)                                     | -           |       35 |            0.007 |            0.266 |                   0.032 |               -2.047 |                      -0.251 |                   32 | True      |            0.071 |
| Korea     | overnight persistence (21d overnight sum; close in, open out)       | +           |       28 |            4.223 |            3.126 |                   0.203 |               -5.786 |                      -0.376 |                   23 | False     |            0.07  |
| Korea     | end-of-day fade (against today's open-to-close; close in, open out) | -           |       28 |            2.259 |            1.738 |                   0.124 |               -6.377 |                      -0.455 |                   23 | False     |            0.07  |
| Korea     | 1-day reversal (against today's close-to-close; close to close)     | -           |       28 |            2.49  |           -1.967 |                  -0.254 |               -5.537 |                      -0.716 |                   23 | False     |            0.07  |
| Korea     | 5-day reversal (close to close)                                     | +           |       28 |            1.511 |            1.143 |                   0.162 |               -0.367 |                      -0.052 |                   23 | False     |            0.07  |
| Taiwan    | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.002 |            4.775 |                   0.278 |               -9.508 |                      -0.554 |                   33 | False     |            0.103 |
| Taiwan    | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            1.39  |            0.931 |                   0.056 |              -12.814 |                      -0.775 |                   33 | False     |            0.103 |
| Taiwan    | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.34  |           -1.87  |                  -0.19  |               -8.311 |                      -0.849 |                   33 | False     |            0.103 |
| Taiwan    | 5-day reversal (close to close)                                     | +           |       30 |            2.246 |            0.829 |                   0.09  |               -2.067 |                      -0.224 |                   33 | False     |            0.103 |
| Australia | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            2.556 |            1.832 |                   0.111 |               -4.811 |                      -0.292 |                   16 | True      |            0.038 |
| Australia | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            0.498 |           -0.755 |                  -0.046 |               -7.439 |                      -0.449 |                   16 | True      |            0.038 |
| Australia | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.43  |            0.633 |                   0.065 |               -2.379 |                      -0.245 |                   16 | True      |            0.038 |
| Australia | 5-day reversal (close to close)                                     | +           |       30 |            0.642 |            0.266 |                   0.028 |               -1.123 |                      -0.117 |                   16 | True      |            0.038 |
| India     | overnight persistence (21d overnight sum; close in, open out)       | +           |       30 |            3.675 |            4.545 |                   0.155 |              -13.982 |                      -0.475 |                   25 | False     |            0.014 |
| India     | end-of-day fade (against today's open-to-close; close in, open out) | +           |       30 |            3.319 |            0.599 |                   0.023 |              -15.748 |                      -0.607 |                   25 | False     |            0.014 |
| India     | 1-day reversal (against today's close-to-close; close to close)     | -           |       30 |            0.835 |           -0.838 |                  -0.078 |               -6.268 |                      -0.581 |                   25 | False     |            0.014 |
| India     | 5-day reversal (close to close)                                     | +           |       30 |            1.182 |            0.884 |                   0.086 |               -1.515 |                      -0.148 |                   25 | False     |            0.014 |

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

