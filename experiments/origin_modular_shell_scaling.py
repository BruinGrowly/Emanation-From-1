"""Scaling checks for shell-conditioned modular return transfer."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_group_controls import add_group_baseline_fields  # noqa: E402
from experiments.origin_modular_return import RETURN_TARGETS, modular_return_dataset  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    PREDECLARED_METRIC,
    WITHIN_SHELL_METRICS,
    shell_transfer_control,
)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def parse_csv_ints(value: str, label: str) -> list[int]:
    values = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not values or any(item < 1 for item in values):
        raise ValueError(f"{label} must be a comma-separated list of positive integers")
    return values


def scaling_analyses(
    limits: list[int],
    max_bases: int,
    candidate_base_limit: int,
    trials: int,
    seed: int,
) -> list[dict[str, object]]:
    analyses: list[dict[str, object]] = []
    for limit_index, limit in enumerate(limits):
        dataset = modular_return_dataset(limit, max_bases, candidate_base_limit)
        add_group_baseline_fields(dataset)
        controls = [
            shell_transfer_control(
                dataset,
                target,
                trials,
                seed + (limit_index * 10_000) + (target_index * 1000),
            )
            for target_index, target in enumerate(RETURN_TARGETS)
        ]
        analyses.append(
            {
                "limit": limit,
                "rows_scored": len(dataset),
                "controls": controls,
            }
        )
    return analyses


def result_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        controls = analysis["controls"]
        assert isinstance(controls, list)
        for control in controls:
            rows.append(
                [
                    analysis["limit"],
                    analysis["rows_scored"],
                    control["target"],
                    f"{control['predeclared_r']:.4f}",
                    f"{control['predeclared_ge_count']}/{control['trials']}",
                    f"{control['predeclared_p_upper']:.4f}",
                    control["best_metric"],
                    f"{control['best_r']:.4f}",
                    f"{control['best_ge_count']}/{control['trials']}",
                    f"{control['best_p_upper']:.4f}",
                ]
            )
    return rows


def primary_summary_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        controls = analysis["controls"]
        assert isinstance(controls, list)
        primary = next(control for control in controls if control["target"] == "lambda_over_phi")
        rows.append(
            [
                analysis["limit"],
                analysis["rows_scored"],
                f"{primary['predeclared_r']:.4f}",
                f"{primary['predeclared_ge_count']}/{primary['trials']}",
                primary["best_metric"],
                f"{primary['best_r']:.4f}",
                f"{primary['best_ge_count']}/{primary['trials']}",
            ]
        )
    return rows


def scaling_reading(analyses: list[dict[str, object]]) -> str:
    primary_controls = []
    for analysis in analyses:
        controls = analysis["controls"]
        assert isinstance(controls, list)
        primary_controls.append(
            next(control for control in controls if control["target"] == "lambda_over_phi")
        )

    same_direction = all(control["predeclared_r"] > 0 for control in primary_controls)
    no_control_matches = all(control["predeclared_ge_count"] == 0 for control in primary_controls)
    weakest = min(abs(float(control["predeclared_r"])) for control in primary_controls)

    if same_direction and no_control_matches:
        return (
            "The primary within-shell signal is stable across all tested limits: "
            "`radical_compression` remains positively associated with residual "
            f"`lambda_over_phi`, the weakest absolute correlation is `{weakest:.4f}`, "
            "and no shell-shuffled controls matched it."
        )
    return (
        "The primary within-shell signal is not stable across all tested limits. "
        "Treat the shell-transfer claim as constrained until a narrower metric or "
        "stronger range is identified."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limits", default="1000,2500,5000,10000")
    parser.add_argument("--max-bases", type=int, default=16)
    parser.add_argument("--candidate-base-limit", type=int, default=80)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=68000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_SHELL_SCALING.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    limits = parse_csv_ints(args.limits, "limits")
    if any(limit < 3 for limit in limits):
        raise ValueError("limits entries must be >= 3")
    if args.max_bases < 1:
        raise ValueError("max-bases must be >= 1")
    if args.candidate_base_limit < 2:
        raise ValueError("candidate-base-limit must be >= 2")
    if args.trials < 1:
        raise ValueError("trials must be >= 1")

    analyses = scaling_analyses(
        limits,
        args.max_bases,
        args.candidate_base_limit,
        args.trials,
        args.seed,
    )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Origin Modular Shell Scaling",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_shell_scaling.py`.",
            "It checks whether the shell-conditioned modular transfer result persists across larger finite ranges.",
            "The pre-declared within-shell metric remains `radical_compression`; controls still shuffle target residuals within emanation shells.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["limits", args.limits],
                    ["max_bases_per_modulus", args.max_bases],
                    ["candidate_base_limit", args.candidate_base_limit],
                    ["trials_per_target_per_limit", args.trials],
                    ["seed_start", args.seed],
                    ["predeclared_metric", PREDECLARED_METRIC],
                    ["within_shell_metrics", ", ".join(WITHIN_SHELL_METRICS)],
                ],
            ),
            "## Primary Scaling Summary",
            markdown_table(
                [
                    "limit",
                    "rows_scored",
                    "pre_r_lambda_over_phi",
                    "pre_ctrl>=obs",
                    "best_metric",
                    "best_r",
                    "best_ctrl>=obs",
                ],
                primary_summary_rows(analyses),
            ),
            "## Full Target Results",
            markdown_table(
                [
                    "limit",
                    "rows_scored",
                    "target",
                    "pre_r",
                    "pre_ctrl>=obs",
                    "pre_p_upper",
                    "best_metric",
                    "best_r",
                    "best_ctrl>=obs",
                    "best_p_upper",
                ],
                result_rows(analyses),
            ),
            "## Local Interpretation",
            scaling_reading(analyses),
            "A supportive scaling result does not prove the Origin Reframe. It means the same within-shell Origin metric survives repeated finite-range pressure tests without retuning.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
