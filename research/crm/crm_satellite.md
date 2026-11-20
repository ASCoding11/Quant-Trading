## Critical raw materials: satellite activity at smelters vs futures

MODIS: daily thermal anomalies (Terra + Aqua, 1 km); signal uses satellite days up to 12 days before each Friday; direction fixed on 2012-2019, judged on 2020-2026.
SO2: Sentinel-5P TROPOMI plume minus background ring (DU); lag 7 days; direction fixed on 2018-2022, judged on 2023-2026.
Weekly futures returns, Friday close to Friday close. Nickel is tested on the PICK miners ETF, rare earths on REMX (no free futures series).

| source   | signal                                     | commodity     | instrument   | direction       |   weeks_train |   weeks_test |   corr_train |   t_train |   sharpe_train |   hit_train |   corr_test |   t_test |   sharpe_test |   hit_test |
|:---------|:-------------------------------------------|:--------------|:-------------|:----------------|--------------:|-------------:|-------------:|----------:|---------------:|------------:|------------:|---------:|--------------:|-----------:|
| MODIS    | level (28d FRP vs its trailing year)       | copper        | HG=F         | follow activity |           360 |          359 |       -0.021 |    -0.39  |          0.198 |       0.511 |      -0.064 |   -1.219 |        -0.636 |      0.479 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_palladium | PA=F         | follow activity |           360 |          359 |        0.008 |     0.159 |          0.265 |       0.425 |      -0.042 |   -0.802 |        -0.357 |      0.387 |
| MODIS    | level (28d FRP vs its trailing year)       | pgm_platinum  | PL=F         | fade activity   |           360 |          359 |       -0.034 |    -0.646 |          0.595 |       0.542 |      -0.055 |   -1.033 |         0.74  |      0.487 |
| MODIS    | level (28d FRP vs its trailing year)       | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.005 |    -0.081 |          0.264 |       0.305 |      -0.091 |   -1.729 |         0.856 |      0.465 |
| MODIS    | level (28d FRP vs its trailing year)       | rare_earths   | REMX         | follow activity |           360 |          359 |       -0.01  |    -0.182 |          0.337 |       0.503 |      -0.031 |   -0.58  |         0.117 |      0.485 |
| MODIS    | 4-week change of the level                 | copper        | HG=F         | fade activity   |           356 |          359 |       -0.064 |    -1.205 |          0.319 |       0.525 |      -0.002 |   -0.041 |         0.65  |      0.538 |
| MODIS    | 4-week change of the level                 | pgm_palladium | PA=F         | follow activity |           356 |          359 |        0.018 |     0.333 |          0.126 |       0.32  |      -0.008 |   -0.149 |        -0.138 |      0.292 |
| MODIS    | 4-week change of the level                 | pgm_platinum  | PL=F         | fade activity   |           356 |          359 |       -0.021 |    -0.401 |          0.151 |       0.5   |       0.026 |    0.495 |        -0.205 |      0.448 |
| MODIS    | 4-week change of the level                 | aluminium     | ALI=F        | fade activity   |           295 |          359 |       -0.086 |    -1.483 |          0.282 |       0.359 |      -0.018 |   -0.331 |         0.157 |      0.407 |
| MODIS    | 4-week change of the level                 | rare_earths   | REMX         | follow activity |           356 |          359 |        0.058 |     1.089 |          0.023 |       0.497 |      -0.049 |   -0.918 |        -0.218 |      0.462 |
| SO2      | level (28d SO2 plume vs its trailing year) | copper        | HG=F         | follow activity |           131 |          195 |        0.022 |     0.252 |          0.806 |       0.496 |      -0.037 |   -0.511 |        -0.351 |      0.467 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_palladium | PA=F         | follow activity |            73 |           87 |       -0.029 |    -0.248 |          0.032 |       0.548 |       0     |    0.002 |        -0.384 |      0.506 |
| SO2      | level (28d SO2 plume vs its trailing year) | pgm_platinum  | PL=F         | follow activity |           131 |          194 |        0.106 |     1.211 |          0.923 |       0.527 |       0.077 |    1.067 |         0.442 |      0.5   |
| SO2      | level (28d SO2 plume vs its trailing year) | aluminium     | ALI=F        | follow activity |           131 |          195 |        0.037 |     0.419 |          0.068 |       0.427 |      -0.114 |   -1.597 |        -0.169 |      0.467 |
| SO2      | level (28d SO2 plume vs its trailing year) | rare_earths   | REMX         | follow activity |           131 |          192 |        0.191 |     2.212 |          0.938 |       0.565 |       0.003 |    0.047 |        -1.174 |      0.38  |
| SO2      | 4-week change of the SO2 level             | copper        | HG=F         | fade activity   |           123 |          188 |       -0.052 |    -0.568 |          0.213 |       0.52  |      -0.015 |   -0.205 |        -0.26  |      0.505 |
| SO2      | 4-week change of the SO2 level             | pgm_palladium | PA=F         | follow activity |            57 |           67 |        0.199 |     1.508 |          0.74  |       0.544 |       0.043 |    0.35  |        -0.788 |      0.448 |
| SO2      | 4-week change of the SO2 level             | pgm_platinum  | PL=F         | follow activity |           123 |          186 |        0.083 |     0.916 |          0.576 |       0.48  |       0.035 |    0.482 |         0.258 |      0.5   |
| SO2      | 4-week change of the SO2 level             | aluminium     | ALI=F        | follow activity |           123 |          188 |       -0.035 |    -0.383 |          0.112 |       0.488 |      -0.01  |   -0.137 |         0.068 |      0.489 |
| SO2      | 4-week change of the SO2 level             | rare_earths   | REMX         | follow activity |           123 |          184 |        0.236 |     2.675 |          1.359 |       0.569 |       0.015 |    0.203 |        -0.446 |      0.478 |

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
| SO2      | aluminium     | EGA Jebel Ali (UAE)                        |   2632 |              nan |                nan     |       nan     |         2839 |         0.054 |
| SO2      | aluminium     | Hongqiao Zouping (China)                   |   2221 |              nan |                nan     |       nan     |         3305 |         0.028 |
| SO2      | aluminium     | Krasnoyarsk aluminium (Russia)             |   1687 |              nan |                nan     |       nan     |         6151 |        -0.029 |
| SO2      | aluminium     | Xinfa Chiping (China)                      |   2185 |              nan |                nan     |       nan     |         3240 |        -0.002 |
| SO2      | copper        | Altonorte smelter (Chile)                  |   2644 |              nan |                nan     |       nan     |         2896 |         0.032 |
| SO2      | copper        | Caletones smelter (Chile)                  |   2186 |              nan |                nan     |       nan     |         3194 |         0.123 |
| SO2      | copper        | Chuquicamata smelter (Chile)               |   2642 |              nan |                nan     |       nan     |         2834 |         0.058 |
| SO2      | copper        | Guixi smelter (China)                      |   1633 |              nan |                nan     |       nan     |         2932 |         0.05  |
| SO2      | copper        | Kolwezi copper-cobalt (DRC)                |   2387 |              nan |                nan     |       nan     |         2674 |         0.015 |
| SO2      | copper        | Mount Isa smelter (Australia)              |   2508 |              nan |                nan     |       nan     |         2770 |         0.388 |
| SO2      | copper        | Olympic Dam (Australia)                    |   2508 |              nan |                nan     |       nan     |         3167 |         0.054 |
| SO2      | copper        | Potrerillos smelter (Chile)                |   2621 |              nan |                nan     |       nan     |         2988 |         0.021 |
| SO2      | copper        | Tongling copper (China)                    |   1763 |              nan |                nan     |       nan     |         3088 |         0.019 |
| SO2      | nickel        | IMIP Morowali (Indonesia)                  |   2192 |              nan |                nan     |       nan     |         2662 |         0.276 |
| SO2      | nickel        | IWIP Weda Bay (Indonesia)                  |   2233 |              nan |                nan     |       nan     |         2679 |         0.067 |
| SO2      | nickel        | Kalgoorlie nickel smelter (Australia)      |   2482 |              nan |                nan     |       nan     |         3044 |         0.05  |
| SO2      | nickel        | Konawe / Morosi (Indonesia)                |   2236 |              nan |                nan     |       nan     |         2643 |         0.018 |
| SO2      | nickel        | Obi Island (Indonesia)                     |   2231 |              nan |                nan     |       nan     |         2666 |        -0.057 |
| SO2      | nickel        | Sorowako (Indonesia)                       |   2192 |              nan |                nan     |       nan     |         2643 |         0.049 |
| SO2      | nickel        | Sudbury Copper Cliff (Canada)              |   1745 |              nan |                nan     |       nan     |         3940 |         0.054 |
| SO2      | pgm_palladium | Norilsk Nadezhda (Russia)                  |   1351 |              nan |                nan     |       nan     |        15851 |         0.829 |
| SO2      | pgm_palladium | Norilsk Nickel plant (Russia)              |   1366 |              nan |                nan     |       nan     |        15792 |         0.848 |
| SO2      | pgm_platinum  | Polokwane smelter (S. Africa)              |   2405 |              nan |                nan     |       nan     |         2998 |        -0.061 |
| SO2      | pgm_platinum  | Rustenburg / Waterval smelters (S. Africa) |   2435 |              nan |                nan     |       nan     |         2843 |         0.063 |
| SO2      | rare_earths   | Baotou rare earth / steel (China)          |   2379 |              nan |                nan     |       nan     |         3514 |         0.146 |

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

