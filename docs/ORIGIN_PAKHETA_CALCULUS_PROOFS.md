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

## Theorem 7: Compression-Divisor Branching Commutator

**Statement.**

Let $B(n) = d(n)$ be the divisor count of $n$. For any positive integer $n$:

```text
Delta(C, B; n) = rad(d(n)) / 2^omega(n)
```

where `omega(n)` is the number of distinct prime factors of `n`.

**Proof.**

Let $n = \prod_{i=1}^{\omega(n)} p_i^{a_i}$ be the prime factorization of $n$.

By definition:

```text
B(n) = product_{i=1}^{omega(n)} (a_i + 1)
```

Taking the radical/compression:

```text
C(B(n)) = rad( product_{i=1}^{omega(n)} (a_i + 1) ) = rad(d(n))
```

For the alternative path:

```text
C(n) = product_{i=1}^{omega(n)} p_i
```

Since $C(n)$ is squarefree with $\omega(n)$ distinct prime factors, its divisor count is:

```text
B(C(n)) = 2^omega(n)
```

Thus:

```text
Delta(C, B; n) = C(B(n)) / B(C(n)) = rad(d(n)) / 2^omega(n)
```

QED.

## Corollary 7.1: Commutation Conditions for C/B

**Statement.**

For $n > 1$, the compression context $C$ and divisor branching context $B$ commute if and only if $n = p^{2^k - 1}$ for some prime $p$ and integer $k \ge 1$.

**Proof.**

The commutation condition is:

```text
Delta(C, B; n) = 1  <=>  rad(d(n)) = 2^omega(n)
```

Since the left-hand side is squarefree, it is a product of distinct primes. The right-hand side is a power of 2. Thus, the only prime factor that can divide `rad(d(n))` is 2.

This implies:

```text
rad(d(n)) = 1 or 2
```

Since $n > 1$, we have $\omega(n) \ge 1$, so $2^{\omega(n)} \ge 2$. Thus, we must have:

```text
rad(d(n)) = 2  and  2^omega(n) = 2
```

From $2^{\omega(n)} = 2$, we get:

```text
omega(n) = 1
```

which means $n = p^a$ for some prime $p$ and $a \ge 1$.

From $rad(d(n)) = 2$ and $d(n) = a + 1$, the only prime factor of $a + 1$ is 2. Therefore:

```text
a + 1 = 2^k
a = 2^k - 1
```

for some integer $k \ge 1$.

Thus, $n = p^{2^k - 1}$ for some prime $p$ and integer $k \ge 1$. QED.

## Theorem 8: Return-Divisor Branching Commutator

**Statement.**

For any finite set $S$ of primes, and $B(n) = d(n)$:

```text
Delta(R_S, B; n) = (1 / rad_S(d(n))) * product_{p in S, v_p(n) > 0} (v_p(n) + 1) / v_p(n)
```

where `rad_S(x) = product_{q in S, q | x} q`.

**Proof.**

Let $n = \prod p_i^{a_i}$.

The divisor count of $R_S(n)$ is:

```text
B(R_S(n)) = product_{p_i not in S} (a_i + 1) * product_{p_i in S, a_i > 0} a_i
```

The alternative path return-set on the divisor count is:

```text
R_S(B(n)) = B(n) / rad_S(B(n)) = ( product (a_i + 1) ) / rad_S(d(n))
```

Taking the ratio:

```text
Delta(R_S, B; n) = R_S(B(n)) / B(R_S(n))
                 = [ product (a_i + 1) ] / [ rad_S(d(n)) * product_{p_i not in S} (a_i + 1) * product_{p_i in S, a_i > 0} a_i ]
                 = [ product_{p_i in S, a_i > 0} (a_i + 1) ] / [ rad_S(d(n)) * product_{p_i in S, a_i > 0} a_i ]
                 = (1 / rad_S(d(n))) * product_{p in S, v_p(n) > 0} (v_p(n) + 1) / v_p(n)
```

QED.

## Theorem 9: Compression-Carmichael Lambda Commutator

**Statement.**

Let $M(n) = \lambda(n)$ be the Carmichael totient function. For any positive integer $n$:

```text
Delta(C, M; n) = lcm_{p | n} ( rad(p-1) * p^min(1, v_p(n) - 1) ) / lcm_{p | n} (p - 1)
```

**Proof.**

Let $n = \prod p_i^{a_i}$.

By definition:

```text
M(n) = lambda(n) = lcm_{p_i | n} lambda(p_i^{a_i})
```

For each component:

```text
lambda(p_i^{a_i}) = (p_i - 1) * p_i^{a_i - 1}
```

(with the standard $2^{a-2}$ behavior for $p=2$, which preserves the same distinct prime factors as $(2-1) \cdot 2^{a-1}$).

Taking the radical:

```text
C(M(n)) = rad( lcm_{p_i | n} lambda(p_i^{a_i}) )
        = lcm_{p_i | n} rad( lambda(p_i^{a_i}) )
        = lcm_{p_i | n} ( rad(p_i - 1) * p_i^min(1, a_i - 1) )
```

