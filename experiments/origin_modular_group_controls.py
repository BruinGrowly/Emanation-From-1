"""Stronger group-conditioned controls for modular return-to-1 behavior."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_modular_return import (  # noqa: E402
    ORIGIN_METRICS,
    PREDECLARED_METRIC,
    RETURN_TARGETS,
    modular_return_dataset,
)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def add_group_baseline_fields(dataset: list[dict[str, float]]) -> None:
    """Attach conventional group-structure baseline fields in-place."""
    for row in dataset:
        row["phi_over_n"] = row["phi"] / row["n"]
        row["log_phi"] = log(row["phi"])
        row["log_lambda"] = log(row["lambda"])


def baseline_features_for_target(target: str) -> list[str]:
    """Return non-circular conventional baseline features for a target."""
    if target == "lambda_over_phi":
        return ["log_n", "phi_over_n", "log_phi"]
    return ["log_n", "phi_over_n", "lambda_over_phi", "sampled_bases"]


def gaussian_solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Solve a small dense linear system with partial pivoting."""
    size = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]

    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("linear system is singular")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]

        divisor = augmented[column][column]
        for index in range(column, size + 1):
            augmented[column][index] /= divisor

        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            for index in range(column, size + 1):
                augmented[row][index] -= factor * augmented[column][index]

    return [augmented[row][size] for row in range(size)]


def regression_residuals(
    dataset: list[dict[str, float]],
    target: str,
    features: list[str],
) -> list[float]:
    """Return residuals after fitting target to intercept + features."""
    if len(dataset) <= len(features) + 1:
        raise ValueError("not enough rows for regression baseline")

    usable_features = [
        feature
        for feature in features
        if len({row[feature] for row in dataset}) > 1
    ]
    design = [[1.0, *[row[feature] for feature in usable_features]] for row in dataset]
    target_values = [row[target] for row in dataset]
    columns = len(design[0])
    xtx = [
        [
            sum(row[left] * row[right] for row in design)
            for right in range(columns)
        ]
        for left in range(columns)
    ]
    xty = [
        sum(row[column] * value for row, value in zip(design, target_values))
        for column in range(columns)
    ]

    coefficients = gaussian_solve(xtx, xty)
    return [
        value - sum(coefficient * column for coefficient, column in zip(coefficients, row))
        for row, value in zip(design, target_values)
    ]


