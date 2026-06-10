# Origin-Pakheta Commutator Catalog (v1)

**Generated (UTC):** 2026-06-10
**Script:** `experiments/origin_pakheta_commutator_catalog.py`
**Range:** `2..10000`
**Pairs:** `105` unordered pairs over `15` operators

## Operator Roster

| symbol | definition |
| --- | --- |
| C | `rad(n)` |
| R_min | `n / spf(n)` |
| R_max | `n / gpf(n)` |
| R_2 | `n / 2 if 2 | n` |
| R_3 | `n / 3 if 3 | n` |
| G_2 | `2n` |
| G_3 | `3n` |
| Q | `n / rad(n)` |
| B | `d(n)` |
| T | `phi(n)` |
| M | `lambda(n)` |
| S | `sigma(n)` |
| P | `psi(n)` |
| N- | `prod(p-1)` |
| N+ | `prod(p+1)` |

## Summary

| classification | pairs |
| --- | --- |
| always | 9 |
| finite? | 4 |
| never | 7 |
| sparse | 48 |
| dense | 37 |

Proven rows: `43/105` (Theorems 4-14 and Catalog Lemmas C1-C7); the remaining `62` are empirical.

## Full Catalog

`class` heuristics: `always` = no violation found; `finite?` = no
commuting n found in the upper half of the range; `dense` = locus
density >= 0.25; `sparse` = the rest. `count trend` shows the
commuting count at quarter checkpoints of the range.

