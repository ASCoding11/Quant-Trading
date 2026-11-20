## Critical raw materials: satellite activity at smelters vs futures

MODIS: daily thermal anomalies (Terra + Aqua, 1 km); signal uses satellite days up to 12 days before each Friday; direction fixed on 2012-2019, judged on 2020-2026.
SO2: Sentinel-5P TROPOMI plume minus background ring (DU); lag 7 days; direction fixed on 2018-2022, judged on 2023-2026.
Weekly futures returns, Friday close to Friday close. Nickel is tested on the PICK miners ETF, rare earths on REMX (no free futures series).

| source   | signal                                     | commodity     | instrument   | direction       |   weeks_train |   weeks_test |   corr_train |   t_train |   sharpe_train |   hit_train |   corr_test |   t_test |   sharpe_test |   hit_test |
|:---------|:-------------------------------------------|:--------------|:-------------|:----------------|--------------:|-------------:|-------------:|----------:|---------------:|------------:|------------:|---------:|--------------:|-----------:|
| MODIS    | level (28d FRP vs its trailing year)       | copper        | HG=F         | follow activity |           360 |          359 |       -0.021 |    -0.39  |          0.198 |       0.511 |      -0.065 |   -1.223 |        -0.639 |      0.479 |
| MODIS    | level (28d FRP vs its trailing year)       | nickel        | PICK         | fade activity   |           360 |          359 |       -0.035 |    -0.655 |          0.842 |       0.561 |      -0.068 |   -1.293 |         0.76  |      0.543 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_palladium | PA=F         | follow activity |           360 |          359 |        0.008 |     0.159 |          0.265 |       0.425 |      -0.041 |   -0.783 |        -0.351 |      0.387 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_platinum  | PL=F         | fade activity   |           360 |          359 |       -0.034 |    -0.646 |          0.595 |       0.542 |      -0.055 |   -1.032 |         0.74  |      0.487 |
| MODIS    | level (28d FRP vs its trailing year)       | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.005 |    -0.081 |          0.264 |       0.305 |      -0.091 |   -1.723 |         0.856 |      0.465 |
| MODIS    | level (28d FRP vs its trailing year)       | rare_earths   | REMX         | follow activity |           360 |          359 |       -0.01  |    -0.182 |          0.337 |       0.503 |      -0.031 |   -0.58  |         0.117 |      0.485 |
| MODIS    | 4-week change of the level                 | copper        | HG=F         | fade activity   |           356 |          359 |       -0.064 |    -1.205 |          0.319 |       0.525 |      -0.003 |   -0.048 |         0.653 |      0.538 |
| MODIS    | 4-week change of the level                 | nickel        | PICK         | fade activity   |           356 |          359 |       -0.031 |    -0.591 |          0.165 |       0.534 |      -0.016 |   -0.298 |         0.243 |      0.482 |
| MODIS    | 4-week change of the level                 | pgm_palladium | PA=F         | follow activity |           356 |          359 |        0.018 |     0.333 |          0.126 |       0.32  |      -0.008 |   -0.157 |        -0.148 |      0.292 |
| MODIS    | 4-week change of the level                 | pgm_platinum  | PL=F         | fade activity   |           356 |          359 |       -0.021 |    -0.401 |          0.151 |       0.5   |       0.026 |    0.495 |        -0.205 |      0.448 |
| MODIS    | 4-week change of the level                 | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.086 |    -1.483 |          0.282 |       0.359 |      -0.017 |   -0.33  |         0.157 |      0.407 |
| MODIS    | 4-week change of the level                 | rare_earths   | REMX         | follow activity |           356 |          359 |        0.058 |     1.089 |          0.023 |       0.497 |      -0.049 |   -0.918 |        -0.218 |      0.462 |
| SO2      | level (28d SO2 plume vs its trailing year) | copper        | HG=F         | follow activity |           177 |          195 |       -0.01  |    -0.126 |          0.165 |       0.469 |      -0.03  |   -0.413 |        -0.347 |      0.467 |
| SO2      | level (28d SO2 plume vs its trailing year) | nickel        | PICK         | fade activity   |           169 |          195 |       -0.04  |    -0.517 |          0.226 |       0.533 |       0.095 |    1.331 |        -0.108 |      0.508 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_palladium | PA=F         | follow activity |            74 |           87 |       -0.028 |    -0.241 |          0.039 |       0.554 |       0     |    0.002 |        -0.384 |      0.506 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_platinum  | PL=F         | follow activity |           131 |          191 |        0.106 |     1.211 |          0.923 |       0.527 |       0.097 |    1.346 |         0.698 |      0.513 |
| SO2      | level (28d SO2 plume vs its trailing year) | aluminium     | ALI=F        | fade activity   |           156 |          195 |        0.002 |     0.021 |          0.107 |       0.551 |      -0.138 |   -1.935 |         0.179 |      0.533 |
| SO2      | level (28d SO2 plume vs its trailing year) | rare_earths   | REMX         | follow activity |           131 |          189 |        0.188 |     2.176 |          0.884 |       0.557 |       0.003 |    0.043 |        -1.077 |      0.386 |
| SO2      | 4-week change of the SO2 level             | copper        | HG=F         | follow activity |           166 |          188 |        0.062 |     0.793 |          0.434 |       0.512 |      -0.017 |   -0.232 |         0.274 |      0.5   |
| SO2      | 4-week change of the SO2 level             | nickel        | PICK         | follow activity |           155 |          188 |       -0.069 |    -0.854 |          0.015 |       0.503 |       0.07  |    0.957 |         0.5   |      0.5   |
| SO2      | 4-week change of the SO2 level             | pgm_palladium | PA=F         | follow activity |            58 |           67 |        0.203 |     1.552 |          0.86  |       0.569 |       0.043 |    0.35  |        -0.788 |      0.448 |
| SO2      | 4-week change of the SO2 level             | pgm_platinum  | PL=F         | follow activity |           123 |          183 |        0.083 |     0.916 |          0.576 |       0.48  |       0.048 |    0.649 |         0.402 |      0.508 |
| SO2      | 4-week change of the SO2 level             | aluminium     | ALI=F        | fade activity   |           145 |          188 |       -0.121 |    -1.456 |          0.191 |       0.531 |      -0.029 |   -0.401 |        -0.056 |      0.511 |
| SO2      | 4-week change of the SO2 level             | rare_earths   | REMX         | follow activity |           123 |          181 |        0.235 |     2.661 |          1.359 |       0.569 |       0.016 |    0.208 |        -0.537 |      0.475 |

