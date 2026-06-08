"""Held-out prediction tests for prime-gap Origin metrics."""

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

from emanation_from_1.number_theory import first_n_primes  # noqa: E402
from emanation_from_1.statistics import pearson_correlation  # noqa: E402
from experiments.prime_gap_origin_profiles import (  # noqa: E402
    PROFILE_METRICS,
    add_profile_metrics,
    group_indices,
    least_squares_line,
    metric_label,
    shuffled_by_groups,
    top_fraction_flags,
)


@dataclass(frozen=True)
class Predictor:
    """A pre-declared Origin-facing score for large residual gaps."""

    key: str
    label: str
    metric: str
    sign: float
    rationale: str


PREDICTORS = [
    Predictor(
        key="delta_divisor_pressure",
        label="-delta(p+1,p-1).divisor_count",
        metric="adjacent_delta_divisor_count",
        sign=-1.0,
        rationale=(
            "The prior B3 residual scan found delta(p+1,p-1).divisor_count as the "
            "strongest 8192-prime residual metric with negative direction."
        ),
    ),
    Predictor(
        key="p_plus_1_depth_pressure",
        label="-(p + 1).distinct_factor_depth",
        metric="p_plus_1_distinct_factor_depth",
        sign=-1.0,
        rationale=(
            "The prior B3 residual scan repeatedly promoted p + 1 factor depth in "
            "normalized and residual views, also with negative direction."
        ),
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


def parse_csv_ints(value: str, label: str) -> list[int]:
    values = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not values or any(item < 1 for item in values):
        raise ValueError(f"{label} must be a comma-separated list of positive integers")
    return values


def prime_gap_window_dataset(
    start_prime_index: int,
    gap_count: int,
) -> list[dict[str, float]]:
    """Return gap rows starting at a 1-based prime index."""
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
        prime_index = zero_index + 1
        gap = next_prime - prime
        row = {
            "prime_index": float(prime_index),
            "p": float(prime),
            "next_prime": float(next_prime),
            "gap": float(gap),
            "log_p": log(prime),
            "gap_over_log": gap / log(prime),
        }
        p_minus_1 = add_profile_metrics(row, "p_minus_1", prime - 1)
        p_plus_1 = add_profile_metrics(row, "p_plus_1", prime + 1)
        add_profile_metrics(row, "index", prime_index)

        for metric in PROFILE_METRICS:
            row[f"adjacent_delta_{metric}"] = p_plus_1[metric] - p_minus_1[metric]

        rows.append(row)

    return rows


def attach_external_log_residual_gap(
    dataset: list[dict[str, float]],
    intercept: float,
    slope: float,
) -> None:
    for row in dataset:
        row["log_residual_gap"] = row["gap"] - (intercept + slope * row["log_p"])


def roc_auc(scores: list[float], labels: list[float]) -> float | None:
    """Return rank AUC with average ranks for ties."""
    if len(scores) != len(labels):
        raise ValueError("AUC inputs must have equal length")
    positive_count = int(sum(labels))
    negative_count = len(labels) - positive_count
    if positive_count == 0 or negative_count == 0:
        return None

    ordered = sorted(enumerate(scores), key=lambda item: item[1])
    ranks = [0.0] * len(scores)
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][1] == ordered[index][1]:
            end += 1
        average_rank = ((index + 1) + end) / 2
        for ordered_index in range(index, end):
            ranks[ordered[ordered_index][0]] = average_rank
        index = end

    positive_rank_sum = sum(rank for rank, label in zip(ranks, labels) if label == 1.0)
    return (positive_rank_sum - (positive_count * (positive_count + 1) / 2)) / (
        positive_count * negative_count
    )


def precision_at_positive_count(scores: list[float], labels: list[float]) -> dict[str, float]:
    positive_count = int(sum(labels))
    if positive_count < 1:
        raise ValueError("precision requires at least one positive label")

    ranked = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
    selected = ranked[:positive_count]
    hits = sum(1 for index in selected if labels[index] == 1.0)
    precision = hits / positive_count
    base_rate = positive_count / len(labels)
    return {
        "k": float(positive_count),
        "hits": float(hits),
        "precision": precision,
        "base_rate": base_rate,
        "enrichment": precision / base_rate if base_rate else 0.0,
    }


def predictor_scores(dataset: list[dict[str, float]], predictor: Predictor) -> list[float]:
    return [predictor.sign * row[predictor.metric] for row in dataset]


def evaluate_predictor(
    dataset: list[dict[str, float]],
    predictor: Predictor,
    large_gap_fraction: float,
) -> dict[str, float | int | None]:
    residuals = [row["log_residual_gap"] for row in dataset]
    labels = top_fraction_flags(residuals, large_gap_fraction)
    scores = predictor_scores(dataset, predictor)
    precision = precision_at_positive_count(scores, labels)
    return {
        "positive_count": int(sum(labels)),
        "residual_r": pearson_correlation(scores, residuals),
        "auc": roc_auc(scores, labels),
        "hits": int(precision["hits"]),
        "precision": precision["precision"],
        "base_rate": precision["base_rate"],
        "enrichment": precision["enrichment"],
    }


def shuffled_residuals_from_training_baseline(
    dataset: list[dict[str, float]],
    groups: dict[object, list[int]],
    rng: Random,
    intercept: float,
    slope: float,
) -> list[float]:
    gaps = [row["gap"] for row in dataset]
    shuffled = shuffled_by_groups(gaps, groups, rng)
    return [
        gap - (intercept + slope * row["log_p"])
        for gap, row in zip(shuffled, dataset)
    ]


def control_evaluation(
    dataset: list[dict[str, float]],
    predictor: Predictor,
    observed: dict[str, float | int | None],
    trials: int,
    seed: int,
    mode: str,
    size_bins: int,
    large_gap_fraction: float,
    intercept: float,
    slope: float,
) -> dict[str, float | int | str]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    groups = group_indices(dataset, mode, size_bins)
    rng = Random(seed)
    scores = predictor_scores(dataset, predictor)
    auc_values: list[float] = []
    enrichment_values: list[float] = []

    for _trial in range(trials):
        residuals = shuffled_residuals_from_training_baseline(
            dataset,
            groups,
            rng,
            intercept,
            slope,
        )
        labels = top_fraction_flags(residuals, large_gap_fraction)
        auc = roc_auc(scores, labels)
        precision = precision_at_positive_count(scores, labels)
        if auc is not None:
            auc_values.append(auc)
        enrichment_values.append(precision["enrichment"])

    observed_auc = float(observed["auc"] or 0.0)
    observed_enrichment = float(observed["enrichment"] or 0.0)
    auc_ge_count = sum(1 for value in auc_values if value >= observed_auc)
    enrichment_ge_count = sum(
        1 for value in enrichment_values if value >= observed_enrichment
    )
    return {
        "mode": mode,
        "size_bins": size_bins,
        "trials": trials,
        "auc_mean": sum(auc_values) / len(auc_values),
        "auc_max": max(auc_values),
        "auc_ge_count": auc_ge_count,
        "auc_p_upper": (auc_ge_count + 1) / (trials + 1),
        "enrichment_mean": sum(enrichment_values) / len(enrichment_values),
        "enrichment_max": max(enrichment_values),
        "enrichment_ge_count": enrichment_ge_count,
        "enrichment_p_upper": (enrichment_ge_count + 1) / (trials + 1),
    }


def control_label(control: dict[str, float | int | str]) -> str:
    mode = str(control["mode"])
    if mode == "global":
        return "global gap shuffle"
    if mode == "residue30":
        return "shuffle within p mod 30"
    if mode == "residue30_size":
        return f"shuffle within p mod 30 and {control['size_bins']} size bins"
    return mode


def analyze_window(
    start_prime_index: int,
    gap_count: int,
    predictors: list[Predictor],
    intercept: float,
    slope: float,
    large_gap_fraction: float,
    trials: int,
    seed: int,
    size_bins: int,
) -> dict[str, object]:
    dataset = prime_gap_window_dataset(start_prime_index, gap_count)
    attach_external_log_residual_gap(dataset, intercept, slope)

    predictor_rows: list[dict[str, object]] = []
    for predictor_index, predictor in enumerate(predictors):
        observed = evaluate_predictor(dataset, predictor, large_gap_fraction)
        controls = [
            control_evaluation(
                dataset,
                predictor,
                observed,
                trials,
                seed + (predictor_index * 10_000) + offset,
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
        "start_prime_index": start_prime_index,
        "gap_count": gap_count,
        "first_p": int(dataset[0]["p"]),
        "last_p": int(dataset[-1]["p"]),
        "predictor_rows": predictor_rows,
    }


def observed_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        predictor_rows = analysis["predictor_rows"]
        assert isinstance(predictor_rows, list)
        for item in predictor_rows:
            predictor = item["predictor"]
            observed = item["observed"]
            assert isinstance(predictor, Predictor)
            assert isinstance(observed, dict)
            rows.append(
                [
                    analysis["start_prime_index"],
                    analysis["gap_count"],
                    f"{analysis['first_p']}..{analysis['last_p']}",
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


def strongest_control_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        predictor_rows = analysis["predictor_rows"]
        assert isinstance(predictor_rows, list)
        for item in predictor_rows:
            predictor = item["predictor"]
            controls = item["controls"]
            assert isinstance(predictor, Predictor)
            assert isinstance(controls, list)
            strongest = next(
                control for control in controls if control["mode"] == "residue30_size"
            )
            rows.append(
                [
                    analysis["start_prime_index"],
                    predictor.label,
                    control_label(strongest),
                    f"{strongest['auc_mean']:.4f}",
                    f"{strongest['auc_max']:.4f}",
                    f"{strongest['auc_ge_count']}/{strongest['trials']}",
                    f"{strongest['auc_p_upper']:.4f}",
                    f"{strongest['enrichment_mean']:.2f}x",
                    f"{strongest['enrichment_max']:.2f}x",
                    f"{strongest['enrichment_ge_count']}/{strongest['trials']}",
                    f"{strongest['enrichment_p_upper']:.4f}",
                ]
            )
    return rows


def all_control_rows(analysis: dict[str, object]) -> list[list[object]]:
    rows: list[list[object]] = []
    predictor_rows = analysis["predictor_rows"]
    assert isinstance(predictor_rows, list)
    for item in predictor_rows:
        predictor = item["predictor"]
        controls = item["controls"]
        assert isinstance(predictor, Predictor)
        assert isinstance(controls, list)
        for control in controls:
            rows.append(
                [
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


def run_reading(analyses: list[dict[str, object]]) -> str:
    observed_aucs: list[float] = []
    observed_enrichments: list[float] = []
    hard_auc_ge_count = 0
    hard_enrichment_ge_count = 0
    hard_trials = 0

    for analysis in analyses:
        predictor_rows = analysis["predictor_rows"]
        assert isinstance(predictor_rows, list)
        for item in predictor_rows:
            observed = item["observed"]
            controls = item["controls"]
            assert isinstance(observed, dict)
            assert isinstance(controls, list)
            observed_aucs.append(float(observed["auc"] or 0.0))
            observed_enrichments.append(float(observed["enrichment"] or 0.0))
            hard_control = next(
                control for control in controls if control["mode"] == "residue30_size"
            )
            hard_auc_ge_count += int(hard_control["auc_ge_count"])
            hard_enrichment_ge_count += int(hard_control["enrichment_ge_count"])
            hard_trials += int(hard_control["trials"])

    max_auc = max(observed_aucs)
    max_enrichment = max(observed_enrichments)
    if max_auc < 0.55 and hard_auc_ge_count > 0:
        return (
            "In this run, the held-out AUCs stay close to random ranking and the "
            "residue-plus-size controls frequently match or exceed them. Treat this "
            "as constraining evidence for these pre-declared predictors, even though "
            f"the best precision enrichment reaches `{max_enrichment:.2f}x`."
        )
    return (
        "In this run, at least one predictor separates large residual gaps from the "
        "hardest default controls strongly enough to justify a larger follow-up."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration-prime-count", type=int, default=8192)
    parser.add_argument("--test-starts", default="8192,16384")
    parser.add_argument("--test-gap-count", type=int, default=8192)
    parser.add_argument("--large-gap-fraction", type=float, default=0.10)
    parser.add_argument("--shuffle-trials", type=int, default=100)
    parser.add_argument("--size-bins", type=int, default=8)
    parser.add_argument("--seed", type=int, default=28000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "PRIME_GAP_ORIGIN_PREDICTION.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.calibration_prime_count < 2:
        raise ValueError("calibration-prime-count must be >= 2")
    if args.test_gap_count < 2:
        raise ValueError("test-gap-count must be >= 2")
    if args.shuffle_trials < 1:
        raise ValueError("shuffle-trials must be >= 1")
    if args.size_bins < 1:
        raise ValueError("size-bins must be >= 1")
    if not 0 < args.large_gap_fraction < 1:
        raise ValueError("large-gap-fraction must be between 0 and 1")

    calibration = prime_gap_window_dataset(1, args.calibration_prime_count - 1)
    intercept, slope = least_squares_line(
        [row["log_p"] for row in calibration],
        [row["gap"] for row in calibration],
    )
    starts = parse_csv_ints(args.test_starts, "test-starts")
    analyses = [
        analyze_window(
            start,
            args.test_gap_count,
            PREDICTORS,
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
            "# Prime Gap Origin Prediction",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/prime_gap_origin_prediction.py`.",
            "It turns the prior prime-gap origin-profile correlation into a held-out prediction test.",
            "The Origin metrics below are pre-declared from the previous B3 scan before scoring later prime-index windows.",
            "This is finite evidence only: it tests prediction quality under controls, not causation or proof.",
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
                ],
            ),
            "## Pre-Registered Predictors",
            markdown_table(
                ["predictor", "raw metric", "direction", "rationale"],
                [
                    [
                        predictor.label,
                        metric_label(predictor.metric),
                        "higher score predicts larger positive residual gap",
                        predictor.rationale,
                    ]
                    for predictor in PREDICTORS
                ],
            ),
            "## Calibration Baseline",
            f"The ordinary size baseline is fitted only on the calibration prefix: `gap ~= {intercept:.4f} + {slope:.4f} * log(p)`.",
            "Held-out residual gaps use that fixed line; predictor directions are not retuned on the test windows.",
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
            "## Strongest Conditioned Control Summary",
            "This table shows the residue-plus-size shuffled control, the hardest default control in this experiment.",
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
                strongest_control_rows(analyses),
            ),
            "## All Controls For Final Window",
            markdown_table(
                [
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
                all_control_rows(analyses[-1]),
            ),
            "## Local Interpretation",
            "A supportive result would show held-out AUC and enrichment above the residue-plus-size shuffled controls without changing the predictors.",
            "A constraining result would show that the pre-declared metrics do not beat conditioned controls in later windows.",
            run_reading(analyses),
            "This experiment deliberately makes the Origin claim easier to falsify: the metric must identify unusually large residual gaps before seeing the gap labels.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
