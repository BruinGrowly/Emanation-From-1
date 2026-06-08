# Origin Theory Research Bridge

This note translates the wider source corpus in `docs/origin_theory/`,
`docs/SEMANTIC_VOLTAGE_RESEARCH.md`, and `docs/pakheta_layer/` into concrete
research moves for this repo.

The jury remains out on the Origin Reframe until conventional proof or strong
controlled evidence exists. These documents are useful because they suggest what
to test next, not because they settle the question.

## Boundary

Use the theory corpus as:

- hypothesis source;
- vocabulary source;
- source of candidate invariants;
- source of failure conditions.
- source of control design, especially "false partition" tests.

Do not use it as:

- proof of number-theory claims;
- ledger evidence by itself;
- a license to relabel known arithmetic after the fact.

A theory claim enters the evidence ledger only after it becomes a local
measurement with a baseline, control, finite range, and failure condition.

Pakheta language follows the same rule. It can name a candidate grammar of
field, node, anchor, context, actualization, coherence, and decoherence. It does
not count as evidence until those terms become exact repo objects.

## Useful Theory-To-Test Translations

| Theory language | Repo translation | Current status |
| --- | --- | --- |
| `1` as anchor | Fixed point, identity, empty factorization, return target | Operationalized in profiles and modular-return scans |
| Emanation distance | Factor depth, expression depth, return-path length | Factor depth is implemented; expression depth is not yet audited |
| Semantic voltage | Coherence pressure or retention under transformation | Not yet operationalized as one pre-registered metric |
| Anchor echo | Origin-like invariance should beat matched controls | Fixed-point first pass added; independent transfer remains open |
| Pakheta relationship-field | Exact structure preserved across representations | Useful as a test-design grammar; not evidence by itself |
| Pakheta anchor | Fixed point, invariant, basis, or stable access point | First local test added in `reports/ORIGIN_ANCHOR_ECHO_FIXED_POINTS.md` |
| False partition | Break the real relation while preserving shell or size | Implemented as shell shuffles for fixed-point targets |
| Context/path sensitivity | Order of transformations should leave measurable residue | Not yet tested in Origin arithmetic |
| Phi load balance | Proportional weighting should beat over-fused or over-split controls | Hypothesis only; needs non-circular targets |
| Resolution translation | Semantic claim -> exact formula -> finite controls | Best example so far is Carmichael overlap decomposition |
| Primes as irreducibles | First-layer departures from `1` | Operationalized, but semantic claims remain hypothesis material |

## What The Recent Results Say

The modular-return line is the strongest current Origin-first branch:

- shell depth transfers into modular return-exponent compression;
- within-shell radical compression retains a signal;
- the exact mechanism is Carmichael lcm-overlap;
- signal decomposition shows the conditioned log signal is overwhelmingly
  overlap pressure;
- the first non-modular transfer to prime gaps was constraining.

Plainly:

> We found a real mechanism, then discovered it does not automatically generalize.

That is a healthy boundary. It means the next work should be sharper, not louder.

The Pakheta-informed anchor-echo pass is now similarly bounded:

- modular idempotents satisfy the exact identity `idempotent_count(n) = 2^omega(n)`;
- modular involutions are exactly explained by odd prime-power components plus
  the special `2^a` case;
- shell-shuffled controls break the relationship cleanly;
- the mechanism is conventional CRT component branching, not standalone proof
  of the Origin ontology.

Plainly:

> Pakheta helped choose a sharper test; ordinary arithmetic explained the result.

That is still useful. It means Pakheta should be used as a generator of exact
tests and controls, especially for anchors, false partitions, context order, and
coherence loss.

## What Pakheta Adds

The Pakheta folder sharpens the next research vocabulary in five ways:

1. **Anchor-context separation.** A fixed point or invariant is an anchor. A
   transformation, projection, or selected probe is a context. Mixing them makes
   the evidence muddy.
2. **False partition as a control.** A supportive result should disappear when
   the true relationship is shuffled, split, or recombined incorrectly while
   size and shell are preserved.
3. **Relational distance over spatial distance.** In integer work, this becomes
   structural nearness instead of ordinary number-line nearness.
4. **Path sensitivity.** If context order matters, then `A(B(n))` and `B(A(n))`
   should leave different residuals under a declared metric.
5. **Phi as load-balance hypothesis.** Phi should only enter after a non-circular
   weighting task exists. If the data is generated with phi weights, phi success
   is calibration, not discovery.

## Highest-Value Next Moves

### 1. Operationalize Semantic Voltage For Integers

The theory corpus repeatedly frames voltage as coherence retained near the
anchor. The repo needs one narrow numerical proxy before using that language as
evidence.

Candidate pre-registered metric:

```text
origin_coherence(n)
  =
  1 / (1 + normalized_depth(n) + branching_dispersion(n) + overlap_pressure(n))
```

Better immediate move:

Use a small candidate family instead of pretending one formula is final:

