# Modular Overlap Decomposition Test (C2 Counter-Test)

**Generated (UTC):** 2026-06-10
**Script:** `experiments/origin_modular_overlap_decomposition.py`
**Range:** `2..{limit}`
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

For odd squarefree `n` in `2..1000`: `403` of `999` rows.
The identity `lambda(n)/phi(n) = lcm(p-1)/prod(p-1)` holds exactly for
`403/403` of them (integer arithmetic, no floats).

On this subpopulation the transfer target is a deterministic function of
the same generator multiset `{p-1 : p | n}` from which the `C/N_-` gap is
computed, so conditioning on `Z` leaves it zero residual variance there.

## Decomposition Stages

All variables are shell-conditioned and residualized against the listed
baselines. Controls shuffle target residuals within emanation shells.

| stage | metric | baselines | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| replication | path_gap | log_n | -0.4659 | 0.0240 | 0.1070 | 0/250 | 0.0040 |
| classical_baseline_Z | kernel_overlap | log_n | -0.7890 | 0.0261 | 0.1027 | 0/250 | 0.0040 |
| control_Z | path_gap | log_n+kernel_overlap | -0.0697 | 0.0198 | 0.0857 | 2/250 | 0.0120 |
| control_Z_plus_2adic | path_gap | log_n+kernel_overlap+two_adic_defect | -0.0465 | 0.0192 | 0.0737 | 13/250 | 0.0558 |
| control_full_decomposition | path_gap | log_n+kernel_overlap+two_adic_defect+power_kernel_overlap | 0.0900 | 0.0181 | 0.0645 | 0/250 | 0.0040 |

Ancestry of predictor and covariate: `r(path_gap, Z | log n, shells) = 0.5449`.

## Interpretation

1. The published transfer replicates exactly (`r = -0.4659`).
2. The classical covariate `Z` alone is a stronger predictor of the target
   (`r = -0.7890`) than the path gap itself.
3. Conditioning on `Z` removes most of the path-gap signal
   (`r = -0.0697`), and adding the one-bit 2-adic defect
   takes the remainder to `r = -0.0465`.
4. Adding the power-kernel overlap `W` completes the classical controls and
   takes the residual to `r = 0.0900`
   (`p_upper = 0.0040`), which still formally clears the repo's `p < 0.05` shuffle bar at this range; compare its magnitude and sign stability across ranges before treating it as signal.

Read against the preprint's Section 5.1: the strong `C/N_-` modular
transfer decomposes into three named classical overlap channels --
kernel-kernel overlap, the 2-adic lambda defect, and power-kernel
overlap -- none of which require the path calculus to define. It is
not evidence that path-order residue carries novel information about
modular contraction. Any future transfer claim for the v0 neighborhood
operators should be required to beat this three-covariate classical
control, not only size and shell controls. Extending the conditioning further
approaches the circularity boundary noted in the script docstring, so
a sharper test needs a genuinely independent target.

