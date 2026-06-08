"""Test Carmichael overlap pressure as a non-modular prime-gap predictor."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from math import log
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import first_n_primes, modular_return_decomposition  # noqa: E402
from experiments.prime_gap_origin_prediction import (  # noqa: E402
    Predictor,
    attach_external_log_residual_gap,
    control_evaluation,
    control_label,
    evaluate_predictor,
    precision_at_positive_count,
    roc_auc,
)
from experiments.prime_gap_origin_profiles import (  # noqa: E402
    least_squares_line,
    parse_csv_ints,
    top_fraction_flags,
)


PREDICTOR = Predictor(
    key="p_plus_1_overlap_pressure",
    label="log overlap pressure of p + 1",
    metric="p_plus_1_log_overlap_pressure",
    sign=1.0,
    rationale=(
        "E26 identified Carmichael lcm-overlap as the exact driver of modular "
        "return-exponent compression. This test pre-registers the immediate "
        "post-prime composite p + 1 as a non-modular transfer target: higher "
        "overlap pressure predicts a larger positive residual next-prime gap."
    ),
)


@dataclass(frozen=True)
class OverlapWindow:
    """Held-out prime-gap window with overlap metrics attached."""

    start_prime_index: int
    gap_count: int
    first_p: int
    last_p: int
    rows: list[dict[str, float]]


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


def overlap_pressure(n: int) -> float:
    """Return log Carmichael overlap penalty for n."""
    return fraction_log(modular_return_decomposition(n).overlap_penalty)


def add_overlap_metrics(row: dict[str, float], prime: int) -> None:
    minus = overlap_pressure(prime - 1)
    plus = overlap_pressure(prime + 1)
    row["p_minus_1_log_overlap_pressure"] = minus
    row["p_plus_1_log_overlap_pressure"] = plus
    row["adjacent_overlap_delta"] = plus - minus
    row["adjacent_overlap_sum"] = plus + minus


def prime_gap_overlap_window(
    start_prime_index: int,
    gap_count: int,
) -> OverlapWindow:
    """Return one held-out prime-gap window with overlap metrics."""
    if start_prime_index < 1:
        raise ValueError("start_prime_index must be >= 1")
    if gap_count < 2:
        raise ValueError("gap_count must be >= 2")

    needed_primes = start_prime_index + gap_count
    primes = first_n_primes(needed_primes)
    rows: list[dict[str, float]] = []
    start = start_prime_index - 1
    stop = start + gap_count
    for zero_index in range(start, stop):
        prime = primes[zero_index]
        next_prime = primes[zero_index + 1]
        gap = next_prime - prime
        row = {
            "prime_index": float(zero_index + 1),
            "p": float(prime),
            "next_prime": float(next_prime),
            "gap": float(gap),
            "log_p": log(prime),
            "gap_over_log": gap / log(prime),
        }
        add_overlap_metrics(row, prime)
        rows.append(row)

    return OverlapWindow(
        start_prime_index=start_prime_index,
        gap_count=gap_count,
        first_p=int(rows[0]["p"]),
        last_p=int(rows[-1]["p"]),
        rows=rows,
    )


def calibration_baseline(calibration_prime_count: int) -> tuple[float, float]:
    if calibration_prime_count < 3:
        raise ValueError("calibration_prime_count must be >= 3")
    primes = first_n_primes(calibration_prime_count)
    rows = [
        {
            "log_p": log(prime),
            "gap": float(next_prime - prime),
        }
        for prime, next_prime in zip(primes, primes[1:])
    ]
    return least_squares_line(
        [row["log_p"] for row in rows],
        [row["gap"] for row in rows],
    )


def alternate_score_rows(
    window: OverlapWindow,
    fraction: float,
) -> list[list[object]]:
    """Show non-selected overlap scores without treating them as pre-registered wins."""
    labels = top_fraction_flags([row["log_residual_gap"] for row in window.rows], fraction)
    metric_specs = [
        ("p - 1 overlap pressure", "p_minus_1_log_overlap_pressure"),
        ("p + 1 overlap pressure", "p_plus_1_log_overlap_pressure"),
        ("delta(p+1,p-1) overlap", "adjacent_overlap_delta"),
        ("sum adjacent overlap", "adjacent_overlap_sum"),
    ]
    rows: list[list[object]] = []
    for label, metric in metric_specs:
        scores = [row[metric] for row in window.rows]
        auc = roc_auc(scores, labels)
        precision = precision_at_positive_count(scores, labels)
        rows.append(
            [
                label,
                "undefined" if auc is None else f"{auc:.4f}",
                f"{precision['hits']:.0f}/{precision['k']:.0f}",
                f"{precision['enrichment']:.2f}x",
            ]
        )
    return rows


def analyze_window(
    start_prime_index: int,
    gap_count: int,
    intercept: float,
    slope: float,
    large_gap_fraction: float,
    trials: int,
    seed: int,
    size_bins: int,
) -> dict[str, object]:
    window = prime_gap_overlap_window(start_prime_index, gap_count)
    attach_external_log_residual_gap(window.rows, intercept, slope)
    observed = evaluate_predictor(window.rows, PREDICTOR, large_gap_fraction)
    controls = [
        control_evaluation(
            window.rows,
            PREDICTOR,
            observed,
            trials,
            seed + offset,
            mode,
            size_bins,
            large_gap_fraction,
            intercept,
            slope,
        )
        for offset, mode in enumerate(("global", "residue30", "residue30_size"))
    ]
    return {
        "window": window,
        "observed": observed,
        "controls": controls,
        "alternate_rows": alternate_score_rows(window, large_gap_fraction),
    }


def observed_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        window = analysis["window"]
        observed = analysis["observed"]
        assert isinstance(window, OverlapWindow)
        assert isinstance(observed, dict)
        rows.append(
            [
                window.start_prime_index,
                window.gap_count,
                f"{window.first_p}..{window.last_p}",
                PREDICTOR.label,
                observed["positive_count"],
                f"{observed['residual_r']:.4f}",
                f"{observed['auc']:.4f}",
                f"{observed['hits']}/{observed['positive_count']}",
                f"{observed['precision']:.4f}",
                f"{observed['enrichment']:.2f}x",
            ]
        )
    return rows


def control_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        window = analysis["window"]
        controls = analysis["controls"]
        assert isinstance(window, OverlapWindow)
        assert isinstance(controls, list)
        for control in controls:
            rows.append(
                [
                    window.start_prime_index,
                    control_label(control),
                    f"{control['auc_mean']:.4f}",
                    f"{control['auc_max']:.4f}",
                    f"{control['auc_ge_count']}/{control['trials']}",
                    f"{control['auc_p_upper']:.4f}",
                    f"{control['enrichment_mean']:.2f}x",
                    f"{control['enrichment_max']:.2f}x",
                    f"{control['enrichment_ge_count']}/{control['trials']}",
                    f"{control['enrichment_p_upper']:.4f}",
                ]
            )
    return rows


def alternate_rows_for_final_window(analyses: list[dict[str, object]]) -> list[list[object]]:
    final = analyses[-1]
    rows = final["alternate_rows"]
    assert isinstance(rows, list)
    return rows


def run_reading(analyses: list[dict[str, object]]) -> str:
    aucs: list[float] = []
    hard_auc_ge = 0
    hard_enrich_ge = 0
    hard_trials = 0
    for analysis in analyses:
        observed = analysis["observed"]
        controls = analysis["controls"]
        assert isinstance(observed, dict)
        assert isinstance(controls, list)
        aucs.append(float(observed["auc"] or 0.0))
        hard_control = next(
            control for control in controls if control["mode"] == "residue30_size"
        )
        hard_auc_ge += int(hard_control["auc_ge_count"])
        hard_enrich_ge += int(hard_control["enrichment_ge_count"])
        hard_trials += int(hard_control["trials"])

    best_auc = max(aucs)
    if best_auc < 0.55 or hard_auc_ge > 0:
        return (
            "The pre-registered overlap-pressure predictor does not clearly transfer "
            "to held-out large prime gaps in this run. AUCs remain close to random, "
            "and the hardest residue-plus-size controls match or exceed the observed "
            f"AUC in `{hard_auc_ge}/{hard_trials}` trials."
        )
    return (
        "The pre-registered overlap-pressure predictor beats the hardest default "
        "controls strongly enough to justify a larger independent follow-up."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration-prime-count", type=int, default=8192)
    parser.add_argument("--test-starts", default="8192,16384")
    parser.add_argument("--test-gap-count", type=int, default=8192)
    parser.add_argument("--large-gap-fraction", type=float, default=0.10)
    parser.add_argument("--shuffle-trials", type=int, default=100)
    parser.add_argument("--size-bins", type=int, default=8)
    parser.add_argument("--seed", type=int, default=72000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "PRIME_GAP_OVERLAP_TRANSFER.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.calibration_prime_count < 3:
        raise ValueError("calibration-prime-count must be >= 3")
    if args.test_gap_count < 2:
        raise ValueError("test-gap-count must be >= 2")
    if not 0 < args.large_gap_fraction < 1:
        raise ValueError("large-gap-fraction must be between 0 and 1")
    if args.shuffle_trials < 1:
        raise ValueError("shuffle-trials must be >= 1")
    if args.size_bins < 1:
        raise ValueError("size-bins must be >= 1")

    intercept, slope = calibration_baseline(args.calibration_prime_count)
    starts = parse_csv_ints(args.test_starts, "test-starts")
    analyses = [
        analyze_window(
            start,
            args.test_gap_count,
            intercept,
            slope,
            args.large_gap_fraction,
            args.shuffle_trials,
            args.seed + (start * 100),
            args.size_bins,
        )
        for start in starts
    ]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Prime Gap Overlap Transfer",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/prime_gap_overlap_transfer.py`.",
            "It tests whether the Carmichael overlap mechanism from modular return transfers to a non-modular target: unusually large next-prime gaps.",
            "The predictor is pre-registered before scoring: higher log overlap pressure of `p + 1` predicts a larger positive residual gap after `p`.",
            "This is finite evidence only. A failure is useful because it limits the reach of the modular-return mechanism.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["calibration_prime_count", args.calibration_prime_count],
                    ["test_starts", args.test_starts],
                    ["test_gap_count", args.test_gap_count],
                    ["large_gap_fraction", args.large_gap_fraction],
                    ["shuffle_trials_per_control", args.shuffle_trials],
                    ["size_bins", args.size_bins],
                    ["seed_start", args.seed],
                    ["baseline", f"gap ~= {intercept:.4f} + {slope:.4f} * log(p)"],
                ],
            ),
            "## Pre-Registered Predictor",
            markdown_table(
                ["predictor", "metric", "direction", "rationale"],
                [
                    [
                        PREDICTOR.label,
                        PREDICTOR.metric,
                        "higher score predicts larger positive residual gap",
                        PREDICTOR.rationale,
                    ],
                ],
            ),
            "## Held-Out Prediction Results",
            markdown_table(
                [
                    "start_prime_index",
                    "gaps",
                    "p_range",
                    "predictor",
                    "large_residual_gaps",
                    "residual_r",
                    "auc",
                    "hits@k",
                    "precision@k",
                    "enrichment",
                ],
                observed_rows(analyses),
            ),
            "## Conditioned Controls",
            markdown_table(
                [
                    "start_prime_index",
                    "control",
                    "auc_mean",
                    "auc_max",
                    "auc>=obs",
                    "auc_p_upper",
                    "enrich_mean",
                    "enrich_max",
                    "enrich>=obs",
                    "enrich_p_upper",
                ],
                control_rows(analyses),
            ),
            "## Non-Scored Overlap Diagnostics For Final Window",
            "These diagnostics are not treated as the pre-registered result; they show nearby overlap variants for follow-up planning.",
            markdown_table(
                ["score", "auc", "hits@k", "enrichment"],
                alternate_rows_for_final_window(analyses),
            ),
            "## Local Interpretation",
            run_reading(analyses),
            "This is a deliberately hard transfer test: the overlap mechanism must predict prime-gap behavior without using modular-return labels.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
