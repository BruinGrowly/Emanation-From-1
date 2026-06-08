"""Size-banded controls for direct Emanation-from-1 metrics."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402


SHELL_METRICS = [
    "emanation_depth",
    "distinct_factor_depth",
    "phi_attenuation",
]
TRANSFER_TARGETS = [
    "divisor_count",
    "radical_compression",
    "squarefree_flag",
]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def origin_size_dataset(limit: int) -> list[dict[str, float]]:
    """Return direct Origin metrics for integers `2..limit`."""
    if limit < 2:
        raise ValueError("limit must be >= 2")

    rows: list[dict[str, float]] = []
    for n in range(2, limit + 1):
        profile = origin_profile(n)
        factor_set = set(profile.factors)
        radical_ratio = profile.radical / n
        rows.append(
            {
                "n": float(n),
                "log_n": log(n),
                "emanation_depth": float(profile.emanation_depth),
                "distinct_factor_depth": float(profile.distinct_factor_depth),
                "divisor_count": float(profile.divisor_count),
                "radical_ratio": radical_ratio,
                "radical_compression": 1.0 - radical_ratio,
                "phi_attenuation": profile.phi_attenuation,
                "squarefree_flag": 1.0
                if len(profile.factors) == len(factor_set)
                else 0.0,
                "prime_power_flag": 1.0
                if profile.factors and len(factor_set) == 1
                else 0.0,
            }
        )
    return rows


def least_squares_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    if len(xs) != len(ys):
        raise ValueError("line inputs must have equal length")
    if len(xs) < 2:
        raise ValueError("line fit requires at least two paired values")

    x_mean = mean(xs)
    y_mean = mean(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError("line fit requires non-constant x values")

    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    intercept = y_mean - (slope * x_mean)
    return intercept, slope


def residuals_after_log_size(dataset: list[dict[str, float]], target: str) -> list[float]:
    intercept, slope = least_squares_line(
        [row["log_n"] for row in dataset],
        [row[target] for row in dataset],
    )
    return [row[target] - (intercept + slope * row["log_n"]) for row in dataset]


def size_bin_groups(dataset: list[dict[str, float]], size_bins: int) -> dict[int, list[int]]:
    if size_bins < 1:
        raise ValueError("size_bins must be >= 1")

    groups: dict[int, list[int]] = {}
    length = len(dataset)
    for index in range(length):
        size_bin = min((index * size_bins) // length, size_bins - 1)
        groups.setdefault(size_bin, []).append(index)
    return groups


def shuffled_by_groups(
    values: list[float],
    groups: dict[int, list[int]],
    rng: Random,
) -> list[float]:
    shuffled = values[:]
    for indices in groups.values():
        group_values = [values[index] for index in indices]
        rng.shuffle(group_values)
        for index, value in zip(indices, group_values):
            shuffled[index] = value
    return shuffled


def strongest_metric_for_values(
    dataset: list[dict[str, float]],
    values: list[float],
    metrics: list[str],
) -> tuple[str, float] | None:
    correlations: list[tuple[str, float]] = []
    for metric in metrics:
        correlation = pearson_correlation([row[metric] for row in dataset], values)
        if correlation is not None:
            correlations.append((metric, correlation))

    if not correlations:
        return None
    return max(correlations, key=lambda item: abs(item[1]))


def best_abs_metric_correlation(
    dataset: list[dict[str, float]],
    values: list[float],
    metrics: list[str],
) -> float:
    return max(
        abs(pearson_correlation([row[metric] for row in dataset], values) or 0.0)
        for metric in metrics
    )


def target_control(
    dataset: list[dict[str, float]],
    target: str,
    metrics: list[str],
    trials: int,
    seed: int,
    size_bins: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    residuals = residuals_after_log_size(dataset, target)
    observed = strongest_metric_for_values(dataset, residuals, metrics)
    if observed is None:
        raise ValueError(f"no non-constant metric correlations for {target}")

    groups = size_bin_groups(dataset, size_bins)
    rng = Random(seed)
    shuffled_best: list[float] = []
    for _trial in range(trials):
        shuffled = shuffled_by_groups(residuals, groups, rng)
        shuffled_best.append(best_abs_metric_correlation(dataset, shuffled, metrics))

    observed_abs = abs(observed[1])
    ge_count = sum(1 for value in shuffled_best if value >= observed_abs)
    log_r = pearson_correlation(
        [row["log_n"] for row in dataset],
        [row[target] for row in dataset],
    )
    return {
        "target": target,
        "log_r": log_r,
        "observed_metric": observed[0],
        "observed_r": observed[1],
        "trials": trials,
        "control_mean_abs_best": mean(shuffled_best),
        "control_max_abs_best": max(shuffled_best),
        "control_ge_count": ge_count,
        "empirical_p_upper": (ge_count + 1) / (trials + 1),
    }


def control_rows(controls: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            control["target"],
            f"{control['log_r']:.4f}",
            control["observed_metric"],
            f"{control['observed_r']:.4f}",
            f"{control['control_mean_abs_best']:.4f}",
            f"{control['control_max_abs_best']:.4f}",
            f"{control['control_ge_count']}/{control['trials']}",
            f"{control['empirical_p_upper']:.4f}",
        ]
        for control in controls
    ]


def size_band_rows(dataset: list[dict[str, float]], size_bins: int) -> list[list[object]]:
    groups = size_bin_groups(dataset, size_bins)
    rows: list[list[object]] = []
    for size_bin, indices in sorted(groups.items()):
        band = [dataset[index] for index in indices]
        rows.append(
            [
                size_bin + 1,
                int(band[0]["n"]),
                int(band[-1]["n"]),
                len(band),
                f"{mean([row['emanation_depth'] for row in band]):.3f}",
                f"{mean([row['divisor_count'] for row in band]):.3f}",
                f"{mean([row['radical_compression'] for row in band]):.4f}",
                f"{mean([row['squarefree_flag'] for row in band]):.3f}",
            ]
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--size-bins", type=int, default=20)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=51000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_SIZE_BANDED_CONTROLS.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.limit < 2:
        raise ValueError("limit must be >= 2")
    if args.size_bins < 1:
        raise ValueError("size-bins must be >= 1")
    if args.trials < 1:
        raise ValueError("trials must be >= 1")

    dataset = origin_size_dataset(args.limit)
    controls = [
        target_control(
            dataset,
            target,
            SHELL_METRICS,
            args.trials,
            args.seed + (index * 1000),
            args.size_bins,
        )
        for index, target in enumerate(TRANSFER_TARGETS)
    ]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Size-Banded Controls",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_size_banded_controls.py`.",
            "It asks whether direct shell metrics from Emanation-from-`1` retain structure after an ordinary size baseline is removed.",
            "The controls shuffle each residual target inside number-line size bands. This keeps local size comparable while breaking alignment between the target and shell metrics.",
            "This is still internal number-structure evidence, not a proof of the broader Origin Reframe.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["size_bins", args.size_bins],
                    ["trials_per_target", args.trials],
                    ["seed_start", args.seed],
                    ["shell_metrics", ", ".join(SHELL_METRICS)],
                ],
            ),
            "## Size-Band Summary",
            markdown_table(
                [
                    "band",
                    "first_n",
                    "last_n",
                    "count",
                    "avg_depth",
                    "avg_divisors",
                    "avg_compression",
                    "squarefree_rate",
                ],
                size_band_rows(dataset, args.size_bins),
            ),
            "## Residual Origin-Metric Controls",
            "Each target is first residualized against a linear `log(n)` baseline. The observed row then reports the strongest shell metric correlation with that residual target.",
            markdown_table(
                [
                    "target",
                    "raw_log_r",
                    "best_shell_metric",
                    "residual_r",
                    "control_mean_best_abs",
                    "control_max_best_abs",
                    "control>=observed",
                    "empirical_p_upper",
                ],
                control_rows(controls),
            ),
            "## Local Interpretation",
            "A supportive Origin-first result would show shell metrics retaining structure after the number-line size baseline is removed and after size-banded shuffles.",
            "A constraining result would show that the residual shell signal is no stronger than size-banded random alignment.",
            "This experiment stays before Gilbreath, Goldbach, or prime gaps. It tests whether the direct map from `1` carries measurable structure on its own terms.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
