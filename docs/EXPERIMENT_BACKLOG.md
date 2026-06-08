# Experiment Backlog

This backlog lists tests that can add evidence for or against the Origin Reframe.

The order matters: begin with direct emanation structure from `1`, then test whether those measurements transfer into primes, pairings, gaps, modular returns, or Gilbreath-style differencing.

## Priority 1: Origin-First Structure

### B1: Emanation Shell Map

Question:

> What does the integer landscape look like when grouped by distance from `1` instead of position on the number line?

Measured objects:

- Emanation shell `Omega(n)`.
- Return path to `1`.
- Divisor branching.
- Radical compression `radical(n) / n`.
- First appearance of each shell.

Command:

```powershell
python experiments\origin_structure_scan.py
```

Evidence value:

- Operational by itself: it defines the native object of study.
- Supportive only if a metric defined here predicts or discriminates later phenomena without retuning.
- Constraining if shell metrics collapse entirely into ordinary size or density baselines.

Current local reading:

- Shells and return paths are computable and reproducible.
- The first observed member of shell `k` is the repeated binary stack `2^k` in the default range.
- Branching hotspots identify highly composite return structures, but this is not yet evidence for the frame until used predictively.

### B2: Origin Pressure Metric

Question:

> Can one pre-declared Origin metric summarize shell depth, branching, compression, and return pressure?

Candidate family:

```text
origin_pressure(n) = divisor_count(n) * phi_attenuation(n) / log(n)
branching_pressure(n) = divisor_count(n) / (1 + emanation_depth(n))
compression_pressure(n) = 1 - radical(n) / n
```

Evidence value:

- Supportive if one pre-declared metric transfers across multiple settings.
- Neutral if it is descriptive but not predictive.
- Challenging if ordinary size, parity, residue, or factor-density baselines absorb it.

### B3: Size-Banded Origin Controls

Question:

> Do Origin metrics say anything after comparing numbers of similar size?

Controls:

- Equal-width number-line bins.
- Equal-log-size bins.
- Same parity or residue classes where relevant.
- Same emanation shell with different branching, and same branching with different shell.

Evidence value:

- Supportive if shell/branching effects survive size bands.
- Challenging if effects disappear once size and residue are fixed.

Command:

```powershell
python experiments\origin_size_banded_controls.py
```

Current local reading:

- In the default scan through `100000`, shell depth remains strongly associated with log-size residual divisor branching (`r = 0.8582`), radical compression (`r = 0.7729`), and squarefree failure (`r = -0.7101`).
- Size-banded shuffled controls matched or exceeded the observed absolute residual correlations in `0/200` trials for all three targets.
- This is supportive for the Origin-first measurement posture, but it is still internal factor-structure evidence; the next step is transfer beyond the shell map.

## Priority 2: Transfer Tests

### B4: Goldbach Pairing As Origin Transfer

Question:

> Do shell, branching, or compression metrics predict Goldbach witness richness beyond conventional density and singular-factor baselines?

Command:

```powershell
python experiments\goldbach_origin_correlations.py
```

Current local reading:

- Simple factor-depth metrics mostly collapse into conventional arithmetic structure after singular-factor correction.
- This is constraining evidence for simple Origin metrics, not a failure of the entire Origin-first program.

### B5: Adjacent Composite Neighborhoods Around Primes

Question:

> Do `p - 1`, `p + 1`, or their Origin-profile deltas carry transferable information about local prime-gap behavior?

Commands:

```powershell
python experiments\prime_gap_origin_profiles.py
```

```powershell
python experiments\prime_gap_origin_prediction.py
```

Current local reading:

- Residual correlations remain after removing a linear `log(p)` baseline.
- Seeded shuffled-gap, `p mod 30`, and `p mod 30` plus size-bin controls usually did not match the strongest residual correlation at the largest default prefix.
- Direct held-out prediction is constraining: pre-declared metrics produce near-random AUCs and only weak enrichment, with residue-plus-size controls often matching or exceeding them.
- Treat this as an unfinished transfer test, not as the center of the repo.

### B6: Twin-Bridge And Modular-Return Tests

Question:

> Does the first distinction `2` or modular return-to-`1` behavior reveal Origin metrics that transfer better than prime-gap correlations?

Candidate tests:

- Twin-prime neighborhoods compared by shell and branching of `p - 1`, `p + 1`, and midpoint composites.
- Euler/Fermat return tests: `a^phi(n) = 1 mod n` as a modular return probe.
- Compare return-period structure against shell depth and compression.