| pair | class | status | commuting n | density | first | last | first violation | count trend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R_min / R_max | always | Lemma C7 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_max / R_2 | always | Lemma C9 (always for p = 2) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_max / G_2 | always | Lemma C10 (always for p = 2) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_2 / R_3 | always | Lemma C2 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_2 / G_3 | always | Lemma C3 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_2 / Q | always | Lemma C8 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_3 / G_2 | always | Lemma C3 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_3 / Q | always | Lemma C8 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| G_2 / G_3 | always | Lemma C1 (always) | 9999 | 1.0000 | 2 | 10000 | - | 2499 -> 4999 -> 7499 -> 9999 |
| R_min / N+ | finite? | Lemma C13 (locus: n = 2) | 1 | 0.0001 | 2 | 2 | 3 | 1 -> 1 -> 1 -> 1 |
| R_max / S | finite? | Lemma C14 (locus: n = 2) | 1 | 0.0001 | 2 | 2 | 3 | 1 -> 1 -> 1 -> 1 |
| R_max / N+ | finite? | Lemma C15 (locus: n = 2) | 1 | 0.0001 | 2 | 2 | 3 | 1 -> 1 -> 1 -> 1 |
| T / S | finite? | empirical | 6 | 0.0006 | 9 | 3872 | 2 | 5 -> 6 -> 6 -> 6 |
| G_2 / S | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_2 / N- | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_2 / N+ | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_3 / B | never | Lemma C12 (never for p >= 3) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_3 / S | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_3 / N- | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| G_3 / N+ | never | Lemma C11 (never) | 0 | 0.0000 | - | - | 2 | 0 -> 0 -> 0 -> 0 |
| R_2 / N+ | sparse | Thm 14 (exact formula) | 12 | 0.0012 | 4 | 8192 | 2 | 10 -> 11 -> 11 -> 12 |
| R_2 / N- | sparse | Thm 12 (exact formula) | 13 | 0.0013 | 2 | 8192 | 3 | 11 -> 12 -> 12 -> 13 |
| S / N- | sparse | empirical | 17 | 0.0017 | 224 | 9092 | 2 | 6 -> 11 -> 13 -> 17 |
| B / T | sparse | empirical | 24 | 0.0024 | 2 | 9240 | 3 | 17 -> 20 -> 23 -> 24 |
| R_max / N- | sparse | empirical | 25 | 0.0025 | 2 | 8192 | 5 | 21 -> 23 -> 24 -> 25 |
| M / S | sparse | empirical | 26 | 0.0026 | 9 | 9894 | 2 | 13 -> 18 -> 23 -> 26 |
| P / N- | sparse | empirical | 28 | 0.0028 | 98 | 9800 | 2 | 12 -> 19 -> 23 -> 28 |
| R_min / S | sparse | empirical | 35 | 0.0035 | 2 | 9522 | 3 | 18 -> 25 -> 31 -> 35 |
| B / M | sparse | empirical | 42 | 0.0042 | 2 | 9912 | 3 | 21 -> 30 -> 36 -> 42 |
| R_2 / S | sparse | empirical | 49 | 0.0049 | 9 | 9801 | 2 | 24 -> 34 -> 42 -> 49 |
| B / N- | sparse | empirical | 81 | 0.0081 | 2 | 9680 | 3 | 38 -> 54 -> 66 -> 81 |
| T / N+ | sparse | empirical | 83 | 0.0083 | 26 | 9585 | 2 | 32 -> 49 -> 67 -> 83 |
| M / P | sparse | empirical | 151 | 0.0151 | 10 | 9798 | 2 | 52 -> 98 -> 125 -> 151 |
| B / S | sparse | empirical | 210 | 0.0210 | 3 | 9904 | 2 | 74 -> 117 -> 159 -> 210 |
| B / N+ | sparse | empirical | 227 | 0.0227 | 3 | 10000 | 2 | 102 -> 152 -> 188 -> 227 |
| M / N+ | sparse | empirical | 243 | 0.0243 | 70 | 9916 | 2 | 95 -> 152 -> 199 -> 243 |
| N- / N+ | sparse | empirical | 263 | 0.0263 | 26 | 9984 | 2 | 96 -> 165 -> 216 -> 263 |
| B / P | sparse | empirical | 265 | 0.0265 | 3 | 9892 | 2 | 108 -> 179 -> 218 -> 265 |
| T / P | sparse | empirical | 333 | 0.0333 | 10 | 9984 | 2 | 134 -> 212 -> 287 -> 333 |
| R_max / P | sparse | empirical | 391 | 0.0391 | 2 | 10000 | 3 | 151 -> 243 -> 324 -> 391 |
| R_2 / M | sparse | empirical | 412 | 0.0412 | 2 | 9984 | 3 | 112 -> 214 -> 311 -> 412 |
| R_max / T | sparse | empirical | 415 | 0.0415 | 2 | 10000 | 5 | 171 -> 265 -> 347 -> 415 |
| C / S | sparse | empirical | 615 | 0.0615 | 2 | 9986 | 3 | 182 -> 328 -> 475 -> 615 |
| S / P | sparse | empirical | 616 | 0.0616 | 2 | 9986 | 3 | 183 -> 329 -> 476 -> 616 |
| S / N+ | sparse | empirical | 616 | 0.0616 | 2 | 9986 | 3 | 183 -> 329 -> 476 -> 616 |
| Q / S | sparse | empirical | 678 | 0.0678 | 2 | 9986 | 3 | 198 -> 360 -> 526 -> 678 |
| R_min / M | sparse | empirical | 716 | 0.0716 | 2 | 9995 | 5 | 196 -> 375 -> 544 -> 716 |
| Q / P | sparse | empirical | 753 | 0.0753 | 2 | 9986 | 3 | 223 -> 409 -> 582 -> 753 |
| C / P | sparse | empirical | 765 | 0.0765 | 2 | 9986 | 3 | 221 -> 408 -> 591 -> 765 |
| G_2 / M | sparse | empirical | 786 | 0.0786 | 2 | 10000 | 3 | 213 -> 411 -> 603 -> 786 |
| C / N+ | sparse | Thm 13 (locus: prod(p+1) squarefree) | 798 | 0.0798 | 2 | 9986 | 3 | 242 -> 435 -> 622 -> 798 |
| P / N+ | sparse | empirical | 878 | 0.0878 | 2 | 9986 | 3 | 246 -> 465 -> 678 -> 878 |
| Q / N+ | sparse | empirical | 983 | 0.0983 | 2 | 9986 | 3 | 283 -> 527 -> 756 -> 983 |
| Q / T | sparse | empirical | 987 | 0.0987 | 2 | 10000 | 5 | 322 -> 560 -> 775 -> 987 |
| C / T | sparse | Thm 10 (exact formula) | 1053 | 0.1053 | 2 | 9967 | 4 | 333 -> 587 -> 828 -> 1053 |
| T / M | sparse | empirical | 1086 | 0.1086 | 2 | 10000 | 8 | 384 -> 627 -> 864 -> 1086 |
| R_min / N- | sparse | empirical | 1124 | 0.1124 | 2 | 9993 | 5 | 289 -> 567 -> 845 -> 1124 |
| C / N- | sparse | Thm 11 (locus: prod(p-1) squarefree) | 1154 | 0.1154 | 2 | 9967 | 5 | 394 -> 666 -> 919 -> 1154 |
| R_3 / N+ | sparse | Thm 14 (exact formula) | 1180 | 0.1180 | 7 | 9997 | 2 | 319 -> 614 -> 898 -> 1180 |
| C / B | sparse | Thm 7 + Cor 7.1 (locus: p^(2^m - 1)) | 1239 | 0.1239 | 2 | 9973 | 4 | 375 -> 678 -> 960 -> 1239 |
| T / N- | sparse | empirical | 1331 | 0.1331 | 2 | 9967 | 5 | 419 -> 741 -> 1046 -> 1331 |
| R_3 / S | sparse | empirical | 1406 | 0.1406 | 4 | 10000 | 2 | 384 -> 732 -> 1067 -> 1406 |
| Q / N- | sparse | empirical | 1486 | 0.1486 | 2 | 9967 | 5 | 467 -> 827 -> 1167 -> 1486 |
| M / N- | sparse | empirical | 1558 | 0.1558 | 2 | 9992 | 5 | 550 -> 915 -> 1250 -> 1558 |
| G_3 / M | sparse | empirical | 1878 | 0.1878 | 3 | 9999 | 2 | 499 -> 966 -> 1427 -> 1878 |
| R_3 / P | sparse | empirical | 2095 | 0.2095 | 7 | 9999 | 2 | 540 -> 1065 -> 1579 -> 2095 |
| Q / B | sparse | empirical | 2189 | 0.2189 | 2 | 9999 | 4 | 587 -> 1136 -> 1664 -> 2189 |
| C / M | sparse | Thm 9 + Cor 9.1 | 2305 | 0.2305 | 2 | 9989 | 4 | 648 -> 1223 -> 1772 -> 2305 |
| R_2 / P | dense | empirical | 2500 | 0.2500 | 4 | 10000 | 2 | 625 -> 1250 -> 1875 -> 2500 |
| R_min / P | dense | empirical | 2501 | 0.2501 | 2 | 10000 | 3 | 626 -> 1251 -> 1876 -> 2501 |
| R_2 / T | dense | empirical | 2501 | 0.2501 | 2 | 10000 | 3 | 626 -> 1251 -> 1876 -> 2501 |
| R_2 / B | dense | Thm 8 (exact formula) | 2549 | 0.2549 | 2 | 9998 | 3 | 649 -> 1284 -> 1917 -> 2549 |
| Q / M | dense | empirical | 2696 | 0.2696 | 2 | 9990 | 5 | 740 -> 1407 -> 2057 -> 2696 |
| R_max / M | dense | empirical | 2744 | 0.2744 | 2 | 10000 | 5 | 752 -> 1434 -> 2095 -> 2744 |
| R_3 / N- | dense | Thm 12 (exact formula) | 3002 | 0.3002 | 2 | 10000 | 3 | 841 -> 1585 -> 2295 -> 3002 |
| R_3 / G_3 | dense | Lemma C4 (locus: 3 | n) | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| G_3 / Q | dense | Lemma C6 (locus: 3 | n) | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| G_3 / T | dense | empirical | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| G_3 / P | dense | empirical | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| R_3 / T | dense | empirical | 3590 | 0.3590 | 2 | 10000 | 3 | 963 -> 1858 -> 2726 -> 3590 |
| R_min / T | dense | empirical | 3612 | 0.3612 | 2 | 10000 | 5 | 904 -> 1806 -> 2709 -> 3612 |
| R_3 / M | dense | empirical | 4033 | 0.4033 | 2 | 10000 | 3 | 1113 -> 2115 -> 3077 -> 4033 |
| C / G_2 | dense | Thm 6 (locus: 2 ∤ n) | 4999 | 0.4999 | 3 | 9999 | 2 | 1249 -> 2499 -> 3749 -> 4999 |
| G_2 / B | dense | Lemma C12 (locus: 2 ∤ n) | 4999 | 0.4999 | 3 | 9999 | 2 | 1249 -> 2499 -> 3749 -> 4999 |
| R_min / G_2 | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| R_2 / G_2 | dense | Lemma C4 (locus: 2 | n) | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| G_2 / Q | dense | Lemma C6 (locus: 2 | n) | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| G_2 / T | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| G_2 / P | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| R_3 / B | dense | Thm 8 (exact formula) | 5284 | 0.5285 | 2 | 10000 | 3 | 1322 -> 2640 -> 3959 -> 5284 |
| C / Q | dense | Lemma C5 (locus: n squarefree) | 6082 | 0.6083 | 2 | 9998 | 4 | 1522 -> 3041 -> 4560 -> 6082 |
| R_max / Q | dense | empirical | 6484 | 0.6485 | 2 | 10000 | 12 | 1682 -> 3294 -> 4894 -> 6484 |
| C / G_3 | dense | Thm 6 (locus: 3 ∤ n) | 6666 | 0.6667 | 2 | 10000 | 3 | 1666 -> 3333 -> 4999 -> 6666 |
| R_min / G_3 | dense | empirical | 6667 | 0.6668 | 2 | 10000 | 5 | 1667 -> 3333 -> 5000 -> 6667 |
| C / R_min | dense | Cor 4.1 (locus: spf exponent 1) | 6697 | 0.6698 | 2 | 9998 | 4 | 1672 -> 3347 -> 5020 -> 6697 |
| R_min / B | dense | empirical | 6697 | 0.6698 | 2 | 9998 | 4 | 1672 -> 3347 -> 5020 -> 6697 |
| R_max / B | dense | empirical | 6845 | 0.6846 | 2 | 9998 | 4 | 1707 -> 3418 -> 5127 -> 6845 |
| C / R_2 | dense | Thm 4 (locus: v_2 <= 1) | 7499 | 0.7500 | 2 | 9999 | 4 | 1874 -> 3749 -> 5624 -> 7499 |
| R_min / R_2 | dense | empirical | 7500 | 0.7501 | 2 | 10000 | 6 | 1875 -> 3750 -> 5625 -> 7500 |
| C / R_3 | dense | Thm 4 (locus: v_3 <= 1) | 8888 | 0.8889 | 2 | 10000 | 9 | 2222 -> 4444 -> 6666 -> 8888 |
| R_min / R_3 | dense | empirical | 8889 | 0.8890 | 2 | 10000 | 15 | 2222 -> 4445 -> 6667 -> 8889 |
| R_min / Q | dense | empirical | 9384 | 0.9385 | 2 | 10000 | 18 | 2349 -> 4693 -> 7039 -> 9384 |
| C / R_max | dense | empirical | 9597 | 0.9598 | 2 | 9999 | 4 | 2339 -> 4746 -> 7165 -> 9597 |
| R_max / G_3 | dense | Lemma C10 (locus: gpf(n) >= 3) | 9986 | 0.9987 | 3 | 10000 | 2 | 2488 -> 4987 -> 7487 -> 9986 |
| R_max / R_3 | dense | Lemma C9 (locus: not (gpf = 3, v_3 = 1, omega >= 2)) | 9988 | 0.9989 | 2 | 10000 | 6 | 2490 -> 4989 -> 7488 -> 9988 |

