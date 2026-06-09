# Goldbach-Neighborhood Residual Transfer Test (C2)

**Generated (UTC):** 2026-06-09
**Script:** `experiments/goldbach_neighborhood_transfer.py`
**Range:** even integers `4..1000`
**Controls:** `250` shell shuffles, seed `62426`

## Purpose

This report executes an additive C2 (Transfer After Mechanism) target
of the Origin-Pakheta proof program for the prime-neighborhood operators.

It tests whether the log gaps of the compression commutators ($C/N_-$ and $C/N_+$)
predict the fluctuations of Goldbach witness densities around the classical
Hardy-Littlewood singular series baseline, after removing size and emanation shell depth.

## Transfer Controls

All variables are shell-conditioned and residualized against `log(n)`. Controls
shuffle targets within emanation shells to break coordinate alignment.

| metric | target | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- |
| compression_prime_minus_neighborhood_log_gap | log_singular_normalized_density | -0.0215 | 0.0376 | 0.1299 | 158/250 | 0.6335 |
| compression_prime_plus_neighborhood_log_gap | log_singular_normalized_density | -0.0173 | 0.0379 | 0.1451 | 180/250 | 0.7211 |

## Interpretation

A successful transfer requires the observed correlation to beat the shuffled
controls significantly ($p < 0.05$).

If the path gaps predict Goldbach residuals, it proves that the boundary gaps
of $N_-$ and $N_+$ hold information that couples to additive prime distributions,
demonstrating that the calculus has reach in both modular and additive number theory.

