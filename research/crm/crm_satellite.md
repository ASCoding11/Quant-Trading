## Critical raw materials: satellite activity at smelters vs futures

MODIS daily thermal anomalies (Terra + Aqua, 1 km) at 25 plants, 2012-01-01 to 2026-10-23. Signal on each Friday uses satellite days up to 12 days earlier (publication lag). Weekly futures returns, Friday close to Friday close; direction fixed on 2012-2019, judged on 2020-2026. Nickel is tested on the PICK miners ETF (no free nickel futures series).

| signal                               | commodity     | instrument   | direction       |   weeks_train |   weeks_test |   corr_train |   t_train |   sharpe_train |   hit_train |   corr_test |   t_test |   sharpe_test |   hit_test |
|:-------------------------------------|:--------------|:-------------|:----------------|--------------:|-------------:|-------------:|----------:|---------------:|------------:|------------:|---------:|--------------:|-----------:|
| level (28d FRP vs its trailing year) | copper        | HG=F         | follow activity |           360 |          356 |       -0.021 |    -0.39  |          0.198 |       0.511 |      -0.07  |   -1.321 |        -0.735 |      0.475 |
| level (28d FRP vs its trailing year) | nickel        | PICK         | fade activity   |           360 |          356 |       -0.035 |    -0.655 |          0.842 |       0.561 |      -0.064 |   -1.216 |         0.711 |      0.539 |
| level (28d FRP vs its trailing year) | pgm_palladium | PA=F         | follow activity |           360 |          356 |        0.008 |     0.159 |          0.265 |       0.425 |      -0.038 |   -0.711 |        -0.328 |      0.388 |
| level (28d FRP vs its trailing year) | pgm_platinum  | PL=F         | fade activity   |           360 |          356 |       -0.034 |    -0.646 |          0.595 |       0.542 |      -0.045 |   -0.849 |         0.679 |      0.486 |
| level (28d FRP vs its trailing year) | aluminium     | ALI=F        | fade activity   |           295 |          356 |       -0.005 |    -0.081 |          0.264 |       0.305 |      -0.093 |   -1.765 |         0.859 |      0.469 |
| level (28d FRP vs its trailing year) | rare_earths   | REMX         | follow activity |           360 |          356 |       -0.01  |    -0.182 |          0.337 |       0.503 |      -0.035 |   -0.658 |         0.079 |      0.483 |
| 4-week change of the level           | copper        | HG=F         | fade activity   |           356 |          356 |       -0.064 |    -1.205 |          0.319 |       0.525 |      -0.015 |   -0.286 |         0.749 |      0.542 |
| 4-week change of the level           | nickel        | PICK         | fade activity   |           356 |          356 |       -0.031 |    -0.591 |          0.165 |       0.534 |      -0.021 |   -0.388 |         0.304 |      0.486 |
| 4-week change of the level           | pgm_palladium | PA=F         | follow activity |           356 |          356 |        0.018 |     0.333 |          0.126 |       0.32  |      -0.01  |   -0.185 |        -0.184 |      0.289 |
| 4-week change of the level           | pgm_platinum  | PL=F         | fade activity   |           356 |          356 |       -0.021 |    -0.401 |          0.151 |       0.5   |       0.035 |    0.667 |        -0.17  |      0.449 |
| 4-week change of the level           | aluminium     | ALI=F        | fade activity   |           295 |          356 |       -0.086 |    -1.483 |          0.282 |       0.359 |      -0.024 |   -0.443 |         0.196 |      0.41  |
| 4-week change of the level           | rare_earths   | REMX         | follow activity |           356 |          356 |        0.058 |     1.089 |          0.023 |       0.497 |      -0.054 |   -1.012 |        -0.259 |      0.461 |

### Detection by site (is the plant visible to MODIS?)

| commodity     | site                                       |   days |   days_with_fire |   share_days_with_fire |   mean_frp_mw |
|:--------------|:-------------------------------------------|-------:|-----------------:|-----------------------:|--------------:|
| aluminium     | EGA Jebel Ali (UAE)                        |   5234 |               21 |                  0.004 |         0.242 |
| aluminium     | Hongqiao Zouping (China)                   |   5234 |               37 |                  0.007 |         0.15  |
| aluminium     | Krasnoyarsk aluminium (Russia)             |   5242 |               82 |                  0.016 |         0.509 |
| aluminium     | Xinfa Chiping (China)                      |   5234 |              135 |                  0.026 |         1.062 |
| copper        | Altonorte smelter (Chile)                  |   5220 |             1026 |                  0.197 |         3.088 |
| copper        | Caletones smelter (Chile)                  |   5228 |             2645 |                  0.506 |        25.447 |
| copper        | Chuquicamata smelter (Chile)               |   5220 |             1930 |                  0.37  |        21.169 |
| copper        | Guixi smelter (China)                      |   5242 |              183 |                  0.035 |         1.583 |
| copper        | Kolwezi copper-cobalt (DRC)                |   5228 |              946 |                  0.181 |        45.155 |
| copper        | Mount Isa smelter (Australia)              |   5242 |             2512 |                  0.479 |        22.681 |
| copper        | Olympic Dam (Australia)                    |   5242 |              137 |                  0.026 |         0.314 |
| copper        | Potrerillos smelter (Chile)                |   5220 |              760 |                  0.146 |         7.354 |
| copper        | Tongling copper (China)                    |   5242 |              124 |                  0.024 |         0.516 |
| nickel        | IMIP Morowali (Indonesia)                  |   5234 |              532 |                  0.102 |         4.879 |
| nickel        | IWIP Weda Bay (Indonesia)                  |   5242 |              372 |                  0.071 |         2.74  |
| nickel        | Kalgoorlie nickel smelter (Australia)      |   5234 |             2058 |                  0.393 |        28.407 |
| nickel        | Konawe / Morosi (Indonesia)                |   5234 |              787 |                  0.15  |         7.802 |
| nickel        | Obi Island (Indonesia)                     |   5234 |              714 |                  0.136 |         4.79  |
| nickel        | Sorowako (Indonesia)                       |   5234 |             2781 |                  0.531 |       216.397 |
| nickel        | Sudbury Copper Cliff (Canada)              |   5228 |               21 |                  0.004 |         0.751 |
| pgm_palladium | Norilsk Nadezhda (Russia)                  |   5228 |              767 |                  0.147 |        26.053 |
| pgm_palladium | Norilsk Nickel plant (Russia)              |   5228 |              838 |                  0.16  |        27.412 |
| pgm_platinum  | Polokwane smelter (S. Africa)              |   5228 |              128 |                  0.024 |         4.035 |
| pgm_platinum  | Rustenburg / Waterval smelters (S. Africa) |   5228 |             1577 |                  0.302 |        10.124 |
| rare_earths   | Baotou rare earth / steel (China)          |   5234 |             2591 |                  0.495 |        70.101 |

### Latest readings

```
{
 "level (28d FRP vs its trailing year)": {
  "aluminium": 0.0,
  "copper": -0.403,
  "nickel": 1.012,
  "pgm_palladium": 6.835,
  "pgm_platinum": 0.0,
  "rare_earths": -0.298
 },
 "4-week change of the level": {
  "aluminium": -2.667,
  "copper": -1.041,
  "nickel": -0.383,
  "pgm_palladium": -1.438,
  "pgm_platinum": -6.393,
  "rare_earths": -0.152
 }
}
```

