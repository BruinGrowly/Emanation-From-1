"""Test prime-neighborhood commutator gaps as non-modular prime-gap predictors."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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

from emanation_from_1.number_theory import first_n_primes
from emanation_from_1.origin_pakheta import (
    compression_prime_minus_neighborhood_commutator,
    compression_prime_plus_neighborhood_commutator,
)
from experiments.prime_gap_origin_prediction import (
    Predictor,
    attach_external_log_residual_gap,
    control_evaluation,
    control_label,
    evaluate_predictor,
    precision_at_positive_count,
    roc_auc,
)
from experiments.prime_gap_origin_profiles import (
    least_squares_line,
    parse_csv_ints,
    top_fraction_flags,
)

PREDICTORS = [
    Predictor(
        key="p_plus_1_neighborhood_plus_gap",
        label="C/N_+ path gap of p + 1",
        metric="p_plus_1_log_neighborhood_plus_gap",
        sign=-1.0,
        rationale=(
            "The C/N_+ path gap measures the shared symmetries of the quadratic extension boundary. "
            "We pre-register p + 1 neighborhood plus gap as a negative predictor: less boundary "
            "compression (higher gap) corresponds to more obstruction structure, predicting larger next-prime gaps."
        ),
    ),
    Predictor(
        key="delta_neighborhood_minus_gap",
        label="delta(p+1,p-1) C/N_- gap",
        metric="adjacent_delta_neighborhood_minus_gap",
        sign=1.0,
        rationale=(
            "The adjacent delta of the C/N_- path gap measures the asymmetry of prime field boundary "
            "complexity across the prime. Higher delta predicts larger next-prime gaps."
        ),
    ),
]


@dataclass(frozen=True)
class NeighborhoodWindow:
    """Held-out prime-gap window with prime-neighborhood metrics attached."""

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


def add_neighborhood_metrics(row: dict[str, float], prime: int) -> None:
    # Compute neighborhood gaps for adjacent composites
    p_minus_1_nm = compression_prime_minus_neighborhood_commutator(prime - 1).log_abs_gap
    p_minus_1_np = compression_prime_plus_neighborhood_commutator(prime - 1).log_abs_gap
    p_plus_1_nm = compression_prime_minus_neighborhood_commutator(prime + 1).log_abs_gap
    p_plus_1_np = compression_prime_plus_neighborhood_commutator(prime + 1).log_abs_gap

    row["p_minus_1_log_neighborhood_minus_gap"] = p_minus_1_nm
    row["p_minus_1_log_neighborhood_plus_gap"] = p_minus_1_np
    row["p_plus_1_log_neighborhood_minus_gap"] = p_plus_1_nm
    row["p_plus_1_log_neighborhood_plus_gap"] = p_plus_1_np

    row["adjacent_delta_neighborhood_minus_gap"] = p_plus_1_nm - p_minus_1_nm
    row["adjacent_delta_neighborhood_plus_gap"] = p_plus_1_np - p_minus_1_np
    row["adjacent_sum_neighborhood_minus_gap"] = p_plus_1_nm + p_minus_1_nm
    row["adjacent_sum_neighborhood_plus_gap"] = p_plus_1_np + p_minus_1_np


def prime_gap_neighborhood_window(
    start_prime_index: int,
    gap_count: int,
) -> NeighborhoodWindow:
    """Return one held-out prime-gap window with neighborhood metrics."""
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
        add_neighborhood_metrics(row, prime)
        rows.append(row)

    return NeighborhoodWindow(
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
    window: NeighborhoodWindow,
    fraction: float,
) -> list[list[object]]:
    labels = top_fraction_flags([row["log_residual_gap"] for row in window.rows], fraction)
    metric_specs = [
        ("p - 1 C/N_- gap", "p_minus_1_log_neighborhood_minus_gap"),
        ("p + 1 C/N_- gap", "p_plus_1_log_neighborhood_minus_gap"),
        ("p - 1 C/N_+ gap", "p_minus_1_log_neighborhood_plus_gap"),
        ("p + 1 C/N_+ gap", "p_plus_1_log_neighborhood_plus_gap"),
        ("delta C/N_- gap", "adjacent_delta_neighborhood_minus_gap"),
        ("delta C/N_+ gap", "adjacent_delta_neighborhood_plus_gap"),
        ("sum C/N_- gap", "adjacent_sum_neighborhood_minus_gap"),
        ("sum C/N_+ gap", "adjacent_sum_neighborhood_plus_gap"),
    ]
    rows: list[list[object]] = []
    for label, metric in metric_specs:
        scores = [row[metric] for row in window.rows]
        # Test positive correlation (no sign flip)
        auc_pos = roc_auc(scores, labels)
        precision_pos = precision_at_positive_count(scores, labels)
        
        # Test negative correlation (sign flip)
        neg_scores = [-val for val in scores]
        auc_neg = roc_auc(neg_scores, labels)
        precision_neg = precision_at_positive_count(neg_scores, labels)
        
        # Select best direction
        if auc_pos is not None and auc_neg is not None:
            if abs(auc_pos - 0.5) >= abs(auc_neg - 0.5):
                auc = auc_pos
                precision = precision_pos
                direction = "pos"
            else:
                auc = auc_neg
                precision = precision_neg
                direction = "neg"
        else:
            auc = 0.5
            precision = {"hits": 0, "k": 1, "enrichment": 1.0}
            direction = "pos"

        rows.append(
            [
                f"{label} ({direction})",
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
    window = prime_gap_neighborhood_window(start_prime_index, gap_count)
    attach_external_log_residual_gap(window.rows, intercept, slope)
    
    predictor_rows: list[dict[str, object]] = []
    for predictor_index, predictor in enumerate(PREDICTORS):
        observed = evaluate_predictor(window.rows, predictor, large_gap_fraction)
        controls = [
            control_evaluation(
                window.rows,
                predictor,
                observed,
                trials,
                seed + (predictor_index * 1000) + offset,
                mode,
                size_bins,
                large_gap_fraction,
                intercept,
                slope,
            )
            for offset, mode in enumerate(("global", "residue30", "residue30_size"))
        ]
        predictor_rows.append(
            {
                "predictor": predictor,
                "observed": observed,
                "controls": controls,
            }
        )
    return {
        "window": window,
        "predictor_rows": predictor_rows,
        "alternate_rows": alternate_score_rows(window, large_gap_fraction),
    }


def observed_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        window = analysis["window"]
        predictor_rows = analysis["predictor_rows"]
        assert isinstance(window, NeighborhoodWindow)
        assert isinstance(predictor_rows, list)
        for item in predictor_rows:
            predictor = item["predictor"]
            observed = item["observed"]
            assert isinstance(predictor, Predictor)
            assert isinstance(observed, dict)
            rows.append(
                [
                    window.start_prime_index,
                    window.gap_count,
                    f"{window.first_p}..{window.last_p}",
                    predictor.label,
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
        predictor_rows = analysis["predictor_rows"]
        assert isinstance(window, NeighborhoodWindow)
        assert isinstance(predictor_rows, list)
        for item in predictor_rows:
            predictor = item["predictor"]
            controls = item["controls"]
            assert isinstance(predictor, Predictor)
            assert isinstance(controls, list)
            for control in controls:
                rows.append(
                    [
                        window.start_prime_index,
                        predictor.label,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration-prime-count", type=int, default=8192)
    parser.add_argument("--test-starts", default="8192,16384")
    parser.add_argument("--test-gap-count", type=int, default=8192)
    parser.add_argument("--large-gap-fraction", type=float, default=0.10)
    parser.add_argument("--shuffle-trials", type=int, default=100)
    parser.add_argument("--size-bins", type=int, default=8)
    parser.add_argument("--seed", type=int, default=73000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "PRIME_GAP_NEIGHBORHOOD_TRANSFER.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
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
            "# Prime Gap Neighborhood Transfer (C2)",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/prime_gap_neighborhood_transfer.py`.",
            "It tests whether the new prime-neighborhood commutator gaps of adjacent composites (p-1 and p+1) transfer to predicting unusually large next-prime gaps.",
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
            "## Pre-Registered Predictors",
            markdown_table(
                ["predictor", "metric", "direction", "rationale"],
                [
                    [
                        predictor.label,
                        predictor.metric,
                        "higher score predicts larger positive residual gap" if predictor.sign > 0 else "lower score predicts larger positive residual gap",
                        predictor.rationale,
                    ]
                    for predictor in PREDICTORS
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
                    "predictor",
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
            markdown_table(
                ["score", "auc", "hits@k", "enrichment"],
                alternate_rows_for_final_window(analyses),
            ),
            "## Interpretation",
            "This experiment tests the C2 transfer reach of the prime-neighborhood commutator gaps into prime-gap boundaries.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
