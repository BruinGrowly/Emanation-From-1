"""Generate the first Origin Frame experiment report."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.conjectures import (  # noqa: E402
    gilbreath_check,
    gilbreath_row_metrics,
    goldbach_pairs,
    goldbach_scan,
    twin_prime_pairs,
)
from emanation_from_1.number_theory import prime_gaps, sieve  # noqa: E402
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402


GILBREATH_PRIME_COUNT = 1024
GOLDBACH_LIMIT = 10_000
TWIN_LIMIT = 10_000
FACTOR_SAMPLE_LIMIT = 32


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    """Render a simple Markdown table."""
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def factor_profile_section(factor_sample_limit: int) -> str:
    rows: list[list[object]] = []
    for n in range(1, factor_sample_limit + 1):
        profile = origin_profile(n)
        factors = "1" if not profile.factors else " * ".join(map(str, profile.factors))
        path = " -> ".join(map(str, profile.return_path))
        rows.append(
            [
                n,
                factors,
                profile.emanation_depth,
                profile.distinct_factor_depth,
                profile.divisor_count,
                path,
            ]
        )

    return "\n".join(
        [
            "## 1. Factor Profiles",
            "",
            "The first pass treats factorization as a return path to `1`.",
            "",
            markdown_table(
                [
                    "n",
                    "factor layers",
                    "depth",
                    "distinct depth",
                    "divisors",
                    "return path",
                ],
                rows,
            ),
        ]
    )


def gilbreath_section(prime_count: int) -> str:
    check = gilbreath_check(prime_count)
    metric_rows = []
    for metric in gilbreath_row_metrics(prime_count, max_rows=16):
        metric_rows.append(
            [
                metric["row"],
                metric["length"],
                metric["first"],
                metric["min"],
                metric["max"],
                metric["ones"],
                metric["zeros"],
                f"{metric['mean']:.3f}",
            ]
        )

    verdict = "verified for this finite scan" if check.verified else "failure found"
    failures = "none" if check.verified else str(check.failures)

    return "\n".join(
        [
            "## 2. Gilbreath Differentiation",
            "",
            f"Prime count: `{check.prime_count}`",
            f"Difference rows checked: `{check.rows_checked}`",
            f"Finite verdict: **{verdict}**",
            f"Failures: `{failures}`",
            "",
            markdown_table(
                ["row", "length", "first", "min", "max", "ones", "zeros", "mean"],
                metric_rows,
            ),
            "",
            "Origin-frame note: rows `1..n` returning first-column `1` are a concrete recurrence of the origin value under repeated prime-stream differentiation.",
        ]
    )


def goldbach_section(limit: int) -> str:
    scan = goldbach_scan(limit)
    sample_evens = [n for n in (4, 10, 28, 100) if n <= limit]
    for candidate in (1_000, 10_000, limit):
        if candidate <= limit and candidate % 2 == 0 and candidate not in sample_evens:
            sample_evens.append(candidate)

    primes = sieve(limit)
    rows = []
    for n in sample_evens:
        pairs = goldbach_pairs(n, primes)
        preview = ", ".join(f"{a}+{b}" for a, b in pairs[:5])
        if len(pairs) > 5:
            preview += ", ..."
        rows.append([n, len(pairs), preview])

    failures = scan["failures"]
    failure_text = "none" if not failures else str(failures)

    return "\n".join(
        [
            "## 3. Goldbach Pairing",
            "",
            f"Limit: `{scan['limit']}`",
            f"Evens checked: `{scan['evens_checked']}`",
            f"Failures: `{failure_text}`",
            f"Richest even in scan: `{scan['richest_even']}` with `{scan['richest_pair_count']}` pairs",
            "",
            markdown_table(["even n", "pair count", "first witnesses"], rows),
        ]
    )


def twins_and_gaps_section(limit: int) -> str:
    twins = twin_prime_pairs(limit)
    gaps = prime_gaps(limit)
    max_gap = max(gaps) if gaps else 0
    prime_count = len(sieve(limit))
    twin_preview = ", ".join(f"({a}, {b})" for a, b in twins[:12])

    return "\n".join(
        [
            "## 4. Twin Prime Bridges And Prime Gaps",
            "",
            f"Limit: `{limit}`",
            f"Prime count: `{prime_count}`",
            f"Twin-pair count: `{len(twins)}`",
            f"Largest prime gap in range: `{max_gap}`",
            f"First twin pairs: {twin_preview}",
            "",
            "Origin-frame note: twin primes keep recurring at the minimal bridge distance `2`, even while ordinary prime gaps widen irregularly.",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gilbreath-primes", type=int, default=GILBREATH_PRIME_COUNT)
    parser.add_argument("--goldbach-limit", type=int, default=GOLDBACH_LIMIT)
    parser.add_argument("--twin-limit", type=int, default=TWIN_LIMIT)
    parser.add_argument("--factor-limit", type=int, default=FACTOR_SAMPLE_LIMIT)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "INITIAL_EXPERIMENTS.md",
        help="Markdown report path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Initial Emanation Experiments",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/initial_scan.py`.",
            "Finite scans are not proofs; they are instrumentation for the Origin Frame.",
            factor_profile_section(args.factor_limit),
            gilbreath_section(args.gilbreath_primes),
            goldbach_section(args.goldbach_limit),
            twins_and_gaps_section(args.twin_limit),
            "## Next Measurements",
            "\n".join(
                [
                    "- Export long Gilbreath row metrics to CSV.",
                    "- Compare Goldbach witness counts against factor depth of each even number.",
                    "- Track whether high divisor branching predicts richer prime-pair decompositions.",
                    "- Plot row-wise density of `1` values in Gilbreath rows.",
                ]
            ),
        ]
    )

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
