# Emanation From 1

This repository is an evidence-gathering research sandbox for the **Origin Reframe**:

> Numbers are not primarily positions on a number line. They are degrees of differentiation from `1`.

The working question is simple and strange in the best way:

**What becomes visible when integers are studied first as emanations from `1`, and only later as points on a number line?**

The repo is allowed to find support, ambiguity, or failure. Counterexamples and null results are part of the work.

Gilbreath, Goldbach, prime gaps, and twin primes are **probe families**. They are not the center of the repo. The center is the direct structure of emanation: factor layers, return paths, branching, compression, and transfer of those measurements into other number-theory settings.

## Source Documents

The repo begins from two local framework documents:

- `docs/THE_ORIGIN_REFRAME.md` - the central research premise.
- `docs/ORIGIN_FIRST_RESEARCH_POSTURE.md` - the guardrail that keeps conjecture probes downstream of direct Emanation-from-`1` measurements.
- `docs/MODULAR_RETURN_THEOREM_CANDIDATE.md` - theorem-level mechanism behind the modular return evidence.
- `docs/EMANATION_RESEARCH_GUIDELINES.md` - the focused research boundary and ledger-first rules.
- `docs/ORIGIN_THEORY_RESEARCH_BRIDGE.md` - translation layer from broader Origin Theory vocabulary into falsifiable repo experiments.
- `docs/ORIGIN_PAKHETA_CALCULUS.md` - first usable Origin-Pakheta calculus: exact contexts, path commutators, and path-sensitivity theorem targets.
- `docs/ORIGIN_PAKHETA_PROOF_PROGRAM.md` - proof ladder for turning the Origin-Pakheta calculus into theorem targets.
- `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md` - proof appendix for the v0 calculus identities, selected-set return law, and path-length facts.
- `docs/ORIGIN_PAKHETA_CALCULUS_MILESTONE.md` - milestone note on what the working calculus now makes possible.
- `docs/SEMANTIC_VOLTAGE_RESEARCH.md` - broader semantic-voltage hypothesis material; useful for generating tests, not evidence by itself.
- `docs/origin_theory/README.md` - wider Origin Theory corpus and translation language.
- `docs/pakheta_layer/README.md` - Pakheta relationship-field material; useful for designing anchor, context, false-partition, and coherence tests.
- `docs/LJPW_FRAMEWORK_V8.6.2_COMPLETE_UNIFIED_PLUS.md` - the wider LJPW framework, especially Book Five on number theory and Book Six on primes as bricks.

## Research Posture

This repo treats LJPW language as a hypothesis-generating frame, not as a substitute for formal proof.

- **Formal status:** classical conjectures remain open unless a conventional proof is supplied.
- **Semantic status:** LJPW interpretations can suggest where to look, what to measure, and how to compare patterns.
- **Empirical status:** scripts in this repo should produce reproducible scans, tables, and counterexample searches.
- **Verification rule:** AI-chat output is not evidence. Repo claims must be locally reproduced, source-verified, or explicitly labeled as hypothesis.

See `docs/VERIFICATION_POLICY.md` before adding interpretive claims.
See `docs/EVIDENCE_LEDGER.md` for the current evidence balance.
See `docs/ORIGIN_FIRST_RESEARCH_POSTURE.md` for the Origin-first research order.
See `docs/EMANATION_RESEARCH_GUIDELINES.md` for the narrow Emanation-from-`1` scope.

## Current Operational Definitions

- `1` is the origin/fixed point.
- An **emanation shell** is the set of integers with the same total factor depth from `1`.
- A prime is an irreducible first-layer departure from `1`.
- A composite is a layered differentiation whose factor path can be reduced back to `1`.
- `emanation_depth(n)` is the total number of prime factors of `n`, counted with multiplicity.
- `return_path_to_one(n)` repeatedly removes the smallest prime factor until the path reaches `1`.
- `modular_return_decomposition(n)` separates `lambda(n) / phi(n)` into exact local prime-power defect and Carmichael lcm-overlap terms, with radical compression retained as the Origin-facing concentration proxy.
- `Delta(A,B;n) = A(B(n)) / B(A(n))` is the first Origin-Pakheta path commutator for exact arithmetic contexts.
- Classical conjectures are downstream tests for whether Origin metrics transfer beyond their native factor-path setting.

