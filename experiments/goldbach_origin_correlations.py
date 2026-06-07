"""Compare Goldbach witness counts with Origin metrics and size baselines."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import log
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.conjectures import goldbach_pairs  # noqa: E402
from emanation_from_1.number_theory import goldbach_singular_factor, sieve  # noqa: E402
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import pearson_correlation  # noqa: E402


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def goldbach_dataset(limit: int) -> list[dict[str, float]]:
    primes = sieve(limit)
    rows: list[dict[str, float]] = []

    for n in range(4, limit + 1, 2):
        profile = origin_profile(n)
        pair_count = len(goldbach_pairs(n, primes))
        density_baseline = n / (log(n) ** 2)
        singular_factor = goldbach_singular_factor(n)
        singular_baseline = density_baseline * singular_factor
        rows.append(
            {
                "n": float(n),
                "pair_count": float(pair_count),
                "density_baseline": density_baseline,
                "singular_factor": singular_factor,
                "singular_baseline": singular_baseline,
                "normalized_pair_density": pair_count / density_baseline,
                "singular_normalized_density": pair_count / singular_baseline,
                "log_distance": profile.log_distance,
                "emanation_depth": float(profile.emanation_depth),
                "distinct_factor_depth": float(profile.distinct_factor_depth),
                "divisor_count": float(profile.divisor_count),
                "radical_ratio": profile.radical / n,
                "phi_attenuation": profile.phi_attenuation,
            }
        )

    return rows


def correlation_rows(dataset: list[dict[str, float]], target: str) -> list[list[object]]:
    metrics = [
        "n",
        "density_baseline",
        "singular_factor",
        "singular_baseline",
        "log_distance",
        "emanation_depth",
        "distinct_factor_depth",
        "divisor_count",
        "radical_ratio",
        "phi_attenuation",
    ]

    rows: list[list[object]] = []
    target_values = [row[target] for row in dataset]
    for metric in metrics:
        metric_values = [row[metric] for row in dataset]
        correlation = pearson_correlation(metric_values, target_values)
        rows.append(
            [
                metric,
                "undefined" if correlation is None else f"{correlation:.4f}",
            ]
        )
    return rows


def strongest_origin_correlation(dataset: list[dict[str, float]], target: str) -> tuple[str, float] | None:
    """Return the strongest absolute Origin-metric correlation for a target."""
    metrics = [
        "emanation_depth",
        "distinct_factor_depth",
        "divisor_count",
        "radical_ratio",
        "phi_attenuation",
    ]
    target_values = [row[target] for row in dataset]
    correlations: list[tuple[str, float]] = []

    for metric in metrics:
        correlation = pearson_correlation(
            [row[metric] for row in dataset],
            target_values,
        )
        if correlation is not None:
            correlations.append((metric, correlation))

    if not correlations:
        return None
    return max(correlations, key=lambda item: abs(item[1]))


def extremes(
    dataset: list[dict[str, float]],
    key: str,
    count: int = 8,
) -> tuple[list[list[object]], list[list[object]]]:
    low = sorted(dataset, key=lambda row: row[key])[:count]
    high = sorted(dataset, key=lambda row: row[key], reverse=True)[:count]

    def render(rows: list[dict[str, float]]) -> list[list[object]]:
        return [
            [
                int(row["n"]),
                int(row["pair_count"]),
                f"{row['normalized_pair_density']:.3f}",
                int(row["emanation_depth"]),
                int(row["divisor_count"]),
                f"{row['radical_ratio']:.3f}",
            ]
            for row in rows
        ]

    return render(low), render(high)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "GOLDBACH_ORIGIN_CORRELATIONS.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.limit < 4:
        raise ValueError("limit must be >= 4")

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    dataset = goldbach_dataset(args.limit)
    low, high = extremes(dataset, "normalized_pair_density")
    strongest = strongest_origin_correlation(dataset, "normalized_pair_density")
    strongest_residual = strongest_origin_correlation(dataset, "singular_normalized_density")
    strongest_line = (
        "No non-constant Origin metric correlation was available."
        if strongest is None
        else f"Strongest Origin-metric correlation with normalized density in this run: `{strongest[0]}` with `r = {strongest[1]:.4f}`."
    )
    strongest_residual_line = (
        "No non-constant Origin metric residual correlation was available."
        if strongest_residual is None
        else f"Strongest Origin-metric correlation after singular-factor correction: `{strongest_residual[0]}` with `r = {strongest_residual[1]:.4f}`."
    )

    report = "\n\n".join(
        [
            "# Goldbach Origin Correlations",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/goldbach_origin_correlations.py`.",
            "It tests whether simple Origin metrics relate to Goldbach witness counts.",
            "Correlations are descriptive only. They are not proof and they do not control for every confounder.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["evens_checked", len(dataset)],
                ],
            ),
            "## Source Background",
            "The singular-factor comparison is a conventional Hardy-Littlewood-style Goldbach baseline. Its n-dependent product uses the odd prime divisors of `n`; see MathWorld's Goldbach conjecture page and the singular-series formula summarized in the number-theory literature.",
            "- <https://mathworld.wolfram.com/GoldbachConjecture.html>",
            "- <https://www.sciencedirect.com/science/article/am/pii/S0022314X21000974>",
            "## Correlation With Raw Pair Count",
            markdown_table(["metric", "pearson_r"], correlation_rows(dataset, "pair_count")),
            "## Correlation With Size-Normalized Pair Density",
            "Normalized pair density is `pair_count / (n / log(n)^2)`.",
            markdown_table(
                ["metric", "pearson_r"],
                correlation_rows(dataset, "normalized_pair_density"),
            ),
            "## Correlation After Singular-Factor Baseline",
            "Singular-normalized density is `pair_count / ((n / log(n)^2) * singular_factor(n))`, where `singular_factor(n)` is the product of `(p - 1) / (p - 2)` over odd prime divisors of `n`.",
            markdown_table(
                ["metric", "pearson_r"],
                correlation_rows(dataset, "singular_normalized_density"),
            ),
            "## Lowest Normalized Pair Density",
            markdown_table(
                [
                    "n",
                    "pairs",
                    "norm_density",
                    "depth",
                    "divisors",
                    "radical_ratio",
                ],
                low,
            ),
            "## Highest Normalized Pair Density",
            markdown_table(
                [
                    "n",
                    "pairs",
                    "norm_density",
                    "depth",
                    "divisors",
                    "radical_ratio",
                ],
                high,
            ),
            "## Local Interpretation",
            "Raw pair counts are expected to correlate strongly with size. The more important test is whether Origin metrics correlate with size-normalized density.",
            strongest_line,
            strongest_residual_line,
            "A strong normalized correlation is still not automatically supportive; it must be compared against conventional factor-structure explanations.",
            "If Origin-metric correlations mostly vanish after the singular-factor baseline, the result should be treated as conventional arithmetic structure rather than distinctive Origin evidence.",
            "A weak or unstable normalized correlation should be recorded as neutral or challenging evidence.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
