# Modular Overlap Knockout Test (C2 Counter-Test)

**Generated (UTC):** 2026-06-10
**Script:** `experiments/origin_modular_overlap_knockout.py`
**Range:** `2..100000`
**Controls:** `250` shell shuffles, seed `62326`

## Purpose

The prime-neighborhood transfer test reported a strong shell-conditioned
coupling between the `C/N_-` path-commutator gap and `log(lambda/phi)`.
This experiment executes the decomposition step pre-registered in the
README ("prove which part of the shell-conditioned signal comes from
concentration, component splitting, and Carmichael overlap") by
conditioning the transfer on classical covariates definable without the
path calculus:

- `Z(n) = log(prod_{p|n}(p-1) / lcm_{p|n}(p-1))` (Carmichael kernel overlap)
- `d2(n) = log(2)` if `v_2(n) >= 3` else `0` (local 2-adic lambda defect)
- `W(n) = sum min(v_p(prod_{q != p}(q-1)), a-1) * log(p)` (power-kernel overlap)

## Exact Identity (Pre-Wiring Check)

For odd squarefree `n` in `2..100000`: `40526` of `99999` rows.
The identity `lambda(n)/phi(n) = lcm(p-1)/prod(p-1)` holds exactly for
`40526/40526` of them (integer arithmetic, no floats).

On this subpopulation the transfer target is a deterministic function of
the same generator multiset `{p-1 : p | n}` from which the `C/N_-` gap is
computed, so conditioning on `Z` leaves it zero residual variance there.

## Knockout Ladder

All variables are shell-conditioned and residualized against the listed
baselines. Controls shuffle target residuals within emanation shells.

| stage | metric | baselines | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| replication | path_gap | log_n | -0.6507 | 0.0024 | 0.0095 | 0/250 | 0.0040 |
| classical_baseline_Z | kernel_overlap | log_n | -0.8997 | 0.0026 | 0.0114 | 0/250 | 0.0040 |
| knockout_Z | path_gap | log_n+kernel_overlap | -0.0921 | 0.0024 | 0.0089 | 0/250 | 0.0040 |
| knockout_Z_plus_2adic | path_gap | log_n+kernel_overlap+two_adic_defect | -0.0814 | 0.0023 | 0.0074 | 0/250 | 0.0040 |
| knockout_full_ladder | path_gap | log_n+kernel_overlap+two_adic_defect+power_kernel_overlap | -0.0092 | 0.0021 | 0.0075 | 0/250 | 0.0040 |

Ancestry of predictor and covariate: `r(path_gap, Z | log n, shells) = 0.6910`.

## Interpretation

1. The published transfer replicates exactly (`r = -0.6507`).
2. The classical covariate `Z` alone is a stronger predictor of the target
   (`r = -0.8997`) than the path gap itself.
3. Conditioning on `Z` removes most of the path-gap signal
   (`r = -0.0921`), and adding the one-bit 2-adic defect
   takes the remainder to `r = -0.0814`.
4. Adding the power-kernel overlap `W` completes the classical ladder and
   takes the residual to `r = -0.0092`
   (`p_upper = 0.0040`), which still formally clears the repo's `p < 0.05` shuffle bar at this range; compare its magnitude and sign stability across ranges before treating it as signal.

Read against the preprint's Section 5.1: the strong `C/N_-` modular
transfer decomposes into three named classical overlap channels --
kernel-kernel overlap, the 2-adic lambda defect, and power-kernel
overlap -- none of which require the path calculus to define. It is
not evidence that path-order residue carries novel information about
modular contraction. Any future transfer claim for the v0 neighborhood
operators should be required to beat this three-covariate classical
ladder, not only size and shell controls. Extending the ladder further
approaches the circularity boundary noted in the script docstring, so
a sharper test needs a genuinely independent target.

