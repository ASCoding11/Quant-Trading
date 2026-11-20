## Critical raw materials: satellite activity at smelters vs futures

MODIS: daily thermal anomalies (Terra + Aqua, 1 km); signal uses satellite days up to 12 days before each Friday; direction fixed on 2012-2019, judged on 2020-2026.
SO2: Sentinel-5P TROPOMI plume minus background ring (DU); lag 7 days; direction fixed on 2018-2022, judged on 2023-2026.
Weekly futures returns, Friday close to Friday close. Nickel is tested on the PICK miners ETF, rare earths on REMX (no free futures series).

| source   | signal                                     | commodity     | instrument   | direction       |   weeks_train |   weeks_test |   corr_train |   t_train |   sharpe_train |   hit_train |   corr_test |   t_test |   sharpe_test |   hit_test |
|:---------|:-------------------------------------------|:--------------|:-------------|:----------------|--------------:|-------------:|-------------:|----------:|---------------:|------------:|------------:|---------:|--------------:|-----------:|
| MODIS    | level (28d FRP vs its trailing year)       | copper        | HG=F         | follow activity |           360 |          359 |       -0.021 |    -0.39  |          0.198 |       0.511 |      -0.064 |   -1.221 |        -0.637 |      0.479 |
| MODIS    | level (28d FRP vs its trailing year)       | nickel        | PICK         | fade activity   |           360 |          359 |       -0.035 |    -0.655 |          0.842 |       0.561 |      -0.068 |   -1.293 |         0.76  |      0.543 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_palladium | PA=F         | follow activity |           360 |          359 |        0.008 |     0.159 |          0.265 |       0.425 |      -0.042 |   -0.787 |        -0.352 |      0.387 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_platinum  | PL=F         | fade activity   |           360 |          359 |       -0.034 |    -0.646 |          0.595 |       0.542 |      -0.055 |   -1.031 |         0.74  |      0.487 |
| MODIS    | level (28d FRP vs its trailing year)       | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.005 |    -0.081 |          0.264 |       0.305 |      -0.091 |   -1.723 |         0.856 |      0.465 |
| MODIS    | level (28d FRP vs its trailing year)       | rare_earths   | REMX         | follow activity |           360 |          359 |       -0.01  |    -0.182 |          0.337 |       0.503 |      -0.031 |   -0.58  |         0.117 |      0.485 |
| MODIS    | 4-week change of the level                 | copper        | HG=F         | fade activity   |           356 |          359 |       -0.064 |    -1.205 |          0.319 |       0.525 |      -0.002 |   -0.044 |         0.651 |      0.538 |
| MODIS    | 4-week change of the level                 | nickel        | PICK         | fade activity   |           356 |          359 |       -0.031 |    -0.591 |          0.165 |       0.534 |      -0.016 |   -0.298 |         0.243 |      0.482 |
| MODIS    | 4-week change of the level                 | pgm_palladium | PA=F         | follow activity |           356 |          359 |        0.018 |     0.333 |          0.126 |       0.32  |      -0.008 |   -0.155 |        -0.146 |      0.292 |
| MODIS    | 4-week change of the level                 | pgm_platinum  | PL=F         | fade activity   |           356 |          359 |       -0.021 |    -0.401 |          0.151 |       0.5   |       0.026 |    0.494 |        -0.205 |      0.448 |
| MODIS    | 4-week change of the level                 | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.086 |    -1.483 |          0.282 |       0.359 |      -0.017 |   -0.33  |         0.157 |      0.407 |
| MODIS    | 4-week change of the level                 | rare_earths   | REMX         | follow activity |           356 |          359 |        0.058 |     1.089 |          0.023 |       0.497 |      -0.049 |   -0.918 |        -0.218 |      0.462 |
| SO2      | level (28d SO2 plume vs its trailing year) | copper        | HG=F         | follow activity |           186 |          195 |       -0.006 |    -0.077 |          0.234 |       0.484 |      -0.036 |   -0.5   |        -0.349 |      0.467 |
| SO2      | level (28d SO2 plume vs its trailing year) | nickel        | PICK         | fade activity   |           186 |          195 |       -0.04  |    -0.548 |          0.181 |       0.511 |       0.058 |    0.804 |        -0.108 |      0.508 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_palladium | PA=F         | follow activity |           115 |           87 |        0.024 |     0.258 |          0.108 |       0.557 |       0     |    0.002 |        -0.384 |      0.506 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_platinum  | PL=F         | follow activity |           183 |          194 |        0.06  |     0.814 |          0.623 |       0.53  |       0.078 |    1.079 |         0.444 |      0.5   |
| SO2      | level (28d SO2 plume vs its trailing year) | aluminium     | ALI=F        | follow activity |           184 |          195 |        0.042 |     0.565 |          0.575 |       0.478 |      -0.116 |   -1.626 |        -0.179 |      0.467 |
| SO2      | level (28d SO2 plume vs its trailing year) | rare_earths   | REMX         | follow activity |           183 |          192 |        0.176 |     2.409 |          1.111 |       0.563 |       0.004 |    0.06  |        -1.174 |      0.38  |
| SO2      | 4-week change of the SO2 level             | copper        | HG=F         | follow activity |           182 |          188 |        0.023 |     0.305 |          0.052 |       0.489 |      -0.016 |   -0.217 |         0.258 |      0.495 |
| SO2      | 4-week change of the SO2 level             | nickel        | PICK         | follow activity |           182 |          188 |       -0.032 |    -0.43  |          0.098 |       0.511 |       0.037 |    0.505 |         0.279 |      0.495 |
| SO2      | 4-week change of the SO2 level             | pgm_palladium | PA=F         | follow activity |            98 |           67 |        0.226 |     2.27  |          1.32  |       0.571 |       0.043 |    0.35  |        -0.788 |      0.448 |
| SO2      | 4-week change of the SO2 level             | pgm_platinum  | PL=F         | follow activity |           176 |          186 |        0.004 |     0.054 |          0.273 |       0.472 |       0.036 |    0.485 |         0.3   |      0.505 |
| SO2      | 4-week change of the SO2 level             | aluminium     | ALI=F        | fade activity   |           178 |          188 |       -0.065 |    -0.866 |          0.027 |       0.528 |      -0.01  |   -0.13  |        -0.056 |      0.511 |
| SO2      | 4-week change of the SO2 level             | rare_earths   | REMX         | follow activity |           176 |          184 |        0.211 |     2.845 |          1.237 |       0.585 |       0.015 |    0.201 |        -0.446 |      0.478 |

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
| SO2      | aluminium     | EGA Jebel Ali (UAE)                        |   2836 |              nan |                nan     |       nan     |         3056 |         0.059 |
| SO2      | aluminium     | Hongqiao Zouping (China)                   |   2379 |              nan |                nan     |       nan     |         3561 |         0.028 |
| SO2      | aluminium     | Krasnoyarsk aluminium (Russia)             |   1815 |              nan |                nan     |       nan     |         6650 |        -0.027 |
| SO2      | aluminium     | Xinfa Chiping (China)                      |   2332 |              nan |                nan     |       nan     |         3493 |        -0.001 |
| SO2      | copper        | Altonorte smelter (Chile)                  |   2856 |              nan |                nan     |       nan     |         3134 |         0.033 |
| SO2      | copper        | Caletones smelter (Chile)                  |   2378 |              nan |                nan     |       nan     |         3456 |         0.117 |
| SO2      | copper        | Chuquicamata smelter (Chile)               |   2857 |              nan |                nan     |       nan     |         3061 |         0.057 |
| SO2      | copper        | Guixi smelter (China)                      |   1776 |              nan |                nan     |       nan     |         3161 |         0.049 |
| SO2      | copper        | Kolwezi copper-cobalt (DRC)                |   2574 |              nan |                nan     |       nan     |         2878 |         0.014 |
| SO2      | copper        | Mount Isa smelter (Australia)              |   2704 |              nan |                nan     |       nan     |         2987 |         0.39  |
| SO2      | copper        | Olympic Dam (Australia)                    |   2700 |              nan |                nan     |       nan     |         3410 |         0.059 |
| SO2      | copper        | Potrerillos smelter (Chile)                |   2829 |              nan |                nan     |       nan     |         3226 |         0.02  |
| SO2      | copper        | Tongling copper (China)                    |   1909 |              nan |                nan     |       nan     |         3318 |         0.016 |
| SO2      | nickel        | IMIP Morowali (Indonesia)                  |   2341 |              nan |                nan     |       nan     |         2857 |         0.27  |
| SO2      | nickel        | IWIP Weda Bay (Indonesia)                  |   2390 |              nan |                nan     |       nan     |         2883 |         0.06  |
| SO2      | nickel        | Kalgoorlie nickel smelter (Australia)      |   2667 |              nan |                nan     |       nan     |         3286 |         0.049 |
| SO2      | nickel        | Konawe / Morosi (Indonesia)                |   2379 |              nan |                nan     |       nan     |         2834 |         0.019 |
| SO2      | nickel        | Obi Island (Indonesia)                     |   2387 |              nan |                nan     |       nan     |         2870 |        -0.058 |
| SO2      | nickel        | Sorowako (Indonesia)                       |   2343 |              nan |                nan     |       nan     |         2845 |         0.046 |
| SO2      | nickel        | Sudbury Copper Cliff (Canada)              |   1895 |              nan |                nan     |       nan     |         4256 |         0.057 |
| SO2      | pgm_palladium | Norilsk Nadezhda (Russia)                  |   1435 |              nan |                nan     |       nan     |        17083 |         0.827 |
| SO2      | pgm_palladium | Norilsk Nickel plant (Russia)              |   1450 |              nan |                nan     |       nan     |        17024 |         0.85  |
| SO2      | pgm_platinum  | Polokwane smelter (S. Africa)              |   2587 |              nan |                nan     |       nan     |         3229 |        -0.063 |
| SO2      | pgm_platinum  | Rustenburg / Waterval smelters (S. Africa) |   2621 |              nan |                nan     |       nan     |         3059 |         0.059 |
| SO2      | rare_earths   | Baotou rare earth / steel (China)          |   2560 |              nan |                nan     |       nan     |         3782 |         0.143 |

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
  "aluminium": 0.107,
  "copper": 0.034,
  "nickel": 0.021,
  "pgm_palladium": NaN,
  "pgm_platinum": 0.017,
  "rare_earths": -0.021
 },
 "SO2 4-week change of the SO2 level": {
  "aluminium": 0.091,
  "copper": -0.046,
  "nickel": 0.068,
  "pgm_palladium": NaN,
  "pgm_platinum": -0.03,
  "rare_earths": -0.031
 }
}
```

