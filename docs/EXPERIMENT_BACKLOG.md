# Experiment Backlog

This backlog lists tests that can add evidence for or against the Origin Reframe.

## Priority 1: Discriminating Tests

### B1: Gilbreath Control Sweep

Question:

> Which sequence families preserve first-column `1` behavior under absolute differencing?

Controls:

- Prime prefixes.
- Consecutive odds.
- Fixed even-gap odd sequences.
- Seeded random odd sequences with bounded gaps.

Evidence value:

- Supportive only if Origin metrics predict pass/fail structure before the run.
- Challenging if broad controls explain the prime behavior without needing Origin metrics.

Related command:

```powershell
python experiments\gilbreath_deep_dive.py
```

```powershell
python experiments\gilbreath_gap_shuffle.py
```

```powershell
python experiments\gilbreath_prefix_block_shuffle.py
```

### B2: Goldbach Witness Correlations

Question:

> Do factor-depth or return-path metrics explain Goldbach witness counts beyond size/density baselines?

Command:

```powershell
python experiments\goldbach_origin_correlations.py
```

Evidence value:

- Supportive if Origin metrics correlate with normalized witness density.
- Neutral or challenging if ordinary size baselines dominate and Origin metrics add little.

### B3: Prime Gap And Origin Profiles

Question:

> Do origin profiles of `p - 1`, `p + 1`, or prime indices predict local prime gap behavior?

Controls:

- Compare against `log(p)`.
- Shuffle gap assignments.
- Compare adjacent composites with similar size.

## Priority 2: Transfer Tests

### B4: One Metric Across Multiple Phenomena

Question:

> Can one pre-declared origin metric explain multiple patterns without retuning?

Candidate metric:

```text
origin_pressure(n) = divisor_count(n) * phi_attenuation(n) / log(n)
```

This is only a candidate. It should not be treated as meaningful until it beats controls.

### B5: Operation Specificity

Question:

> Is the Gilbreath-style return behavior specific to absolute differencing, or does it survive related operations?

Operations:

- Absolute difference.
- Signed difference.
- Second difference.
- Modular difference.

## Priority 3: Negative Evidence

### B6: Counterexample Registry

Collect cases where Origin-frame readings predict a pattern that does not appear.

Required fields:

- Hypothesis.
- Test command.
- Parameters.
- Result.
- Why it weakens or constrains the hypothesis.
