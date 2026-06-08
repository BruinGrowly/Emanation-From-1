"""Test whether leftover anchor structure transfers after exact mechanisms."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from math import log, sqrt
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
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_anchor_echo_fixed_points import (  # noqa: E402
    two_adic_involution_log,
)
from experiments.origin_modular_group_controls import (  # noqa: E402
    add_group_baseline_fields,
    baseline_features_for_target,
)
from experiments.origin_modular_return import (  # noqa: E402
    modular_return_dataset,
)
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    shell_conditioned_residuals,
    shell_groups,
    shuffled_within_shell,
)


LOG2 = log(2.0)
ZERO_TOLERANCE = 1e-10
ANCHOR_RESIDUALS = [
    (
        "idempotent_exact_residual",
        "log(idempotents) - log(2) * component_count",
    ),
    (
        "idempotent_density_exact_residual",
        "log(idempotents/n) - (log(2) * component_count - log(n))",
    ),
    (
        "involution_exact_residual",
        "log(involutions) - (log(2) * odd_component_count + two_adic_log)",
    ),
    (
        "involution_density_exact_residual",
        "log(involutions/n) - (log(2) * odd_component_count + two_adic_log - log(n))",
    ),
]
TRANSFER_TARGETS = [
    (
        "log_lambda_over_phi",
        ["log_n", "phi_over_n", "log_phi", "component_count", "odd_component_count"],
    ),
    (
        "average_order_ratio",
        [*baseline_features_for_target("average_order_ratio"), "component_count"],
    ),
    (
        "max_order_ratio",
        [*baseline_features_for_target("max_order_ratio"), "component_count"],
    ),
    (
        "full_exponent_hit",
        [*baseline_features_for_target("full_exponent_hit"), "component_count"],
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


def root_mean_square(values: list[float]) -> float:
    if not values:
        raise ValueError("root mean square requires at least one value")
    return sqrt(mean([value * value for value in values]))


def anchor_residual_transfer_dataset(
    limit: int,
    max_bases: int,
    candidate_base_limit: int,
) -> list[dict[str, float]]:
    """Return modular-return rows with exact anchor residual fields."""
    dataset = modular_return_dataset(limit, max_bases, candidate_base_limit)
    add_group_baseline_fields(dataset)

    for row in dataset:
        n = int(row["n"])
        counter = dict(factor_counter(n))
        decomposition = modular_return_decomposition(n)
        idempotent_count = modular_idempotent_count(n)
        involution_count = modular_involution_count(n)
        two_adic_log = two_adic_involution_log(counter)

        row["component_count"] = float(decomposition.component_count)
        row["odd_component_count"] = float(decomposition.odd_component_count)
        row["two_adic_involution_log"] = two_adic_log
        row["log_lambda_over_phi"] = fraction_log(lambda_phi_ratio(n))
        row["overlap_pressure_log"] = fraction_log(decomposition.overlap_penalty)
        row["log_idempotent_count"] = log(idempotent_count)
        row["log_involution_count"] = log(involution_count)
        row["log_idempotent_density"] = log(idempotent_count) - log(n)
        row["log_involution_density"] = log(involution_count) - log(n)

        idempotent_model = LOG2 * row["component_count"]
        involution_model = (LOG2 * row["odd_component_count"]) + two_adic_log
        row["idempotent_exact_residual"] = (
            row["log_idempotent_count"] - idempotent_model
        )
        row["idempotent_density_exact_residual"] = (
            row["log_idempotent_density"] - (idempotent_model - row["log_n"])
        )
        row["involution_exact_residual"] = (
            row["log_involution_count"] - involution_model
        )
        row["involution_density_exact_residual"] = (
            row["log_involution_density"] - (involution_model - row["log_n"])
        )

    return dataset


def residual_summary(
    dataset: list[dict[str, float]],
    key: str,
) -> dict[str, float | bool]:
    values = shell_conditioned_residuals(dataset, key, [])
    max_abs = max(abs(value) for value in values)
    rms = root_mean_square(values)
    return {
        "max_abs": max_abs,
        "rms": rms,
        "has_leftover_variance": max_abs > ZERO_TOLERANCE,
    }


def transfer_control(
    dataset: list[dict[str, float]],
    anchor_residual: str,
    target: str,
    target_features: list[str],
    trials: int,
    seed: int,
) -> dict[str, object]:
    """Return transfer control for one anchor residual and target."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    anchor_values = shell_conditioned_residuals(dataset, anchor_residual, [])
    anchor_max_abs = max(abs(value) for value in anchor_values)
    target_values = shell_conditioned_residuals(dataset, target, target_features)
    target_rms = root_mean_square(target_values)

    if anchor_max_abs <= ZERO_TOLERANCE:
        return {
            "anchor_residual": anchor_residual,
            "target": target,
            "status": "no_leftover_anchor_variance",
            "anchor_max_abs": anchor_max_abs,
            "anchor_rms": root_mean_square(anchor_values),
            "target_rms": target_rms,
            "target_features": ", ".join(target_features),
            "observed_r": None,
            "control_mean_abs": None,
            "control_max_abs": None,
            "control_ge_count": None,
            "p_upper": None,
            "trials": trials,
        }

    observed_r = pearson_correlation(anchor_values, target_values)
    if observed_r is None:
        raise ValueError(f"undefined transfer correlation for {anchor_residual}")

    groups = shell_groups(dataset)
    rng = Random(seed)
    control_abs: list[float] = []
    for _trial in range(trials):
        shuffled = shuffled_within_shell(target_values, groups, rng)
        control_abs.append(abs(pearson_correlation(anchor_values, shuffled) or 0.0))

    ge_count = sum(1 for value in control_abs if value >= abs(observed_r))
    return {
        "anchor_residual": anchor_residual,
        "target": target,
        "status": "tested",
        "anchor_max_abs": anchor_max_abs,
        "anchor_rms": root_mean_square(anchor_values),
        "target_rms": target_rms,
        "target_features": ", ".join(target_features),
        "observed_r": observed_r,
        "control_mean_abs": mean(control_abs),
        "control_max_abs": max(control_abs),
        "control_ge_count": ge_count,
        "p_upper": (ge_count + 1) / (trials + 1),
        "trials": trials,
    }


