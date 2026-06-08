"""Origin-first modular return-to-1 experiment."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import gcd, log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.number_theory import (  # noqa: E402
    carmichael_lambda,
    euler_totient,
    multiplicative_order,
)
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402


PREDECLARED_METRIC = "emanation_depth"
ORIGIN_METRICS = [
    "emanation_depth",
    "distinct_factor_depth",
    "divisor_count",
    "radical_compression",
    "phi_attenuation",
]
RETURN_TARGETS = [
    "lambda_over_phi",
    "average_order_ratio",
    "max_order_ratio",
    "full_exponent_hit",
]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def sampled_unit_bases(n: int, max_bases: int, candidate_limit: int) -> list[int]:
    """Return the first coprime bases in `[2, candidate_limit]`."""
    if max_bases < 1:
        raise ValueError("max_bases must be >= 1")
    if candidate_limit < 2:
        raise ValueError("candidate_limit must be >= 2")

    bases: list[int] = []
    for base in range(2, min(n, candidate_limit + 1)):
        if gcd(base, n) == 1:
            bases.append(base)
            if len(bases) == max_bases:
                break
    return bases


def modular_return_dataset(
    limit: int,
    max_bases: int,
    candidate_limit: int,
) -> list[dict[str, float]]:
    """Return modular return rows for moduli with at least one sampled unit base."""
    if limit < 3:
        raise ValueError("limit must be >= 3")

    rows: list[dict[str, float]] = []
    for n in range(2, limit + 1):
        bases = sampled_unit_bases(n, max_bases, candidate_limit)
        if not bases:
            continue

        profile = origin_profile(n)
        phi_n = euler_totient(n)
        lambda_n = carmichael_lambda(n)
        orders = [multiplicative_order(base, n) for base in bases]
        max_order = max(orders)
        average_order = mean([float(order) for order in orders])
        radical_ratio = profile.radical / n
        rows.append(
            {
                "n": float(n),
                "log_n": log(n),
                "sampled_bases": float(len(bases)),
                "phi": float(phi_n),
                "lambda": float(lambda_n),
                "lambda_over_phi": lambda_n / phi_n,
                "average_order": average_order,
                "max_order": float(max_order),
                "average_order_ratio": average_order / lambda_n,
                "max_order_ratio": max_order / lambda_n,
                "full_exponent_hit": 1.0 if max_order == lambda_n else 0.0,
                "emanation_depth": float(profile.emanation_depth),
                "distinct_factor_depth": float(profile.distinct_factor_depth),
                "divisor_count": float(profile.divisor_count),
                "radical_compression": 1.0 - radical_ratio,
                "phi_attenuation": profile.phi_attenuation,
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
    trials: int,
    seed: int,
    size_bins: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    residuals = residuals_after_log_size(dataset, target)
    predeclared_r = pearson_correlation(
        [row[PREDECLARED_METRIC] for row in dataset],
        residuals,
    )
    best = strongest_metric_for_values(dataset, residuals, ORIGIN_METRICS)
    if predeclared_r is None or best is None:
        raise ValueError(f"undefined correlations for {target}")

    groups = size_bin_groups(dataset, size_bins)
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
    return {
        "target": target,
        "raw_log_r": pearson_correlation(
            [row["log_n"] for row in dataset],
            [row[target] for row in dataset],
        ),
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
            f"{control['raw_log_r']:.4f}",
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


def sample_rows(dataset: list[dict[str, float]], count: int = 10) -> list[list[object]]:
    ranked = sorted(
        dataset,
        key=lambda row: (
            row["lambda_over_phi"],
            row["full_exponent_hit"],
            row["n"],
        ),
    )
    rows: list[list[object]] = []
    for row in ranked[:count]:
        rows.append(
            [
                int(row["n"]),
                int(row["phi"]),
                int(row["lambda"]),
                f"{row['lambda_over_phi']:.3f}",
                f"{row['average_order_ratio']:.3f}",
                f"{row['max_order_ratio']:.3f}",
                int(row["emanation_depth"]),
                int(row["divisor_count"]),
                f"{row['radical_compression']:.3f}",
            ]
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--max-bases", type=int, default=16)
    parser.add_argument("--candidate-base-limit", type=int, default=80)
    parser.add_argument("--size-bins", type=int, default=10)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=62000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_RETURN.md",
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
    if args.size_bins < 1:
        raise ValueError("size-bins must be >= 1")
    if args.trials < 1:
        raise ValueError("trials must be >= 1")

    dataset = modular_return_dataset(
        args.limit,
        args.max_bases,
        args.candidate_base_limit,
    )
    controls = [
        target_control(
            dataset,
            target,
            args.trials,
            args.seed + (index * 1000),
            args.size_bins,
        )
        for index, target in enumerate(RETURN_TARGETS)
    ]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Modular Return",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_return.py`.",
            "It tests a direct Origin-first transfer target: modular multiplication returns coprime bases to `1` after a finite period.",
            "The pre-declared Origin metric is `emanation_depth`, chosen from the shell map before scoring these modular-return targets.",
            "Targets are residualized against `log(n)`, then residuals are shuffled within size bands as controls.",
            "This is not a proof of the broader Origin Reframe; it asks whether shell structure transfers into modular return behavior beyond size.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["rows_scored", len(dataset)],
                    ["max_bases_per_modulus", args.max_bases],
                    ["candidate_base_limit", args.candidate_base_limit],
                    ["size_bins", args.size_bins],
                    ["trials_per_target", args.trials],
                    ["seed_start", args.seed],
                    ["predeclared_metric", PREDECLARED_METRIC],
                    ["origin_metric_family", ", ".join(ORIGIN_METRICS)],
                ],
            ),
            "## Measurement Definitions",
            "\n".join(
                [
                    "- `phi` is Euler's totient: the count of units modulo `n`.",
                    "- `lambda` is the Carmichael exponent: the guaranteed return exponent for all units modulo `n`.",
                    "- `lambda_over_phi` measures group-exponent compression relative to Euler's group-size baseline.",
                    "- `average_order_ratio` is the sampled mean multiplicative order divided by `lambda(n)`.",
                    "- `max_order_ratio` is the largest sampled order divided by `lambda(n)`.",
                    "- `full_exponent_hit` records whether the sampled bases include one whose order equals `lambda(n)`.",
                ]
            ),
            "## Residual Modular-Return Controls",
            markdown_table(
                [
                    "target",
                    "raw_log_r",
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
            "## Strong Return-Compression Examples",
            "These rows have the smallest `lambda / phi` ratios in the scan.",
            markdown_table(
                [
                    "n",
                    "phi",
                    "lambda",
                    "lambda/phi",
                    "avg_order/lambda",
                    "max_order/lambda",
                    "depth",
                    "divisors",
                    "compression",
                ],
                sample_rows(dataset),
            ),
            "## Local Interpretation",
            "A supportive Origin-first transfer result would show the pre-declared shell metric beating size-banded controls on modular-return targets.",
            "A constraining result would show that any apparent modular-return signal is no stronger than size-banded random alignment, or only appears after post-hoc metric selection.",
            "This experiment keeps the center on return to `1`: the object is the finite period required for modular multiplication to come home.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
