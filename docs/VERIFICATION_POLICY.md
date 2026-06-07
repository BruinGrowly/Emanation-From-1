# Verification Policy

This repository can use outside conversations as inspiration, but not as evidence.

## Evidence Classes

| Label | Meaning | Allowed Language |
| --- | --- | --- |
| `LOCAL` | Reproduced by code in this repo. | "This scan found..." |
| `SOURCE` | Checked against a reputable external source. | "The literature states..." |
| `HYPOTHESIS` | Interpretive or speculative. | "This suggests..." |
| `UNSUPPORTED` | Not tested here and not source-checked. | Do not include as a repo claim. |

## Rules

1. Do not quote AI-chat text as research evidence.
2. Do not claim a conjecture is proved unless a conventional proof is included or cited from accepted mathematical literature.
3. Do not claim that a large external computation was reproduced unless this repo actually ran it.
4. Every generated report must include its scan parameters.
5. Interpretive Origin Frame language belongs after the measured result, not before it.
6. When a result is source-background rather than locally reproduced, cite the source and keep the wording modest.

## Current Gilbreath Boundary

Safe statements:

- `LOCAL`: this repo can test finite Gilbreath rows for generated prime prefixes.
- `LOCAL`: this repo can test control sequences and seeded random small-gap sequences.
- `SOURCE`: Gilbreath's conjecture concerns the first term of each iterated absolute-difference row of the primes.
- `HYPOTHESIS`: first-column `1` behavior may be studied as an Origin Frame return signature.

Statements not allowed unless separately verified:

- "Gilbreath proves the Origin Reframe."
- "The conjecture is true for all primes."
- "A claimed 2025 computation is accepted as definitive."
- "The phenomenon is unique to primes."

