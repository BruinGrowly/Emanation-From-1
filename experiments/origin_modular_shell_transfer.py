"""Shell-conditioned modular return transfer tests."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_modular_group_controls import (  # noqa: E402
    add_group_baseline_fields,
    baseline_features_for_target,
    gaussian_solve,
)
from experiments.origin_modular_return import (  # noqa: E402
    RETURN_TARGETS,
    modular_return_dataset,
)


PREDECLARED_METRIC = "radical_compression"
WITHIN_SHELL_METRICS = [
    "radical_compression",
    "divisor_count",
    "distinct_factor_depth",
]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def shell_groups(dataset: list[dict[str, float]]) -> dict[int, list[int]]:
    groups: dict[int, list[int]] = defaultdict(list)
    for index, row in enumerate(dataset):
        groups[int(row["emanation_depth"])].append(index)
    return dict(groups)


def shell_centered_values(dataset: list[dict[str, float]], key: str) -> list[float]:
    groups = shell_groups(dataset)
    shell_means = {
        shell: mean([dataset[index][key] for index in indices])
        for shell, indices in groups.items()
    }
    return [row[key] - shell_means[int(row["emanation_depth"])] for row in dataset]


def regression_residuals_from_values(
    target_values: list[float],
    feature_columns: list[list[float]],
) -> list[float]:
    if not feature_columns:
        return target_values[:]
    if any(len(column) != len(target_values) for column in feature_columns):
        raise ValueError("feature columns must match target length")

    usable_features = [
        column for column in feature_columns if len(set(column)) > 1
    ]
    if not usable_features:
        return target_values[:]

    design = [
        [1.0, *[column[index] for column in usable_features]]
        for index in range(len(target_values))
    ]
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


def shell_conditioned_residuals(
    dataset: list[dict[str, float]],
    key: str,
    baseline_features: list[str],
) -> list[float]:
    centered_target = shell_centered_values(dataset, key)
    centered_features = [
        shell_centered_values(dataset, feature)
        for feature in baseline_features
        if feature != key
    ]
    return regression_residuals_from_values(centered_target, centered_features)


def shuffled_within_shell(
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
    metric_residuals: dict[str, list[float]],
    target_residuals: list[float],
) -> tuple[str, float] | None:
    correlations: list[tuple[str, float]] = []
    for metric, values in metric_residuals.items():
        correlation = pearson_correlation(values, target_residuals)
        if correlation is not None:
            correlations.append((metric, correlation))
    if not correlations:
        return None
    return max(correlations, key=lambda item: abs(item[1]))


def best_abs_metric_correlation(
    metric_residuals: dict[str, list[float]],
    target_residuals: list[float],
) -> float:
    return max(
        abs(pearson_correlation(values, target_residuals) or 0.0)
        for values in metric_residuals.values()
    )


def shell_transfer_control(
    dataset: list[dict[str, float]],
    target: str,
    trials: int,
    seed: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    features = baseline_features_for_target(target)
    target_residuals = shell_conditioned_residuals(dataset, target, features)
    metric_residuals = {
        metric: shell_conditioned_residuals(dataset, metric, features)
        for metric in WITHIN_SHELL_METRICS
    }
    predeclared_r = pearson_correlation(
        metric_residuals[PREDECLARED_METRIC],
        target_residuals,
    )
    best = strongest_metric_for_values(metric_residuals, target_residuals)
    if predeclared_r is None or best is None:
        raise ValueError(f"undefined shell transfer correlations for {target}")

    groups = shell_groups(dataset)
    rng = Random(seed)
    predeclared_abs_controls: list[float] = []
    best_abs_controls: list[float] = []
    for _trial in range(trials):
        shuffled = shuffled_within_shell(target_residuals, groups, rng)
        predeclared_abs_controls.append(
            abs(
                pearson_correlation(
                    metric_residuals[PREDECLARED_METRIC],
                    shuffled,
                )
                or 0.0
            )
        )
        best_abs_controls.append(best_abs_metric_correlation(metric_residuals, shuffled))

    predeclared_ge_count = sum(
        1 for value in predeclared_abs_controls if value >= abs(predeclared_r)
    )
    best_ge_count = sum(1 for value in best_abs_controls if value >= abs(best[1]))
    group_sizes = [len(indices) for indices in groups.values()]
    return {
        "target": target,
        "baseline_features": ", ".join(features),
        "shells": len(groups),
        "min_shell_size": min(group_sizes),
        "mean_shell_size": mean([float(size) for size in group_sizes]),
        "predeclared_metric": PREDECLARED_METRIC,
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
            control["baseline_features"],
            control["shells"],
            control["min_shell_size"],
            f"{control['mean_shell_size']:.2f}",
            control["predeclared_metric"],
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
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=66000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_SHELL_TRANSFER.md",
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
    if args.trials < 1:
        raise ValueError("trials must be >= 1")

    dataset = modular_return_dataset(
        args.limit,
        args.max_bases,
        args.candidate_base_limit,
    )
    add_group_baseline_fields(dataset)
    controls = [
        shell_transfer_control(dataset, target, args.trials, args.seed + (index * 1000))
        for index, target in enumerate(RETURN_TARGETS)
    ]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Modular Shell Transfer",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_shell_transfer.py`.",
            "It asks whether Origin branching/compression metrics retain modular-return signal inside the same emanation shell.",
            "For each target, both the target and candidate metrics are shell-centered, then residualized against conventional group features.",
            "Controls shuffle the target residuals within emanation shells, preserving the shell distribution while breaking within-shell alignment.",
            "The pre-declared within-shell metric is `radical_compression`.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["rows_scored", len(dataset)],
                    ["max_bases_per_modulus", args.max_bases],
                    ["candidate_base_limit", args.candidate_base_limit],
                    ["trials_per_target", args.trials],
                    ["seed_start", args.seed],
                    ["predeclared_metric", PREDECLARED_METRIC],
                    ["within_shell_metrics", ", ".join(WITHIN_SHELL_METRICS)],
                ],
            ),
            "## Shell-Conditioned Residual Controls",
            markdown_table(
                [
                    "target",
                    "baseline_features",
                    "shells",
                    "min_shell",
                    "mean_shell",
                    "pre_metric",
                    "pre_r",
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
            "A supportive result would show a within-shell Origin metric predicting modular-return residuals after shell means and conventional group baselines are removed.",
            "A constraining result would show that the modular-return signal belongs mainly to shell depth itself, with little extra signal inside each shell.",
            "This experiment keeps the object Origin-first: it asks whether the way a number branches and compresses from `1` matters after the total shell depth is already fixed.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
