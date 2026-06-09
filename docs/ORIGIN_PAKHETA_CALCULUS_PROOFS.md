# Origin-Pakheta Calculus Proofs

**Status:** Proof appendix  
**Scope:** v0 positive-integer calculus  
**Calculus definition:** `docs/ORIGIN_PAKHETA_CALCULUS.md`  
**Proof program:** `docs/ORIGIN_PAKHETA_PROOF_PROGRAM.md`

This appendix records the theorem-level facts currently available in the
Origin-Pakheta calculus.

## Definitions

Let `n` be a positive integer with prime factorization:

```text
n = product p_i^a_i
```

Define:

```text
Omega(n) = sum a_i
rad(n) = product p_i
C(n) = rad(n)
G_p(n) = p * n
```

For a prime `p`, define selected return:

```text
R_p(n) =
  n / p, if p divides n
  n,     otherwise
```

For a finite set `S` of primes, define selected-set return:

```text
R_S(n) = n / product_{p in S, p divides n} p
```

For `n > 1`, define least-prime return:

```text
R_min(n) = n / spf(n)
```

For two contexts `A` and `B`, define the path commutator:

```text
Delta(A, B; n) = A(B(n)) / B(A(n))
```

The ratio is understood in positive rationals.

## Theorem 1: Minimal Emanation Length

**Statement.**

The minimal number of prime-gather steps needed to build `n` from `1` is
`Omega(n)`.

**Proof.**

A prime-gather step has the form:

```text
G_p(x) = p * x
```

Starting at `1`, a sequence of `k` prime-gather steps produces:

```text
p_1 p_2 ... p_k
```

counted with multiplicity. Therefore any path from `1` to `n` must contain
exactly the prime factors of `n`, including repetitions. By unique
factorization, the number of such factors is:

```text
Omega(n)
```

So no shorter gather path can produce `n`.

Conversely, multiplying the prime factors of `n` in any order constructs `n`
in exactly `Omega(n)` gather steps.

Therefore the minimal gather length from `1` to `n` is `Omega(n)`. QED.

## Theorem 2: Return Path Length

**Statement.**

Every full one-layer return path from `n` to `1` has length `Omega(n)`.

**Proof.**

A one-layer return step divides the current integer by one prime factor that is
present. Each step reduces the total prime-factor multiplicity by exactly one.

The starting value has multiplicity:

```text
Omega(n)
```

The target value `1` has multiplicity:

```text
Omega(1) = 0
```

Therefore exactly `Omega(n)` one-layer returns are required. Fewer steps cannot
remove all prime layers, and `Omega(n)` steps can remove them all in any order.
QED.

## Theorem 3: Compression Idempotence

**Statement.**

For every positive integer `n`:

```text
C(C(n)) = C(n)
```

**Proof.**

By definition:

```text
C(n) = rad(n)
```

`rad(n)` is squarefree. The radical of a squarefree integer is itself. Thus:

```text
C(C(n)) = rad(rad(n)) = rad(n) = C(n)
```

QED.

## Theorem 4: Compression-Selected-Return Commutator

**Statement.**

For prime `p`:

```text
Delta(C, R_p; n)
  =
  p, if v_p(n) > 1
  1, otherwise
```

**Proof.**

Write:

```text
n = p^a * m
```

where `a >= 0` and `p` does not divide `m`.

There are three cases.

### Case 1: `a = 0`

The prime `p` is absent.

```text
R_p(n) = n
C(R_p(n)) = C(n) = rad(m)
C(n) = rad(m)
R_p(C(n)) = rad(m)
```

So:

```text
Delta(C, R_p; n) = 1
```

### Case 2: `a = 1`

The prime `p` appears once.

```text
R_p(n) = m
C(R_p(n)) = rad(m)
C(n) = p * rad(m)
R_p(C(n)) = rad(m)
```

So:

```text
Delta(C, R_p; n) = 1
```

### Case 3: `a > 1`

The prime `p` is repeated.

```text
R_p(n) = p^(a-1) * m
C(R_p(n)) = p * rad(m)
C(n) = p * rad(m)
R_p(C(n)) = rad(m)
```