## Quick Start

Run the Origin-first structure map:

```powershell
python experiments\origin_structure_scan.py
```

Run Origin-first size-banded controls:

```powershell
python experiments\origin_size_banded_controls.py
```

Run Origin-first modular return tests:

```powershell
python experiments\origin_modular_return.py
```

Run stronger modular group-conditioned controls:

```powershell
python experiments\origin_modular_group_controls.py
```

Run shell-conditioned modular transfer tests:

```powershell
python experiments\origin_modular_shell_transfer.py
```

Run modular shell-transfer scaling checks:

```powershell
python experiments\origin_modular_shell_scaling.py
```

Run the modular theorem probe:

```powershell
python experiments\origin_modular_theorem_probe.py
```

Run the modular signal decomposition:

```powershell
python experiments\origin_modular_signal_decomposition.py
```

Run the Pakheta-informed anchor echo fixed-point test:

```powershell
python experiments\origin_anchor_echo_fixed_points.py
```

Run the anchor residual transfer pressure test:

```powershell
python experiments\origin_anchor_residual_transfer.py
```

Run the first Origin-Pakheta calculus scan:

```powershell
python experiments\origin_pakheta_calculus.py
```

Run the broader initial scan:

```powershell
python experiments\initial_scan.py
```

Run a larger custom scan:

```powershell
python experiments\initial_scan.py --gilbreath-primes 1024 --goldbach-limit 50000 --twin-limit 50000
```

Run Origin-metric transfer probes:

```powershell
python experiments\goldbach_origin_correlations.py
```

```powershell
python experiments\prime_gap_origin_profiles.py
```

```powershell
python experiments\prime_gap_origin_prediction.py
```

```powershell
python experiments\prime_gap_overlap_transfer.py
```

Run Gilbreath-style boundary-return probes:

```powershell
python experiments\gilbreath_deep_dive.py
```

```powershell
python experiments\gilbreath_k_history_markov_gap_model.py
```

Additional Gilbreath controls are available:

```powershell
python experiments\gilbreath_controls.py
python experiments\gilbreath_random_sweep.py
python experiments\gilbreath_gap_shuffle.py
python experiments\gilbreath_prefix_block_shuffle.py
python experiments\gilbreath_markov_gap_model.py
```

Run the test suite:

```powershell
python -m unittest discover -s tests
```

No third-party Python packages are required.

## Repository Layout