For the alternative path:

```text
C(n) = product_{p_i | n} p_i
M(C(n)) = lambda( rad(n) ) = lcm_{p_i | n} (p_i - 1)
```

Dividing the two values gives the statement. QED.

## Corollary 9.1: Commutation Conditions for C/M

**Statement.**

For squarefree $n$, the compression context $C$ and Carmichael lambda context $M$ commute if and only if $\lambda(n)$ is squarefree.

**Proof.**

For squarefree $n$, $v_p(n) \le 1$ for all prime factors $p$. Thus $\min(1, v_p(n) - 1) = 0$.

Theorem 9 simplifies to:

```text
Delta(C, M; n) = lcm_{p | n} rad(p - 1) / lcm_{p | n} (p - 1)
               = rad( lambda(n) ) / lambda(n)
```

This ratio equals 1 if and only if $\text{rad}(\lambda(n)) = \lambda(n)$, which is the definition of $\lambda(n)$ being squarefree. QED.

## Theorem 10: Compression-Euler Totient Commutator

**Statement.**

Let $T(n) = \phi(n)$ be the Euler totient function. For any positive integer $n$:

```text
Delta(C, T; n) = rad(phi(n)) / phi(rad(n))
```

**Proof.**

By definition:

```text
C(T(n)) = rad(phi(n))
C(n) = rad(n)
T(C(n)) = phi(rad(n))
```

Dividing the two yields the theorem. QED.

## Theorem 11: Compression-Prime Minus Commutator

**Statement.**

Let $N_-(n) = \prod_{p | n} (p - 1)$ be the prime-minus neighborhood context. For any positive integer $n$:

```text
Delta(C, N_-; n) = rad( product_{p | n} (p - 1) ) / product_{p | n} (p - 1)
```

**Proof.**

Let $P$ be the set of distinct prime factors of $n$.

By definition:

```text
N_-(n) = product_{p in P} (p - 1)
```

Taking the radical/compression:

```text
C(N_-(n)) = rad( product_{p in P} (p - 1) )
```

For the alternative path:

```text
C(n) = rad(n) = product_{p in P} p
```

Since the distinct prime factors of $\text{rad}(n)$ are exactly the set $P$, we have:

```text
N_-(C(n)) = product_{p in P} (p - 1)
```

Dividing the two values yields the statement. QED.

## Theorem 12: Return-Prime Minus Commutator

**Statement.**

For any finite set $S$ of primes, and $N_-(n) = \prod_{p | n} (p - 1)$:

```text
Delta(R_S, N_-; n) = product_{p in S, v_p(n) = 1} (p - 1) / rad_S( product_{p | n} (p - 1) )
```

where `rad_S(x) = product_{q in S, q | x} q`.

**Proof.**

Let $P$ be the set of distinct prime factors of $n$.

Primes in $S$ are removed from the prime factors of $R_S(n)$ if and only if they appear in $n$ with multiplicity exactly 1. Primes in $S$ with multiplicity greater than 1 remain prime factors of $R_S(n)$. Thus:

```text
N_-(R_S(n)) = product_{p in P \ (S \cap {q | v_q(n) = 1})} (p - 1)
```

Dividing the full product $N_-(n)$ by $N_-(R_S(n))$ leaves:

```text
N_-(n) / N_-(R_S(n)) = product_{p in S, v_p(n) = 1} (p - 1)
```

The alternative path return-set on the prime-minus context is:

```text
R_S(N_-(n)) = N_-(n) / rad_S(N_-(n))
```

Taking the ratio:

```text
Delta(R_S, N_-; n) = R_S(N_-(n)) / N_-(R_S(n))
                   = [ N_-(n) / rad_S(N_-(n)) ] / N_-(R_S(n))
                   = [ N_-(n) / N_-(R_S(n)) ] / rad_S(N_-(n))
                   = product_{p in S, v_p(n) = 1} (p - 1) / rad_S( product_{p | n} (p - 1) )
```

QED.

## Theorem 13: Compression-Prime Plus Commutator

**Statement.**

Let $N_+(n) = \prod_{p | n} (p + 1)$ be the prime-plus neighborhood context. For any positive integer $n$:

```text
Delta(C, N_+; n) = rad( product_{p | n} (p + 1) ) / product_{p | n} (p + 1)
```

**Proof.**

Let $P$ be the set of distinct prime factors of $n$.

By definition:

```text
N_+(n) = product_{p in P} (p + 1)
```

Taking the radical/compression:

```text
C(N_+(n)) = rad( product_{p in P} (p + 1) )
```

For the alternative path:

```text
C(n) = rad(n) = product_{p in P} p
```

Since the distinct prime factors of $\text{rad}(n)$ are exactly $P$:

```text
N_+(C(n)) = product_{p in P} (p + 1)
```

Dividing the two yields the statement. QED.

