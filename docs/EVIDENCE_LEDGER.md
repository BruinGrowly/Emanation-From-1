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

## What Would Increase Weight

- Origin metrics improve prediction after ordinary baselines are included.
- A pre-registered Origin metric identifies where a pattern should strengthen, weaken, or fail.
- The same metric transfers across distinct phenomena: factorization, prime gaps, Gilbreath rows, and Goldbach witnesses.
- Controls fail where the Origin metric predicts failure, not merely where a post-hoc interpretation can be supplied.

## What Would Decrease Weight

- Conventional baselines explain all observed structure.
- Origin metrics add no predictive or discriminating value.
- The frame only re-describes known facts after the fact.
- Similar behavior appears in controls where the frame predicts it should not.

## Current Bottom Line

The Origin Reframe is operationalized but not established. Current local evidence is mixed. The Goldbach witness test weighs against treating simple factor-depth metrics as distinctive Origin evidence, because the conventional singular-factor baseline absorbs most of that signal. The Gilbreath gap-order tests are currently the strongest candidate-supportive evidence: prime prefixes preserve the boundary `1` until certificate lock across tested scales, while shuffled, block-shuffled, and first-order Markov versions of their own gap structure usually fail before reaching lock.
