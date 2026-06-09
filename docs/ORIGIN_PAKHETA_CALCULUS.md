# Origin-Pakheta Calculus v0

**Status:** Working calculus  
**Scope:** Positive integers  
**Companion scan:** `experiments/origin_pakheta_calculus.py`  
**Report:** `reports/ORIGIN_PAKHETA_CALCULUS.md`  
**Proof appendix:** `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md`
**Milestone note:** `docs/ORIGIN_PAKHETA_CALCULUS_MILESTONE.md`

This document defines the first usable Origin-Pakheta calculus for the repo.

It is not the full theory. It is the first formal surface where Origin and
Pakheta language becomes exact arithmetic.

## Core Move

The Origin Reframe supplies the object:

```text
n as differentiation from 1
```

The Pakheta Layer supplies the relational grammar:

```text
field, node, anchor, context, path, coherence, false partition
```

The first calculus combines them:

```text
integer field + exact context operators + path commutators
```

## Integer Field

For a positive integer

```text
n = product p_i^a_i
```

define its Origin-Pakheta field as:

| Object | Definition | Reading |
| --- | --- | --- |
| shell | `Omega(n) = sum a_i` | distance from `1` by prime layers |
| component field | `{p_i^a_i}` | differentiated prime-power facets |
| squarefree skeleton | `rad(n) = product p_i` | compressed field identity |
| branching | `divisor_count(n)` | number of return decompositions |
| return target | `1` | origin anchor |

## v0 Context Operators

The context operators include the base set, branching/modular projections, and prime-neighborhoods.

| Symbol | Definition | Pakheta Function |
| --- | --- | --- |
| `C(n)` | `rad(n)` | compress to squarefree field skeleton |
| `R_min(n)` | remove one least-prime factor | return one layer toward `1` |
| `R_p(n)` | remove one selected `p` layer if present | selected return context |
| `R_S(n)` | remove one layer for each selected prime in finite set `S` | multi-anchor return context |
| `G_p(n)` | `p * n` for prime `p` | gather one prime facet into the field |
| `B(n)` | `divisor_count(n)` | divisor-branching context |
| `M(n)` | `carmichael_lambda(n)` | modular-return exponent/period context |
| `T(n)` | `euler_totient(n)` | modular-return size/density context |
| `N_-(n)` | `product_{p | n} (p - 1)` | prime-minus neighborhood context |
| `N_+(n)` | `product_{p | n} (p + 1)` | prime-plus neighborhood context |

These are not metaphors. They are exact maps on positive integers.

## Path Commutator

For two context operators `A` and `B`, define:

```text
Delta(A, B; n) = A(B(n)) / B(A(n))
```

If:

```text
Delta(A, B; n) = 1
```

then the two paths commute at `n`.

If:

```text
Delta(A, B; n) != 1
```

then the integer field remembers path order.

This is the first exact Origin-Pakheta path-sensitivity object.

## First Exact Identities

### Compression-Return Identity

Let `spf(n)` be the least prime factor of `n`.

For `n > 1`:

```text
C(R_min(n)) / R_min(C(n))
  =
  spf(n), if v_{spf(n)}(n) > 1
  1,      otherwise
```

Plainly:

```text
compress then return != return then compress
exactly when the least-prime return layer is repeated
```

This makes repeated least-prime structure a first path-memory signal.

Proof sketch:

Let `n = p^a * m`, where `p = spf(n)`, `a >= 1`, and `p` does not divide
`m`.

If `a = 1`:

```text
C(R_min(n)) = C(m) = rad(m)
R_min(C(n)) = R_min(p * rad(m)) = rad(m)
```

If `a > 1`:

```text
C(R_min(n)) = C(p^(a-1) * m) = p * rad(m)
R_min(C(n)) = R_min(p * rad(m)) = rad(m)
```

So the ratio is `p` exactly when the least-prime layer is repeated, and `1`
otherwise.

### Compression-Selected-Return Identity

For a chosen prime `p`, define:

```text
R_p(n) =
  n / p, if p divides n
  n,     otherwise
```

Then:

```text
C(R_p(n)) / R_p(C(n))
  =
  p, if v_p(n) > 1
  1, otherwise
```

Plainly:

```text
compress then R_p != R_p then compress
exactly when the chosen p-layer is repeated
```

This generalizes the least-prime return identity from `R_min` to a selected
prime-return family.

Proof sketch:

Write `n = p^a * m`, where `p` does not divide `m`.

If `a = 0`, both paths leave the `p` facet absent:

```text
C(R_p(n)) = C(n) = rad(m)
R_p(C(n)) = R_p(rad(m)) = rad(m)
```

If `a = 1`, both paths remove the single `p` facet:

```text
C(R_p(n)) = C(m) = rad(m)
R_p(C(n)) = R_p(p * rad(m)) = rad(m)
```

If `a > 1`, compression preserves the presence of `p`, while return-after-
compression removes it:

```text
C(R_p(n)) = C(p^(a-1) * m) = p * rad(m)
R_p(C(n)) = R_p(p * rad(m)) = rad(m)
```

So the ratio is `p` exactly when the selected prime layer is repeated.

### Compression-Selected-Set-Return Identity

For a finite set `S` of selected primes, define:

```text
R_S(n) = n / product_{p in S, p divides n} p
```

Then:

```text
C(R_S(n)) / R_S(C(n))
  =
  product_{p in S, v_p(n) > 1} p
```

