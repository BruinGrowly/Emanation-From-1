"""Systematic commutator catalog for the Origin-Pakheta operator family.

Theorems 1-15 treat eleven operator pairs individually. This experiment
turns the path commutator Delta(A, B; n) = A(B(n)) / B(A(n)) into a
survey instrument: every unordered pair from a fifteen-operator roster
is scanned over 2..limit, and each pair's commutation locus
{n : A(B(n)) = B(A(n))} is classified by density and growth.

The roster covers the v0 operators plus four standard extensions
(greatest-prime return, powerful quotient, divisor sigma, Dedekind psi).
Pairs whose loci are already characterized by a proof are annotated with
the theorem or catalog-lemma reference; the remaining structured loci
are emitted as an explicit theorem-candidate queue, which is the point
of the catalog: the open mathematics lives in the unproven rows.

Operators are evaluated through a factorization cache so composed values
(e.g. lambda(sigma(n))) stay cheap; tests verify the cached evaluators
agree with the canonical context functions in src.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import lcm
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import factor_counter  # noqa: E402


_FACTOR_CACHE: dict[int, Counter[int]] = {}


def cached_factor_counter(n: int) -> Counter[int]:
    cached = _FACTOR_CACHE.get(n)
    if cached is None:
        cached = factor_counter(n)
        _FACTOR_CACHE[n] = cached
    return cached


def op_compression(n: int) -> int:
    product = 1
    for prime in cached_factor_counter(n):
        product *= prime
    return product


def op_return_min(n: int) -> int:
    if n == 1:
        return 1
    return n // min(cached_factor_counter(n))


def op_return_max(n: int) -> int:
    if n == 1:
        return 1
    return n // max(cached_factor_counter(n))


def op_return_2(n: int) -> int:
    return n // 2 if n % 2 == 0 else n


def op_return_3(n: int) -> int:
    return n // 3 if n % 3 == 0 else n


def op_gather_2(n: int) -> int:
    return 2 * n


def op_gather_3(n: int) -> int:
    return 3 * n


def op_powerful_quotient(n: int) -> int:
    return n // op_compression(n)


def op_divisor_count(n: int) -> int:
    total = 1
    for exponent in cached_factor_counter(n).values():
        total *= exponent + 1
    return total


def op_euler_totient(n: int) -> int:
    total = 1
    for prime, exponent in cached_factor_counter(n).items():
        total *= prime ** (exponent - 1) * (prime - 1)
    return total


def op_carmichael_lambda(n: int) -> int:
    result = 1
    for prime, exponent in cached_factor_counter(n).items():
        if prime == 2 and exponent >= 3:
            component = 2 ** (exponent - 2)
        else:
            component = prime ** (exponent - 1) * (prime - 1)
        result = lcm(result, component)
    return result


def op_divisor_sigma(n: int) -> int:
    total = 1
    for prime, exponent in cached_factor_counter(n).items():
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def op_dedekind_psi(n: int) -> int:
    total = 1
    for prime, exponent in cached_factor_counter(n).items():
        total *= prime ** (exponent - 1) * (prime + 1)
    return total


def op_prime_minus(n: int) -> int:
    product = 1
    for prime in cached_factor_counter(n):
        product *= prime - 1
    return product


def op_prime_plus(n: int) -> int:
    product = 1
    for prime in cached_factor_counter(n):
        product *= prime + 1
    return product


OPERATORS: list[tuple[str, str]] = [
    ("C", "rad(n)"),
    ("R_min", "n / spf(n)"),
    ("R_max", "n / gpf(n)"),
    ("R_2", "n / 2 if 2 | n"),
    ("R_3", "n / 3 if 3 | n"),
    ("G_2", "2n"),
    ("G_3", "3n"),
    ("Q", "n / rad(n)"),
    ("B", "d(n)"),
    ("T", "phi(n)"),
    ("M", "lambda(n)"),
    ("S", "sigma(n)"),
    ("P", "psi(n)"),
    ("N-", "prod(p-1)"),
    ("N+", "prod(p+1)"),
]

OPERATOR_FUNCTIONS = {
    "C": op_compression,
    "R_min": op_return_min,
    "R_max": op_return_max,
    "R_2": op_return_2,
    "R_3": op_return_3,
    "G_2": op_gather_2,
    "G_3": op_gather_3,
    "Q": op_powerful_quotient,
    "B": op_divisor_count,
    "T": op_euler_totient,
    "M": op_carmichael_lambda,
    "S": op_divisor_sigma,
    "P": op_dedekind_psi,
    "N-": op_prime_minus,
    "N+": op_prime_plus,
}

PROVEN_STATUS: dict[frozenset[str], str] = {
    frozenset({"C", "R_min"}): "Cor 4.1 (locus: spf exponent 1)",
    frozenset({"C", "R_2"}): "Thm 4 (locus: v_2 <= 1)",
    frozenset({"C", "R_3"}): "Thm 4 (locus: v_3 <= 1)",
    frozenset({"C", "G_2"}): "Thm 6 (locus: 2 ∤ n)",
    frozenset({"C", "G_3"}): "Thm 6 (locus: 3 ∤ n)",
    frozenset({"C", "B"}): "Thm 7 + Cor 7.1 (locus: p^(2^m - 1))",
    frozenset({"R_2", "B"}): "Thm 8 (exact formula)",
    frozenset({"R_3", "B"}): "Thm 8 (exact formula)",
    frozenset({"C", "M"}): "Thm 9 + Cor 9.1",
    frozenset({"C", "T"}): "Thm 10 (exact formula)",
    frozenset({"C", "N-"}): "Thm 11 (locus: prod(p-1) squarefree)",
    frozenset({"R_2", "N-"}): "Thm 12 (exact formula)",
    frozenset({"R_3", "N-"}): "Thm 12 (exact formula)",
    frozenset({"C", "N+"}): "Thm 13 (locus: prod(p+1) squarefree)",
    frozenset({"R_2", "N+"}): "Thm 14 (exact formula)",
    frozenset({"R_3", "N+"}): "Thm 14 (exact formula)",
    frozenset({"G_2", "G_3"}): "Lemma C1 (always)",
    frozenset({"R_2", "R_3"}): "Lemma C2 (always)",
    frozenset({"R_2", "G_3"}): "Lemma C3 (always)",
    frozenset({"R_3", "G_2"}): "Lemma C3 (always)",
    frozenset({"R_2", "G_2"}): "Lemma C4 (locus: 2 | n)",
    frozenset({"R_3", "G_3"}): "Lemma C4 (locus: 3 | n)",
    frozenset({"C", "Q"}): "Lemma C5 (locus: n squarefree)",
    frozenset({"G_2", "Q"}): "Lemma C6 (locus: 2 | n)",
    frozenset({"G_3", "Q"}): "Lemma C6 (locus: 3 | n)",
    frozenset({"R_min", "R_max"}): "Lemma C7 (always)",
    frozenset({"R_2", "Q"}): "Lemma C8 (always)",
    frozenset({"R_3", "Q"}): "Lemma C8 (always)",
    frozenset({"R_max", "R_2"}): "Lemma C9 (always for p = 2)",
    frozenset({"R_max", "R_3"}): "Lemma C9 (locus: not (gpf = 3, v_3 = 1, omega >= 2))",
    frozenset({"R_max", "G_2"}): "Lemma C10 (always for p = 2)",
    frozenset({"R_max", "G_3"}): "Lemma C10 (locus: gpf(n) >= 3)",
    frozenset({"G_2", "S"}): "Lemma C11 (never)",
    frozenset({"G_3", "S"}): "Lemma C11 (never)",
    frozenset({"G_2", "N-"}): "Lemma C11 (never)",
    frozenset({"G_3", "N-"}): "Lemma C11 (never)",
    frozenset({"G_2", "N+"}): "Lemma C11 (never)",
    frozenset({"G_3", "N+"}): "Lemma C11 (never)",
    frozenset({"G_2", "B"}): "Lemma C12 (locus: 2 ∤ n)",
    frozenset({"G_3", "B"}): "Lemma C12 (never for p >= 3)",
}


@dataclass
class PairScan:
    """Commutation census for one unordered operator pair."""

    left: str
    right: str
    limit: int
    commute_count: int = 0
    first_commuting: int | None = None
    last_commuting: int | None = None
    first_noncommuting: int | None = None
    checkpoint_counts: dict[int, int] = field(default_factory=dict)

    @property
    def density(self) -> float:
        return self.commute_count / (self.limit - 1)

    @property
    def status(self) -> str:
        return PROVEN_STATUS.get(frozenset({self.left, self.right}), "empirical")

    @property
    def classification(self) -> str:
        if self.first_noncommuting is None:
            return "always"
        if self.commute_count == 0:
            return "never"
        assert self.last_commuting is not None
        if self.last_commuting <= self.limit // 2:
            return "finite?"
        if self.density >= 0.25:
            return "dense"
        return "sparse"


def catalog_pairs() -> list[tuple[str, str]]:
    names = [name for name, _ in OPERATORS]
    return [
        (names[i], names[j])
        for i in range(len(names))
        for j in range(i + 1, len(names))
    ]


def scan_pair(left: str, right: str, limit: int) -> PairScan:
    if limit < 2:
        raise ValueError("limit must be >= 2")
    left_op = OPERATOR_FUNCTIONS[left]
    right_op = OPERATOR_FUNCTIONS[right]
    checkpoints = sorted({limit // 4, limit // 2, (3 * limit) // 4, limit} - {0, 1})
    scan = PairScan(left=left, right=right, limit=limit)
    checkpoint_index = 0
    for n in range(2, limit + 1):
        if left_op(right_op(n)) == right_op(left_op(n)):
            scan.commute_count += 1
            if scan.first_commuting is None:
                scan.first_commuting = n
            scan.last_commuting = n
        elif scan.first_noncommuting is None:
            scan.first_noncommuting = n
        while (
            checkpoint_index < len(checkpoints)
            and n == checkpoints[checkpoint_index]
        ):
            scan.checkpoint_counts[n] = scan.commute_count
            checkpoint_index += 1
    return scan


def run_catalog(limit: int) -> list[PairScan]:
    return [scan_pair(left, right, limit) for left, right in catalog_pairs()]


def theorem_candidates(scans: list[PairScan]) -> list[PairScan]:
    """Return unproven pairs with structured loci, ordered by sparsity.

    A locus is a theorem candidate when it is neither everything nor
    nothing: 'always' rows need a general proof, and sparse/finite rows
    have characterizable exceptional sets. Dense unproven rows are listed
    after sparse ones because their complements are usually the cleaner
    object.
    """
    order = {"always": 0, "never": 1, "finite?": 2, "sparse": 3, "dense": 4}
    unproven = [scan for scan in scans if scan.status == "empirical"]
    return sorted(
        unproven,
        key=lambda scan: (order[scan.classification], scan.density),
    )


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def scan_row(scan: PairScan) -> list[object]:
    trend = " -> ".join(
        str(scan.checkpoint_counts[key]) for key in sorted(scan.checkpoint_counts)
    )
    return [
        f"{scan.left} / {scan.right}",
        scan.classification,
        scan.status,
        scan.commute_count,
        f"{scan.density:.4f}",
        scan.first_commuting if scan.first_commuting is not None else "-",
        scan.last_commuting if scan.last_commuting is not None else "-",
        scan.first_noncommuting if scan.first_noncommuting is not None else "-",
        trend,
    ]


def write_report(report_path: Path, scans: list[PairScan], limit: int) -> None:
    classifications = Counter(scan.classification for scan in scans)
    proven = sum(1 for scan in scans if scan.status != "empirical")
    candidates = theorem_candidates(scans)
    headers = [
        "pair",
        "class",
        "status",
        "commuting n",
        "density",
        "first",
        "last",
        "first violation",
        "count trend",
    ]
    order = {"always": 0, "finite?": 1, "never": 2, "sparse": 3, "dense": 4}
    sorted_scans = sorted(
        scans, key=lambda scan: (order[scan.classification], scan.density)
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Origin-Pakheta Commutator Catalog (v1)",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                "**Script:** `experiments/origin_pakheta_commutator_catalog.py`",
                f"**Range:** `2..{limit}`",
                f"**Pairs:** `{len(scans)}` unordered pairs over `{len(OPERATORS)}` operators",
                "",
                "## Operator Roster",
                "",
                markdown_table(
                    ["symbol", "definition"],
                    [[name, f"`{definition}`"] for name, definition in OPERATORS],
                ),
                "",
                "## Summary",
                "",
                markdown_table(
                    ["classification", "pairs"],
                    [[key, classifications.get(key, 0)] for key in order],
                )
                + "\n",
                f"Proven rows: `{proven}/{len(scans)}` "
                f"(Theorems 4-14 and Catalog Lemmas C1-C7); the remaining "
                f"`{len(scans) - proven}` are empirical.",
                "",
                "## Full Catalog",
                "",
                "`class` heuristics: `always` = no violation found; `finite?` = no",
                f"commuting n found in the upper half of the range; `dense` = locus",
                "density >= 0.25; `sparse` = the rest. `count trend` shows the",
                "commuting count at quarter checkpoints of the range.",
                "",
                markdown_table(headers, [scan_row(scan) for scan in sorted_scans]),
                "",
                "## Theorem Candidate Queue",
                "",
                "Unproven pairs ordered by how structured the locus looks (always,",
                "then finite-looking, then sparse, then dense). Each row is a",
                "candidate for the next exact identity or locus characterization.",
                "",
                markdown_table(headers, [scan_row(scan) for scan in candidates]),
                "",
                "## Interpretation",
                "",
                "The catalog is an instrument, not evidence: it maps where path",
                "order is and is not remembered across the operator family, and it",
                "turns 'find a new theorem' into a ranked work queue. Proven rows",
                "double as regression anchors -- their loci must match the stated",
                "characterizations exactly, and the test suite checks samples of",
                "each.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_PAKHETA_COMMUTATOR_CATALOG.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scans = run_catalog(args.limit)
    write_report(args.report, scans, args.limit)
    classifications = Counter(scan.classification for scan in scans)
    print(f"pairs: {len(scans)}")
    for key in ("always", "finite?", "never", "sparse", "dense"):
        print(f"{key}: {classifications.get(key, 0)}")
    candidates = theorem_candidates(scans)
    print(f"theorem candidates: {len(candidates)}")
    print(f"report: {args.report}")


if __name__ == "__main__":
    main()
