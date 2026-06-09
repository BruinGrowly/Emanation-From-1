# Origin-Pakheta Proof Program

**Status:** Active proof program  
**Scope:** Positive integers first; transfer targets second  
**Depends on:** `docs/ORIGIN_PAKHETA_CALCULUS.md`  
**Proof appendix:** `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md`

This document turns "prove the Origin Reframe" into a stack of exact theorem
targets.

The goal is not to prove a vague interpretation. The goal is to prove a formal
mathematical program and then test how far it transfers.

## The Claim To Prove

The broad Origin Reframe says:

```text
Numbers are not primarily positions on a number line.
They are degrees of differentiation from 1.
```

To prove that mathematically, the repo needs exact versions:

1. Positive integers have a complete Origin representation.
2. Emanation depth is a minimal path length from `1`.
3. Return paths are dual to emanation paths.
4. Compression, return, gather, and anchor operators form a useful calculus.
5. Path residues classify real arithmetic structure.
6. Some Origin-Pakheta metrics transfer beyond the local mechanism that defines
   them.

The first five are theorem-shaped and now have a proof base in the v0 calculus.
The sixth is the hardest evidential frontier.

## Proof Status Map

| ID | Statement | Status |
| --- | --- | --- |
| P1 | Every positive integer has a unique prime-power field representation | established by the fundamental theorem of arithmetic |
| P2 | `Omega(n)` is the minimal number of prime-gather steps from `1` to `n` | proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md` |
| P3 | Any one-layer return path from `n` to `1` has length `Omega(n)` | proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md` |
| P4 | `rad(n)` is the canonical squarefree compression of the integer field | definition plus standard radical properties |
| P5 | `Delta(A,B;n)=A(B(n))/B(A(n))` is an exact path commutator for positive integer contexts | definition |
| P6 | `C/R_min`, `C/R_p`, `C/R_S`, and `C/G_p` commutator laws classify repeated or present prime facets | proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md` |
| P7 | Modular return compression is exactly local defect divided by Carmichael overlap | proved in `docs/MODULAR_RETURN_THEOREM_CANDIDATE.md` |
| P8 | Fixed-point anchor richness is exactly CRT component branching for idempotents and involutions | theorem-level, implemented and regression-tested |
| P9 | Fixed-point anchor residuals transfer after exact mechanisms are removed | false for the tested definitions |
| P10 | `C/B`, `R_S/B`, `C/M`, and `C/T` commutator laws classify branching and modular-return complexity | proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md` |
| P11 | Richer path residues transfer beyond their local commutation laws | open |

## What Is Already Proved Enough To Build On

The current proof base is not empty.

We can already use:

- unique prime-power decomposition;
- shell depth `Omega(n)`;
- radical compression `rad(n)`;
- one-layer return maps;
- selected prime return maps;
- selected prime-set return maps;
- gather maps;
- exact path commutators;
- exact commutator laws for `C/R_min`, `C/R_p`, `C/R_S`, and `C/G_p`;
- exact modular-return decomposition;
- exact fixed-point component counts.

This is enough to build new mathematics. The open question is how far the new
objects transfer.

## Core Theorem Ladder

### Theorem Ladder A: Origin Coordinates

**A1. Unique Field Representation**

Every positive integer `n` has a unique expression:

```text
n = product p_i^a_i
```

This gives the integer field:

```text
F(n) = {(p_i, a_i)}
```

Status: established by standard number theory.

**A2. Minimal Emanation Length**

Let a prime-gather step multiply by one prime:

```text
G_p(n) = p * n
```

Then the minimal number of gather steps from `1` to `n` is:

```text
Omega(n) = sum a_i
```

This makes emanation shell an exact minimal path length.

