# Origin-Pakheta Calculus v0 Scan

**Generated (UTC):** 2026-06-09
**Script:** `experiments/origin_pakheta_calculus.py`
**Range:** `2..10000`
**Controls:** `250` shell shuffles, seed `62226`

## Purpose

This is the first executable Origin-Pakheta calculus. It treats
positive integers as relationship-fields and exact arithmetic
maps as contexts. The first usable object is a path commutator:

```text
Delta(A, B; n) = A(B(n)) / B(A(n))
```

If `Delta = 1`, the two contexts commute at `n`. If not, the
integer field remembers the path order.

## v0 Operators

| Symbol | Definition | Pakheta reading |
| --- | --- | --- |
| `C(n)` | `rad(n)` | compression / squarefree field skeleton |
| `R_min(n)` | remove one least-prime factor | return one layer toward `1` |
| `R_p(n)` | remove one selected `p` layer if present | selected return context |
| `G_p(n)` | `p * n` for prime `p` | gather one prime facet into the field |
| `Delta(A,B;n)` | `A(B(n)) / B(A(n))` | path-order residue |

## Exact Formula Checks

| commutator | identity | mismatches |
| --- | --- | --- |
| C/R_min | `C(R_min(n)) / R_min(C(n)) = spf(n) if v_spf(n)(n) > 1 else 1` | 0 |
| C/R_2 | `C(R_2(n)) / R_2(C(n)) = 2 if v_2(n) > 1 else 1` | 0 |
| C/R_3 | `C(R_3(n)) / R_3(C(n)) = 3 if v_3(n) > 1 else 1` | 0 |
| C/R_5 | `C(R_5(n)) / R_5(C(n)) = 5 if v_5(n) > 1 else 1` | 0 |
| C/R_7 | `C(R_7(n)) / R_7(C(n)) = 7 if v_7(n) > 1 else 1` | 0 |
| C/G_2 | `C(G_2(n)) / G_2(C(n)) = 1/2 if 2 divides n else 1` | 0 |
| C/G_3 | `C(G_3(n)) / G_3(C(n)) = 1/3 if 3 divides n else 1` | 0 |
| C/G_5 | `C(G_5(n)) / G_5(C(n)) = 1/5 if 5 divides n else 1` | 0 |

## Path-Sensitivity Summary

| path_gap | nonzero | rate | mean_log_gap | max_log_gap |
| --- | --- | --- | --- | --- |
| compression_return_log_gap | 3302/9999 | 0.3302 | 0.2837 | 4.5747 |
| return_2_log_gap | 2500/9999 | 0.2500 | 0.1733 | 0.6931 |
| return_3_log_gap | 1111/9999 | 0.1111 | 0.1221 | 1.0986 |
| return_5_log_gap | 400/9999 | 0.0400 | 0.0644 | 1.6094 |
| return_7_log_gap | 204/9999 | 0.0204 | 0.0397 | 1.9459 |
| gather_2_log_gap | 5000/9999 | 0.5001 | 0.3466 | 0.6931 |
| gather_3_log_gap | 3333/9999 | 0.3333 | 0.3662 | 1.0986 |
| gather_5_log_gap | 2000/9999 | 0.2000 | 0.3219 | 1.6094 |

## Shell-Controlled Signals

Targets and metrics are shell-centered and residualized against
`log(n)`. Controls shuffle target residuals within emanation shells.

| target | metric | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- |
| compression_return_log_gap | radical_compression | 0.6819 | 0.0102 | 0.0384 | 0/250 | 0.0040 |
| return_2_log_gap | repeated_factor_2 | 1.0000 | 0.0115 | 0.0506 | 0/250 | 0.0040 |
| return_3_log_gap | repeated_factor_3 | 1.0000 | 0.0118 | 0.0401 | 0/250 | 0.0040 |
| return_5_log_gap | repeated_factor_5 | 1.0000 | 0.0111 | 0.0430 | 0/250 | 0.0040 |
| return_7_log_gap | repeated_factor_7 | 1.0000 | 0.0106 | 0.0412 | 0/250 | 0.0040 |
| gather_2_log_gap | has_factor_2 | 1.0000 | 0.0093 | 0.0333 | 0/250 | 0.0040 |
| gather_3_log_gap | has_factor_3 | 1.0000 | 0.0093 | 0.0367 | 0/250 | 0.0040 |
| gather_5_log_gap | has_factor_5 | 1.0000 | 0.0091 | 0.0334 | 0/250 | 0.0040 |

## Largest C/R_min Path Gaps

| n | Omega | spf | v_spf | radical_compression | C_R_gap | C_G2_gap | C_G3_gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9409 | 2 | 97 | 2 | 0.9897 | 4.5747 | 0.0000 | 0.0000 |
| 7921 | 2 | 89 | 2 | 0.9888 | 4.4886 | 0.0000 | 0.0000 |
| 6889 | 2 | 83 | 2 | 0.9880 | 4.4188 | 0.0000 | 0.0000 |
| 6241 | 2 | 79 | 2 | 0.9873 | 4.3694 | 0.0000 | 0.0000 |
| 5329 | 2 | 73 | 2 | 0.9863 | 4.2905 | 0.0000 | 0.0000 |
| 5041 | 2 | 71 | 2 | 0.9859 | 4.2627 | 0.0000 | 0.0000 |
| 4489 | 2 | 67 | 2 | 0.9851 | 4.2047 | 0.0000 | 0.0000 |
| 3721 | 2 | 61 | 2 | 0.9836 | 4.1109 | 0.0000 | 0.0000 |
| 3481 | 2 | 59 | 2 | 0.9831 | 4.0775 | 0.0000 | 0.0000 |
| 2809 | 2 | 53 | 2 | 0.9811 | 3.9703 | 0.0000 | 0.0000 |
| 2209 | 2 | 47 | 2 | 0.9787 | 3.8501 | 0.0000 | 0.0000 |
| 1849 | 2 | 43 | 2 | 0.9767 | 3.7612 | 0.0000 | 0.0000 |

## Interpretation

This is new math in the working sense: we now have named operators,
an exact commutator, theorem candidates, executable scans, and
controls. The strongest v0 result is simple but useful:

```text
compress then return != return then compress
exactly when the least-prime return layer is repeated
```

The selected-prime return family generalizes this:

```text
compress then R_p != R_p then compress
exactly when the chosen p-layer is repeated
```

That gives the Origin-Pakheta program a first path-sensitive
calculus. It does not prove the full Origin Reframe, but it creates
a usable formal surface where Pakheta ideas become exact arithmetic.

