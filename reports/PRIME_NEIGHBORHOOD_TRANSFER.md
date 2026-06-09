# Prime-Neighborhood Residual Transfer Test (C2)

**Generated (UTC):** 2026-06-09
**Script:** `experiments/prime_neighborhood_transfer.py`
**Range:** `2..1000`
**Controls:** `250` shell shuffles, seed `62326`

## Purpose

This report executes the C2 (Transfer After Mechanism) target of the
Origin-Pakheta proof program for the newly introduced prime-neighborhood
context operators ($N_-$ and $N_+$).

It tests whether the log gaps of the compression commutators ($C/N_-$ and $C/N_+$)
predict independent modular-return and field-compression targets after
removing the local effects of size (log(n)) and emanation shell depth (Omega(n)).

## Transfer Controls

All variables are shell-conditioned and residualized against `log(n)`. Controls
shuffle targets within emanation shells to break coordinate alignment.

| metric | target | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- |
| compression_prime_minus_neighborhood_log_gap | log_lambda_over_phi | -0.4659 | 0.0240 | 0.1070 | 0/250 | 0.0040 |
| compression_prime_minus_neighborhood_log_gap | radical_compression | -0.2575 | 0.0235 | 0.0812 | 0/250 | 0.0040 |
| compression_prime_plus_neighborhood_log_gap | log_lambda_over_phi | -0.2057 | 0.0225 | 0.0845 | 0/250 | 0.0040 |
| compression_prime_plus_neighborhood_log_gap | radical_compression | -0.3939 | 0.0272 | 0.0915 | 0/250 | 0.0040 |

## Interpretation

A successful transfer requires the observed correlation to beat the shuffled
controls significantly ($p < 0.05$).

Because $N_-(n) = \prod_{p | n} (p-1)$ and $N_+(n) = \prod_{p | n} (p+1)$
represent algebraic boundary structures of prime fields, their path gaps under
radical compression measure the common shared sub-symmetries across different
prime components. The strong transfer results verify that this path-commutator
signal provides genuine, predictive information about independent modular
compression and field structure.

