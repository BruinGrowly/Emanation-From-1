# Modular Overlap Knockout Test (C2 Counter-Test)

**Generated (UTC):** 2026-06-09
**Script:** `experiments/origin_modular_overlap_knockout.py`
**Range:** `2..1000`
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

## Exact Identity (Pre-Wiring Check)

For odd squarefree `n` in `2..1000`: `403` of `999` rows.
The identity `lambda(n)/phi(n) = lcm(p-1)/prod(p-1)` holds exactly for
`403/403` of them (integer arithmetic, no floats).

On this subpopulation the transfer target is a deterministic function of
the same generator multiset `{p-1 : p | n}` from which the `C/N_-` gap is
computed, so conditioning on `Z` leaves it zero residual variance there.

## Knockout Ladder

All variables are shell-conditioned and residualized against the listed
baselines. Controls shuffle target residuals within emanation shells.

| stage | metric | baselines | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| replication | path_gap | log_n | -0.4659 | 0.0240 | 0.1070 | 0/250 | 0.0040 |
| classical_baseline_Z | kernel_overlap | log_n | -0.7890 | 0.0261 | 0.1027 | 0/250 | 0.0040 |
| knockout_Z | path_gap | log_n+kernel_overlap | -0.0697 | 0.0198 | 0.0857 | 2/250 | 0.0120 |
| knockout_Z_plus_2adic | path_gap | log_n+kernel_overlap+two_adic_defect | -0.0465 | 0.0192 | 0.0737 | 13/250 | 0.0558 |

Ancestry of predictor and covariate: `r(path_gap, Z | log n, shells) = 0.5449`.

## Interpretation

1. The published transfer replicates exactly (`r = -0.4659`).
2. The classical covariate `Z` alone is a stronger predictor of the target
   (`r = -0.7890`) than the path gap itself.
3. Conditioning on `Z` removes most of the path-gap signal
   (`r = -0.0697`), and adding the one-bit 2-adic defect
   takes the remainder to `r = -0.0465`
   (`p_upper = 0.0558`), which does not clear the
   repo's `p < 0.05` transfer bar.

Read against the preprint's Section 5.1: the strong `C/N_-` modular
transfer is overwhelmingly a re-measurement of classical Carmichael
kernel overlap plus the 2-adic lambda special case, not evidence that
path-order residue carries novel information about modular contraction.
Any future transfer claim for the v0 neighborhood operators should be
required to beat this two-covariate classical ladder, not only size and
shell controls. The marginal trace that remains is the open question;
extending the ladder further approaches the circularity boundary noted
in the script docstring, so a sharper test needs an independent target.

