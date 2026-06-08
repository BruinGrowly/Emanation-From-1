"""Decompose the shell-conditioned modular-return signal into mechanism parts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
from math import log
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import modular_return_decomposition  # noqa: E402
from emanation_from_1.statistics import pearson_correlation  # noqa: E402
from experiments.origin_modular_group_controls import (  # noqa: E402
    add_group_baseline_fields,
    baseline_features_for_target,
)
from experiments.origin_modular_return import modular_return_dataset  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    regression_residuals_from_values,
    shell_conditioned_residuals,
)


TARGET = "log_lambda_over_phi"
LOCAL_DEFECT = "log_local_defect"
OVERLAP = "neg_log_overlap_penalty"
PROXY_GROUPS = [
    ("concentration_proxy", ["radical_compression"]),
    ("splitting_pressure", ["component_count", "odd_component_count"]),
]
EXACT_GROUPS = [
    ("local_prime_power_defect", [LOCAL_DEFECT]),
    ("carmichael_overlap", [OVERLAP]),
]
MODEL_GROUPS = [*PROXY_GROUPS, *EXACT_GROUPS]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def fraction_log(value: Fraction) -> float:
    """Return log(value) without converting the whole Fraction first."""
    return log(value.numerator) - log(value.denominator)


def add_decomposition_fields(dataset: list[dict[str, float]]) -> None:
    """Attach exact modular-return mechanism fields in-place."""
    for row in dataset:
        decomposition = modular_return_decomposition(int(row["n"]))
        row["component_count"] = float(decomposition.component_count)
        row["odd_component_count"] = float(decomposition.odd_component_count)
        row["local_defect_ratio"] = float(decomposition.local_defect_ratio)
        row["overlap_penalty"] = float(decomposition.overlap_penalty)
        row[TARGET] = fraction_log(decomposition.lambda_phi_ratio)
        row[LOCAL_DEFECT] = fraction_log(decomposition.local_defect_ratio)
        row["log_overlap_penalty"] = fraction_log(decomposition.overlap_penalty)
        row[OVERLAP] = -row["log_overlap_penalty"]


def prepared_dataset(
    limit: int,
    max_bases: int,
    candidate_base_limit: int,
) -> list[dict[str, float]]:
    """Return modular-return rows with group and exact decomposition fields."""
    dataset = modular_return_dataset(limit, max_bases, candidate_base_limit)
    add_group_baseline_fields(dataset)
    add_decomposition_fields(dataset)
    return dataset


def conditioned_values(
    dataset: list[dict[str, float]],
    key: str,
    baseline_features: list[str],
) -> list[float]:
    """Shell-center and residualize one column against shared baselines."""
    return shell_conditioned_residuals(dataset, key, baseline_features)


def conditioned_columns(
    dataset: list[dict[str, float]],
    keys: list[str],
    baseline_features: list[str],
) -> list[list[float]]:
    return [conditioned_values(dataset, key, baseline_features) for key in keys]


def r_squared(target_values: list[float], feature_columns: list[list[float]]) -> float:
    """Return R^2 for target ~ intercept + feature columns."""
    total = sum(value * value for value in target_values)
    if total == 0:
        raise ValueError("R^2 requires non-zero target variance")
    if not feature_columns:
        return 0.0

    residuals = regression_residuals_from_values(target_values, feature_columns)
    residual_sum = sum(value * value for value in residuals)
    score = 1.0 - (residual_sum / total)
    return max(0.0, min(1.0, score))


def r_squared_for_keys(
    dataset: list[dict[str, float]],
    target_values: list[float],
    keys: list[str],
    baseline_features: list[str],
) -> float:
    return r_squared(target_values, conditioned_columns(dataset, keys, baseline_features))


def exact_log_contribution_summary(
    dataset: list[dict[str, float]],
    baseline_features: list[str],
) -> dict[str, float]:
    """Return exact covariance shares for local defect and overlap terms."""
    target_values = conditioned_values(dataset, TARGET, baseline_features)
    local_values = conditioned_values(dataset, LOCAL_DEFECT, baseline_features)
    overlap_values = conditioned_values(dataset, OVERLAP, baseline_features)

    denominator = sum(value * value for value in target_values)
    if denominator == 0:
        raise ValueError("contribution shares require non-zero target variance")

    local_contribution = sum(
        target * local for target, local in zip(target_values, local_values)
    ) / denominator
    overlap_contribution = sum(
        target * overlap for target, overlap in zip(target_values, overlap_values)
    ) / denominator
    max_identity_error = max(
        abs(target - local - overlap)
        for target, local, overlap in zip(target_values, local_values, overlap_values)
    )
    return {
        "target_variance": denominator / len(target_values),
        "local_defect_share": local_contribution,
        "overlap_share": overlap_contribution,
        "share_sum": local_contribution + overlap_contribution,
        "max_identity_error": max_identity_error,
        "local_defect_r": pearson_correlation(local_values, target_values) or 0.0,
        "overlap_r": pearson_correlation(overlap_values, target_values) or 0.0,
    }


def model_rows(
    dataset: list[dict[str, float]],
    baseline_features: list[str],
) -> list[list[object]]:
    target_values = conditioned_values(dataset, TARGET, baseline_features)
    models = [
        ("concentration_proxy", ["radical_compression"]),
        ("splitting_pressure", ["component_count", "odd_component_count"]),
        (
            "concentration_plus_splitting",
            ["radical_compression", "component_count", "odd_component_count"],
        ),
        ("local_prime_power_defect", [LOCAL_DEFECT]),
        ("carmichael_overlap", [OVERLAP]),
        ("exact_local_plus_overlap", [LOCAL_DEFECT, OVERLAP]),
    ]
    rows: list[list[object]] = []
    for label, keys in models:
        score = r_squared_for_keys(dataset, target_values, keys, baseline_features)
        rows.append([label, ", ".join(keys), f"{score:.4f}", f"{100 * score:.2f}%"])
    return rows


def r_squared_for_groups(
    dataset: list[dict[str, float]],
    target_values: list[float],
    groups: list[tuple[str, list[str]]],
    selected: set[str],
    baseline_features: list[str],
) -> float:
    keys: list[str] = []
    for label, group_keys in groups:
        if label in selected:
            keys.extend(group_keys)
    return r_squared_for_keys(dataset, target_values, keys, baseline_features)


def shapley_r2_attribution(
    dataset: list[dict[str, float]],
    groups: list[tuple[str, list[str]]],
    baseline_features: list[str],
) -> list[dict[str, float]]:
    """Return permutation-averaged marginal R^2 shares for grouped features."""
    target_values = conditioned_values(dataset, TARGET, baseline_features)
    totals = {label: 0.0 for label, _keys in groups}
    orderings = list(permutations([label for label, _keys in groups]))

    for ordering in orderings:
        selected: set[str] = set()
        current_score = 0.0
        for label in ordering:
            selected.add(label)
            next_score = r_squared_for_groups(
                dataset,
                target_values,
                groups,
                selected,
                baseline_features,
            )
            totals[label] += next_score - current_score
            current_score = next_score

    return [
        {
            "part": label,
            "r2_share": totals[label] / len(orderings),
        }
        for label, _keys in groups
    ]


def contribution_rows(summary: dict[str, float]) -> list[list[object]]:
    return [
        [
            "local_prime_power_defect",
            f"{summary['local_defect_share']:.4f}",
            f"{100 * summary['local_defect_share']:.2f}%",
            f"{summary['local_defect_r']:.4f}",
        ],
        [
            "carmichael_overlap",
            f"{summary['overlap_share']:.4f}",
            f"{100 * summary['overlap_share']:.2f}%",
            f"{summary['overlap_r']:.4f}",
        ],
        [
            "sum",
            f"{summary['share_sum']:.4f}",
            f"{100 * summary['share_sum']:.2f}%",
            "",
        ],
    ]


def shapley_rows(attribution: list[dict[str, float]]) -> list[list[object]]:
    total = sum(row["r2_share"] for row in attribution)
    rows = [
        [
            row["part"],
            f"{row['r2_share']:.4f}",
            f"{100 * row['r2_share']:.2f}%",
        ]
        for row in attribution
    ]
    rows.append(["sum", f"{total:.4f}", f"{100 * total:.2f}%"])
    return rows


def interpretation(summary: dict[str, float]) -> str:
    if summary["overlap_share"] > 0.8:
        return (
            "The conditioned log signal is dominated by Carmichael lcm-overlap. "
            "Local prime-power defects matter, especially for high powers of `2`, "
            "but they are secondary in this finite scan."
        )
    return (
        "The conditioned log signal is split across local prime-power defects and "
        "Carmichael lcm-overlap. Treat the mechanism as multi-part in this finite scan."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument("--max-bases", type=int, default=16)
    parser.add_argument("--candidate-base-limit", type=int, default=80)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_SIGNAL_DECOMPOSITION.md",
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

    dataset = prepared_dataset(
        args.limit,
        args.max_bases,
        args.candidate_base_limit,
    )
    baseline_features = baseline_features_for_target("lambda_over_phi")
    contribution_summary = exact_log_contribution_summary(dataset, baseline_features)
    proxy_attribution = shapley_r2_attribution(dataset, PROXY_GROUPS, baseline_features)
    full_attribution = shapley_r2_attribution(dataset, MODEL_GROUPS, baseline_features)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = "\n\n".join(
        [
            "# Origin Modular Signal Decomposition",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_signal_decomposition.py`.",
            "It decomposes the shell-conditioned modular-return signal into exact mechanism terms.",
            "The target is `log(lambda(n) / phi(n))`, because the exact mechanism is additive on the log scale:",
            "```text\nlog(lambda(n) / phi(n)) = log(local_defect_ratio(n)) - log(overlap_penalty(n))\n```",
            "All target and mechanism columns are shell-centered, then residualized against the same conventional group baselines used for `lambda_over_phi`.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limit", args.limit],
                    ["rows_scored", len(dataset)],
                    ["max_bases_per_modulus", args.max_bases],
                    ["candidate_base_limit", args.candidate_base_limit],
                    ["baseline_features", ", ".join(baseline_features)],
                    ["target", TARGET],
                    ["max_identity_error", f"{contribution_summary['max_identity_error']:.3e}"],
                    ["conditioned_target_variance", f"{contribution_summary['target_variance']:.6f}"],
                ],
            ),
            "## Exact Mechanism Contribution",
            "These signed covariance shares add to `100%` because the log identity remains exact after shell-centering and shared linear residualization.",
            markdown_table(
                ["mechanism_part", "variance_share", "percent", "correlation_with_target"],
                contribution_rows(contribution_summary),
            ),
            "## Proxy And Exact Model Fits",
            "`R^2` here means the share of conditioned log-signal variance captured by each feature set.",
            markdown_table(["model", "features", "r2", "percent"], model_rows(dataset, baseline_features)),
            "## Proxy-Only Attribution",
            "This asks how much of the conditioned log signal the Origin-facing proxy groups capture before exact mechanism terms are added.",
            markdown_table(["part", "shapley_r2_share", "percent"], shapley_rows(proxy_attribution)),
            "## Full Model Attribution",
            "This includes both Origin-facing proxies and exact mechanism terms. It is model attribution, not a universal theorem, because correlated features can share explanatory credit.",
            markdown_table(["part", "shapley_r2_share", "percent"], shapley_rows(full_attribution)),
            "## Local Interpretation",
            interpretation(contribution_summary),
            "The proof-level part is the exact log decomposition. The finite empirical part is how much variance each proxy or grouped model captures in this scanned range.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