Plainly:

```text
compress then R_S != R_S then compress
exactly when at least one selected prime layer is repeated
```

This is the first multi-anchor return law in the calculus. It says the path
gap is not a vague disturbance: it is exactly the product of the selected
repeated layers.

### Compression-Gather Identity

For prime `p`:

```text
C(G_p(n)) / G_p(C(n))
  =
  1 / p, if p divides n
  1,     otherwise
```

Plainly:

```text
gather then compress != compress then gather
exactly when the gathered prime facet is already present
```

This makes facet re-entry measurable.

Proof sketch:

If `p` does not divide `n`, then:

```text
C(G_p(n)) = C(pn) = p * rad(n)
G_p(C(n)) = p * rad(n)
```

If `p` divides `n`, then:

```text
C(G_p(n)) = C(pn) = rad(n)
G_p(C(n)) = p * rad(n)
```

So the ratio is `1/p` exactly when the gathered prime facet is already present,
and `1` otherwise.

### Compression-Divisor Branching Identity

Let $B(n) = d(n)$ be the divisor count of $n$. For any positive integer $n$:

```text
C(B(n)) / B(C(n)) = rad(d(n)) / 2^omega(n)
```

Where $n > 1$ commutes under $C$ and $B$ if and only if $n = p^{2^k - 1}$ for some prime $p$ and integer $k \ge 1$.

### Return-Divisor Branching Identity

For any finite set $S$ of primes, and $B(n) = d(n)$:

```text
R_S(B(n)) / B(R_S(n)) = (1 / rad_S(d(n))) * product_{p in S, v_p(n) > 0} (v_p(n) + 1) / v_p(n)
```

### Compression-Carmichael Lambda Identity

Let $M(n) = \lambda(n)$ be the Carmichael exponent of $n$. For any positive integer $n$:

```text
C(M(n)) / M(C(n)) = lcm_{p | n} ( rad(p-1) * p^min(1, v_p(n) - 1) ) / lcm_{p | n} (p - 1)
```

Where squarefree $n > 2$ commutes under $C$ and $M$ if and only if $\lambda(n)$ is squarefree.

### Compression-Euler Totient Identity

Let $T(n) = \phi(n)$ be Euler's totient of $n$. For any positive integer $n$:

```text
C(T(n)) / T(C(n)) = rad(phi(n)) / phi(rad(n))
```

### Compression-Prime Minus Identity

Let $N_-(n) = \prod_{p | n} (p - 1)$. For any positive integer $n$:

```text
C(N_-(n)) / N_-(C(n)) = rad( product_{p | n} (p - 1) ) / product_{p | n} (p - 1)
```

### Return-Prime Minus Identity

For any finite set $S$ of primes, and $N_-(n) = \prod_{p | n} (p - 1)$:

```text
R_S(N_-(n)) / N_-(R_S(n)) = product_{p in S, p | n} (p - 1) / rad_S( product_{p | n} (p - 1) )
```

### Compression-Prime Plus Identity

Let $N_+(n) = \prod_{p | n} (p + 1)$. For any positive integer $n$:

```text
C(N_+(n)) / N_+(C(n)) = rad( product_{p | n} (p + 1) ) / product_{p | n} (p + 1)
```

### Return-Prime Plus Identity

For any finite set $S$ of primes, and $N_+(n) = \prod_{p | n} (p + 1)$:

```text
R_S(N_+(n)) / N_+(R_S(n)) = product_{p in S, p | n} (p + 1) / rad_S( product_{p | n} (p + 1) )
```

### Neighborhood Period Bound

For any positive integer $n \ge 2$:

```text
lambda(n) >= rad(N_-(n))
```

where $\lambda(n)$ is the Carmichael lambda function, and $\text{rad}(N_-(n))$ is the radical of the prime-minus neighborhood context.


## Why This Is A Calculus

It has:

- objects: positive integer fields;
- operators: `C`, `R_min`, `R_p`, `R_S`, `G_p`, `B`, `M`, `T`, `N_-`, `N_+`;
- observables: shell, branching, compression, path gap;
- equations: exact commutator identities;
- controls: shell shuffles and size residuals;
- theorem targets: conditions for commutation and non-commutation.

That is enough to start doing mathematics with it.

## Status Labels

| Claim Type | Status |
| --- | --- |
| `C`, `R_min`, `R_p`, `R_S`, `G_p`, `B`, `M`, `T`, `N_-`, and `N_+` are exact maps | definition |
| path commutator `Delta(A,B;n)` is exact | definition |
| v0 commutator identities | proved in proof appendix with finite regression coverage |
| shell-controlled path signals | local finite evidence |
| full Origin Reframe | not proved by v0 calculus |
| Pakheta Layer as universal relation layer | theory source and methodology |

## Next Calculus Extensions

1. Add more context operators:
   - prime-neighborhood quadratic extension fields;
   - divisor-branching projection divisor topology;
   - fixed-point anchor projection before/after branching.
2. Classify operator pairs by commutation law.
3. Define false-partition controls as broken recombinations of the same field.
4. Define path coherence as low commutator gap under relation-preserving paths.
5. Test whether path gaps predict independent targets after exact mechanisms are
   subtracted.

## Short Form

```text
Origin gives the integer as emanation from 1.
Pakheta gives the relation grammar.
The v0 calculus studies exact context paths through integer fields.
The first new object is the path commutator.
```
