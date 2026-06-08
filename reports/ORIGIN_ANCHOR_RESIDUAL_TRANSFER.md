# Origin Anchor Residual Transfer Test

**Generated (UTC):** 2026-06-08
**Script:** `experiments/origin_anchor_residual_transfer.py`
**Range:** modular-return rows through `10000`
**Sampling:** `12` unit bases from candidates through `40`
**Controls:** `250` shell shuffles, seed `62126`

## Purpose

This is the next proof-pressure move after the fixed-point anchor
test. The prior result found exact anchor mechanisms:

```text
idempotent_count(n) = 2^omega(n)
involution_count(n) = product component roots of x^2 = 1
```

This test removes those exact component explanations first. It then
asks whether any leftover anchor residual transfers into independent
modular-return targets.

## Pre-Registered Question

After the exact CRT component formulas are subtracted from modular
fixed-point richness, is there any remaining anchor residual that
predicts modular-return behavior better than shell-shuffled controls?

## Leftover Anchor Residuals

| residual | formula removed | max_abs | rms | has_leftover_variance |
| --- | --- | --- | --- | --- |
| idempotent_exact_residual | log(idempotents) - log(2) * component_count | 0.000e+00 | 0.000e+00 | False |
| idempotent_density_exact_residual | log(idempotents/n) - (log(2) * component_count - log(n)) | 0.000e+00 | 0.000e+00 | False |
| involution_exact_residual | log(involutions) - (log(2) * odd_component_count + two_adic_log) | 4.346e-16 | 4.303e-17 | False |
| involution_density_exact_residual | log(involutions/n) - (log(2) * odd_component_count + two_adic_log - log(n)) | 8.693e-16 | 8.315e-17 | False |

## Transfer Controls

Targets are shell-centered and residualized against their listed
baseline features before scoring. If an anchor residual has no
variance left, the transfer row is not statistically testable.

| anchor_residual | target | status | anchor_max_abs | target_rms | observed_r | ctrl_mean_abs | ctrl_max_abs | ctrl_ge | p_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| idempotent_exact_residual | log_lambda_over_phi | no_leftover_anchor_variance | 0.000e+00 | 5.703e-01 | n/a | n/a | n/a | n/a | n/a |
| idempotent_exact_residual | average_order_ratio | no_leftover_anchor_variance | 0.000e+00 | 1.278e-01 | n/a | n/a | n/a | n/a | n/a |
| idempotent_exact_residual | max_order_ratio | no_leftover_anchor_variance | 0.000e+00 | 4.301e-02 | n/a | n/a | n/a | n/a | n/a |
| idempotent_exact_residual | full_exponent_hit | no_leftover_anchor_variance | 0.000e+00 | 8.557e-02 | n/a | n/a | n/a | n/a | n/a |
| idempotent_density_exact_residual | log_lambda_over_phi | no_leftover_anchor_variance | 0.000e+00 | 5.703e-01 | n/a | n/a | n/a | n/a | n/a |
| idempotent_density_exact_residual | average_order_ratio | no_leftover_anchor_variance | 0.000e+00 | 1.278e-01 | n/a | n/a | n/a | n/a | n/a |
| idempotent_density_exact_residual | max_order_ratio | no_leftover_anchor_variance | 0.000e+00 | 4.301e-02 | n/a | n/a | n/a | n/a | n/a |
| idempotent_density_exact_residual | full_exponent_hit | no_leftover_anchor_variance | 0.000e+00 | 8.557e-02 | n/a | n/a | n/a | n/a | n/a |
| involution_exact_residual | log_lambda_over_phi | no_leftover_anchor_variance | 4.346e-16 | 5.703e-01 | n/a | n/a | n/a | n/a | n/a |
| involution_exact_residual | average_order_ratio | no_leftover_anchor_variance | 4.346e-16 | 1.278e-01 | n/a | n/a | n/a | n/a | n/a |
| involution_exact_residual | max_order_ratio | no_leftover_anchor_variance | 4.346e-16 | 4.301e-02 | n/a | n/a | n/a | n/a | n/a |
| involution_exact_residual | full_exponent_hit | no_leftover_anchor_variance | 4.346e-16 | 8.557e-02 | n/a | n/a | n/a | n/a | n/a |
| involution_density_exact_residual | log_lambda_over_phi | no_leftover_anchor_variance | 8.693e-16 | 5.703e-01 | n/a | n/a | n/a | n/a | n/a |
| involution_density_exact_residual | average_order_ratio | no_leftover_anchor_variance | 8.693e-16 | 1.278e-01 | n/a | n/a | n/a | n/a | n/a |
| involution_density_exact_residual | max_order_ratio | no_leftover_anchor_variance | 8.693e-16 | 4.301e-02 | n/a | n/a | n/a | n/a | n/a |
| involution_density_exact_residual | full_exponent_hit | no_leftover_anchor_variance | 8.693e-16 | 8.557e-02 | n/a | n/a | n/a | n/a | n/a |

## Interpretation

The result is constraining. Once the exact CRT component explanation
is removed, the tested fixed-point anchors leave no measurable
residual signal. With no leftover variance, there is nothing for this
anchor definition to transfer into modular-return targets.

Plainly:

> The fixed-point anchor echo is real, but exhausted by its exact
> component mechanism in this test.

This does not disprove the Origin Reframe or the Pakheta Layer. It
does block one tempting overclaim: fixed-point anchor richness should
not be treated as extra Origin evidence unless a new, non-exhausted
anchor metric is defined or it predicts an independent target before
the exact component mechanism is removed.