## Theorem Candidate Queue

Unproven pairs ordered by how structured the locus looks (always,
then finite-looking, then sparse, then dense). Each row is a
candidate for the next exact identity or locus characterization.

| pair | class | status | commuting n | density | first | last | first violation | count trend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T / S | finite? | empirical | 6 | 0.0006 | 9 | 3872 | 2 | 5 -> 6 -> 6 -> 6 |
| S / N- | sparse | empirical | 17 | 0.0017 | 224 | 9092 | 2 | 6 -> 11 -> 13 -> 17 |
| B / T | sparse | empirical | 24 | 0.0024 | 2 | 9240 | 3 | 17 -> 20 -> 23 -> 24 |
| R_max / N- | sparse | empirical | 25 | 0.0025 | 2 | 8192 | 5 | 21 -> 23 -> 24 -> 25 |
| M / S | sparse | empirical | 26 | 0.0026 | 9 | 9894 | 2 | 13 -> 18 -> 23 -> 26 |
| P / N- | sparse | empirical | 28 | 0.0028 | 98 | 9800 | 2 | 12 -> 19 -> 23 -> 28 |
| R_min / S | sparse | empirical | 35 | 0.0035 | 2 | 9522 | 3 | 18 -> 25 -> 31 -> 35 |
| B / M | sparse | empirical | 42 | 0.0042 | 2 | 9912 | 3 | 21 -> 30 -> 36 -> 42 |
| R_2 / S | sparse | empirical | 49 | 0.0049 | 9 | 9801 | 2 | 24 -> 34 -> 42 -> 49 |
| B / N- | sparse | empirical | 81 | 0.0081 | 2 | 9680 | 3 | 38 -> 54 -> 66 -> 81 |
| T / N+ | sparse | empirical | 83 | 0.0083 | 26 | 9585 | 2 | 32 -> 49 -> 67 -> 83 |
| M / P | sparse | empirical | 151 | 0.0151 | 10 | 9798 | 2 | 52 -> 98 -> 125 -> 151 |
| B / S | sparse | empirical | 210 | 0.0210 | 3 | 9904 | 2 | 74 -> 117 -> 159 -> 210 |
| B / N+ | sparse | empirical | 227 | 0.0227 | 3 | 10000 | 2 | 102 -> 152 -> 188 -> 227 |
| M / N+ | sparse | empirical | 243 | 0.0243 | 70 | 9916 | 2 | 95 -> 152 -> 199 -> 243 |
| N- / N+ | sparse | empirical | 263 | 0.0263 | 26 | 9984 | 2 | 96 -> 165 -> 216 -> 263 |
| B / P | sparse | empirical | 265 | 0.0265 | 3 | 9892 | 2 | 108 -> 179 -> 218 -> 265 |
| T / P | sparse | empirical | 333 | 0.0333 | 10 | 9984 | 2 | 134 -> 212 -> 287 -> 333 |
| R_max / P | sparse | empirical | 391 | 0.0391 | 2 | 10000 | 3 | 151 -> 243 -> 324 -> 391 |
| R_2 / M | sparse | empirical | 412 | 0.0412 | 2 | 9984 | 3 | 112 -> 214 -> 311 -> 412 |
| R_max / T | sparse | empirical | 415 | 0.0415 | 2 | 10000 | 5 | 171 -> 265 -> 347 -> 415 |
| C / S | sparse | empirical | 615 | 0.0615 | 2 | 9986 | 3 | 182 -> 328 -> 475 -> 615 |
| S / P | sparse | empirical | 616 | 0.0616 | 2 | 9986 | 3 | 183 -> 329 -> 476 -> 616 |
| S / N+ | sparse | empirical | 616 | 0.0616 | 2 | 9986 | 3 | 183 -> 329 -> 476 -> 616 |
| Q / S | sparse | empirical | 678 | 0.0678 | 2 | 9986 | 3 | 198 -> 360 -> 526 -> 678 |
| R_min / M | sparse | empirical | 716 | 0.0716 | 2 | 9995 | 5 | 196 -> 375 -> 544 -> 716 |
| Q / P | sparse | empirical | 753 | 0.0753 | 2 | 9986 | 3 | 223 -> 409 -> 582 -> 753 |
| C / P | sparse | empirical | 765 | 0.0765 | 2 | 9986 | 3 | 221 -> 408 -> 591 -> 765 |
| G_2 / M | sparse | empirical | 786 | 0.0786 | 2 | 10000 | 3 | 213 -> 411 -> 603 -> 786 |
| P / N+ | sparse | empirical | 878 | 0.0878 | 2 | 9986 | 3 | 246 -> 465 -> 678 -> 878 |
| Q / N+ | sparse | empirical | 983 | 0.0983 | 2 | 9986 | 3 | 283 -> 527 -> 756 -> 983 |
| Q / T | sparse | empirical | 987 | 0.0987 | 2 | 10000 | 5 | 322 -> 560 -> 775 -> 987 |
| T / M | sparse | empirical | 1086 | 0.1086 | 2 | 10000 | 8 | 384 -> 627 -> 864 -> 1086 |
| R_min / N- | sparse | empirical | 1124 | 0.1124 | 2 | 9993 | 5 | 289 -> 567 -> 845 -> 1124 |
| T / N- | sparse | empirical | 1331 | 0.1331 | 2 | 9967 | 5 | 419 -> 741 -> 1046 -> 1331 |
| R_3 / S | sparse | empirical | 1406 | 0.1406 | 4 | 10000 | 2 | 384 -> 732 -> 1067 -> 1406 |
| Q / N- | sparse | empirical | 1486 | 0.1486 | 2 | 9967 | 5 | 467 -> 827 -> 1167 -> 1486 |
| M / N- | sparse | empirical | 1558 | 0.1558 | 2 | 9992 | 5 | 550 -> 915 -> 1250 -> 1558 |
| G_3 / M | sparse | empirical | 1878 | 0.1878 | 3 | 9999 | 2 | 499 -> 966 -> 1427 -> 1878 |
| R_3 / P | sparse | empirical | 2095 | 0.2095 | 7 | 9999 | 2 | 540 -> 1065 -> 1579 -> 2095 |
| Q / B | sparse | empirical | 2189 | 0.2189 | 2 | 9999 | 4 | 587 -> 1136 -> 1664 -> 2189 |
| R_2 / P | dense | empirical | 2500 | 0.2500 | 4 | 10000 | 2 | 625 -> 1250 -> 1875 -> 2500 |
| R_min / P | dense | empirical | 2501 | 0.2501 | 2 | 10000 | 3 | 626 -> 1251 -> 1876 -> 2501 |
| R_2 / T | dense | empirical | 2501 | 0.2501 | 2 | 10000 | 3 | 626 -> 1251 -> 1876 -> 2501 |
| Q / M | dense | empirical | 2696 | 0.2696 | 2 | 9990 | 5 | 740 -> 1407 -> 2057 -> 2696 |
| R_max / M | dense | empirical | 2744 | 0.2744 | 2 | 10000 | 5 | 752 -> 1434 -> 2095 -> 2744 |
| G_3 / T | dense | empirical | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| G_3 / P | dense | empirical | 3333 | 0.3333 | 3 | 9999 | 2 | 833 -> 1666 -> 2500 -> 3333 |
| R_3 / T | dense | empirical | 3590 | 0.3590 | 2 | 10000 | 3 | 963 -> 1858 -> 2726 -> 3590 |
| R_min / T | dense | empirical | 3612 | 0.3612 | 2 | 10000 | 5 | 904 -> 1806 -> 2709 -> 3612 |
| R_3 / M | dense | empirical | 4033 | 0.4033 | 2 | 10000 | 3 | 1113 -> 2115 -> 3077 -> 4033 |
| R_min / G_2 | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| G_2 / T | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| G_2 / P | dense | empirical | 5000 | 0.5001 | 2 | 10000 | 3 | 1250 -> 2500 -> 3750 -> 5000 |
| R_max / Q | dense | empirical | 6484 | 0.6485 | 2 | 10000 | 12 | 1682 -> 3294 -> 4894 -> 6484 |
| R_min / G_3 | dense | empirical | 6667 | 0.6668 | 2 | 10000 | 5 | 1667 -> 3333 -> 5000 -> 6667 |
| R_min / B | dense | empirical | 6697 | 0.6698 | 2 | 9998 | 4 | 1672 -> 3347 -> 5020 -> 6697 |
| R_max / B | dense | empirical | 6845 | 0.6846 | 2 | 9998 | 4 | 1707 -> 3418 -> 5127 -> 6845 |
| R_min / R_2 | dense | empirical | 7500 | 0.7501 | 2 | 10000 | 6 | 1875 -> 3750 -> 5625 -> 7500 |
| R_min / R_3 | dense | empirical | 8889 | 0.8890 | 2 | 10000 | 15 | 2222 -> 4445 -> 6667 -> 8889 |
| R_min / Q | dense | empirical | 9384 | 0.9385 | 2 | 10000 | 18 | 2349 -> 4693 -> 7039 -> 9384 |
| C / R_max | dense | empirical | 9597 | 0.9598 | 2 | 9999 | 4 | 2339 -> 4746 -> 7165 -> 9597 |

## Interpretation

The catalog is an instrument, not evidence: it maps where path
order is and is not remembered across the operator family, and it
turns 'find a new theorem' into a ranked work queue. Proven rows
double as regression anchors -- their loci must match the stated
characterizations exactly, and the test suite checks samples of
each.

