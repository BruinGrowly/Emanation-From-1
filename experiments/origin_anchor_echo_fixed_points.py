"""Anchor-echo fixed-point tests for modular arithmetic."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from math import log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import (  # noqa: E402
    factor_counter,
    lambda_phi_ratio,
    modular_idempotent_count,
    modular_involution_count,
    modular_return_decomposition,
)
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    best_abs_metric_correlation,
    regression_residuals_from_values,
    shell_conditioned_residuals,
    shell_groups,
    shuffled_within_shell,
    strongest_metric_for_values,
)


PREDECLARED_METRIC = "component_count"
BASELINE_FEATURES = ["log_n"]
ANCHOR_METRICS = [
    "component_count",
    "odd_component_count",
    "radical_compression",
    "divisor_count",
    "lambda_phi_log",
    "overlap_pressure_log",
]
TARGETS = [
    "log_idempotent_count",
    "log_idempotent_density",
    "log_involution_count",
    "log_involution_density",
]
MECHANISM_MODELS = [
    ("component_count", ["component_count"]),
    ("odd_plus_two_presence", ["odd_component_count", "two_component_present"]),
    ("involution_formula_shape", ["odd_component_count", "two_adic_involution_log"]),
    (
        "return_overlap_pack",
        [
            "radical_compression",
            "component_count",
            "overlap_pressure_log",
            "lambda_phi_log",
        ],
    ),
]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def fraction_log(value: Fraction) -> float:
    return log(value.numerator) - log(value.denominator)


def component_involution_count(prime: int, exponent: int) -> int:
    if prime == 2:
        if exponent == 1:
            return 1
        if exponent == 2:
            return 2
        return 4
    return 2


def two_adic_involution_log(counter: dict[int, int]) -> float:
    exponent = counter.get(2, 0)
    if exponent == 0:
        return 0.0
    return log(component_involution_count(2, exponent))


def fixed_point_dataset(limit: int) -> list[dict[str, float]]:
    """Return modular fixed-point rows for 2..limit."""
    if limit < 2:
        raise ValueError("limit must be >= 2")

    rows: list[dict[str, float]] = []
    for n in range(2, limit + 1):
        counter = dict(factor_counter(n))
        profile = origin_profile(n)
        decomposition = modular_return_decomposition(n)
        idempotent_count = modular_idempotent_count(n)
        involution_count = modular_involution_count(n)

        rows.append(
            {
                "n": float(n),
                "log_n": log(n),
                "emanation_depth": float(profile.emanation_depth),
                "component_count": float(decomposition.component_count),
                "odd_component_count": float(decomposition.odd_component_count),
                "two_component_present": 1.0 if 2 in counter else 0.0,
                "two_adic_involution_log": two_adic_involution_log(counter),
                "divisor_count": float(profile.divisor_count),
                "radical_compression": float(decomposition.radical_compression),
                "lambda_phi_log": fraction_log(lambda_phi_ratio(n)),
                "overlap_pressure_log": fraction_log(decomposition.overlap_penalty),
                "idempotent_count": float(idempotent_count),
                "involution_count": float(involution_count),
                "log_idempotent_count": log(idempotent_count),
                "log_involution_count": log(involution_count),
                "log_idempotent_density": log(idempotent_count) - log(n),
                "log_involution_density": log(involution_count) - log(n),
            }
        )
    return rows


def brute_force_check(limit: int) -> dict[str, int]:
    """Compare closed-form fixed-point counts with brute force up to limit."""
    if limit < 1:
        raise ValueError("brute force limit must be >= 1")

    max_idempotent_error = 0
    max_involution_error = 0
    for n in range(1, limit + 1):
        idempotents = sum(1 for x in range(n) if (x * x - x) % n == 0)
        involutions = sum(1 for x in range(n) if (x * x - 1) % n == 0)
        max_idempotent_error = max(
            max_idempotent_error,
            abs(modular_idempotent_count(n) - idempotents),
        )
        max_involution_error = max(
            max_involution_error,
            abs(modular_involution_count(n) - involutions),
        )

    return {
        "limit": limit,
        "max_idempotent_error": max_idempotent_error,
        "max_involution_error": max_involution_error,
    }


def conditioned_metric_residuals(
    dataset: list[dict[str, float]],
    metrics: list[str],
) -> dict[str, list[float]]:
    return {
        metric: shell_conditioned_residuals(dataset, metric, BASELINE_FEATURES)
        for metric in metrics
    }


def r_squared(target_values: list[float], feature_columns: list[list[float]]) -> float:
    total = sum(value * value for value in target_values)
    if total == 0:
        return 0.0
    residuals = regression_residuals_from_values(target_values, feature_columns)
    residual_sum = sum(value * value for value in residuals)
    return max(0.0, min(1.0, 1.0 - (residual_sum / total)))


def model_r_squared(
    dataset: list[dict[str, float]],
    target: str,
    features: list[str],
) -> float:
    target_residuals = shell_conditioned_residuals(
        dataset,
        target,
        BASELINE_FEATURES,
    )
    feature_columns = [
        shell_conditioned_residuals(dataset, feature, BASELINE_FEATURES)
        for feature in features
    ]
    return r_squared(target_residuals, feature_columns)


def target_control(
    dataset: list[dict[str, float]],
    target: str,
    trials: int,
    seed: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    target_residuals = shell_conditioned_residuals(
        dataset,
        target,
        BASELINE_FEATURES,
    )
    metric_residuals = conditioned_metric_residuals(dataset, ANCHOR_METRICS)
    predeclared_r = pearson_correlation(
        metric_residuals[PREDECLARED_METRIC],
        target_residuals,
    )
    best = strongest_metric_for_values(metric_residuals, target_residuals)
    if predeclared_r is None or best is None:
        raise ValueError(f"undefined correlations for {target}")

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
    return {
        "target": target,
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


def mechanism_rows(dataset: list[dict[str, float]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for target in TARGETS:
        for label, features in MECHANISM_MODELS:
            rows.append(
                [
                    target,
                    label,
                    ", ".join(features),
                    f"{model_r_squared(dataset, target, features):.4f}",
                ]
            )
    return rows


def shell_summary_rows(dataset: list[dict[str, float]]) -> list[list[object]]:
    groups = shell_groups(dataset)
    rows: list[list[object]] = []
    for shell in sorted(groups):
        members = [dataset[index] for index in groups[shell]]
        rows.append(
            [
                shell,
                len(members),
                f"{mean([row['component_count'] for row in members]):.3f}",
                f"{mean([row['idempotent_count'] for row in members]):.3f}",
                f"{mean([row['involution_count'] for row in members]):.3f}",
                f"{mean([row['radical_compression'] for row in members]):.4f}",
            ]
        )
    return rows


def top_fixed_point_rows(
    dataset: list[dict[str, float]],
    count: int,
) -> list[list[object]]:
    rows: list[list[object]] = []
    for row in sorted(
        dataset,
        key=lambda item: (
            item["idempotent_count"],
            item["involution_count"],
            -item["n"],
        ),
        reverse=True,
    )[:count]:
        rows.append(
            [
                int(row["n"]),
                int(row["emanation_depth"]),
                int(row["component_count"]),
                int(row["idempotent_count"]),
                int(row["involution_count"]),
                f"{row['radical_compression']:.4f}",
                f"{row['overlap_pressure_log']:.4f}",
            ]
        )
    return rows


def write_report(
    dataset: list[dict[str, float]],
    controls: list[dict[str, object]],
    brute_check: dict[str, int],
    report_path: Path,
    limit: int,
    trials: int,
    seed: int,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Origin Anchor Echo Fixed-Point Test",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                f"**Script:** `experiments/origin_anchor_echo_fixed_points.py`",
                f"**Range:** `2..{limit}`",
                f"**Controls:** `{trials}` shell shuffles, seed `{seed}`",
                "",
                "## Purpose",
                "",
                "This is the first Origin-side test suggested by the Pakheta Layer",
                "documents. It translates `anchor echo` into exact modular",
                "fixed-point structures:",
                "",
                "```text",
                "idempotent anchor: x^2 = x mod n",
                "return-symmetry anchor: x^2 = 1 mod n",
                "```",
                "",
                "The Pakheta language is treated as hypothesis grammar only. The",
                "evidence standard remains ordinary arithmetic: closed formulas,",
                "brute-force checks, size/shell conditioning, and shuffled controls.",
                "",
                "## Pre-Registered Question",
                "",
                "After controlling for `log(n)` and emanation shell `Omega(n)`, does",
                "prime-power component structure predict modular fixed-point",
                "richness better than shell-shuffled controls?",
                "",
                "## Exact Mechanism",
                "",
                "The conventional theorem-level mechanism is:",
                "",
                "```text",
                "idempotent_count(n) = 2^omega(n)",
                "involution_count(n) = product component roots of x^2 = 1",
                "```",
                "",
                "For odd prime powers the involution component count is `2`. For",
                "`2^a` it is `1` when `a = 1`, `2` when `a = 2`, and `4` when",
                "`a >= 3`.",
                "",
                "Formula check:",
                "",
                markdown_table(
                    ["brute_limit", "max_idempotent_error", "max_involution_error"],
                    [
                        [
                            brute_check["limit"],
                            brute_check["max_idempotent_error"],
                            brute_check["max_involution_error"],
                        ]
                    ],
                ),
                "",
                "## Shell-Controlled Fixed-Point Signal",
                "",
                "Targets and metrics below are shell-centered, then residualized",
                "against `log(n)`. Controls shuffle the target residuals within",
                "emanation shells.",
                "",
                markdown_table(
                    [
                        "target",
                        "pre_metric",
                        "pre_r",
                        "ctrl_mean_abs",
                        "ctrl_max_abs",
                        "ctrl_ge",
                        "p_upper",
                        "best_metric",
                        "best_r",
                        "best_ge",
                        "best_p_upper",
                    ],
                    control_rows(controls),
                ),
                "",
                "## Mechanism R2",
                "",
                "These rows ask how much of the conditioned fixed-point target is",
                "explained by each feature group.",
                "",
                markdown_table(
                    ["target", "model", "features", "R2"],
                    mechanism_rows(dataset),
                ),
                "",
                "## Shell Summary",
                "",
                markdown_table(
                    [
                        "Omega",
                        "rows",
                        "avg_components",
                        "avg_idempotents",
                        "avg_involutions",
                        "avg_radical_compression",
                    ],
                    shell_summary_rows(dataset),
                ),
                "",
                "## Highest Fixed-Point Rows",
                "",
                markdown_table(
                    [
                        "n",
                        "Omega",
                        "components",
                        "idempotents",
                        "involutions",
                        "radical_compression",
                        "log_overlap_penalty",
                    ],
                    top_fixed_point_rows(dataset, 12),
                ),
                "",
                "## Interpretation",
                "",
                "The anchor echo is real in the precise modular sense, but its",
                "mechanism is not mysterious: fixed-point richness is controlled by",
                "prime-power component branching and the special `2^a` involution",
                "case. In Pakheta terms, the useful translation is:",
                "",
                "```text",
                "anchor richness = coherent CRT recombination across prime-power facets",
                "false partition control = shuffle inside shell and lose the relation",
                "```",
                "",
                "This supports the next research move only modestly and cleanly: use",
                "Pakheta vocabulary to design sharper tests, while recording the",
                "ordinary number-theory mechanism as the actual evidence.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def run_experiment(
    limit: int,
    trials: int,
    seed: int,
    brute_check_limit: int,
    report_path: Path,
) -> dict[str, object]:
    dataset = fixed_point_dataset(limit)
    controls = [
        target_control(dataset, target, trials=trials, seed=seed + index)
        for index, target in enumerate(TARGETS)
    ]
    brute_check = brute_force_check(brute_check_limit)
    write_report(
        dataset,
        controls,
        brute_check,
        report_path,
        limit=limit,
        trials=trials,
        seed=seed,
    )
    return {
        "rows": len(dataset),
        "controls": controls,
        "brute_check": brute_check,
        "report_path": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
    )
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--trials", type=int, default=250)
    parser.add_argument("--seed", type=int, default=62026)
    parser.add_argument("--brute-check-limit", type=int, default=200)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_ANCHOR_ECHO_FIXED_POINTS.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_experiment(
        limit=args.limit,
        trials=args.trials,
        seed=args.seed,
        brute_check_limit=args.brute_check_limit,
        report_path=args.report,
    )
    print(f"rows: {result['rows']}")
    print(f"report: {result['report_path']}")


if __name__ == "__main__":
    main()
