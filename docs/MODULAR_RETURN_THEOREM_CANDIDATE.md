# Modular Return Theorem Candidate

This note turns the strongest Origin-first evidence line into theorem-shaped mathematics.

Current empirical line:

> Within a fixed emanation shell, radical compression predicts modular return-exponent compression.

Operational terms:

- Emanation shell: `Omega(n)`, the total number of prime factors with multiplicity.
- Radical ratio: `rad(n) / n`.
- Radical compression: `1 - rad(n) / n`.
- Return-exponent compression: `lambda(n) / phi(n)`, where `lambda` is the Carmichael exponent.

## Exact Theorem 1: Coprime Product Law

If `gcd(a, b) = 1`, then:

```text
lambda(ab) / phi(ab)
  =
  (lambda(a) / phi(a))
  * (lambda(b) / phi(b))
  / gcd(lambda(a), lambda(b))
```

Reason:

```text
lambda(ab) = lcm(lambda(a), lambda(b))
phi(ab) = phi(a) phi(b)
lcm(x, y) = xy / gcd(x, y)
```

Interpretation:

Every new coprime component introduces a return-exponent compression factor. The penalty is controlled by overlap in the component return periods.

This is the exact mechanism behind the modular-return signal.

## Exact Theorem 2: Prime-Power Component Formula

Let:

```text
n = product p_i^a_i
c_i = lambda(p_i^a_i)
d_i = c_i / phi(p_i^a_i)
G(n) = product(c_i) / lcm(c_i)
```

Then:

```text
lambda(n) / phi(n) = product(d_i) / G(n)
```

For odd prime powers, `d_i = 1`. For `2^a` with `a >= 3`, `d_i = 1/2`.

Interpretation:

For odd `n`, all return-exponent compression comes from the lcm-overlap penalty `G(n)`. The more the number is split into coprime prime-power components, the more opportunities there are for lcm compression.

## Exact Decomposition: Three Pressure Terms

The reusable code path is now:

```python
from emanation_from_1.number_theory import modular_return_decomposition
```

`modular_return_decomposition(n)` returns exact `Fraction` values for:

- concentration proxy: `radical_compression = 1 - rad(n) / n`;
- splitting pressure: `component_count = omega(n)`, the number of distinct prime-power components;
- odd splitting pressure: `odd_component_count`;
- local defect: `product(lambda(p_i^a_i) / phi(p_i^a_i))`;
- overlap pressure: `product(lambda(p_i^a_i)) / lcm(lambda(p_i^a_i))`;
- return-exponent compression: `lambda(n) / phi(n)`.

The formal identity is:

```text
lambda(n) / phi(n)
  =
  local_defect_ratio(n) / overlap_penalty(n)
```

So the exact arithmetic mechanism is local defect plus Carmichael lcm overlap. Radical compression is not a term in that identity by itself; it is the Origin-facing concentration proxy that predicts the balance between concentrated prime powers and split coprime components inside fixed shells.

On the log scale this becomes additive:

```text
log(lambda(n) / phi(n))
  =
  log(local_defect_ratio(n)) - log(overlap_penalty(n))
```

`experiments/origin_modular_signal_decomposition.py` uses this additive identity to quantify the shell-conditioned signal after applying the same group baselines used by the modular transfer tests.

Default local result through `10000`:

- maximum identity error after shell-centering and shared residualization: `4.441e-15`;
- local prime-power defect contribution: `0.12%`;
- Carmichael lcm-overlap contribution: `99.88%`;
- Origin-facing concentration/splitting proxies capture `33.33%` of the conditioned log-signal variance before exact mechanism terms are added.

Interpretation:

The modular-return signal is overwhelmingly an overlap-pressure signal in the default finite scan. Radical compression and component splitting remain useful Origin-facing proxies, but they are not the source of the full mechanism.

First non-modular transfer check:

- `experiments/prime_gap_overlap_transfer.py` pre-registers `p + 1` overlap pressure as a predictor for unusually large held-out prime gaps.
- In the default held-out windows, AUCs were `0.5029` and `0.4974`.
- Residue-plus-size controls matched or exceeded the observed AUC in `73/200` trials.

So overlap pressure is currently a strong mechanism for modular return-exponent compression, not a demonstrated general predictor across number-theory phenomena.

## Exact Corollary: Odd Distinct-Prime Bound

For odd `n` with `omega(n)` distinct prime factors:

```text
lambda(n) / phi(n) <= 2^(1 - omega(n))
```

Reason:

Each odd prime-power component has even Carmichael value. The product-to-lcm overlap penalty contains at least one shared factor `2` for each additional odd component.

Interpretation:

More distinct odd components force return-exponent compression. This is a theorem-level bridge between factor splitting and modular return to `1`.

## Endpoint Shell Result

Inside shell `k`:

- Odd prime powers are maximally concentrated:

```text
n = p^k
rad(n) / n = p^(1-k)
lambda(n) / phi(n) = 1
```

- Odd squarefree products are maximally split:

```text
n = p_1 p_2 ... p_k
rad(n) / n = 1
lambda(n) / phi(n) <= 2^(1-k)
```

So, at the shell endpoints, radical compression and return-exponent compression are linked by proof:

- High radical compression can reach maximal `lambda/phi`.
- Zero radical compression is forced into lcm-overlap compression when multiple odd components are present.

## What Is Not True

The naive monotonic theorem is false:

> If two numbers have the same shell and one has higher radical compression, then it must have higher `lambda/phi`.

Counterexamples exist because `p_i - 1` overlap can dominate radical compression.

Example from the local probe:

```text
Omega(30) = Omega(63) = 3

radical_compression(30) = 0
lambda(30) / phi(30) = 0.5

radical_compression(63) = 2/3
lambda(63) / phi(63) = 1/6
```

So radical compression is not a total ordering. It is a structural proxy for concentration versus splitting, while Carmichael overlap supplies the exact arithmetic mechanism.

## Theorem Candidate

The realistic theorem is not simple monotonicity. It is:

> Modular return-exponent compression is exactly controlled by coprime component splitting and Carmichael lcm-overlap. Radical compression predicts it in finite shell-conditioned scans because radical compression measures concentration of factor mass inside a shell, while `lambda/phi` penalizes splitting into multiple coprime return components.

Proof status:

- Exact product law: proved.
- Exact component formula: proved.
- Odd distinct-prime bound: proved.
- Endpoint shell contrast: proved.
- Universal monotonicity by radical compression alone: false.
- Statistical within-shell prediction by radical compression: empirically supported by `E22` and `E23`, not yet a universal theorem.

## Next Proof Move

The decomposition and signal-attribution moves are now implemented and regression-tested. The next theorem should explain when Origin-facing proxies track the exact overlap term:

1. Concentration pressure: measured by radical compression.
2. Splitting pressure: measured by `omega(n)` and the component count.
3. Overlap pressure: measured exactly by Carmichael lcm overlap.

The strongest realistic target is not:

> Radical compression universally orders `lambda(n) / phi(n)`.

That is false. The next target is:

> Inside fixed emanation shells, radical compression predicts `lambda(n) / phi(n)` only insofar as it tracks concentration/splitting, while the exact return compression is determined by local prime-power defects and Carmichael lcm overlap.

The next strongest statement should bound or characterize when `rad(n) / n`, component count, or odd component count can predict:

```text
product(lambda(p_i^a_i)) / lcm(lambda(p_i^a_i))
```

That is the rigorous path from the Origin language to standard number theory.
