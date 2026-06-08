# Origin Anchor Echo Fixed-Point Test

**Generated (UTC):** 2026-06-08
**Script:** `experiments/origin_anchor_echo_fixed_points.py`
**Range:** `2..10000`
**Controls:** `250` shell shuffles, seed `62026`

## Purpose

This is the first Origin-side test suggested by the Pakheta Layer
documents. It translates `anchor echo` into exact modular
fixed-point structures:

```text
idempotent anchor: x^2 = x mod n
return-symmetry anchor: x^2 = 1 mod n
```

The Pakheta language is treated as hypothesis grammar only. The
evidence standard remains ordinary arithmetic: closed formulas,
brute-force checks, size/shell conditioning, and shuffled controls.

## Pre-Registered Question

After controlling for `log(n)` and emanation shell `Omega(n)`, does
prime-power component structure predict modular fixed-point
richness better than shell-shuffled controls?

## Exact Mechanism

The conventional theorem-level mechanism is:

```text
idempotent_count(n) = 2^omega(n)
involution_count(n) = product component roots of x^2 = 1
```

For odd prime powers the involution component count is `2`. For
`2^a` it is `1` when `a = 1`, `2` when `a = 2`, and `4` when
`a >= 3`.

Formula check:

| brute_limit | max_idempotent_error | max_involution_error |
| --- | --- | --- |
| 200 | 0 | 0 |

## Shell-Controlled Fixed-Point Signal

Targets and metrics below are shell-centered, then residualized
against `log(n)`. Controls shuffle the target residuals within
emanation shells.

| target | pre_metric | pre_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper | best_metric | best_r | best_ge | best_p_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| log_idempotent_count | component_count | 1.0000 | 0.0108 | 0.0379 | 0/250 | 0.0040 | component_count | 1.0000 | 0/250 | 0.0040 |
| log_idempotent_density | component_count | 1.0000 | 0.0109 | 0.0364 | 0/250 | 0.0040 | component_count | 1.0000 | 0/250 | 0.0040 |
| log_involution_count | component_count | 0.4538 | 0.0086 | 0.0348 | 0/250 | 0.0040 | odd_component_count | 0.6391 | 0/250 | 0.0040 |
| log_involution_density | component_count | 0.4538 | 0.0100 | 0.0342 | 0/250 | 0.0040 | odd_component_count | 0.6391 | 0/250 | 0.0040 |

## Mechanism R2

These rows ask how much of the conditioned fixed-point target is
explained by each feature group.

| target | model | features | R2 |
| --- | --- | --- | --- |
| log_idempotent_count | component_count | component_count | 1.0000 |
| log_idempotent_count | odd_plus_two_presence | odd_component_count, two_component_present | 1.0000 |
| log_idempotent_count | involution_formula_shape | odd_component_count, two_adic_involution_log | 0.5452 |
| log_idempotent_count | return_overlap_pack | radical_compression, component_count, overlap_pressure_log, lambda_phi_log | 1.0000 |
| log_idempotent_density | component_count | component_count | 1.0000 |
| log_idempotent_density | odd_plus_two_presence | odd_component_count, two_component_present | 1.0000 |
| log_idempotent_density | involution_formula_shape | odd_component_count, two_adic_involution_log | 0.5452 |
| log_idempotent_density | return_overlap_pack | radical_compression, component_count, overlap_pressure_log, lambda_phi_log | 1.0000 |
| log_involution_count | component_count | component_count | 0.2059 |
| log_involution_count | odd_plus_two_presence | odd_component_count, two_component_present | 0.4092 |
| log_involution_count | involution_formula_shape | odd_component_count, two_adic_involution_log | 1.0000 |
| log_involution_count | return_overlap_pack | radical_compression, component_count, overlap_pressure_log, lambda_phi_log | 0.5862 |
| log_involution_density | component_count | component_count | 0.2059 |
| log_involution_density | odd_plus_two_presence | odd_component_count, two_component_present | 0.4092 |
| log_involution_density | involution_formula_shape | odd_component_count, two_adic_involution_log | 1.0000 |
| log_involution_density | return_overlap_pack | radical_compression, component_count, overlap_pressure_log, lambda_phi_log | 0.5862 |

## Shell Summary

| Omega | rows | avg_components | avg_idempotents | avg_involutions | avg_radical_compression |
| --- | --- | --- | --- | --- | --- |
| 1 | 1229 | 1.000 | 2.000 | 1.999 | 0.0000 |
| 2 | 2625 | 1.990 | 3.981 | 3.472 | 0.0088 |
| 3 | 2569 | 2.698 | 6.796 | 5.257 | 0.1934 |
| 4 | 1712 | 3.046 | 9.192 | 7.529 | 0.5056 |
| 5 | 963 | 3.151 | 10.158 | 11.117 | 0.7566 |
| 6 | 485 | 3.089 | 9.682 | 14.495 | 0.8927 |
| 7 | 231 | 2.965 | 8.762 | 15.532 | 0.9530 |
| 8 | 105 | 2.781 | 7.619 | 14.781 | 0.9789 |
| 9 | 47 | 2.553 | 6.340 | 12.596 | 0.9912 |
| 10 | 22 | 2.364 | 5.545 | 11.091 | 0.9958 |
| 11 | 7 | 2.000 | 4.286 | 8.571 | 0.9982 |
| 12 | 3 | 1.667 | 3.333 | 6.667 | 0.9993 |
| 13 | 1 | 1.000 | 2.000 | 4.000 | 0.9998 |

## Highest Fixed-Point Rows

| n | Omega | components | idempotents | involutions | radical_compression | log_overlap_penalty |
| --- | --- | --- | --- | --- | --- | --- |
| 9240 | 7 | 5 | 32 | 64 | 0.7500 | 2.7726 |
| 4620 | 6 | 5 | 32 | 32 | 0.5000 | 2.7726 |
| 5460 | 6 | 5 | 32 | 32 | 0.5000 | 4.5643 |
| 7140 | 6 | 5 | 32 | 32 | 0.5000 | 3.4657 |
| 7980 | 6 | 5 | 32 | 32 | 0.5000 | 3.8712 |
| 8580 | 6 | 5 | 32 | 32 | 0.5000 | 3.4657 |
| 9660 | 6 | 5 | 32 | 32 | 0.5000 | 2.7726 |
| 2310 | 5 | 5 | 32 | 16 | 0.0000 | 2.0794 |
| 2730 | 5 | 5 | 32 | 16 | 0.0000 | 3.8712 |
| 3570 | 5 | 5 | 32 | 16 | 0.0000 | 2.7726 |
| 3990 | 5 | 5 | 32 | 16 | 0.0000 | 3.1781 |
| 4290 | 5 | 5 | 32 | 16 | 0.0000 | 2.7726 |

## Interpretation

The anchor echo is real in the precise modular sense, but its
mechanism is not mysterious: fixed-point richness is controlled by
prime-power component branching and the special `2^a` involution
case. In Pakheta terms, the useful translation is:

```text
anchor richness = coherent CRT recombination across prime-power facets
false partition control = shuffle inside shell and lose the relation
```

This supports the next research move only modestly and cleanly: use
Pakheta vocabulary to design sharper tests, while recording the
ordinary number-theory mechanism as the actual evidence.