So:

```text
Delta(C, R_p; n) = p
```

Combining the cases:

```text
Delta(C, R_p; n)
  =
  p, if v_p(n) > 1
  1, otherwise
```

QED.

## Corollary 4.1: Compression-Least-Return Commutator

**Statement.**

For `n > 1`:

```text
Delta(C, R_min; n)
  =
  spf(n), if v_{spf(n)}(n) > 1
  1,      otherwise
```

**Proof.**

Let:

```text
p = spf(n)
```

Then `R_min(n) = R_p(n)`. Apply Theorem 4. QED.

## Theorem 5: Compression-Selected-Set-Return Commutator

**Statement.**

For any finite set `S` of primes:

```text
Delta(C, R_S; n)
  =
  product_{p in S, v_p(n) > 1} p
```

The empty product is `1`.

**Proof.**

Write the prime factorization of `n` as:

```text
n = product q^a_q
```

Only primes with `a_q > 0` appear in `C(n)`.

Consider one prime `q`.

In `C(R_S(n))`, the prime `q` is present exactly when:

```text
q not in S and a_q > 0
```

or:

```text
q in S and a_q > 1
```

That is because `R_S` removes one layer of each selected present prime before
compression.

In `R_S(C(n))`, the prime `q` is present exactly when:

```text
q not in S and a_q > 0
```

That is because `C(n)` leaves at most one copy of each prime, and `R_S` removes
that copy for every selected present prime.

Therefore the exponent difference between `C(R_S(n))` and `R_S(C(n))` is:

```text
1, if q in S and a_q > 1
0, otherwise
```

Multiplying those prime contributions gives:

```text
Delta(C, R_S; n)
  =
  product_{p in S, v_p(n) > 1} p
```

QED.

## Theorem 6: Compression-Gather Commutator

**Statement.**

For prime `p`:

```text
Delta(C, G_p; n)
  =
  1 / p, if p divides n
  1,     otherwise
```

**Proof.**

Again write:

```text
n = p^a * m
```

where `a >= 0` and `p` does not divide `m`.

There are two cases.

### Case 1: `a = 0`

The prime `p` is absent.

```text
G_p(n) = p * m
C(G_p(n)) = p * rad(m)
C(n) = rad(m)
G_p(C(n)) = p * rad(m)
```

So:

```text
Delta(C, G_p; n) = 1
```

### Case 2: `a > 0`

The prime `p` is present.

```text
G_p(n) = p^(a+1) * m
C(G_p(n)) = p * rad(m)
C(n) = p * rad(m)
G_p(C(n)) = p^2 * rad(m)
```

So:

```text
Delta(C, G_p; n) = 1 / p
```

Combining the cases:

```text
Delta(C, G_p; n)
  =
  1 / p, if p divides n
  1,     otherwise
```

QED.

## Consequence: Path Memory Is Exact

The v0 calculus proves that path memory is not only a metaphor.

For the contexts `C`, `R_p`, `R_S`, `R_min`, and `G_p`, non-commutation detects
exact prime-layer structure:

| Commutator | Nontrivial exactly when |
| --- | --- |
| `Delta(C, R_p; n)` | the selected `p` layer is repeated |
| `Delta(C, R_S; n)` | at least one selected layer in `S` is repeated |
| `Delta(C, R_min; n)` | the least-prime layer is repeated |
| `Delta(C, G_p; n)` | the selected `p` layer is present |

This gives the Origin-Pakheta calculus its first theorem-level foundation.

## Next Proof Target

The immediate return-family theorem is now proved for finite selected prime
sets. The next proof target should introduce a richer context, such as:

```text
B(n) = divisor-branching projection
```

or:

```text
M(n) = modular-return mechanism projection
```

Then prove or disprove exact commutator laws:

```text
Delta(C, B; n)
Delta(R_S, B; n)
Delta(C, M; n)
Delta(R_S, M; n)
```

The goal is to discover whether path residues continue to classify local
structure, and then whether any residual signal transfers after the local law is
removed.