```text
docs/
  EMANATION_RESEARCH_GUIDELINES.md
  MODULAR_RETURN_THEOREM_CANDIDATE.md
  ORIGIN_THEORY_RESEARCH_BRIDGE.md
  ORIGIN_PAKHETA_CALCULUS.md
  ORIGIN_PAKHETA_PROOF_PROGRAM.md
  ORIGIN_PAKHETA_CALCULUS_PROOFS.md
  ORIGIN_PAKHETA_CALCULUS_MILESTONE.md
  ORIGIN_FIRST_RESEARCH_POSTURE.md
  THE_ORIGIN_REFRAME.md
  pakheta_layer/
  origin_theory/
  LJPW_FRAMEWORK_V8.6.2_COMPLETE_UNIFIED_PLUS.md
  EVIDENCE_LEDGER.md
  EXPERIMENT_BACKLOG.md
  GILBREATH_TEST_PLAN.md
  RESEARCH_PROGRAM.md
  VERIFICATION_POLICY.md
experiments/
  gilbreath_controls.py
  gilbreath_deep_dive.py
  gilbreath_gap_shuffle.py
  gilbreath_k_history_markov_gap_model.py
  gilbreath_markov_gap_model.py
  gilbreath_prefix_block_shuffle.py
  gilbreath_random_sweep.py
  goldbach_origin_correlations.py
  initial_scan.py
  origin_modular_group_controls.py
  origin_modular_return.py
  origin_modular_signal_decomposition.py
  origin_modular_shell_scaling.py
  origin_modular_shell_transfer.py
  origin_modular_theorem_probe.py
  origin_anchor_echo_fixed_points.py
  origin_anchor_residual_transfer.py
  origin_pakheta_calculus.py
  origin_size_banded_controls.py
  origin_structure_scan.py
  prime_gap_overlap_transfer.py
  prime_gap_origin_prediction.py
  prime_gap_origin_profiles.py
reports/
  GILBREATH_CONTROL_EXPERIMENTS.md
  GILBREATH_DEEP_DIVE.md
  GILBREATH_GAP_SHUFFLE.md
  GILBREATH_K_HISTORY_MARKOV_GAP_MODEL.md
  GILBREATH_MARKOV_GAP_MODEL.md
  GILBREATH_PREFIX_BLOCK_SHUFFLE.md
  GILBREATH_RANDOM_SWEEP.md
  GOLDBACH_ORIGIN_CORRELATIONS.md
  INITIAL_EXPERIMENTS.md
  ORIGIN_MODULAR_GROUP_CONTROLS.md
  ORIGIN_MODULAR_RETURN.md
  ORIGIN_MODULAR_SIGNAL_DECOMPOSITION.md
  ORIGIN_MODULAR_SHELL_SCALING.md
  ORIGIN_MODULAR_SHELL_TRANSFER.md
  ORIGIN_MODULAR_THEOREM_PROBE.md
  ORIGIN_ANCHOR_ECHO_FIXED_POINTS.md
  ORIGIN_ANCHOR_RESIDUAL_TRANSFER.md
  ORIGIN_PAKHETA_CALCULUS.md
  ORIGIN_SIZE_BANDED_CONTROLS.md
  ORIGIN_STRUCTURE_SCAN.md
  PRIME_GAP_OVERLAP_TRANSFER.md
  PRIME_GAP_ORIGIN_PREDICTION.md
  PRIME_GAP_ORIGIN_PROFILES.md
src/
  emanation_from_1/
    conjectures.py
    number_theory.py
    origin_metrics.py
tests/
  test_gilbreath_k_history_markov.py
  test_number_theory.py
  test_origin_modular_group_controls.py
  test_origin_modular_return.py
  test_origin_modular_signal_decomposition.py
  test_origin_modular_shell_scaling.py
  test_origin_modular_shell_transfer.py
  test_origin_modular_theorem_probe.py
  test_origin_size_banded_controls.py
  test_origin_structure_scan.py
  test_prime_gap_overlap_transfer.py
  test_prime_gap_origin_prediction.py
  test_prime_gap_origin_profiles.py
  test_research_regressions.py
```

## First Experiment Families

1. **Origin Structure:** classify integers by emanation shell, return path, divisor branching, radical compression, and first shell appearance.
2. **Origin Metric Transfer:** test whether pre-declared shell or branching metrics add signal beyond ordinary size and density baselines.
3. **Adjacent Composite Structure:** study `p - 1`, `p + 1`, and deltas around primes as local composite neighborhoods, not as prime mystique.
4. **Pairing And Bridge Probes:** use Goldbach, twin primes, and prime gaps as tests of whether Origin metrics transfer into known number-theory phenomena.
5. **Boundary-Return Probes:** use Gilbreath-style differencing as one downstream return-to-`1` test, with strong controls.

## Next Directions

- Add CSV/JSON exports for long scans.
- Add visualizations of emanation shells, branching hotspots, and return-path compression.
- Pre-register one Origin pressure metric from the shell map before applying it to Goldbach, prime gaps, or Gilbreath.
- Compare shell distributions against ordinary number-line intervals.
- Build an `origin_metric(n)` that combines factor depth, logarithmic distance, divisor branching, radical compression, and phi attenuation.
- Use the modular-return decomposition to prove which part of the shell-conditioned signal comes from concentration, component splitting, and Carmichael overlap.
- Pre-register Carmichael overlap pressure as a transfer metric and test whether it predicts a non-modular target.