### Coverage by site

| source   | commodity     | site                                       |   days |   days_with_fire |   share_days_with_fire |   mean_frp_mw |   overpasses |   mean_enh_du |
|:---------|:--------------|:-------------------------------------------|-------:|-----------------:|-----------------------:|--------------:|-------------:|--------------:|
| MODIS    | aluminium     | EGA Jebel Ali (UAE)                        |   5258 |               21 |                  0.004 |         0.241 |          nan |       nan     |
| MODIS    | aluminium     | Hongqiao Zouping (China)                   |   5266 |               37 |                  0.007 |         0.149 |          nan |       nan     |
| MODIS    | aluminium     | Krasnoyarsk aluminium (Russia)             |   5258 |               82 |                  0.016 |         0.508 |          nan |       nan     |
| MODIS    | aluminium     | Xinfa Chiping (China)                      |   5266 |              135 |                  0.026 |         1.056 |          nan |       nan     |
| MODIS    | copper        | Altonorte smelter (Chile)                  |   5252 |             1026 |                  0.195 |         3.069 |          nan |       nan     |
| MODIS    | copper        | Caletones smelter (Chile)                  |   5252 |             2652 |                  0.505 |        25.436 |          nan |       nan     |
| MODIS    | copper        | Chuquicamata smelter (Chile)               |   5252 |             1939 |                  0.369 |        21.09  |          nan |       nan     |
| MODIS    | copper        | Guixi smelter (China)                      |   5266 |              183 |                  0.035 |         1.576 |          nan |       nan     |
| MODIS    | copper        | Kolwezi copper-cobalt (DRC)                |   5260 |              946 |                  0.18  |        44.88  |          nan |       nan     |
| MODIS    | copper        | Mount Isa smelter (Australia)              |   5274 |             2515 |                  0.477 |        22.567 |          nan |       nan     |
| MODIS    | copper        | Olympic Dam (Australia)                    |   5266 |              137 |                  0.026 |         0.313 |          nan |       nan     |
| MODIS    | copper        | Potrerillos smelter (Chile)                |   5252 |              760 |                  0.145 |         7.309 |          nan |       nan     |
| MODIS    | copper        | Tongling copper (China)                    |   5266 |              124 |                  0.024 |         0.514 |          nan |       nan     |
| MODIS    | nickel        | IMIP Morowali (Indonesia)                  |   5266 |              538 |                  0.102 |         4.88  |          nan |       nan     |
| MODIS    | nickel        | IWIP Weda Bay (Indonesia)                  |   5266 |              385 |                  0.073 |         2.771 |          nan |       nan     |
| MODIS    | nickel        | Kalgoorlie nickel smelter (Australia)      |   5258 |             2058 |                  0.391 |        28.278 |          nan |       nan     |
| MODIS    | nickel        | Konawe / Morosi (Indonesia)                |   5266 |              800 |                  0.152 |         7.928 |          nan |       nan     |
| MODIS    | nickel        | Obi Island (Indonesia)                     |   5266 |              731 |                  0.139 |         4.924 |          nan |       nan     |
| MODIS    | nickel        | Sorowako (Indonesia)                       |   5266 |             2803 |                  0.532 |       216.515 |          nan |       nan     |
| MODIS    | nickel        | Sudbury Copper Cliff (Canada)              |   5260 |               21 |                  0.004 |         0.747 |          nan |       nan     |
| MODIS    | pgm_palladium | Norilsk Nadezhda (Russia)                  |   5252 |              767 |                  0.146 |        25.934 |          nan |       nan     |
| MODIS    | pgm_palladium | Norilsk Nickel plant (Russia)              |   5252 |              838 |                  0.16  |        27.287 |          nan |       nan     |
| MODIS    | pgm_platinum  | Polokwane smelter (S. Africa)              |   5260 |              129 |                  0.025 |         4.014 |          nan |       nan     |
| MODIS    | pgm_platinum  | Rustenburg / Waterval smelters (S. Africa) |   5260 |             1578 |                  0.3   |        10.067 |          nan |       nan     |
| MODIS    | rare_earths   | Baotou rare earth / steel (China)          |   5258 |             2594 |                  0.493 |        69.912 |          nan |       nan     |
| SO2      | aluminium     | EGA Jebel Ali (UAE)                        |   2603 |              nan |                nan     |       nan     |         2807 |         0.053 |
| SO2      | aluminium     | Hongqiao Zouping (China)                   |   2194 |              nan |                nan     |       nan     |         3264 |         0.028 |
| SO2      | aluminium     | Krasnoyarsk aluminium (Russia)             |   1695 |              nan |                nan     |       nan     |         6135 |        -0.028 |
| SO2      | aluminium     | Xinfa Chiping (China)                      |   2158 |              nan |                nan     |       nan     |         3199 |        -0.002 |
| SO2      | copper        | Altonorte smelter (Chile)                  |   2674 |              nan |                nan     |       nan     |         2922 |         0.027 |
| SO2      | copper        | Caletones smelter (Chile)                  |   2206 |              nan |                nan     |       nan     |         3209 |         0.118 |
| SO2      | copper        | Chuquicamata smelter (Chile)               |   2671 |              nan |                nan     |       nan     |         2862 |         0.06  |
| SO2      | copper        | Guixi smelter (China)                      |   1611 |              nan |                nan     |       nan     |         2895 |         0.048 |
| SO2      | copper        | Kolwezi copper-cobalt (DRC)                |   2354 |              nan |                nan     |       nan     |         2630 |         0.015 |
| SO2      | copper        | Mount Isa smelter (Australia)              |   2476 |              nan |                nan     |       nan     |         2730 |         0.392 |
| SO2      | copper        | Olympic Dam (Australia)                    |   2480 |              nan |                nan     |       nan     |         3124 |         0.055 |
| SO2      | copper        | Potrerillos smelter (Chile)                |   2651 |              nan |                nan     |       nan     |         3014 |         0.022 |
| SO2      | copper        | Tongling copper (China)                    |   1747 |              nan |                nan     |       nan     |         3050 |         0.019 |
| SO2      | nickel        | IMIP Morowali (Indonesia)                  |   2156 |              nan |                nan     |       nan     |         2630 |         0.27  |
| SO2      | nickel        | IWIP Weda Bay (Indonesia)                  |   2197 |              nan |                nan     |       nan     |         2647 |         0.066 |
| SO2      | nickel        | Kalgoorlie nickel smelter (Australia)      |   2460 |              nan |                nan     |       nan     |         3013 |         0.049 |
| SO2      | nickel        | Konawe / Morosi (Indonesia)                |   2199 |              nan |                nan     |       nan     |         2611 |         0.017 |
| SO2      | nickel        | Obi Island (Indonesia)                     |   2200 |              nan |                nan     |       nan     |         2633 |        -0.058 |
| SO2      | nickel        | Sorowako (Indonesia)                       |   2156 |              nan |                nan     |       nan     |         2612 |         0.048 |
| SO2      | nickel        | Sudbury Copper Cliff (Canada)              |   1782 |              nan |                nan     |       nan     |         3991 |         0.053 |
| SO2      | pgm_palladium | Norilsk Nadezhda (Russia)                  |   1371 |              nan |                nan     |       nan     |        15779 |         0.833 |
| SO2      | pgm_palladium | Norilsk Nickel plant (Russia)              |   1387 |              nan |                nan     |       nan     |        15722 |         0.855 |
| SO2      | pgm_platinum  | Polokwane smelter (S. Africa)              |   2367 |              nan |                nan     |       nan     |         2949 |        -0.061 |
| SO2      | pgm_platinum  | Rustenburg / Waterval smelters (S. Africa) |   2398 |              nan |                nan     |       nan     |         2799 |         0.062 |
| SO2      | rare_earths   | Baotou rare earth / steel (China)          |   2355 |              nan |                nan     |       nan     |         3475 |         0.144 |

### Latest readings

```
{
 "MODIS level (28d FRP vs its trailing year)": {
  "aluminium": 0.0,
  "copper": -0.498,
  "nickel": 0.534,
  "pgm_palladium": 0.0,
  "pgm_platinum": 3.603,
  "rare_earths": -0.412
 },
 "MODIS 4-week change of the level": {
  "aluminium": 0.0,
  "copper": -0.443,
  "nickel": -0.661,
  "pgm_palladium": -8.024,
  "pgm_platinum": -0.337,
  "rare_earths": -0.002
 },
 "SO2 level (28d SO2 plume vs its trailing year)": {
  "aluminium": NaN,
  "copper": 0.01,
  "nickel": -0.09,
  "pgm_palladium": NaN,
  "pgm_platinum": NaN,
  "rare_earths": NaN
 },
 "SO2 4-week change of the SO2 level": {
  "aluminium": NaN,
  "copper": -0.079,
  "nickel": 0.071,
  "pgm_palladium": NaN,
  "pgm_platinum": NaN,
  "rare_earths": NaN
 }
}
```