## Theorem 14: Return-Prime Plus Commutator

**Statement.**

For any finite set $S$ of primes, and $N_+(n) = \prod_{p | n} (p + 1)$:

```text
Delta(R_S, N_+; n) = product_{p in S, v_p(n) = 1} (p + 1) / rad_S( product_{p | n} (p + 1) )
```

where `rad_S(x) = product_{q in S, q | x} q`.

**Proof.**

Let $P$ be the set of distinct prime factors of $n$.

Primes in $S$ are removed from the prime factors of $R_S(n)$ if and only if they appear in $n$ with multiplicity exactly 1. Primes in $S$ with multiplicity greater than 1 remain prime factors of $R_S(n)$. Thus:

```text
N_+(R_S(n)) = product_{p in P \ (S \cap {q | v_q(n) = 1})} (p + 1)
```

Dividing the full product $N_+(n)$ by $N_+(R_S(n))$ leaves:

```text
N_+(n) / N_+(R_S(n)) = product_{p in S, v_p(n) = 1} (p + 1)
```

The alternative path return-set on the prime-plus context is:

```text
R_S(N_+(n)) = N_+(n) / rad_S(N_+(n))
```

Taking the ratio:

```text
Delta(R_S, N_+; n) = R_S(N_+(n)) / N_+(R_S(n))
                   = [ N_+(n) / rad_S(N_+(n)) ] / N_+(R_S(n))
                   = [ N_+(n) / N_+(R_S(n)) ] / rad_S(N_+(n))
                   = product_{p in S, v_p(n) = 1} (p + 1) / rad_S( product_{p | n} (p + 1) )
```

QED.

## Theorem 15: Neighborhood Period Bound

**Statement.**

Let $N_-(n) = \prod_{p | n} (p - 1)$ be the prime-minus neighborhood context, and $\lambda(n)$ be the Carmichael lambda function. For any positive integer $n \ge 2$:

```text
lambda(n) >= rad(N_-(n))
```

Furthermore, the radical of the prime-minus neighborhood, $\text{rad}(N_-(n))$, always divides the Carmichael lambda, $\lambda(n)$.

**Proof.**

Let $n = \prod_{i=1}^k p_i^{a_i}$ be the prime factorization of $n$, where $p_i$ are distinct prime factors of $n$ and $a_i \ge 1$.

By definition, the Carmichael lambda of $n$ is the least common multiple of the lambdas of its prime power components:
```text
lambda(n) = lcm_{i=1}^k lambda(p_i^{a_i})
```
where the component lambdas are:
```text
lambda(p_i^{a_i}) = (p_i - 1) * p_i^{a_i - 1}  (if p_i is odd)
lambda(2^{a_i}) = 2^{a_i - 1}  (if p_i = 2 and a_i <= 2)
lambda(2^{a_i}) = 2^{a_i - 2}  (if p_i = 2 and a_i >= 3)
```
In both cases, notice that for any prime component $p_i$, the component lambda $\lambda(p_i^{a_i})$ is divisible by $p_i - 1$.

The prime-minus neighborhood is defined as the product of $p_i - 1$ over the distinct prime factors:
```text
N_-(n) = product_{i=1}^k (p_i - 1)
```
Let $q$ be any prime factor of $N_-(n)$. Since $q$ divides the product $\prod_{i=1}^k (p_i - 1)$, it must divide at least one of the terms $(p_j - 1)$ for some $j \in \{1, \dots, k\}$.

Since $(p_j - 1)$ divides $\lambda(p_j^{a_j})$, $q$ must divide $\lambda(p_j^{a_j})$.

Since $\lambda(n)$ is the least common multiple:
```text
lambda(n) = lcm( lambda(p_1^{a_1}), ..., lambda(p_k^{a_k}) )
```
and $q$ divides the component $\lambda(p_j^{a_j})$, it must divide the least common multiple $\lambda(n)$.

Since this holds for every prime factor $q$ of $N_-(n)$, the set of prime factors of $N_-(n)$ is a subset of the prime factors of $\lambda(n)$. 

The radical operator $\text{rad}(x)$ is the product of the distinct prime factors of $x$. Thus:
```text
rad(N_-(n)) = product_{q | N_-(n)} q
```
Since every such prime factor $q$ divides $\lambda(n)$, and they are all distinct primes, their product $\text{rad}(N_-(n))$ must divide $\lambda(n)$ (since any set of distinct primes that divide a number also has their product dividing that number).

Because $\text{rad}(N_-(n))$ divides $\lambda(n)$, and both are positive integers for $n \ge 2$, we have:
```text
lambda(n) >= rad(N_-(n))
```
QED.

## Next Proof Target

The calculus now establishes the Neighborhood Period Bound (Theorem 15), linking modular return periods directly to boundary contexts. Future proof targets should extend this bounding method to other modular and additive targets, such as formulating bounds on divisors and Goldbach witness densities using compositions of return and neighborhood operators.


