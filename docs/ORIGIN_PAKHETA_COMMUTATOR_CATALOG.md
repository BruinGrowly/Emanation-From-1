# Origin-Pakheta Commutator Catalog: Lemmas C1-C12

**Status:** Proven lemma appendix for the v1 commutator catalog
**Instrument:** `experiments/origin_pakheta_commutator_catalog.py`
**Generated catalog:** [reports/ORIGIN_PAKHETA_COMMUTATOR_CATALOG.md](../reports/ORIGIN_PAKHETA_COMMUTATOR_CATALOG.md)

## Purpose

Theorems 1-15 ([ORIGIN_PAKHETA_CALCULUS_PROOFS.md](ORIGIN_PAKHETA_CALCULUS_PROOFS.md))
characterize eleven operator pairs individually. The catalog turns the path
commutator $\Delta(A, B; n) = A(B(n)) / B(A(n))$ into a survey instrument over
a fifteen-operator roster (105 unordered pairs), classifying every commutation
locus $\{n : A(B(n)) = B(A(n))\}$ and emitting the unproven structured rows as
a ranked theorem-candidate queue.

This appendix proves the loci that the queue has surfaced so far. Lemmas
C1-C7 were written alongside the instrument; **Lemmas C8-C12 were read
directly off the first catalog run** — the top of the candidate queue turned
out to be provable on sight, which is the working pattern the catalog is
meant to sustain: scan, rank, prove, re-annotate, repeat.

Notation: $v_p(n)$ is the exponent of $p$ in $n$, $\mathrm{spf}/\mathrm{gpf}$
the smallest/greatest prime factor, $\omega(n)$ the distinct-prime count,
$Q(n) = n/\mathrm{rad}(n)$ the powerful quotient, and $R_p, G_p$ the selected
return and gather operators of the v0 calculus.

## Organizing Remark: the Compression Row

For *any* arithmetic operator $F$, unfolding definitions gives

$$\Delta(C, F; n) = \frac{\mathrm{rad}(F(n))}{F(\mathrm{rad}(n))},$$

so the commutation locus of the pair $(C, F)$ is always
$\{n : \mathrm{rad}(F(n)) = F(\mathrm{rad}(n))\}$. Theorems 7, 9, 10, 11, 13
and Lemma C5 are instances; the open $C$-row entries of the catalog ($C/S$,
$C/P$, $C/R_{\max}$) reduce to characterizing this set for each $F$.

## Lemmas

### Lemma C1 (Gathers commute)
For primes $p, q$: $G_p(G_q(n)) = pqn = G_q(G_p(n))$. $\blacksquare$

### Lemma C2 (Selected returns commute)
For primes $p \ne q$: $R_q$ does not change $v_p$, and $R_p$ does not change
$v_q$, so both orders produce $n / (p^{[v_p(n) \ge 1]} q^{[v_q(n) \ge 1]})$.
The case $p = q$ is trivial. $\blacksquare$

### Lemma C3 (Cross return-gather commutes)
For primes $p \ne q$: $G_q$ does not change $v_p$, and $R_p$ does not change
$v_q$, so both orders produce $qn / p^{[v_p(n) \ge 1]}$. $\blacksquare$

### Lemma C4 (Same-prime return-gather locus)
$R_p(G_p(n)) = n$ always. $G_p(R_p(n)) = n$ if $p \mid n$ and $pn$ otherwise.
Hence $\Delta(R_p, G_p; n) = 1$ if $p \mid n$ and $1/p$ otherwise:
**$R_p$ and $G_p$ commute exactly when $p \mid n$.** $\blacksquare$

### Lemma C5 (Compression-powerful quotient locus)
$C(Q(n)) = \mathrm{rad}(n/\mathrm{rad}(n))$, while
$Q(C(n)) = \mathrm{rad}(n)/\mathrm{rad}(\mathrm{rad}(n)) = 1$. Thus
$\Delta(C, Q; n) = \mathrm{rad}(n/\mathrm{rad}(n))$, which equals $1$ exactly
when $n$ is squarefree. The commuting density therefore tends to
$6/\pi^2 \approx 0.6079$, a built-in calibration value for the scan.
$\blacksquare$

### Lemma C6 (Gather-powerful quotient locus)
If $p \mid n$: $Q(G_p(n)) = pn/\mathrm{rad}(n) = G_p(Q(n))$. If $p \nmid n$:
$Q(G_p(n)) = pn/(p \cdot \mathrm{rad}(n)) = Q(n)$ while $G_p(Q(n)) = pQ(n)$.
**$G_p$ and $Q$ commute exactly when $p \mid n$.** $\blacksquare$

