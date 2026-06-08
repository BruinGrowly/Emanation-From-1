# Research Program: Number Emanation From 1

## Foundational Claim

`THE_ORIGIN_REFRAME.md` reframes mathematics around `1` as the origin, not around a linear sequence starting at `0`. In this repo, that claim becomes an evidence-gathering program:

> Every integer can be studied by how it differentiates from, and can be traced back to, `1`.

The purpose is not to replace conventional number theory. The purpose is to generate measurable structure from the Origin Frame itself, then test whether that structure transfers into known number-theory phenomena better than ordinary baselines or controls.

The repo's central question:

> Does starting from `1` as source produce reproducible measurements of integer structure that are useful before, and beyond, the ordinary number-line view?

## Null Hypothesis

The null hypothesis stays active throughout the project:

> Apparent Origin Frame patterns are artifacts of standard arithmetic, sequence construction, operation choice, or post-hoc interpretation.

Evidence only counts as weight for the Origin Reframe when it survives relevant controls.

## Guardrails

- A script result is evidence for a finite range, not a proof.
- LJPW semantic claims should be labeled separately from conventional mathematical claims.
- Any proposed theorem needs a formal proof appendix before the repo calls it proved.
- Counterexamples are valuable. They clarify the frame.
- AI-chat output is hypothesis material only. It should not be quoted as evidence.
- Ordinary explanations get first right of refusal. If a standard baseline explains the result, record that.

The focused research boundary is maintained in:

- `docs/EMANATION_RESEARCH_GUIDELINES.md`

That document should be read with `docs/EVIDENCE_LEDGER.md` before adding new claims or experiment families.

## Vocabulary Map

| Origin Frame | Conventional Object | Operational Measurement |
| --- | --- | --- |
| Origin | `1` | Fixed point; empty factorization |
| Emanation shell | Total factor layer | `emanation_depth(n) = Omega(n)` |
| First distinction | `2` | First prime; first bridge; first gap unit |
| Irreducible departure | Prime | `is_prime(n)` and factor depth `1` |
| Layered differentiation | Composite | Prime factorization with depth `> 1` |
| Branching | Divisor structure | `divisor_count(n)` and factor exponent shape |
| Compression | Repeated factor overlap | `radical(n) / n` |
| Return path | Factor reduction | Repeatedly divide by smallest prime factor |
| Boundary-return probe | Gilbreath rows | Absolute differences of the prime stream |
| Minimal bridge | Twin prime gap | Prime pairs `(p, p + 2)` |
| Pair-bond decomposition | Goldbach pair | Even `n = p + q` |

## Hypotheses To Explore

### H1: Factor Depth Is Emanation Depth

The total number of prime factors of `n`, counted with multiplicity, measures how many irreducible differentiations separate `n` from `1`.

Example:

```text
60 = 2 * 2 * 3 * 5
emanation_depth(60) = 4
return_path_to_one(60) = 60 -> 30 -> 15 -> 5 -> 1
```

### H2: Emanation Shells Are The Native Object

Before asking about primes or conjectures, group integers by their distance from `1` under multiplicative differentiation.

Experimentally:

- Count each shell `Omega(n) = k` inside finite ranges.
- Track first shell appearance, especially the minimal binary stack `2^k`.
- Measure how squarefree structure, prime powers, divisor branching, and radical compression change by shell.
- Compare shell behavior against ordinary number-line intervals.

### H3: Branching Measures Return Complexity

Two integers can have the same shell depth but very different numbers of return decompositions. Divisor count and factor-exponent shape measure how branched the return toward `1` becomes.

Experimentally:

- Identify branching hotspots by divisor count.
- Compare high-branching numbers against low-branching numbers in the same shell and size band.
- Test whether branching metrics predict richer pairings, denser local composite neighborhoods, or stronger modular return behavior.

### H4: Origin Metrics May Transfer Across Phenomena

Candidate metrics:

- `emanation_depth(n)`
- `distinct_factor_depth(n)`
- `radical(n)`
- `radical_ratio(n) = radical(n) / n`
- `divisor_count(n)`
- `log_distance(n) = ln(n)`
- `phi_attenuation(n) = phi ** -emanation_depth(n)`

The first goal is descriptive: find patterns worth proving or falsifying.

### H5: Pairing And Bridge Probes

Goldbach witnesses, twin primes, and prime gaps are useful only after the Origin metrics are defined independently. They test whether shell and branching measures transfer into pairing and bridge phenomena.

Experimentally:

- Count Goldbach witnesses for each even number.
- Track twin-prime recurrence at the minimal bridge distance `2`.
- Study `p - 1`, `p + 1`, and adjacent-composite deltas as local composite neighborhoods around primes.

### H6: Boundary-Return Probes

Gilbreath-style differencing is one finite return-to-`1` probe, not the organizing center of the repo.

Origin-frame reading:

```text
prime stream -> difference stream -> difference stream -> ...
first-column recurrence -> 1
```

This does not prove the conjecture. It gives a concrete place to test whether repeated differentiation produces origin-return behavior under strong controls.

### H7: Origin Metrics Add Signal Beyond Size Baselines

Many number-theoretic quantities scale mostly with size. A useful Origin metric should explain something after accounting for ordinary size proxies such as `n`, `log(n)`, or density heuristics.

Experimentally:

- Compare shell and branching metrics within size bands.
- Compare Goldbach witness counts with `n / log(n)^2`.
- Compare residual or normalized witness density against `emanation_depth`, `divisor_count`, `radical_ratio`, and `phi_attenuation`.
- Record neutral or negative results.

## Experiment Log

Generated reports include:

- `reports/INITIAL_EXPERIMENTS.md`
- `reports/ORIGIN_STRUCTURE_SCAN.md`
- `reports/ORIGIN_SIZE_BANDED_CONTROLS.md`
- `reports/ORIGIN_MODULAR_RETURN.md`
- `reports/ORIGIN_MODULAR_GROUP_CONTROLS.md`
- `reports/ORIGIN_MODULAR_SHELL_TRANSFER.md`
- `reports/ORIGIN_MODULAR_SHELL_SCALING.md`
- `reports/ORIGIN_MODULAR_THEOREM_PROBE.md`
- `reports/ORIGIN_MODULAR_SIGNAL_DECOMPOSITION.md`
- `reports/PRIME_GAP_OVERLAP_TRANSFER.md`
- `reports/PRIME_GAP_ORIGIN_PROFILES.md`
- `reports/PRIME_GAP_ORIGIN_PREDICTION.md`
- `reports/GILBREATH_K_HISTORY_MARKOV_GAP_MODEL.md`

Regenerate it with:

```powershell
python experiments\initial_scan.py
```

Use custom limits with:

```powershell
python experiments\initial_scan.py --gilbreath-primes 1024 --goldbach-limit 50000 --twin-limit 50000
```

Current evidence balance:

- `docs/EVIDENCE_LEDGER.md`

Planned tests:

- `docs/EXPERIMENT_BACKLOG.md`
