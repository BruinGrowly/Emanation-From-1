# Evidence Ledger

This ledger tracks whether tested results increase, decrease, or merely constrain confidence in the Origin Reframe.

The target is not confirmation. The target is evidence quality.

## Evidence Scale

| Rating | Meaning |
| --- | --- |
| `SUPPORTIVE` | Result survives controls and is naturally anticipated by the Origin Frame. |
| `CONSTRAINING` | Result fits part of the frame but also reveals limits or non-specificity. |
| `NEUTRAL` | Result is reproducible but does not distinguish the Origin Frame from ordinary explanations. |
| `CHALLENGING` | Result weighs against a proposed Origin-frame hypothesis. |
| `UNTESTED` | Not yet locally checked. |

## Current Results

| ID | Result | Evidence Class | Rating | Notes |
| --- | --- | --- | --- | --- |
| E1 | Factor profiles and return paths to `1` are computable for positive integers. | `LOCAL` | `NEUTRAL` | This operationalizes the vocabulary, but definitions are not evidence by themselves. |
| E2 | Prime-prefix Gilbreath rows passed the finite first-column test for the generated local scan. | `LOCAL` | `CONSTRAINING` | Interesting, but finite prefix tests are not proofs. |
| E3 | Consecutive odd control also passed the same finite first-column test. | `LOCAL` | `CONSTRAINING` | Shows the behavior is not automatically prime-specific. |
| E4 | Gap-6 odd control failed the finite first-column test. | `LOCAL` | `CONSTRAINING` | Shows the behavior is not automatic for all odd sequences beginning with `2, 3`. |
| E5 | Seeded random small-gap controls mostly failed at the default short local length. | `LOCAL` | `NEUTRAL` | Needs broader parameter sweep before interpretation. |
| E6 | In the default Goldbach scan through `10000`, size-normalized witness density correlates with distinct factor depth (`r = 0.7110`) and divisor count (`r = 0.7071`). | `LOCAL` | `CONSTRAINING` | Factor structure matters after a simple size baseline. |
| E7 | After applying the conventional singular-factor baseline, the strongest Origin-metric residual correlation in the default Goldbach scan is small (`phi_attenuation`, `r = 0.1355`). | `LOCAL` | `CHALLENGING` | This weakens H6 for Goldbach witnesses: the factor-depth signal appears mostly explainable by conventional arithmetic structure. |
| E8 | Prime prefixes reached certified Gilbreath lock rows before any first-column failure: row `20` for `256` primes and row `23` for `512` primes. | `LOCAL` | `SUPPORTIVE` | This is a finite candidate signal: prime gap order preserved boundary return until certificate lock. |
| E9 | Shuffling the exact prime-gap multiset while preserving the first gap produced low certified-lock rates: `3/200` for `256` primes and `2/100` for `512` primes. | `LOCAL` | `SUPPORTIVE` | This suggests prime-gap order matters, not just the multiset of gap sizes. Needs comparison against stronger prime-gap dependency models. |
| E10 | Consecutive odd numbers reach a trivial certificate at row `1`. | `LOCAL` | `CONSTRAINING` | Boundary-return behavior is not unique to primes; controls must exclude simple construction artifacts. |
| E11 | Prime-prefix certified locks persisted across tested prefix sizes: `64 -> 10`, `128 -> 15`, `256 -> 20`, `512 -> 23`, `1024 -> 35`, `2048 -> 35`, `4096 -> 52`. | `LOCAL` | `SUPPORTIVE` | The lock row grows slowly across tested scales and no first-column failure was observed before lock. |
| E12 | Block-shuffled prime-gap controls stayed low-rate even when preserving local gap order in blocks. For `2048` primes, blocks `1..64` had `0/20` locks and block `128` had `1/20`; for `4096`, blocks `1..128` had `0/20`. | `LOCAL` | `SUPPORTIVE` | This is stronger than full shuffling: local prime-gap order alone did not recover the prime-prefix lock behavior in these finite tests. |
| E13 | First-order Markov prime-gap controls produced certified-lock rates below the real prime prefixes and declining with size: `14/100` at `256`, `11/100` at `512`, `9/100` at `1024`, `5/100` at `2048`, `3/100` at `4096`. | `LOCAL` | `SUPPORTIVE` | One-step empirical gap transitions explain more than full shuffling, but not enough to recover the observed prime-prefix lock behavior. |
| E14 | Prime-gap origin-profile scan across `1024`, `2048`, `4096`, and `8192` prime prefixes found `log(p)` stronger than Origin metrics for raw gaps. After subtracting a linear `log(p)` baseline, the strongest residual metric at `8192` primes was `delta(p+1,p-1).divisor_count` with `r = -0.0631`; `0/100` shuffled-gap controls matched or exceeded it. | `LOCAL` | `SUPPORTIVE` | The support is specific: local composite structure around primes survived the ordinary size baseline and seeded shuffled-gap controls. This does not prove causation, but it is strong enough to promote `p + 1` and adjacent-composite deltas to first-class follow-up targets. |
| E15 | Stronger B3 controls at the `8192`-prime prefix kept the residual Origin signal above controls: shuffling within `p mod 30` matched or exceeded it in `3/100` trials, and shuffling within both `p mod 30` and `8` size bins also matched or exceeded it in `3/100` trials. Large residual-gap classification found the same `delta(p+1,p-1).divisor_count` metric, but the strongest residue-plus-size control matched or exceeded it in `11/100` trials. | `LOCAL` | `SUPPORTIVE` | The residual correlation survives stronger controls. The classification version is promising but less settled, so the next step should model large residual gaps directly with stronger conditioning rather than only report correlations. |
| E16 | Held-out prime-gap prediction with pre-declared metrics did not robustly identify unusually large residual gaps. In the default later windows, `-delta(p+1,p-1).divisor_count` produced AUCs `0.4983` and `0.5232`; `-(p + 1).distinct_factor_depth` produced AUCs `0.4983` and `0.5088`. Residue-plus-size controls often matched or exceeded these AUCs (`62/100`, `61/100`, `9/100`, `53/100` depending on window and metric). | `LOCAL` | `CONSTRAINING` | This pressure-test weakens the direct predictive version of B3. The residual association in E14-E15 remains interesting, but these two pre-declared metrics are not yet strong held-out predictors of large residual gaps. |
| E17 | K-history Markov Gilbreath controls showed that local two-gap memory is a significant confounder. At history `2`, certified-lock rates were `50/100`, `43/100`, `29/100`, `23/100`, and `16/100` for prime counts `256` through `4096`; history `3` controls were lower but still nonzero. | `LOCAL` | `CONSTRAINING` | The real prime prefixes still lock in every tested size while controls do not, but the jump from first-order to two-gap Markov controls shows the Gilbreath signal is partly recoverable from short local gap memory. Future supportive claims need to beat this stronger null. |
| E18 | The Origin structure scan through `10000` maps integers directly by emanation shell, return path, divisor branching, radical compression, and first shell appearance. First observed shell members match `2^k` through depth `13`; high-branching hotspots such as `7560` and `9240` expose many-return-path structures. | `LOCAL` | `NEUTRAL` | This is the correct native object of the repo, but it is operational rather than evidential until a pre-declared shell, branching, or compression metric predicts something beyond standard baselines. |
| E19 | Direct size-banded Origin controls through `100000` found that shell depth retains strong residual structure after removing a `log(n)` size baseline: divisor branching (`r = 0.8582`), radical compression (`r = 0.7729`), and squarefree failure (`r = -0.7101`). Size-banded shuffled controls matched or exceeded the observed absolute residual correlations in `0/200` trials for all three targets. | `LOCAL` | `SUPPORTIVE` | This supports the Origin-first measurement posture: emanation shell is not reducible to number-line size in this scan. It is not proof of the broader frame because all targets remain internal factorization properties; the next evidential step is transfer to an independently chosen phenomenon. |
| E20 | Modular return-to-`1` tests through `5000` found that the pre-declared shell metric `emanation_depth` predicts residual modular-return structure after removing a `log(n)` size baseline. Results: `lambda_over_phi` (`r = -0.6529`), `average_order_ratio` (`r = 0.2520`), `max_order_ratio` (`r = 0.0574`), and `full_exponent_hit` (`r = 0.0574`); size-banded controls matched or exceeded the observed absolute predeclared correlations in `0/100` trials for each target. | `LOCAL` | `SUPPORTIVE` | This is the strongest Origin-first transfer result so far: a shell metric defined before the modular probe carries signal into return-period behavior. Caveat: modular group structure is itself factorization-linked, so the next control should condition on stronger group baselines such as `phi(n)`, `lambda(n)`, residue, or shell-preserving shuffles. |