def quantile_bins(values: list[float], bin_count: int) -> list[int]:
    """Assign values to approximately equal-count bins."""
    if bin_count < 1:
        raise ValueError("bin_count must be >= 1")
    ranked = sorted(range(len(values)), key=lambda index: values[index])
    bins = [0] * len(values)
    for rank, index in enumerate(ranked):
        bins[index] = min((rank * bin_count) // len(values), bin_count - 1)
    return bins


def grouped_indices(
    dataset: list[dict[str, float]],
    features: list[str],
    bins_per_feature: int,
) -> dict[tuple[int, ...], list[int]]:
    if bins_per_feature < 1:
        raise ValueError("bins_per_feature must be >= 1")

    feature_bins = [
        quantile_bins([row[feature] for row in dataset], bins_per_feature)
        for feature in features
    ]
    groups: dict[tuple[int, ...], list[int]] = {}
    for index in range(len(dataset)):
        key = tuple(bins[index] for bins in feature_bins)
        groups.setdefault(key, []).append(index)
    return groups


def shuffled_by_groups(
    values: list[float],
    groups: dict[tuple[int, ...], list[int]],
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


def group_control(
    dataset: list[dict[str, float]],
    target: str,
    trials: int,
    seed: int,
    bins_per_feature: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    features = baseline_features_for_target(target)
    residuals = regression_residuals(dataset, target, features)
    predeclared_r = pearson_correlation(
        [row[PREDECLARED_METRIC] for row in dataset],
        residuals,
    )
    best = strongest_metric_for_values(dataset, residuals, ORIGIN_METRICS)
    if predeclared_r is None or best is None:
        raise ValueError(f"undefined correlations for {target}")

    groups = grouped_indices(dataset, features, bins_per_feature)
    rng = Random(seed)
    predeclared_abs_controls: list[float] = []
    best_abs_controls: list[float] = []

    for _trial in range(trials):
        shuffled = shuffled_by_groups(residuals, groups, rng)
        predeclared_abs_controls.append(
            abs(
                pearson_correlation(
                    [row[PREDECLARED_METRIC] for row in dataset],
                    shuffled,
                )
                or 0.0
            )
        )
        best_abs_controls.append(
            best_abs_metric_correlation(dataset, shuffled, ORIGIN_METRICS)
        )

    predeclared_ge_count = sum(
        1 for value in predeclared_abs_controls if value >= abs(predeclared_r)
    )
    best_ge_count = sum(1 for value in best_abs_controls if value >= abs(best[1]))
    group_sizes = [len(indices) for indices in groups.values()]
    return {
        "target": target,
        "features": ", ".join(features),
        "groups": len(groups),
        "min_group_size": min(group_sizes),
        "mean_group_size": mean([float(size) for size in group_sizes]),
        "predeclared_r": predeclared_r,
        "predeclared_control_mean_abs": mean(predeclared_abs_controls),
        "predeclared_control_max_abs": max(predeclared_abs_controls),
        "predeclared_ge_count": predeclared_ge_count,
        "predeclared_p_upper": (predeclared_ge_count + 1) / (trials + 1),
        "best_metric": best[0],
        "best_r": best[1],
        "best_control_mean_abs": mean(best_abs_controls),
        "best_control_max_abs": max(best_abs_controls),
        "best_ge_count": best_ge_count,
        "best_p_upper": (best_ge_count + 1) / (trials + 1),
        "trials": trials,
    }


def control_rows(controls: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            control["target"],
            control["features"],
            control["groups"],
            control["min_group_size"],
            f"{control['mean_group_size']:.2f}",
            f"{control['predeclared_r']:.4f}",
            f"{control['predeclared_control_mean_abs']:.4f}",
            f"{control['predeclared_control_max_abs']:.4f}",
            f"{control['predeclared_ge_count']}/{control['trials']}",
            f"{control['predeclared_p_upper']:.4f}",
            control["best_metric"],
            f"{control['best_r']:.4f}",
            f"{control['best_ge_count']}/{control['trials']}",
            f"{control['best_p_upper']:.4f}",
        ]
        for control in controls
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--max-bases", type=int, default=16)
    parser.add_argument("--candidate-base-limit", type=int, default=80)
    parser.add_argument("--bins-per-feature", type=int, default=4)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=64000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_GROUP_CONTROLS.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.limit < 3:
        raise ValueError("limit must be >= 3")
    if args.max_bases < 1:
        raise ValueError("max-bases must be >= 1")
    if args.candidate_base_limit < 2:
        raise ValueError("candidate-base-limit must be >= 2")
    if args.bins_per_feature < 1:
        raise ValueError("bins-per-feature must be >= 1")
    if args.trials < 1:
        raise ValueError("trials must be >= 1")

    dataset = modular_return_dataset(
        args.limit,
        args.max_bases,
        args.candidate_base_limit,
    )
    add_group_baseline_fields(dataset)
    controls = [
        group_control(
            dataset,
            target,
            args.trials,
            args.seed + (index * 1000),
            args.bins_per_feature,
        )
        for index, target in enumerate(RETURN_TARGETS)
    ]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Modular Group Controls",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_group_controls.py`.",
            "It pressure-tests the modular return signal with conventional group baselines beyond number-line size.",
            "Targets are residualized against non-circular group features and shuffled inside quantile groups of those same features.",
            "The pre-declared Origin metric remains `emanation_depth`.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["rows_scored", len(dataset)],
                    ["max_bases_per_modulus", args.max_bases],
                    ["candidate_base_limit", args.candidate_base_limit],
                    ["bins_per_feature", args.bins_per_feature],
                    ["trials_per_target", args.trials],
                    ["seed_start", args.seed],
                    ["predeclared_metric", PREDECLARED_METRIC],
                    ["origin_metric_family", ", ".join(ORIGIN_METRICS)],
                ],
            ),
            "## Group-Baseline Residual Controls",
            markdown_table(
                [
                    "target",
                    "baseline_features",
                    "groups",
                    "min_group",
                    "mean_group",
                    "predeclared_r",
                    "pre_ctrl_mean",
                    "pre_ctrl_max",
                    "pre_ctrl>=obs",
                    "pre_p_upper",
                    "best_metric",
                    "best_r",
                    "best_ctrl>=obs",
                    "best_p_upper",
                ],
                control_rows(controls),
            ),
            "## Local Interpretation",
            "A supportive result would show `emanation_depth` retaining modular-return signal after conventional group baselines and grouped shuffles.",
            "A constraining result would show that the E20 modular-return signal was mostly a proxy for standard group quantities such as unit density or Carmichael compression.",
            "This is a stricter test than size-banded controls, but it is still finite and still operates inside arithmetic structure where factorization is expected to matter.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