Status: proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md`.

**A3. Return Duality**

Let a one-layer return step divide by one prime factor present in `n`.

Any full return path from `n` to `1` using one-layer returns has length:

```text
Omega(n)
```

Status: proved in `docs/ORIGIN_PAKHETA_CALCULUS_PROOFS.md`.

### Theorem Ladder B: Path Calculus

**B1. Context Operators**

Define:

```text
C(n) = rad(n)
R_min(n) = n / spf(n)
R_p(n) = n / p if p divides n, otherwise n
R_S(n) = n / product_{p in S, p divides n} p
G_p(n) = p * n
B(n) = divisor_count(n)
M(n) = carmichael_lambda(n)
T(n) = euler_totient(n)
```

All are exact maps on positive integers.

Status: definitions.

**B2. Path Commutator**

For exact contexts `A` and `B`, define:

```text
Delta(A,B;n) = A(B(n)) / B(A(n))
```

Status: definition.

**B3. Compression-Return Law**

```text
Delta(C, R_p; n)
  =
  p, if v_p(n) > 1
  1, otherwise
```

Status: proved.

**B4. Compression-Selected-Set-Return Law**

```text
Delta(C, R_S; n)
  =
  product_{p in S, v_p(n) > 1} p
```

Status: proved.

**B5. Compression-Gather Law**

```text
Delta(C, G_p; n)
  =
  1 / p, if p divides n
  1,     otherwise
```

Status: proved.

**B6. Compression-Divisor Branching Law**

```text
Delta(C, B; n)
  =
  rad(d(n)) / 2^omega(n)
```

Status: proved.

**B7. Return-Divisor Branching Law**

```text
Delta(R_S, B; n)
  =
  (1 / rad_S(d(n))) * product_{p in S, v_p(n) > 0} (v_p(n) + 1) / v_p(n)
```

Status: proved.

**B8. Compression-Carmichael Lambda Law**

```text
Delta(C, M; n)
  =
  lcm_{p | n} ( rad(p-1) * p^min(1, v_p(n) - 1) ) / lcm_{p | n} (p - 1)
```

Status: proved.

**B9. Compression-Euler Totient Law**

```text
Delta(C, T; n)
  =
  rad(phi(n)) / phi(rad(n))
```

Status: proved.

### Theorem Ladder C: Mechanism And Transfer

**C1. Local Mechanism Removal**

For a candidate Origin-Pakheta signal, first prove or model the local mechanism.
Then remove it.

Status: implemented for fixed-point anchors; result was constraining.

**C2. Transfer After Mechanism**

A strong Origin-Pakheta result must show:

```text
residual signal after local mechanism removal
predicts an independent target
better than controls
```

Status: open.

This is the proof-pressure frontier.

## What Would Count As Proof Of The Reframe

The Origin Reframe becomes mathematically strong when these conditions hold:

1. Origin coordinates are complete and minimal.
2. Origin-Pakheta operators generate exact non-trivial identities.
3. Those identities classify structure not naturally visible from the number
   line alone.
4. At least one Origin-Pakheta metric transfers to an independent target after
   ordinary mechanisms and baselines are removed.
5. The transfer result becomes theorem-level or converges to a proof-backed
   conjecture.

The first three are now substantially underway. The fourth and fifth are the
main proof frontier.

## What We Should Prove Next

The immediate v0 path laws are now theorem-level. The next proof target should
extend beyond return-layer bookkeeping into a richer context while preserving
exact domains.

A good next theorem target is:

```text
Define a divisor-branching or modular-return mechanism context B.
Classify Delta(C, B; n) or prove that no lossless integer-valued B exists.
```

Why this matters:

- It moves the calculus from prime-layer memory into mechanism memory.
- It tests whether Pakheta relation-context ideas produce new exact structure.
- It prepares the transfer test by removing the exact local explanation first.

After that, test transfer:

```text
Does any residual path structure predict an independent target after the exact
component explanation is removed?
```

That is the current proof-pressure move.

## Short Version

```text
Do not prove "Origin" as a slogan.
Prove Origin coordinates.
Prove Origin paths.
Prove Pakheta commutators.
Remove local mechanisms.
Then test transfer.
```

That is the route from working calculus to proof.