## What Would Increase Weight

- Origin metrics improve prediction after ordinary baselines are included.
- A metric defined on the Origin shell map predicts behavior before any conjecture-specific tuning.
- A pre-registered Origin metric identifies where a pattern should strengthen, weaken, or fail.
- The same metric transfers across distinct phenomena: factorization, prime gaps, Gilbreath rows, and Goldbach witnesses.
- Controls fail where the Origin metric predicts failure, not merely where a post-hoc interpretation can be supplied.

## What Would Decrease Weight

- Conventional baselines explain all observed structure.
- Origin metrics add no predictive or discriminating value.
- The frame only re-describes known facts after the fact.
- Similar behavior appears in controls where the frame predicts it should not.

## Current Bottom Line

The Origin Reframe is operationalized but not established. Current local evidence is mixed, and the repo has been over-weighted toward conjecture probes because they are easier to test than the broader Emanation claim. The Origin structure scan now restores the proper center: shells, return paths, branching, and compression are the native objects; Gilbreath, Goldbach, twin primes, and prime gaps are downstream transfer tests. The direct size-banded Origin controls are supportive for the measurement posture: shell depth retains strong residual structure after the number-line size baseline is removed. The modular-return scan adds the first clearer Origin-first transfer result: pre-declared shell depth predicts return-to-`1` compression beyond size-banded controls. The next pressure test is stronger conditioning on conventional group structure, especially `phi(n)`, `lambda(n)`, and shell-preserving controls. The Goldbach witness test weighs against treating simple factor-depth metrics as distinctive Origin evidence, because the conventional singular-factor baseline absorbs most of that signal. Gilbreath remains a useful boundary-return probe, but k-history Markov controls show that local gap memory is a serious null model. The prime-gap origin-profile scan is candidate-supportive at the residual-correlation level, but held-out prediction is constraining.

## Regression Coverage

`tests/test_research_regressions.py` protects the main local ledger claims without adding new evidence by itself:

- Prime-prefix certified lock rows for `64`, `128`, `256`, `512`, and `1024` primes.
- Basic constraining controls: consecutive odds lock trivially, while the gap-6 odd control fails.
- Fixed-seed prime-gap order controls fail early for full shuffle, block shuffle, and first-order Markov generation.
- K-history Markov generation preserves initial history gaps, is deterministic, and remains scannable by the certified-lock test.
- The default Goldbach scan through `10000` reproduces the no-failure result and the constrained post-singular-baseline correlation.
- Prime-gap origin-profile construction, log-residual calculation, and deterministic shuffle controls.
- Held-out prime-gap prediction plumbing, AUC tie handling, deterministic predictor evaluation, and conditioned controls.
- Origin structure scan construction, shell summaries, first shell appearances, and branching hotspot ranking.
- Origin size-banded controls, log-size residualization, deterministic shuffles, and seeded control summaries.
- Modular return helpers, modular-return dataset construction, log-size residualization, predeclared-metric controls, and seeded size-banded shuffles.
