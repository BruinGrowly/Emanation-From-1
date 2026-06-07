# Gilbreath Test Plan

## Formal Object Under Test

Given an initial sequence:

```text
row[0] = initial sequence
row[k + 1][i] = abs(row[k][i + 1] - row[k][i])
```

The finite test used here checks whether every generated row after the initial row begins with `1`.

For the prime sequence, this is a finite prefix test only. Passing a prefix is not a proof of Gilbreath's conjecture.

## Source-Checked Background

- Encyclopedia of Mathematics defines the conjecture using iterated absolute differences and says Odlyzko verified it for primes up to `10^13`: <https://encyclopediaofmath.org/wiki/Gilbreath_conjecture>
- Zachary Chase's random analogue is published in *Mathematische Annalen* and proves a precise random-sequence analogue under stated conditions: <https://link.springer.com/article/10.1007/s00208-023-02579-w>
- arXiv record for Chase preprint: <https://arxiv.org/abs/2005.00530>

These are source-background facts, not computations reproduced by this repo.

## Local Tests

### T1: Prime Prefix

Generate the first `N` primes and check all finite difference rows.

```powershell
python experiments\initial_scan.py --gilbreath-primes 1024
```

### T2: Non-Prime Controls

Compare the prime prefix with deterministic non-prime sequences.

```powershell
python experiments\gilbreath_controls.py
```

Current controls:

- Consecutive odd numbers after `2, 3`.
- Odd arithmetic sequence with gap `6` after `2, 3`.
- Seeded random odd sequences with bounded even gaps.

### T3: Failure Search

Controls are required because first-column `1` behavior is not assumed to be prime-specific. A useful experiment should include both passing and failing non-prime sequences.

### T4: Certificate Rows

A finite difference triangle has a certificate row when a generated row begins with `1` and every later value in that row is either `0` or `2`.

```text
[1, 0, 2, 2, 0, ...]
```

This matters because the next first value must be `1`, and differencing the tail keeps producing only `0` and `2`.

Run:

```powershell
python experiments\gilbreath_deep_dive.py
```

### T5: Random Control Sweep

Measure how often seeded random small-gap controls preserve the boundary `1` until a certificate row.

```powershell
python experiments\gilbreath_random_sweep.py
```

### T6: Prime-Gap Shuffle

Keep the prime-gap multiset fixed, preserve the first gap `1`, and shuffle all later gaps.

This asks whether finite Gilbreath behavior depends on the order of prime gaps rather than only their sizes.

```powershell
python experiments\gilbreath_gap_shuffle.py
```

### T7: Prefix Scaling And Block Shuffle

Test several prime-prefix lengths and compare against controls that preserve local gap order inside shuffled blocks.

```powershell
python experiments\gilbreath_prefix_block_shuffle.py
```

This is stronger than full gap shuffling because larger block sizes preserve more short-range prime-gap dependency.

### T8: First-Order Markov Gap Model

Generate controls from the empirical one-step transition map of prime gaps in each prefix.

```powershell
python experiments\gilbreath_markov_gap_model.py
```

This asks whether local gap-transition statistics explain the certified-lock behavior.

## Interpretive Boundary

Allowed hypothesis:

> First-column `1` behavior can be studied as a boundary-return pattern under repeated absolute differencing.

Not allowed as a result:

> Gilbreath proves that all numbers emanate from `1`.
