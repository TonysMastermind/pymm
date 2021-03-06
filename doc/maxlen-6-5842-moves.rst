Tree analysis for data/maxlen-6-5842-moves.json
===============================================

Average game: 4.5077 moves, Longest game: 6 moves


.. table:: Prefix properties of a game tree (\$: problem size <= possible scores, \+: optimal split, \*: root code not a solution.)
  :widths: 1 1 1 1 1 1 1 1 
  :column-wrapping: false true true true true true true true
  :column-alignment: left right right right right right right right
  :column-dividers: single single single single single single single single single


  ================================== ====== ========= ============ ============== =========== ============ =============
  prefix                              flags #children problem size max subproblem #preserving #distinct/in #distinct/all
  ================================== ====== ========= ============ ============== =========== ============ =============
  ([3210],)                                        13        1,296            312          48           56            56
  ([3210], [0021])                     \$\*         4            9              3           2            9           774
  ([3210], [2100])                     \$\*         4            8              3           2            8           774
  ([3210], [2420])                       \*         9          132             30           2           69           694
  ([3210], [2420])                       \*         9           48             10           2           26           694
  ([3210], [3100])                     \$\*         4            6              3           2            6           774
  ([3210], [4321])                                 10          136             29           1          135         1,294
  ([3210], [5420])                                 13          252             57           1          251         1,294
  ([3210], [5420])                       \*        12           96             19           1           96         1,294
  ([3210], [5420])                       \*         7           20              6           1           20         1,294
  ([3210], [5421])                                 13          312             64           1          311         1,294
  ([3210], [5440])                       \*         8           16              4           2           12           694
  ([3210], [5441])                                 12          152             30           1          151         1,294
  ([3210], [5441])                       \*        13          108             22           1          108         1,294
  ([3210], [0021], [1000])           \$\*\+         3            3              1           2            3           773
  ([3210], [0021], [1000])           \$\*\+         3            3              1           2            3           773
  ([3210], [2100], [0200])           \$\*\+         3            3              1           2            3           773
  ([3210], [2100], [0200])           \$\*\+         3            3              1           2            3           773
  ([3210], [2420], [1100])             \$\*         5            6              2           1            6         1,293
  ([3210], [2420], [1204])               \$         8           10              2           1            9         1,293
  ([3210], [2420], [1220])             \$\*         8           10              2           1           10         1,293
  ([3210], [2420], [1314])             \$\*         9           14              2           1           14         1,293
  ([3210], [2420], [2051])           \$\*\+         6            6              1           1            6         1,293
  ([3210], [2420], [2100])                          8           17              3           1           16         1,293
  ([3210], [2420], [2100])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [2420], [2315])                          9           18              4           1           17         1,293
  ([3210], [2420], [3031])                         10           25              6           1           24         1,293
  ([3210], [2420], [3051])             \$\*         8           10              2           1           10         1,293
  ([3210], [2420], [4000])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [2420], [4100])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [2420], [4300])             \$\*         7            9              2           1            9         1,293
  ([3210], [2420], [5012])                         10           30              6           1           29         1,293
  ([3210], [2420], [5314])           \$\*\+         7            7              1           1            7         1,293
  ([3210], [3100], [1100])           \$\*\+         3            3              1           2            3           773
  ([3210], [4321], [0143])                         10           20              4           1           19         1,293
  ([3210], [4321], [0315])             \$\*         9           14              2           1           14         1,293
  ([3210], [4321], [0425])             \$\*         9           11              2           1           11         1,293
  ([3210], [4321], [1024])                          9           20              4           1           19         1,293
  ([3210], [4321], [1030])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [4321], [1300])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [4321], [1421])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [4321], [2311])           \$\*\+         5            5              1           1            5         1,293
  ([3210], [4321], [5103])                         10           29              5           1           28         1,293
  ([3210], [4321], [5302])                         10           26              6           1           25         1,293
  ([3210], [5420], [0040])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5420], [0100])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5420], [0530])               \*        10           19              4           1           19         1,293
  ([3210], [5420], [0530])               \*        10           19              4           1           19         1,293
  ([3210], [5420], [1040])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5420], [1100])             \$\*         9           13              2           1           13         1,293
  ([3210], [5420], [1110])           \$\*\+         6            6              1           1            6         1,293
  ([3210], [5420], [1110])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5420], [1153])               \*        10           21              5           1           21         1,293
  ([3210], [5420], [1314])                         12           31              5           1           30         1,293
  ([3210], [5420], [1441])             \$\*         8           11              2           1           11         1,293
  ([3210], [5420], [1531])             \$\*         9           13              2           1           13         1,293
  ([3210], [5420], [2010])           \$\*\+         6            6              1           1            6         1,293
  ([3210], [5420], [2040])             \$\*         8            9              2           1            9         1,293
  ([3210], [5420], [2115])                         13           57             10           1           56         1,293
  ([3210], [5420], [2201])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5420], [2400])           \$\*\+         6            6              1           1            6         1,293
  ([3210], [5420], [3352])               \*        10           16              4           1           16         1,293
  ([3210], [5420], [4000])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5420], [4100])                         12           50              9           1           49         1,293
  ([3210], [5420], [4140])             \$\*         8           10              2           1           10         1,293
  ([3210], [5420], [4251])                         10           23              7           1           22         1,293
  ([3210], [5420], [5000])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5420], [5253])               \*         9           21              4           1           21         1,293
  ([3210], [5421], [0100])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5421], [1354])                         10           32              6           1           31         1,293
  ([3210], [5421], [1451])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5421], [1521])             \$\*         4            5              2           1            5         1,293
  ([3210], [5421], [2443])                         13           63             12           1           62         1,293
  ([3210], [5421], [3503])               \*        11           22              4           1           22         1,293
  ([3210], [5421], [4003])                         11           28              4           1           27         1,293
  ([3210], [5421], [4150])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5421], [4223])             \$\*         7            8              2           1            8         1,293
  ([3210], [5421], [4325])                         10           34              7           1           33         1,293
  ([3210], [5421], [5302])               \*         9           16              3           1           16         1,293
  ([3210], [5421], [5352])               \*        13           64             12           1           64         1,293
  ([3210], [5421], [5352])               \*        11           27              5           1           27         1,293
  ([3210], [5440], [4400])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5440], [4400])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5440], [5500])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5441], [0404])             \$\*        10           13              2           1           13         1,293
  ([3210], [5441], [1400])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5441], [2000])           \$\*\+         3            3              1           1            3         1,293
  ([3210], [5441], [2052])             \$\*         9           14              3           1           14         1,293
  ([3210], [5441], [2511])             \$\*         6            7              2           1            7         1,293
  ([3210], [5441], [2524])             \$\*        10           14              3           1           14         1,293
  ([3210], [5441], [2545])               \*        10           20              3           1           20         1,293
  ([3210], [5441], [3053])             \$\*         9           14              2           1           14         1,293
  ([3210], [5441], [4343])               \*        11           22              3           1           22         1,293
  ([3210], [5441], [4401])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5441], [4530])             \$\*         9           11              2           1           11         1,293
  ([3210], [5441], [4542])                         10           21              3           1           20         1,293
  ([3210], [5441], [5054])                         12           30              5           1           29         1,293
  ([3210], [5441], [5110])           \$\*\+         5            5              1           1            5         1,293
  ([3210], [5441], [5150])             \$\*         7            8              2           1            8         1,293
  ([3210], [5441], [5200])           \$\*\+         4            4              1           1            4         1,293
  ([3210], [5441], [5404])               \$         8           12              2           1           11         1,293
  ([3210], [5441], [5524])               \*        10           21              4           1           21         1,293
  ([3210], [5441], [5530])               \*         9           17              2           1           17         1,293
  ([3210], [5441], [5550])             \$\*         9           10              2           1           10         1,293
  ([3210], [2420], [2100], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [2100], [1100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [2100], [3300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [2315], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [2315], [1010])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [2420], [3031], [1010])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [2420], [3031], [5000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [3031], [5000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [3031], [5300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [2420], [5012], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [2420], [5012], [4000])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [2420], [5012], [4130])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [2420], [5012], [5030])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [0143], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [0143], [2500])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [1024], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [4321], [1024], [2000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [4321], [1024], [5100])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [5103], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [5103], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [4321], [5103], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [4321], [5103], [2000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [5103], [2510])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [4321], [5302], [0220])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [4321], [5302], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [4321], [5302], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [4321], [5302], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [0530], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [0530], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [0530], [3302])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [0530], [5501])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [1153], [0100])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5420], [1153], [3000])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5420], [1314], [2200])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5420], [1314], [3300])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [1314], [3300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [1314], [3530])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5420], [2115], [0100])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [5420], [2115], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [2115], [1352])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5420], [2115], [3302])     \$\*         7            8              2           1            8         1,292
  ([3210], [5420], [2115], [4040])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5420], [2115], [4110])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [5420], [2115], [5000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [2115], [5000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [2115], [5500])     \$\*         8           10              2           1           10         1,292
  ([3210], [5420], [3352], [4110])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [4100], [2421])   \$\*\+         9            9              1           1            9         1,292
  ([3210], [5420], [4100], [3000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [4100], [3310])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [4100], [4342])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5420], [4100], [5132])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5420], [4100], [5332])     \$\*         7            8              2           1            8         1,292
  ([3210], [5420], [4251], [2200])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [4251], [2402])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5420], [5253], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [5253], [2000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5420], [5253], [3200])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5420], [5253], [4000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [1354], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [1354], [1100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [1354], [1300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [1354], [2000])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [1354], [2520])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [5421], [1354], [4000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [2443], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [2443], [1031])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5421], [2443], [2400])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5421], [2443], [4100])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [2443], [4351])   \$\*\+         9            9              1           1            9         1,292
  ([3210], [5421], [2443], [5000])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [2443], [5050])     \$\*         6            7              2           1            7         1,292
  ([3210], [5421], [2443], [5252])     \$\*        10           12              2           1           12         1,292
  ([3210], [5421], [3503], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [3503], [2000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [3503], [4100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4003], [0100])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [4003], [0100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4003], [0100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4003], [3300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4003], [3300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4003], [3300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [4325], [0130])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [4325], [1400])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [5421], [4325], [4000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [4325], [4141])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [4325], [5100])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5421], [5302], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5302], [1100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [5352], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [1210])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5421], [5352], [1500])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5421], [5352], [2000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5421], [5352], [2440])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5421], [5352], [2543])   \$\*\+         8            8              1           1            8         1,292
  ([3210], [5421], [5352], [3342])     \$\*         9           12              2           1           12         1,292
  ([3210], [5421], [5352], [4100])   \$\*\+         6            6              1           1            6         1,292
  ([3210], [5421], [5352], [4142])     \$\*         8           10              2           1           10         1,292
  ([3210], [5421], [5352], [4422])   \$\*\+         7            7              1           1            7         1,292
  ([3210], [5441], [2052], [0000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [2052], [0300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [2524], [0000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [2545], [0500])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [2545], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [2545], [4000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4343], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4343], [2000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4343], [2020])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4343], [5100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4343], [5500])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4542], [0050])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4542], [1000])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4542], [4100])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [4542], [4400])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [5054], [0300])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [5054], [1000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5441], [5054], [4000])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5441], [5054], [4300])   \$\*\+         5            5              1           1            5         1,292
  ([3210], [5441], [5524], [0030])   \$\*\+         4            4              1           1            4         1,292
  ([3210], [5441], [5524], [0050])   \$\*\+         3            3              1           1            3         1,292
  ([3210], [5441], [5524], [1000])   \$\*\+         3            3              1           1            3         1,292
  ================================== ====== ========= ============ ============== =========== ============ =============