def fmt_optional(value: object, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def residual_summary_rows(
    summaries: dict[str, dict[str, float | bool]],
) -> list[list[object]]:
    rows: list[list[object]] = []
    for key, description in ANCHOR_RESIDUALS:
        summary = summaries[key]
        rows.append(
            [
                key,
                description,
                f"{summary['max_abs']:.3e}",
                f"{summary['rms']:.3e}",
                summary["has_leftover_variance"],
            ]
        )
    return rows


def transfer_rows(controls: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            control["anchor_residual"],
            control["target"],
            control["status"],
            f"{control['anchor_max_abs']:.3e}",
            f"{control['target_rms']:.3e}",
            fmt_optional(control["observed_r"]),
            fmt_optional(control["control_mean_abs"]),
            fmt_optional(control["control_max_abs"]),
            (
                "n/a"
                if control["control_ge_count"] is None
                else f"{control['control_ge_count']}/{control['trials']}"
            ),
            fmt_optional(control["p_upper"]),
        ]
        for control in controls
    ]


def write_report(
    report_path: Path,
    dataset: list[dict[str, float]],
    summaries: dict[str, dict[str, float | bool]],
    controls: list[dict[str, object]],
    limit: int,
    max_bases: int,
    candidate_base_limit: int,
    trials: int,
    seed: int,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Origin Anchor Residual Transfer Test",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                f"**Script:** `experiments/origin_anchor_residual_transfer.py`",
                f"**Range:** modular-return rows through `{limit}`",
                (
                    f"**Sampling:** `{max_bases}` unit bases from candidates through "
                    f"`{candidate_base_limit}`"
                ),
                f"**Controls:** `{trials}` shell shuffles, seed `{seed}`",
                "",
                "## Purpose",
                "",
                "This is the next proof-pressure move after the fixed-point anchor",
                "test. The prior result found exact anchor mechanisms:",
                "",
                "```text",
                "idempotent_count(n) = 2^omega(n)",
                "involution_count(n) = product component roots of x^2 = 1",
                "```",
                "",
                "This test removes those exact component explanations first. It then",
                "asks whether any leftover anchor residual transfers into independent",
                "modular-return targets.",
                "",
                "## Pre-Registered Question",
                "",
                "After the exact CRT component formulas are subtracted from modular",
                "fixed-point richness, is there any remaining anchor residual that",
                "predicts modular-return behavior better than shell-shuffled controls?",
                "",
                "## Leftover Anchor Residuals",
                "",
                markdown_table(
                    [
                        "residual",
                        "formula removed",
                        "max_abs",
                        "rms",
                        "has_leftover_variance",
                    ],
                    residual_summary_rows(summaries),
                ),
                "",
                "## Transfer Controls",
                "",
                "Targets are shell-centered and residualized against their listed",
                "baseline features before scoring. If an anchor residual has no",
                "variance left, the transfer row is not statistically testable.",
                "",
                markdown_table(
                    [
                        "anchor_residual",
                        "target",
                        "status",
                        "anchor_max_abs",
                        "target_rms",
                        "observed_r",
                        "ctrl_mean_abs",
                        "ctrl_max_abs",
                        "ctrl_ge",
                        "p_upper",
                    ],
                    transfer_rows(controls),
                ),
                "",
                "## Interpretation",
                "",
                "The result is constraining. Once the exact CRT component explanation",
                "is removed, the tested fixed-point anchors leave no measurable",
                "residual signal. With no leftover variance, there is nothing for this",
                "anchor definition to transfer into modular-return targets.",
                "",
                "Plainly:",
                "",
                "> The fixed-point anchor echo is real, but exhausted by its exact",
                "> component mechanism in this test.",
                "",
                "This does not disprove the Origin Reframe or the Pakheta Layer. It",
                "does block one tempting overclaim: fixed-point anchor richness should",
                "not be treated as extra Origin evidence unless a new, non-exhausted",
                "anchor metric is defined or it predicts an independent target before",
                "the exact component mechanism is removed.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def run_experiment(
    limit: int,
    max_bases: int,
    candidate_base_limit: int,
    trials: int,
    seed: int,
    report_path: Path,
) -> dict[str, object]:
    dataset = anchor_residual_transfer_dataset(
        limit,
        max_bases=max_bases,
        candidate_base_limit=candidate_base_limit,
    )
    summaries = {
        key: residual_summary(dataset, key)
        for key, _description in ANCHOR_RESIDUALS
    }
    controls = [
        transfer_control(
            dataset,
            anchor_key,
            target,
            target_features,
            trials=trials,
            seed=seed + (anchor_index * 100) + target_index,
        )
        for anchor_index, (anchor_key, _description) in enumerate(ANCHOR_RESIDUALS)
        for target_index, (target, target_features) in enumerate(TRANSFER_TARGETS)
    ]
    write_report(
        report_path,
        dataset,
        summaries,
        controls,
        limit=limit,
        max_bases=max_bases,
        candidate_base_limit=candidate_base_limit,
        trials=trials,
        seed=seed,
    )
    return {
        "rows": len(dataset),
        "summaries": summaries,
        "controls": controls,
        "report_path": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--max-bases", type=int, default=12)
    parser.add_argument("--candidate-base-limit", type=int, default=40)
    parser.add_argument("--trials", type=int, default=250)
    parser.add_argument("--seed", type=int, default=62126)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_ANCHOR_RESIDUAL_TRANSFER.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_experiment(
        limit=args.limit,
        max_bases=args.max_bases,
        candidate_base_limit=args.candidate_base_limit,
        trials=args.trials,
        seed=args.seed,
        report_path=args.report,
    )
    print(f"rows: {result['rows']}")
    print(f"report: {result['report_path']}")


if __name__ == "__main__":
    main()