Command:

```powershell
python experiments\origin_modular_return.py
```

```powershell
python experiments\origin_modular_group_controls.py
```

```powershell
python experiments\origin_modular_shell_transfer.py
```

```powershell
python experiments\origin_modular_shell_scaling.py
```

```powershell
python experiments\origin_modular_theorem_probe.py
```

Current local reading:

- The pre-declared shell metric `emanation_depth` beats size-banded controls on modular-return targets in the default scan through `5000`.
- Strongest predeclared result: `lambda_over_phi`, with residual `r = -0.6529`; size-banded controls matched or exceeded it in `0/100` trials.
- Sampled order ratios are weaker but still above controls: `average_order_ratio` residual `r = 0.2520`, `max_order_ratio` residual `r = 0.0574`, and `full_exponent_hit` residual `r = 0.0574`, each with `0/100` controls matching or exceeding.
- Treat this as supportive transfer evidence, with the caveat that modular return behavior is still deeply tied to factorization.
- Stronger group-conditioned controls split the result: `lambda_over_phi` remains supportive after conditioning on `log(n)`, `phi(n)/n`, and `log(phi(n))` (`r = -0.3422`, `0/100` controls matched), but the sampled order-ratio targets mostly collapse after conditioning on `lambda_over_phi`.
- Shell-conditioned transfer keeps the Origin-first line alive inside fixed shell depth: pre-declared `radical_compression` predicts residual `lambda_over_phi` (`r = 0.5142`, `0/100` controls matched) and weakly predicts `average_order_ratio` (`r = 0.0622`, `0/100` controls matched), while `max_order_ratio` and `full_exponent_hit` do not survive.
- Scaling checks across limits `1000`, `2500`, `5000`, and `10000` keep the primary within-shell `radical_compression -> lambda_over_phi` signal stable: `r = 0.5741`, `0.5400`, `0.5142`, and `0.4887`; shell-shuffled controls matched `0/100` at every limit.
- The theorem probe proves the exact coprime product/lcm mechanism behind return-exponent compression and proves endpoint shell bounds. It also finds counterexamples to naive monotonicity by radical compression alone.
- The modular-return mechanism is now represented in code by `modular_return_decomposition(n)`, which separates concentration proxy, component splitting, local prime-power defect, and Carmichael lcm-overlap pressure using exact ratios.

Evidence value:

- Supportive if an Origin metric predicts return-period or bridge behavior beyond size, parity, and residue controls.
- Constraining if modular behavior is fully explained by standard group structure with no added metric value.

Next proof target after decomposition:

- Use the implemented decomposition to replace the false monotonic claim with a theorem using three terms:
  - concentration pressure: `radical(n) / n`,
  - splitting pressure: `omega(n)`,
  - overlap pressure: `product(lambda(p_i^a_i)) / lcm(lambda(p_i^a_i))`.
- Prove which parts of the modular-return signal come from each term.

## Priority 3: Boundary-Return Probes

### B7: Gilbreath Boundary Return

Question:

> Which sequence families preserve first-column `1` behavior under absolute differencing, and can Origin metrics predict pass/fail structure?

Commands:

```powershell
python experiments\gilbreath_deep_dive.py
```

```powershell
python experiments\gilbreath_gap_shuffle.py
```

```powershell
python experiments\gilbreath_prefix_block_shuffle.py
```

```powershell
python experiments\gilbreath_markov_gap_model.py
```

```powershell
python experiments\gilbreath_k_history_markov_gap_model.py
```

Evidence value:

- Supportive only if Origin metrics predict pass/fail structure before the run.
- Constraining if broad controls explain the prime behavior without needing Origin metrics.

Current local reading:

- Prime prefixes preserve boundary `1` until certified lock across tested sizes.
- Shuffled, block-shuffled, and first-order Markov gap controls usually fail earlier.
- Two-gap Markov controls recover many more locks, so local gap memory is a serious null model.
- Gilbreath remains useful, but it is a boundary-return probe, not the central definition of Emanation from `1`.

## Priority 4: Negative Evidence

### B8: Counterexample Registry

Collect cases where Origin-frame readings predict a pattern that does not appear.

Required fields:

- Hypothesis.
- Origin metric.
- Test command.
- Parameters.
- Result.
- Why it weakens or constrains the hypothesis.