- `depth_coherence = 1 / (1 + Omega(n))`
- `compression_coherence = radical(n) / n`
- `return_coherence = lambda(n) / phi(n)`
- `overlap_coherence = 1 / (1 + log(overlap_penalty(n)))`

Then require a pre-declared target before scoring.

Failure condition:

> If these coherence proxies do not beat size, shell, and factor-count baselines,
> semantic voltage remains vocabulary, not evidence.

### 2. Test The Anchor Echo Hypothesis Directly

`MATH_REALM_MAP_AND_HYPOTHESES_2026-03-14.md` gives the cleanest falsifiable
language:

> Fixed-point, identity, or return structures should score as stronger coherence
> carriers than matched controls.

First pass now exists:

- `experiments/origin_anchor_echo_fixed_points.py`
- `reports/ORIGIN_ANCHOR_ECHO_FIXED_POINTS.md`

Result:

- idempotent fixed-point richness is exactly component branching;
- involution richness is exactly odd component branching plus the `2^a`
  correction;
- this is a clean theorem-level mechanism, but not yet a downstream transfer.

Remaining local tests:

- Compare fixed-point richness to divisor branching and Carmichael overlap.
- Ask whether origin-coherence proxies predict fixed-point richness after
  conventional baselines.
- Test whether fixed-point richness predicts an independent downstream target
  after its exact component mechanism is accounted for.

Why this is promising:

- Fixed points are mathematically exact.
- They are close to the theory language of anchor/return.
- They are not the same target as `lambda/phi`, though they remain factor-linked.

### 3. Audit The Existing Emanation Map

`THE_EMANATION_MAP.md` contains a structural-depth map for `1..1000`. It may
encode a different depth notion than `Omega(n)`.

Next test:

- Reconstruct the expression-depth rules behind that map.
- Compare expression depth against:
  - `Omega(n)`;
  - addition-chain length;
  - shortest formula length using `{1, +, *, ^, -1}`;
  - Mersenne lineage membership.

Failure condition:

> If the map cannot be reproduced by explicit rules, it stays source material and
> should not be used as evidence.

### 4. Turn Resolution Translation Into A Checklist

`RESOLUTION_INDEPENDENT_PROOF_METHODOLOGY.md` is most useful as a workflow, not
as a proof standard.

Repo translation:

1. State the semantic claim.
2. Translate it into a conventional object.
3. Name the exact theorem candidate.
4. Name the finite experiment.
5. Name the control that would break the interpretation.

This matches the modular-return progress:

```text
return to 1
-> lambda(n)/phi(n)
-> Carmichael lcm-overlap identity
-> shell-conditioned scans
-> controls and failed transfer test
```

### 5. Keep Prime-Conjecture Claims Downstream

`PRIME_SEMANTIC_FOUNDATIONS.md` contains strong language about Goldbach,
Riemann, and prime meaning. In this repo, those statements should be treated as
semantic hypotheses only.

Current evidence already warns us:

- Goldbach simple factor-depth signals mostly collapse into conventional
  singular-factor structure.
- Prime-gap held-out prediction is constraining.
- Overlap-pressure transfer to prime gaps was constraining.
- Gilbreath remains interesting but has strong local-memory confounders.

Therefore the next prime-related move should be narrow and pre-registered, not a
large interpretive claim.

## Recommended Next Experiment

The fixed-point anchor test has been added. The cleanest next executable
experiment is now:

> Test whether fixed-point anchor richness transfers into an independent target
> after the exact CRT mechanism is removed.

Pre-registered question:

> After size, shell, and component-count baselines, do idempotent or involution
> residuals predict modular-return residuals, local prime-neighborhood residuals,
> or another pre-declared target better than shuffled controls?

Candidate targets:

- `lambda(n) / phi(n)` residuals after the known overlap decomposition;
- prime-neighborhood targets on `p - 1` and `p + 1`;
- context-order deltas such as `compress_then_return(n)` versus
  `return_then_compress(n)`, if defined exactly.

Metrics:

- idempotent residual after component count;
- involution residual after odd component count and `2^a` correction;
- radical compression;
- overlap pressure;
- origin-coherence candidate family.

Controls:

- residualize against `log(n)`;
- residualize or group by shell `Omega(n)`;
- residualize against exact component baselines;
- shuffle targets within shell and size bins;
- compare against conventional factor-count baselines.

Why this is the best next move:

- It follows directly from the theory and Pakheta corpus.
- It remains inside conventional arithmetic.
- It does not re-count the theorem we already know.
- It asks whether anchor structure carries signal beyond its exact local
  mechanism.

## Current Research Posture

The Origin Reframe now has three layers:

1. **Theory source:** origin theory and semantic-voltage corpus.
2. **Operational map:** shell, branching, compression, return path, modular
   decomposition.
3. **Evidence ledger:** local tests that can support, constrain, or challenge
   the frame.

The next proof path is not to assert that the theory corpus is true. It is to
keep translating its best claims into exact arithmetic and let the controls
decide how far the frame really reaches.
