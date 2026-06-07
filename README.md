# Emanation From 1

This repository is a research sandbox for the **Origin Reframe**:

> Numbers are not primarily positions on a number line. They are degrees of differentiation from `1`.

The working question is simple and strange in the best way:

**What changes when factorization, prime behavior, and conjectural number theory are studied as traces back to `1` rather than motion outward on a line?**

## Source Documents

The repo begins from two local framework documents:

- `docs/THE_ORIGIN_REFRAME.md` - the central research premise.
- `docs/LJPW_FRAMEWORK_V8.6.2_COMPLETE_UNIFIED_PLUS.md` - the wider LJPW framework, especially Book Five on number theory and Book Six on primes as bricks.

## Research Posture

This repo treats LJPW language as a hypothesis-generating frame, not as a substitute for formal proof.

- **Formal status:** classical conjectures remain open unless a conventional proof is supplied.
- **Semantic status:** LJPW interpretations can suggest where to look, what to measure, and how to compare patterns.
- **Empirical status:** scripts in this repo should produce reproducible scans, tables, and counterexample searches.

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
  RESEARCH_PROGRAM.md
experiments/
  initial_scan.py
reports/
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

## Next Directions

- Add CSV/JSON exports for long scans.
- Add visualizations of Gilbreath row density and first-column persistence.
- Compare factor-depth distributions against prime gaps and Goldbach pair counts.
- Build an `origin_metric(n)` that combines factor depth, logarithmic distance, divisor branching, and phi attenuation.
