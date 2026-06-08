"""Map integers by direct emanation structure from 1."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import mean  # noqa: E402


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def origin_rows(limit: int) -> list[dict[str, object]]:
    """Return direct Origin profiles for integers `1..limit`."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    rows: list[dict[str, object]] = []
    for n in range(1, limit + 1):
        profile = origin_profile(n)
        factor_set = set(profile.factors)
        depth = profile.emanation_depth
        rows.append(
            {
                "n": n,
                "factors": profile.factors,
                "depth": depth,
                "distinct_depth": profile.distinct_factor_depth,
                "divisor_count": profile.divisor_count,
                "radical_ratio": profile.radical / n,
                "phi_attenuation": profile.phi_attenuation,
                "return_path": profile.return_path,
                "is_origin": n == 1,
                "is_prime_layer": depth == 1,
                "is_layered": depth > 1,
                "is_squarefree": len(profile.factors) == len(factor_set),
                "is_prime_power": depth > 0 and len(factor_set) == 1,
            }
        )
    return rows


def shell_summaries(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Group rows by emanation depth."""
    shells: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        shells[int(row["depth"])].append(row)

    summaries: list[dict[str, object]] = []
    for depth in sorted(shells):
        shell = shells[depth]
        summaries.append(
            {
                "depth": depth,
                "count": len(shell),
                "first_n": min(int(row["n"]) for row in shell),
                "last_n": max(int(row["n"]) for row in shell),
                "prime_layer_count": sum(1 for row in shell if row["is_prime_layer"]),
                "layered_count": sum(1 for row in shell if row["is_layered"]),
                "squarefree_count": sum(1 for row in shell if row["is_squarefree"]),
                "prime_power_count": sum(1 for row in shell if row["is_prime_power"]),
                "avg_divisor_count": mean(
                    [float(row["divisor_count"]) for row in shell]
                ),
                "avg_radical_ratio": mean(
                    [float(row["radical_ratio"]) for row in shell]
                ),
            }
        )
    return summaries


def first_depth_occurrences(rows: list[dict[str, object]]) -> list[dict[str, int]]:
    """Return the first integer observed at each emanation depth."""
    firsts: dict[int, int] = {}
    for row in rows:
        depth = int(row["depth"])
        firsts.setdefault(depth, int(row["n"]))

    return [
        {
            "depth": depth,
            "first_n": first_n,
            "minimal_binary_stack": 2**depth,
            "matches_binary_stack": int(first_n == 2**depth),
        }
        for depth, first_n in sorted(firsts.items())
    ]


def shell_summary_table(rows: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            summary["depth"],
            summary["count"],
            summary["first_n"],
            summary["last_n"],
            summary["prime_layer_count"],
            summary["layered_count"],
            summary["squarefree_count"],
            summary["prime_power_count"],
            f"{summary['avg_divisor_count']:.2f}",
            f"{summary['avg_radical_ratio']:.3f}",
        ]
        for summary in shell_summaries(rows)
    ]


def first_depth_table(rows: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            item["depth"],
            item["first_n"],
            item["minimal_binary_stack"],
            "yes" if item["matches_binary_stack"] else "no",
        ]
        for item in first_depth_occurrences(rows)
    ]


def branching_hotspots(rows: list[dict[str, object]], count: int) -> list[list[object]]:
    ranked = sorted(
        rows,
        key=lambda row: (
            int(row["divisor_count"]),
            int(row["depth"]),
            int(row["n"]),
        ),
        reverse=True,
    )
    return [
        [
            row["n"],
            row["depth"],
            row["distinct_depth"],
            row["divisor_count"],
            f"{row['radical_ratio']:.3f}",
            " * ".join(map(str, row["factors"])) or "1",
            " -> ".join(map(str, row["return_path"])),
        ]
        for row in ranked[:count]
    ]


def sample_path_table(rows: list[dict[str, object]], samples: list[int]) -> list[list[object]]:
    by_n = {int(row["n"]): row for row in rows}
    table: list[list[object]] = []
    for n in samples:
        row = by_n.get(n)
        if row is None:
            continue
        table.append(
            [
                row["n"],
                row["depth"],
                row["distinct_depth"],
                row["divisor_count"],
                " * ".join(map(str, row["factors"])) or "1",
                " -> ".join(map(str, row["return_path"])),
            ]
        )
    return table


def parse_csv_ints(value: str, label: str) -> list[int]:
    values = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not values or any(item < 1 for item in values):
        raise ValueError(f"{label} must be a comma-separated list of positive integers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument("--hotspots", type=int, default=12)
    parser.add_argument("--samples", default="1,2,3,4,6,8,12,18,24,30,60,120")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_STRUCTURE_SCAN.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.limit < 1:
        raise ValueError("limit must be >= 1")
    if args.hotspots < 1:
        raise ValueError("hotspots must be >= 1")

    rows = origin_rows(args.limit)
    samples = parse_csv_ints(args.samples, "samples")
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Structure Scan",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_structure_scan.py`.",
            "It begins from `1` directly: integers are grouped by factor-layer distance from the origin, return path, and divisor branching before any classical conjecture is invoked.",
            "This scan is operational rather than evidential by itself. It defines the native object of study for the repo.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["hotspots", args.hotspots],
                    ["samples", args.samples],
                ],
            ),
            "## Emanation Shells",
            "An emanation shell is the set of integers with the same total factor depth `Omega(n)`. The origin has depth `0`; primes have depth `1`; composites occupy deeper shells.",
            markdown_table(
                [
                    "depth",
                    "count",
                    "first_n",
                    "last_n",
                    "prime_layer",
                    "layered",
                    "squarefree",
                    "prime_powers",
                    "avg_divisors",
                    "avg_radical_ratio",
                ],
                shell_summary_table(rows),
            ),
            "## First Appearance Of Each Shell",
            "The first observed member of depth `k` is compared with the minimal repeated-binary emanation `2^k`.",
            markdown_table(
                ["depth", "first_n", "2^depth", "matches"],
                first_depth_table(rows),
            ),
            "## Branching Hotspots",
            "These are the highest-divisor-count integers in the scan. They are places where one emanated value has many return decompositions back toward `1`.",
            markdown_table(
                [
                    "n",
                    "depth",
                    "distinct_depth",
                    "divisors",
                    "radical_ratio",
                    "factor_layers",
                    "return_path",
                ],
                branching_hotspots(rows, args.hotspots),
            ),
            "## Sample Return Paths",
            markdown_table(
                [
                    "n",
                    "depth",
                    "distinct_depth",
                    "divisors",
                    "factor_layers",
                    "return_path",
                ],
                sample_path_table(rows, samples),
            ),
            "## Local Interpretation",
            "The Origin-first object is not a prime conjecture. It is the layered multiplicative structure by which every positive integer can be generated from, and reduced back to, `1`.",
            "This scan should be treated as the baseline map. Later conjecture probes should refer back to these shells and branching measures instead of becoming the center of the project.",
            "A stronger future test would pre-register one shell or branching metric here, then ask whether it transfers to prime gaps, Goldbach witnesses, modular returns, or Gilbreath-style differencing without retuning.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
