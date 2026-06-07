# Emanation From 1

This repository is an evidence-gathering research sandbox for the **Origin Reframe**:

> Numbers are not primarily positions on a number line. They are degrees of differentiation from `1`.

The working question is simple and strange in the best way:

**Does studying factorization, prime behavior, and conjectural number theory as traces back to `1` reveal reproducible structure that survives controls?**

The repo is allowed to find support, ambiguity, or failure. Counterexamples and null results are part of the work.

## Source Documents

The repo begins from two local framework documents:

- `docs/THE_ORIGIN_REFRAME.md` - the central research premise.
- `docs/LJPW_FRAMEWORK_V8.6.2_COMPLETE_UNIFIED_PLUS.md` - the wider LJPW framework, especially Book Five on number theory and Book Six on primes as bricks.

## Research Posture

This repo treats LJPW language as a hypothesis-generating frame, not as a substitute for formal proof.

- **Formal status:** classical conjectures remain open unless a conventional proof is supplied.
- **Semantic status:** LJPW interpretations can suggest where to look, what to measure, and how to compare patterns.
- **Empirical status:** scripts in this repo should produce reproducible scans, tables, and counterexample searches.
- **Verification rule:** AI-chat output is not evidence. Repo claims must be locally reproduced, source-verified, or explicitly labeled as hypothesis.

See `docs/VERIFICATION_POLICY.md` before adding interpretive claims.
See `docs/EVIDENCE_LEDGER.md` for the current evidence balance.

## Current Operational Definitions

- `1` is the origin/fixed point.
- A prime is an irreducible first-layer departure from `1`.
- A composite is a layered differentiation whose factor path can be reduced back to `1`.
- `emanation_depth(n)` is the total number of prime factors of `n`, counted with multiplicity.
- `return_path_to_one(n)` repeatedly removes the smallest prime factor until the path reaches `1`.
- Gilbreath rows are interpreted as repeated discrete differentiation of the prime stream; the conjectural first-column `1`s are treated as origin-return signatures.

## Quick Start

Run the initial scan and regenerate the first report:

```powershell
python experiments\initial_scan.py
```

Run a larger custom scan:

```powershell
python experiments\initial_scan.py --gilbreath-primes 1024 --goldbach-limit 50000 --twin-limit 50000
```

Run Gilbreath control-sequence tests:

```powershell
python experiments\gilbreath_controls.py
```

Run deeper Gilbreath certificate-row diagnostics:

```powershell
python experiments\gilbreath_deep_dive.py
```

Run a seeded random-control sweep:

```powershell
python experiments\gilbreath_random_sweep.py
```

Run shuffled prime-gap controls:

```powershell
python experiments\gilbreath_gap_shuffle.py
```

Run prefix scaling plus block-shuffled prime-gap controls:

```powershell
python experiments\gilbreath_prefix_block_shuffle.py
```

Run first-order Markov prime-gap controls:

```powershell
python experiments\gilbreath_markov_gap_model.py
```

Run a Goldbach/origin-metric correlation scan:

```powershell
python experiments\goldbach_origin_correlations.py
```

Run the test suite:

```powershell
python -m unittest discover -s tests
```

No third-party Python packages are required.

## Repository Layout

```text
docs/
  THE_ORIGIN_REFRAME.md
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
  gilbreath_markov_gap_model.py
  gilbreath_prefix_block_shuffle.py
  gilbreath_random_sweep.py
  goldbach_origin_correlations.py
  initial_scan.py
reports/
  GILBREATH_CONTROL_EXPERIMENTS.md
  GILBREATH_DEEP_DIVE.md
  GILBREATH_GAP_SHUFFLE.md
  GILBREATH_MARKOV_GAP_MODEL.md
  GILBREATH_PREFIX_BLOCK_SHUFFLE.md
  GILBREATH_RANDOM_SWEEP.md
  GOLDBACH_ORIGIN_CORRELATIONS.md
  INITIAL_EXPERIMENTS.md
src/
  emanation_from_1/
    conjectures.py
    number_theory.py
    origin_metrics.py
tests/
  test_number_theory.py
```

## First Experiment Families

1. **Factor Profiles:** classify integers by their factor layers, radical, divisor count, and return path to `1`.
2. **Gilbreath Differentiation:** build absolute-difference rows from the prime sequence and search for first-column failures.
3. **Goldbach Pairing:** scan even numbers for prime-pair decompositions as a Love/Justice pairing model.
4. **Twin Prime Bridges:** track minimal prime gaps as the `2` bridge recurs through the prime stream.
5. **Origin Metric Tests:** check whether factor-depth and return-path metrics add explanatory power beyond conventional baselines.

## Next Directions

- Add CSV/JSON exports for long scans.
- Add visualizations of Gilbreath row density and first-column persistence.
- Compare factor-depth distributions against prime gaps and Goldbach pair counts.
- Build an `origin_metric(n)` that combines factor depth, logarithmic distance, divisor branching, and phi attenuation.
