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

The Origin Reframe is operationalized but not established. Current local evidence is mostly constraining: it gives better questions and sharper controls, not proof. The Goldbach witness test currently weighs against treating simple factor-depth metrics as distinctive Origin evidence, because the conventional singular-factor baseline absorbs most of that signal.
