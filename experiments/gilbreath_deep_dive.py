"""Deeper finite diagnostics for Gilbreath-style return behavior."""

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
    boundary_return_check,
    consecutive_odd_sequence,
    difference_row_summaries,
    difference_rows,
    first_certificate_row,
    odd_arithmetic_after_boundary,
    random_odd_small_gap_sequence,
)
from emanation_from_1.number_theory import first_n_primes  # noqa: E402


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def analyze_sequence(name: str, sequence: list[int], tracked_rows: int) -> dict[str, object]:
    rows = difference_rows(sequence)
    summaries = difference_row_summaries(rows)
    boundary = boundary_return_check(sequence)
    certificate = first_certificate_row(rows)
    certified_lock = certificate if boundary.verified and certificate is not None else None
    first_max_le_2 = next(
        (summary.row_index for summary in summaries[1:] if summary.max_value <= 2),
        None,
    )
    first_zero_defects = next(
        (
            summary.row_index
            for summary in summaries[1:]
            if summary.certificate_defects == 0
        ),
        None,
    )

    return {
        "name": name,
        "length": len(sequence),
        "boundary_pass": boundary.verified,
        "first_failure": boundary.first_failure,
        "certificate_row": certificate,
        "certified_lock_row": certified_lock,
        "first_max_le_2": first_max_le_2,
        "first_zero_defects": first_zero_defects,
        "rows": rows,
        "summaries": summaries[:tracked_rows],
    }


def deterministic_analyses(length: int, tracked_rows: int) -> list[dict[str, object]]:
    analyses = [
        analyze_sequence("prime prefix", first_n_primes(length), tracked_rows),
        analyze_sequence(
            "consecutive odd control",
            consecutive_odd_sequence(length),
            tracked_rows,
        ),
    ]

    for gap in (4, 6, 8, 10, 12):
        analyses.append(
            analyze_sequence(
                f"fixed odd gap {gap}",
                odd_arithmetic_after_boundary(length, gap=gap),
                tracked_rows,
            )
        )

    return analyses


def seeded_random_analyses(args: argparse.Namespace) -> list[dict[str, object]]:
    return [
        analyze_sequence(
            f"random seed {args.seed + offset}",
            random_odd_small_gap_sequence(
                args.length,
                max_gap_units=args.random_max_gap_units,
                seed=args.seed + offset,
            ),
            args.tracked_rows,
        )
        for offset in range(args.random_trials)
    ]


def summary_table(analyses: list[dict[str, object]]) -> str:
    rows: list[list[object]] = []
    for analysis in analyses:
        rows.append(
            [
                analysis["name"],
                analysis["length"],
                "pass" if analysis["boundary_pass"] else "fail",
                "none" if analysis["first_failure"] is None else analysis["first_failure"],
                "none" if analysis["certificate_row"] is None else analysis["certificate_row"],
                "none" if analysis["certified_lock_row"] is None else analysis["certified_lock_row"],
                "none" if analysis["first_max_le_2"] is None else analysis["first_max_le_2"],
            ]
        )

    return markdown_table(
        [
            "sequence",
            "length",
            "boundary",
            "first failure",
            "certificate row",
            "certified lock row",
            "first max<=2 row",
        ],
        rows,
    )


def row_summary_table(analysis: dict[str, object]) -> str:
    rows: list[list[object]] = []
    for summary in analysis["summaries"]:
        rows.append(
            [
                summary.row_index,
                summary.length,
                summary.first,
                summary.max_value,
                summary.odd_count,
                summary.certificate_defects,
                "yes" if summary.is_certificate else "no",
            ]
        )

    return markdown_table(
        [
            "row",
            "length",
            "first",
            "max",
            "odd_count",
            "certificate_defects",
            "certificate",
        ],
        rows,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=256)
    parser.add_argument("--tracked-rows", type=int, default=24)
    parser.add_argument("--random-trials", type=int, default=24)
    parser.add_argument("--random-max-gap-units", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "GILBREATH_DEEP_DIVE.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.length < 2:
        raise ValueError("length must be >= 2")

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    deterministic = deterministic_analyses(args.length, args.tracked_rows)
    random_analyses = seeded_random_analyses(args)
    random_pass_count = sum(1 for analysis in random_analyses if analysis["boundary_pass"])
    random_certificate_count = sum(
        1 for analysis in random_analyses if analysis["certificate_row"] is not None
    )
    random_certified_lock_count = sum(
        1 for analysis in random_analyses if analysis["certified_lock_row"] is not None
    )

    prime_analysis = deterministic[0]
    odd_control_analysis = deterministic[1]

    report = "\n\n".join(
        [
            "# Gilbreath Deep Dive",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/gilbreath_deep_dive.py`.",
            "A certificate row begins with `1` and has only `0` or `2` after the first value. Once a finite triangle reaches this shape, every later first-column value in that finite triangle remains `1`.",
            "A certified lock row is stricter: it is a certificate row reached without any earlier first-column failure.",
            "These are finite diagnostics, not an infinite proof.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["length", args.length],
                    ["tracked_rows", args.tracked_rows],
                    ["random_trials", args.random_trials],
                    ["random_max_gap_units", args.random_max_gap_units],
                    ["seed_start", args.seed],
                ],
            ),
            "## Deterministic Sequence Summary",
            summary_table(deterministic),
            "## Seeded Random Summary",
            f"Boundary passes: `{random_pass_count}` of `{args.random_trials}`.",
            f"Certificate rows found: `{random_certificate_count}` of `{args.random_trials}`.",
            f"Certified lock rows found: `{random_certified_lock_count}` of `{args.random_trials}`.",
            summary_table(random_analyses),
            "## Prime Prefix Row Diagnostics",
            row_summary_table(prime_analysis),
            "## Consecutive Odd Control Row Diagnostics",
            row_summary_table(odd_control_analysis),
            "## Local Interpretation",
            "The certificate-row metric is stricter than first-column success alone.",
            "A later certificate row does not repair an earlier first-column failure; the meaningful finite diagnostic is the certified lock row.",
            "If prime prefixes reach certificate rows while many plausible controls do not, that gives a sharper phenomenon to study.",
            "If simple controls reach certificates earlier than primes, the result is constraining: the boundary-return pattern is not distinctively prime-origin evidence by itself.",
            "A future supportive result would need a pre-declared Origin metric that predicts which controls should pass, fail, or reach certificates quickly.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
