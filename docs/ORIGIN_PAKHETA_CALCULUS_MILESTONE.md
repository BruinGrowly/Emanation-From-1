# Origin-Pakheta Calculus Milestone

**Status:** Research milestone  
**Date:** June 9, 2026  
**Depends on:** `docs/ORIGIN_PAKHETA_CALCULUS.md`  
**Companion report:** `reports/ORIGIN_PAKHETA_CALCULUS.md`

This note captures what became possible once the first Origin-Pakheta calculus
started working.

## What Changed

Before this milestone, Pakheta was useful as research language. It helped us
ask better questions about anchors, fields, contexts, false partitions, and
coherence.

After this milestone, Pakheta has an executable arithmetic surface.

The first exact object is:

```text
Delta(A, B; n) = A(B(n)) / B(A(n))
```

where `A` and `B` are exact context operators on positive integers.

This object measures whether two paths through an integer field commute.

Plainly:

```text
Delta = 1      means path order leaves no residue.
Delta != 1    means the integer field remembers the path.
```

That is the key transition.

## Why This Matters

The Origin Reframe says that numbers should be studied as differentiations from
`1`, not only as positions on a line.

The Pakheta Layer says relation, context, anchor, and path matter.

The calculus joins those claims:

```text
integer as emanation field
+ exact context operators
+ path commutators
= path-sensitive arithmetic
```

This means we can now study positive integers by ordered relational behavior,
not only by static properties such as size, factors, residues, or divisor count.

## First Working Operators

The first calculus uses four context families:

| Symbol | Definition | Reading |
| --- | --- | --- |
| `C(n)` | `rad(n)` | compress to squarefree skeleton |
| `R_min(n)` | remove one least-prime factor | return one least layer toward `1` |
| `R_p(n)` | remove one selected `p` layer if present | selected return context |
| `G_p(n)` | `p * n` | gather one prime facet |

These operators are deliberately small. Their value is that they are exact and
already produce non-trivial path laws.

## First Path Laws

### Least-Prime Return Law

```text
C(R_min(n)) / R_min(C(n))
  =
  spf(n), if the least-prime layer is repeated
  1,      otherwise
```

Meaning:

```text
compress then return != return then compress
exactly when the least-prime return layer is repeated
```

### Selected-Prime Return Law

For prime `p`:

```text
C(R_p(n)) / R_p(C(n))
  =
  p, if v_p(n) > 1
  1, otherwise
```

Meaning:

```text
compress then selected-return != selected-return then compress
exactly when the selected prime layer is repeated
```

### Gather Law

For prime `p`:

```text
C(G_p(n)) / G_p(C(n))
  =
  1 / p, if p divides n
  1,     otherwise
```

Meaning:

```text
compress then gather != gather then compress
exactly when the gathered prime facet is already present
```

## What The Scan Shows

The default scan through `2..10000` found:

- `0` mismatches for `C/R_min`;
- `0` mismatches for `C/R_p` with `p in {2, 3, 5, 7}`;
- `0` mismatches for `C/G_p` with `p in {2, 3, 5}`;
- `C/R_min` path gap nonzero for `3302/9999` integers;
- shell-controlled `radical_compression -> C/R_min path gap` correlation
  `r = 0.6819`;
- shell-shuffled controls matched or exceeded that correlation in `0/250`
  trials.

This does not prove the full Origin Reframe. It does show that the
Origin-Pakheta vocabulary can produce exact arithmetic objects, exact laws,
finite scans, and controls.

## What This Makes Possible

### 1. Path-Sensitive Number Theory

We can now classify integers by whether context order matters.

Instead of only asking:

```text
What factors does n have?
```

we can ask:

```text
Which context paths through n commute?
Which paths leave residue?
What does that residue measure?
```

### 2. Operator Families

The calculus can grow by defining more exact contexts:

- modular-return contexts;
- divisor-branching projections;
- fixed-point anchor projections;
- prime-neighborhood transforms;
- radical and squarefree projections;
- shell-preserving transformations.

Each new operator creates new commutator families.

### 3. New Theorem Targets

Every operator pair gives theorem-shaped questions:

```text
When does Delta(A, B; n) = 1?
When is Delta(A, B; n) > 1?
What exact factor controls the gap?
Does the gap classify a known arithmetic structure?
```

This gives a repeatable method for creating and proving local laws.

### 4. Better Transfer Tests

The next evidential question is not merely whether a path gap exists. It does.

The next question is:

```text
After the local commutation law is removed,
does any path residue predict an independent target?
```

That is the right pressure test.

### 5. A Formal Bridge From Pakheta To Arithmetic

Pakheta terms now have arithmetic counterparts:

| Pakheta Term | Arithmetic Counterpart |
| --- | --- |
| field | positive integer with prime-power facets |
| node/facet | prime-power component |
| context | exact operator such as `C`, `R_p`, or `G_p` |
| path | ordered composition of contexts |
| path memory | non-commuting path commutator |
| coherence | commutation or low path gap under declared contexts |
| false partition | broken or shuffled relation preserving superficial features |

This is the first usable bridge from Pakheta language into number-theoretic
machinery.

## What This Does Not Yet Prove

This milestone does not prove:

- the full Origin Reframe;
- that Pakheta is a universal relation layer;
- that path residues transfer to prime gaps, Goldbach, Gilbreath, or modular
  behavior;
- that every Pakheta concept has a useful arithmetic counterpart.

It does prove something narrower and important:

```text
Origin-Pakheta calculus is constructible.
```

The first operators work. The first commutators are exact. The first path laws
are testable and reproducible.

## Research Posture From Here

The project should now build boldly but label carefully.

Use these labels:

| Label | Meaning |
| --- | --- |
| definition | an exact object we introduce |
| identity | a proved local law |
| finite evidence | a scan result with controls |
| conjecture | expected generalization not yet proved |
| transfer claim | evidence that a metric predicts an independent target |
| interpretation | broader Origin/Pakheta meaning |

This lets the repo develop new math without pretending every working object is
already a full proof of the whole frame.

## Next Best Move

Extend the calculus to one richer context family, preferably:

```text
M(n) = modular-return decomposition context
```

or:

```text
B(n) = divisor-branching projection
```

Then compute commutators such as:

```text
Delta(C, M; n)
Delta(R_p, M; n)
Delta(C, B; n)
Delta(R_p, B; n)
```

The goal is to find whether path residues remain merely local identities or
begin to predict independent arithmetic behavior.

## Short Summary

```text
We now have a working Origin-Pakheta calculus.
Its first object is the path commutator.
Its first laws classify when compression, return, and gather remember order.
This opens path-sensitive arithmetic as a new research surface.
```
