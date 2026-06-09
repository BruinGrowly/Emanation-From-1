# Origin-Pakheta Calculus v0 Scan

**Generated (UTC):** 2026-06-09
**Script:** `experiments/origin_pakheta_calculus.py`
**Range:** `2..1000`
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
| `B(n)` | `divisor_count(n)` | divisor-branching context |
| `M(n)` | `carmichael_lambda(n)` | modular-return exponent/period context |
| `T(n)` | `euler_totient(n)` | modular-return size/density context |
| `Delta(A,B;n)` | `A(B(n)) / B(A(n))` | path-order residue |

## Exact Formula Checks

| commutator | identity | mismatches |
| --- | --- | --- |
| C/R_min | `C(R_min(n)) / R_min(C(n)) = spf(n) if v_{spf(n)}(n) > 1 else 1` | 0 |
| C/R_2 | `C(R_2(n)) / R_2(C(n)) = 2 if v_2(n) > 1 else 1` | 0 |
| C/R_3 | `C(R_3(n)) / R_3(C(n)) = 3 if v_3(n) > 1 else 1` | 0 |
| C/R_5 | `C(R_5(n)) / R_5(C(n)) = 5 if v_5(n) > 1 else 1` | 0 |
| C/R_7 | `C(R_7(n)) / R_7(C(n)) = 7 if v_7(n) > 1 else 1` | 0 |
| C/R_{2,3} | `C(R_S(n)) / R_S(C(n)) = product of selected repeated primes` | 0 |
| C/R_{2,3,5} | `C(R_S(n)) / R_S(C(n)) = product of selected repeated primes` | 0 |
| C/R_{3,5,7} | `C(R_S(n)) / R_S(C(n)) = product of selected repeated primes` | 0 |
| C/G_2 | `C(G_2(n)) / G_2(C(n)) = 1/2 if 2 divides n else 1` | 0 |
| C/G_3 | `C(G_3(n)) / G_3(C(n)) = 1/3 if 3 divides n else 1` | 0 |
| C/G_5 | `C(G_5(n)) / G_5(C(n)) = 1/5 if 5 divides n else 1` | 0 |
| C/B | `C(B(n)) / B(C(n)) = rad(d(n)) / 2^omega(n)` | 0 |
| R_{2,3}/B | `R_S(B(n)) / B(R_S(n)) = formula with rad_S(d(n))` | 0 |
| R_{2,3,5}/B | `R_S(B(n)) / B(R_S(n)) = formula with rad_S(d(n))` | 0 |
| R_{3,5,7}/B | `R_S(B(n)) / B(R_S(n)) = formula with rad_S(d(n))` | 0 |
| C/M | `C(M(n)) / M(C(n)) = lcm formula` | 0 |
| C/T | `C(T(n)) / T(C(n)) = rad(phi(n)) / phi(rad(n))` | 0 |

## Path-Sensitivity Summary

| path_gap | nonzero | rate | mean_log_gap | max_log_gap |
| --- | --- | --- | --- | --- |
| compression_return_log_gap | 332/999 | 0.3323 | 0.2884 | 3.4340 |
| return_2_log_gap | 250/999 | 0.2503 | 0.1735 | 0.6931 |
| return_3_log_gap | 111/999 | 0.1111 | 0.1221 | 1.0986 |
| return_5_log_gap | 40/999 | 0.0400 | 0.0644 | 1.6094 |
| return_7_log_gap | 20/999 | 0.0200 | 0.0390 | 1.9459 |
| gather_2_log_gap | 500/999 | 0.5005 | 0.3469 | 0.6931 |
| gather_3_log_gap | 333/999 | 0.3333 | 0.3662 | 1.0986 |
| gather_5_log_gap | 200/999 | 0.2002 | 0.3222 | 1.6094 |
| compression_divisor_branching_log_gap | 826/999 | 0.8268 | 0.6373 | 2.0794 |
| compression_carmichael_lambda_log_gap | 711/999 | 0.7117 | 0.9902 | 4.8520 |
| compression_totient_log_gap | 836/999 | 0.8368 | 1.4591 | 5.5452 |

## Shell-Controlled Signals

Targets and metrics are shell-centered and residualized against
`log(n)`. Controls shuffle target residuals within emanation shells.

| target | metric | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- |
| compression_return_log_gap | radical_compression | 0.6982 | 0.0275 | 0.1006 | 0/250 | 0.0040 |
| return_2_log_gap | repeated_factor_2 | 1.0000 | 0.0350 | 0.1278 | 0/250 | 0.0040 |
| return_3_log_gap | repeated_factor_3 | 1.0000 | 0.0379 | 0.1340 | 0/250 | 0.0040 |
| return_5_log_gap | repeated_factor_5 | 1.0000 | 0.0381 | 0.1843 | 0/250 | 0.0040 |
| return_7_log_gap | repeated_factor_7 | 1.0000 | 0.0363 | 0.1173 | 0/250 | 0.0040 |
| gather_2_log_gap | has_factor_2 | 1.0000 | 0.0308 | 0.1091 | 0/250 | 0.0040 |
| gather_3_log_gap | has_factor_3 | 1.0000 | 0.0290 | 0.1138 | 0/250 | 0.0040 |
| gather_5_log_gap | has_factor_5 | 1.0000 | 0.0252 | 0.1140 | 0/250 | 0.0040 |
| compression_divisor_branching_log_gap | radical_compression | -0.7231 | 0.0307 | 0.1082 | 0/250 | 0.0040 |
| compression_carmichael_lambda_log_gap | radical_compression | 0.1004 | 0.0242 | 0.0787 | 0/250 | 0.0040 |
| compression_totient_log_gap | radical_compression | -0.2414 | 0.0255 | 0.0830 | 0/250 | 0.0040 |

## Largest C/R_min Path Gaps

| n | Omega | spf | v_spf | radical_compression | C_R_gap | C_G2_gap | C_G3_gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 961 | 2 | 31 | 2 | 0.9677 | 3.4340 | 0.0000 | 0.0000 |
| 841 | 2 | 29 | 2 | 0.9655 | 3.3673 | 0.0000 | 0.0000 |
| 529 | 2 | 23 | 2 | 0.9565 | 3.1355 | 0.0000 | 0.0000 |
| 361 | 2 | 19 | 2 | 0.9474 | 2.9444 | 0.0000 | 0.0000 |
| 289 | 2 | 17 | 2 | 0.9412 | 2.8332 | 0.0000 | 0.0000 |
| 169 | 2 | 13 | 2 | 0.9231 | 2.5649 | 0.0000 | 0.0000 |
| 121 | 2 | 11 | 2 | 0.9091 | 2.3979 | 0.0000 | 0.0000 |
| 343 | 3 | 7 | 3 | 0.9796 | 1.9459 | 0.0000 | 0.0000 |
| 49 | 2 | 7 | 2 | 0.8571 | 1.9459 | 0.0000 | 0.0000 |
| 539 | 3 | 7 | 2 | 0.8571 | 1.9459 | 0.0000 | 0.0000 |
| 637 | 3 | 7 | 2 | 0.8571 | 1.9459 | 0.0000 | 0.0000 |
| 833 | 3 | 7 | 2 | 0.8571 | 1.9459 | 0.0000 | 0.0000 |

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

