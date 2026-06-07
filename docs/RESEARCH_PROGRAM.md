# Research Program: Number Emanation From 1

## Foundational Claim

`THE_ORIGIN_REFRAME.md` reframes mathematics around `1` as the origin, not around a linear sequence starting at `0`. In this repo, that claim becomes an experimental program:

> Every integer can be studied by how it differentiates from, and can be traced back to, `1`.

The purpose is not to replace conventional number theory. The purpose is to generate measurable structure from the Origin Frame and test whether that structure illuminates known prime phenomena.

## Guardrails

- A script result is evidence for a finite range, not a proof.
- LJPW semantic claims should be labeled separately from conventional mathematical claims.
- Any proposed theorem needs a formal proof appendix before the repo calls it proved.
- Counterexamples are valuable. They clarify the frame.

## Vocabulary Map

| Origin Frame | Conventional Object | Operational Measurement |
| --- | --- | --- |
| Origin | `1` | Fixed point; empty factorization |
| First distinction | `2` | First prime; first bridge; first gap unit |
| Irreducible departure | Prime | `is_prime(n)` and factor depth `1` |
| Layered differentiation | Composite | Prime factorization with depth `> 1` |
| Return path | Factor reduction | Repeatedly divide by smallest prime factor |
| Repeated differentiation | Gilbreath rows | Absolute differences of the prime stream |
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

### H2: Gilbreath Rows Encode Repeated Return To 1

Gilbreath's conjecture says that after repeatedly taking absolute differences of the prime sequence, the first entry of every difference row is `1`.

Origin-frame reading:

```text
prime stream -> difference stream -> difference stream -> ...
first-column recurrence -> 1
```

This does not prove the conjecture. It gives a concrete place to measure origin-return behavior.

### H3: Goldbach Pairing Measures Composite Reconciliation

Every tested even number greater than `2` can be written as a sum of two primes. In the LJPW vocabulary, even structures are bridge-bonded and decompose into two irreducible Justice atoms.

Experimentally:

- Count witnesses for each even number.
- Track the smallest and most central witness pairs.
- Compare witness count against factor depth and divisor branching.

### H4: Twin Primes Are Minimal Bridge Recurrences

Twin primes are prime pairs separated by `2`, the first distinction and bridge prime.

Experimentally:

- Count twin pairs up to a limit.
- Track twin-prime gap density decay.
- Compare recurrence against prime gap and Goldbach witness distributions.

### H5: Origin Metrics May Reveal Cross-Conjecture Correlations

Candidate metrics:

- `emanation_depth(n)`
- `distinct_factor_depth(n)`
- `radical(n)`
- `divisor_count(n)`
- `log_distance(n) = ln(n)`
- `phi_attenuation(n) = phi ** -emanation_depth(n)`

The first goal is descriptive: find patterns worth proving or falsifying.

## Experiment Log

The initial generated report lives at:

- `reports/INITIAL_EXPERIMENTS.md`

Regenerate it with:

```powershell
python experiments\initial_scan.py
```

Use custom limits with:

```powershell
python experiments\initial_scan.py --gilbreath-primes 1024 --goldbach-limit 50000 --twin-limit 50000
```