### Lemma C7 (Extremal returns commute)
If $\omega(n) \le 1$ both operators divide by the same prime (or fix $1$).
If $\omega(n) \ge 2$, then $\mathrm{spf}(n) \ne \mathrm{gpf}(n)$; removing one
layer of the least prime cannot change the greatest prime and vice versa, so
both orders produce $n/(\mathrm{spf}(n) \cdot \mathrm{gpf}(n))$.
$\blacksquare$

### Lemma C8 (Selected returns commute with the powerful quotient)
Let $a = v_p(n)$. If $a = 0$ both sides fix the $p$-exponent. If $a = 1$:
$Q(R_p(n)) = (n/p)/(\mathrm{rad}(n)/p) = Q(n)$, and $v_p(Q(n)) = 0$ so
$R_p(Q(n)) = Q(n)$. If $a \ge 2$: $\mathrm{rad}(R_p(n)) = \mathrm{rad}(n)$ so
$Q(R_p(n)) = Q(n)/p$, and $v_p(Q(n)) = a - 1 \ge 1$ so $R_p(Q(n)) = Q(n)/p$.
**$R_p$ and $Q$ commute for every prime $p$ and every $n$.** $\blacksquare$

### Lemma C9 (Greatest-prime return vs selected return)
Let $q = \mathrm{gpf}(n)$. If $p < q$, the two removals target different
primes and commute as in Lemma C2. If $p = q$ and $v_p(n) \ge 2$, the
greatest prime survives one removal, and both orders give $n/p^2$. If
$p = q$, $v_p(n) = 1$, and $\omega(n) \ge 2$: $R_p(R_{\max}(n)) = n/p$
(the prime is already gone), while $R_{\max}(R_p(n))$ removes a second,
smaller prime — they differ. If $p > q$, $R_p$ fixes $n$ and both orders
give $n/q$. Hence **$R_p$ and $R_{\max}$ commute exactly when not
($p = \mathrm{gpf}(n)$, $v_p(n) = 1$, $\omega(n) \ge 2$)**. For $p = 2$ the
failing case forces $n = 2^a$, which has $\omega = 1$, so $R_2$ and
$R_{\max}$ always commute. $\blacksquare$

### Lemma C10 (Greatest-prime return vs gather)
If $p \le \mathrm{gpf}(n)$, gathering $p$ does not change the greatest prime,
so both orders give $pn/\mathrm{gpf}(n)$. If $p > \mathrm{gpf}(n)$, then
$\mathrm{gpf}(G_p(n)) = p$ and $R_{\max}(G_p(n)) = n$, while
$G_p(R_{\max}(n)) = pn/\mathrm{gpf}(n) \ne n$. Hence **$G_p$ and $R_{\max}$
commute exactly when $p \le \mathrm{gpf}(n)$**; for $p = 2$ this is every
$n \ge 2$. $\blacksquare$

### Lemma C11 (Gathers never commute with sigma or the neighborhoods)
For $n \ge 2$ and any prime $p$:
* **Sigma:** with $a = v_p(n)$ and $n = p^a m$,
  $\sigma(p^{a+1}) = p\,\sigma(p^a) + 1$, so
  $\sigma(pn) = \sigma(m)(p\,\sigma(p^a) + 1) = p\,\sigma(n) + \sigma(m)
  > p\,\sigma(n) = G_p(\sigma(n))$.
* **$N_-$:** if $p \mid n$ then $N_-(pn) = N_-(n) < pN_-(n)$; otherwise
  $N_-(pn) = (p-1)N_-(n) < pN_-(n)$.
* **$N_+$:** if $p \mid n$ then $N_+(pn) = N_+(n) \ne pN_+(n)$; otherwise
  $N_+(pn) = (p+1)N_+(n) \ne pN_+(n)$.

In every case the two paths differ, so the commutation loci are empty.
$\blacksquare$

### Lemma C12 (Gather vs divisor branching)
With $a = v_p(n)$: $B(G_p(n)) = d(n) \cdot \frac{a+2}{a+1}$ while
$G_p(B(n)) = p \cdot d(n)$. Equality requires $a + 2 = p(a + 1)$, i.e.
$a(p-1) = 2 - p$. For $p = 2$ this forces $a = 0$; for $p \ge 3$ it has no
non-negative solution. Hence **$G_2$ and $B$ commute exactly when $n$ is
odd, and $G_p$ and $B$ never commute for $p \ge 3$.** $\blacksquare$

## Verification Status

Every locus above is checked empirically to $n = 20000$ with zero mismatches,
and the test suite pins samples of each (including the Corollary 7.1 locus
recovery $\{p^{2^m - 1}\}$ as a catalog calibration). The catalog report
annotates all 40 proven rows; the remaining 65 pairs form the open queue.
