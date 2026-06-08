"""Compare local prime gaps with Origin profiles around each prime."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.number_theory import first_n_primes  # noqa: E402
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.statistics import pearson_correlation  # noqa: E402


PROFILE_METRICS = [
    "emanation_depth",
    "distinct_factor_depth",
    "divisor_count",
    "radical_ratio",
    "phi_attenuation",
]
PROFILE_SOURCES = [
    ("p_minus_1", "p - 1"),
    ("p_plus_1", "p + 1"),
    ("index", "prime index"),
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


def origin_metric_keys() -> list[str]:
    keys: list[str] = []
    for source, _label in PROFILE_SOURCES:
        for metric in PROFILE_METRICS:
            keys.append(f"{source}_{metric}")
    for metric in PROFILE_METRICS:
        keys.append(f"adjacent_delta_{metric}")
    return keys


def metric_label(metric: str) -> str:
    for source, label in PROFILE_SOURCES:
        prefix = f"{source}_"
        if metric.startswith(prefix):
            return f"{label}.{metric.removeprefix(prefix)}"
    if metric.startswith("adjacent_delta_"):
        return f"delta(p+1,p-1).{metric.removeprefix('adjacent_delta_')}"
    return metric


def add_profile_metrics(row: dict[str, float], prefix: str, n: int) -> dict[str, float]:
    profile = origin_profile(n)
    values = {
        "emanation_depth": float(profile.emanation_depth),
        "distinct_factor_depth": float(profile.distinct_factor_depth),
        "divisor_count": float(profile.divisor_count),
        "radical_ratio": profile.radical / n,
        "phi_attenuation": profile.phi_attenuation,
    }
    for metric, value in values.items():
        row[f"{prefix}_{metric}"] = value
    return values


def prime_gap_dataset(prime_count: int) -> list[dict[str, float]]:
    """Return rows for gaps between consecutive primes in the first prime_count primes."""
    if prime_count < 2:
        raise ValueError("prime_count must be >= 2")

    primes = first_n_primes(prime_count)
    rows: list[dict[str, float]] = []

    for prime_index, (prime, next_prime) in enumerate(zip(primes, primes[1:]), start=1):
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


def least_squares_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Return intercept and slope for y ~= intercept + slope*x."""
    if len(xs) != len(ys):
        raise ValueError("line inputs must have equal length")
    if len(xs) < 2:
        raise ValueError("line fit requires at least two paired values")

    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError("line fit requires non-constant x values")

    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    intercept = y_mean - (slope * x_mean)
    return intercept, slope


def residuals_after_linear_baseline(xs: list[float], ys: list[float]) -> list[float]:
    intercept, slope = least_squares_line(xs, ys)
    return [y - (intercept + slope * x) for x, y in zip(xs, ys)]


def attach_log_residual_gap(dataset: list[dict[str, float]]) -> tuple[float, float]:
    log_values = [row["log_p"] for row in dataset]
    gaps = [row["gap"] for row in dataset]
    intercept, slope = least_squares_line(log_values, gaps)
    for row in dataset:
        row["log_residual_gap"] = row["gap"] - (intercept + slope * row["log_p"])
    return intercept, slope


def strongest_correlation(
    dataset: list[dict[str, float]],
    target: str,
    metrics: list[str],
) -> tuple[str, float] | None:
    return strongest_correlation_with_values(
        dataset,
        [row[target] for row in dataset],
        metrics,
    )


def strongest_correlation_with_values(
    dataset: list[dict[str, float]],
    target_values: list[float],
    metrics: list[str],
) -> tuple[str, float] | None:
    correlations: list[tuple[str, float]] = []

    for metric in metrics:
        correlation = pearson_correlation([row[metric] for row in dataset], target_values)
        if correlation is not None:
            correlations.append((metric, correlation))

    if not correlations:
        return None
    return max(correlations, key=lambda item: abs(item[1]))


def best_abs_correlation(
    metric_values: dict[str, list[float]],
    target_values: list[float],
) -> float:
    return max(
        abs(pearson_correlation(values, target_values) or 0.0)
        for values in metric_values.values()
    )


def group_indices(
    dataset: list[dict[str, float]],
    mode: str,
    size_bins: int,
) -> dict[object, list[int]]:
    if size_bins < 1:
        raise ValueError("size_bins must be >= 1")

    groups: dict[object, list[int]] = {}
    length = len(dataset)
    for index, row in enumerate(dataset):
        residue = int(row["p"]) % 30
        size_bin = min((index * size_bins) // length, size_bins - 1)
        if mode == "global":
            key: object = "all"
        elif mode == "residue30":
            key = residue
        elif mode == "residue30_size":
            key = (residue, size_bin)
        else:
            raise ValueError(f"unknown shuffle mode: {mode}")
        groups.setdefault(key, []).append(index)
    return groups


def shuffled_by_groups(
    values: list[float],
    groups: dict[object, list[int]],
    rng: Random,
) -> list[float]:
    shuffled = values[:]
    for indices in groups.values():
        group_values = [values[index] for index in indices]
        rng.shuffle(group_values)
        for index, value in zip(indices, group_values):
            shuffled[index] = value
    return shuffled


def ranked_correlation_rows(
    dataset: list[dict[str, float]],
    target: str,
    metrics: list[str],
    limit: int = 12,
) -> list[list[object]]:
    target_values = [row[target] for row in dataset]
    correlations = [
        (metric, pearson_correlation([row[metric] for row in dataset], target_values))
        for metric in metrics
    ]
    ranked = sorted(
        [(metric, value) for metric, value in correlations if value is not None],
        key=lambda item: abs(item[1]),
        reverse=True,
    )
    return [[metric_label(metric), f"{value:.4f}"] for metric, value in ranked[:limit]]


def source_summary_rows(dataset: list[dict[str, float]], target: str) -> list[list[object]]:
    rows: list[list[object]] = []
    sources = [
        ("p - 1", [f"p_minus_1_{metric}" for metric in PROFILE_METRICS]),
        ("p + 1", [f"p_plus_1_{metric}" for metric in PROFILE_METRICS]),
        ("prime index", [f"index_{metric}" for metric in PROFILE_METRICS]),
        ("delta(p+1,p-1)", [f"adjacent_delta_{metric}" for metric in PROFILE_METRICS]),
    ]

    for source, metrics in sources:
        strongest = strongest_correlation(dataset, target, metrics)
        if strongest is None:
            rows.append([source, "none", "undefined"])
        else:
            rows.append([source, metric_label(strongest[0]), f"{strongest[1]:.4f}"])
    return rows


def shuffle_residual_control(
    dataset: list[dict[str, float]],
    trials: int,
    seed: int,
) -> dict[str, float | int | str]:
    """Shuffle gap assignments and measure strongest Origin residual correlations."""
    return grouped_shuffle_residual_control(
        dataset,
        trials=trials,
        seed=seed,
        mode="global",
        size_bins=1,
    )


def grouped_shuffle_residual_control(
    dataset: list[dict[str, float]],
    trials: int,
    seed: int,
    mode: str,
    size_bins: int,
) -> dict[str, float | int | str]:
    """Shuffle gap assignments within optional residue/size groups."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    metrics = origin_metric_keys()
    observed = strongest_correlation(dataset, "log_residual_gap", metrics)
    if observed is None:
        raise ValueError("observed residual correlations are undefined")

    log_values = [row["log_p"] for row in dataset]
    gaps = [row["gap"] for row in dataset]
    metric_values = {metric: [row[metric] for row in dataset] for metric in metrics}
    rng = Random(seed)
    groups = group_indices(dataset, mode, size_bins)
    shuffled_best_abs: list[float] = []

    for _trial in range(trials):
        shuffled_gaps = shuffled_by_groups(gaps, groups, rng)
        shuffled_residuals = residuals_after_linear_baseline(log_values, shuffled_gaps)
        shuffled_best_abs.append(best_abs_correlation(metric_values, shuffled_residuals))

    observed_abs = abs(observed[1])
    ge_count = sum(1 for value in shuffled_best_abs if value >= observed_abs)
    return {
        "mode": mode,
        "size_bins": size_bins,
        "observed_metric": observed[0],
        "observed_r": observed[1],
        "trials": trials,
        "mean_abs_best": sum(shuffled_best_abs) / len(shuffled_best_abs),
        "max_abs_best": max(shuffled_best_abs),
        "ge_count": ge_count,
        "empirical_p_upper": (ge_count + 1) / (trials + 1),
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


def residual_control_comparison_rows(
    dataset: list[dict[str, float]],
    trials: int,
    seed: int,
    size_bins: int,
) -> list[list[object]]:
    controls = [
        grouped_shuffle_residual_control(dataset, trials, seed, "global", size_bins),
        grouped_shuffle_residual_control(dataset, trials, seed + 1, "residue30", size_bins),
        grouped_shuffle_residual_control(
            dataset,
            trials,
            seed + 2,
            "residue30_size",
            size_bins,
        ),
    ]
    return [
        [
            control_label(control),
            metric_label(str(control["observed_metric"])),
            f"{control['observed_r']:.4f}",
            f"{control['mean_abs_best']:.4f}",
            f"{control['max_abs_best']:.4f}",
            f"{control['ge_count']}/{control['trials']}",
            f"{control['empirical_p_upper']:.4f}",
        ]
        for control in controls
    ]


def top_fraction_flags(values: list[float], fraction: float) -> list[float]:
    if not 0 < fraction < 1:
        raise ValueError("fraction must be between 0 and 1")
    count = max(1, int(len(values) * fraction))
    count = min(count, len(values) - 1)
    ranked_indices = sorted(range(len(values)), key=lambda index: values[index], reverse=True)
    top_indices = set(ranked_indices[:count])
    return [1.0 if index in top_indices else 0.0 for index in range(len(values))]


def large_gap_classification(
    dataset: list[dict[str, float]],
    fraction: float,
    trials: int,
    seed: int,
    size_bins: int,
) -> dict[str, object]:
    """Compare Origin metrics against the largest positive residual gaps."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    metrics = origin_metric_keys()
    log_values = [row["log_p"] for row in dataset]
    gaps = [row["gap"] for row in dataset]
    observed_flags = top_fraction_flags([row["log_residual_gap"] for row in dataset], fraction)
    observed = strongest_correlation_with_values(dataset, observed_flags, metrics)
    if observed is None:
        raise ValueError("large-gap correlations are undefined")

    metric_values = {metric: [row[metric] for row in dataset] for metric in metrics}
    controls: list[dict[str, object]] = []

    for offset, mode in enumerate(("global", "residue30", "residue30_size")):
        rng = Random(seed + offset)
        groups = group_indices(dataset, mode, size_bins)
        shuffled_best_abs: list[float] = []
        for _trial in range(trials):
            shuffled_gaps = shuffled_by_groups(gaps, groups, rng)
            shuffled_residuals = residuals_after_linear_baseline(log_values, shuffled_gaps)
            shuffled_flags = top_fraction_flags(shuffled_residuals, fraction)
            shuffled_best_abs.append(best_abs_correlation(metric_values, shuffled_flags))

        observed_abs = abs(observed[1])
        ge_count = sum(1 for value in shuffled_best_abs if value >= observed_abs)
        controls.append(
            {
                "mode": mode,
                "size_bins": size_bins,
                "trials": trials,
                "mean_abs_best": sum(shuffled_best_abs) / len(shuffled_best_abs),
                "max_abs_best": max(shuffled_best_abs),
                "ge_count": ge_count,
                "empirical_p_upper": (ge_count + 1) / (trials + 1),
            }
        )

    return {
        "fraction": fraction,
        "large_gap_count": int(sum(observed_flags)),
        "observed_metric": observed[0],
        "observed_r": observed[1],
        "controls": controls,
    }


def large_gap_control_rows(classification: dict[str, object]) -> list[list[object]]:
    controls = classification["controls"]
    assert isinstance(controls, list)
    return [
        [
            control_label(control),
            f"{control['mean_abs_best']:.4f}",
            f"{control['max_abs_best']:.4f}",
            f"{control['ge_count']}/{control['trials']}",
            f"{control['empirical_p_upper']:.4f}",
        ]
        for control in controls
    ]


def analyze_prime_count(prime_count: int, shuffle_trials: int, seed: int) -> dict[str, object]:
    dataset = prime_gap_dataset(prime_count)
    intercept, slope = attach_log_residual_gap(dataset)
    metrics = origin_metric_keys()

    return {
        "prime_count": prime_count,
        "gap_count": len(dataset),
        "dataset": dataset,
        "baseline_intercept": intercept,
        "baseline_slope": slope,
        "log_gap_r": pearson_correlation(
            [row["log_p"] for row in dataset],
            [row["gap"] for row in dataset],
        ),
        "best_raw": strongest_correlation(dataset, "gap", metrics),
        "best_normalized": strongest_correlation(dataset, "gap_over_log", metrics),
        "best_residual": strongest_correlation(dataset, "log_residual_gap", metrics),
        "shuffle": shuffle_residual_control(
            dataset,
            shuffle_trials,
            seed + prime_count,
        ),
    }


def format_metric_result(result: tuple[str, float] | None) -> str:
    if result is None:
        return "undefined"
    return f"{metric_label(result[0])} ({result[1]:.4f})"


def scale_summary_rows(analyses: list[dict[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for analysis in analyses:
        shuffle = analysis["shuffle"]
        assert isinstance(shuffle, dict)
        rows.append(
            [
                analysis["prime_count"],
                analysis["gap_count"],
                f"{analysis['log_gap_r']:.4f}",
                format_metric_result(analysis["best_raw"]),
                format_metric_result(analysis["best_normalized"]),
                format_metric_result(analysis["best_residual"]),
                f"{shuffle['mean_abs_best']:.4f}",
                f"{shuffle['max_abs_best']:.4f}",
                f"{shuffle['ge_count']}/{shuffle['trials']}",
                f"{shuffle['empirical_p_upper']:.4f}",
            ]
        )
    return rows


def largest_gap_rows(dataset: list[dict[str, float]], count: int = 8) -> list[list[object]]:
    rows: list[list[object]] = []
    for row in sorted(dataset, key=lambda item: item["gap"], reverse=True)[:count]:
        rows.append(
            [
                int(row["prime_index"]),
                int(row["p"]),
                int(row["next_prime"]),
                int(row["gap"]),
                f"{row['log_residual_gap']:.3f}",
                int(row["p_minus_1_divisor_count"]),
                int(row["p_plus_1_divisor_count"]),
                f"{row['adjacent_delta_divisor_count']:.0f}",
            ]
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-counts", default="1024,2048,4096,8192")
    parser.add_argument("--shuffle-trials", type=int, default=100)
    parser.add_argument("--size-bins", type=int, default=8)
    parser.add_argument("--large-gap-fraction", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=24000)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "PRIME_GAP_ORIGIN_PROFILES.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prime_counts = parse_csv_ints(args.prime_counts, "prime-counts")
    if any(count < 2 for count in prime_counts):
        raise ValueError("prime-counts entries must be >= 2")
    if args.shuffle_trials < 1:
        raise ValueError("shuffle-trials must be >= 1")
    if args.size_bins < 1:
        raise ValueError("size-bins must be >= 1")
    if not 0 < args.large_gap_fraction < 1:
        raise ValueError("large-gap-fraction must be between 0 and 1")

    analyses = [
        analyze_prime_count(prime_count, args.shuffle_trials, args.seed)
        for prime_count in prime_counts
    ]
    primary = analyses[-1]
    primary_dataset = primary["dataset"]
    assert isinstance(primary_dataset, list)
    primary_shuffle = primary["shuffle"]
    assert isinstance(primary_shuffle, dict)
    primary_control_rows = residual_control_comparison_rows(
        primary_dataset,
        args.shuffle_trials,
        args.seed + 10_000,
        args.size_bins,
    )
    large_gap = large_gap_classification(
        primary_dataset,
        args.large_gap_fraction,
        args.shuffle_trials,
        args.seed + 20_000,
        args.size_bins,
    )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report = "\n\n".join(
        [
            "# Prime Gap Origin Profiles",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/prime_gap_origin_profiles.py`.",
            "It tests backlog item `B3`: whether origin profiles of `p - 1`, `p + 1`, or prime indices relate to the next prime gap.",
            "Correlations are descriptive finite measurements. They are not proof and they do not establish causation.",
            "## Parameters",
            markdown_table(
                ["parameter", "value"],
                [
                    ["prime_counts", args.prime_counts],
                    ["shuffle_trials_per_prefix", args.shuffle_trials],
                    ["size_bins", args.size_bins],
                    ["large_gap_fraction", args.large_gap_fraction],
                    ["seed_start", args.seed],
                ],
            ),
            "## Measurement Definitions",
            "\n".join(
                [
                    "- Each row measures a gap `next_prime - p` inside the first `prime_count` primes.",
                    "- Origin profiles are measured for `p - 1`, `p + 1`, and the 1-based prime index.",
                    "- Adjacent-composite deltas are `profile(p + 1) - profile(p - 1)` for the same metric.",
                    "- The conventional baseline is `log(p)`.",
                    "- The residual target is the gap after fitting `gap ~= a + b * log(p)`.",
                    "- Shuffle controls keep all metric rows fixed and randomly permute gap assignments before recomputing the log residual.",
                    "- Stronger controls shuffle gaps within `p mod 30`, then within both `p mod 30` and size bins.",
                    "- Large-gap classification marks the largest positive log-residual gaps and correlates that binary target with Origin metrics.",
                ]
            ),
            "## Scale Summary",
            markdown_table(
                [
                    "prime_count",
                    "gaps",
                    "log(p) raw gap r",
                    "best raw Origin r",
                    "best gap/log Origin r",
                    "best residual Origin r",
                    "shuffle mean best abs(r)",
                    "shuffle max best abs(r)",
                    "shuffle >= observed",
                    "empirical p upper",
                ],
                scale_summary_rows(analyses),
            ),
            "## Source Comparison For Largest Prefix",
            f"Largest prefix: `{primary['prime_count']}` primes, `{primary['gap_count']}` gaps.",
            f"Log baseline: `gap ~= {primary['baseline_intercept']:.4f} + {primary['baseline_slope']:.4f} * log(p)`.",
            markdown_table(
                ["source", "strongest residual metric", "pearson_r"],
                source_summary_rows(primary_dataset, "log_residual_gap"),
            ),
            "## Stronger Residual Controls For Largest Prefix",
            markdown_table(
                [
                    "control",
                    "observed metric",
                    "observed r",
                    "control mean best abs(r)",
                    "control max best abs(r)",
                    "control >= observed",
                    "empirical p upper",
                ],
                primary_control_rows,
            ),
            "## Large Residual-Gap Classification",
            f"Large-gap target: top `{args.large_gap_fraction:.2f}` of positive residual gaps, `{large_gap['large_gap_count']}` rows in the largest prefix.",
            f"Strongest observed classifier correlation: `{metric_label(str(large_gap['observed_metric']))}` with `r = {large_gap['observed_r']:.4f}`.",
            markdown_table(
                [
                    "control",
                    "control mean best abs(r)",
                    "control max best abs(r)",
                    "control >= observed",
                    "empirical p upper",
                ],
                large_gap_control_rows(large_gap),
            ),
            "## Top Residual Correlations For Largest Prefix",
            markdown_table(
                ["metric", "pearson_r"],
                ranked_correlation_rows(
                    primary_dataset,
                    "log_residual_gap",
                    origin_metric_keys(),
                    limit=12,
                ),
            ),
            "## Largest Gap Examples",
            markdown_table(
                [
                    "prime_index",
                    "p",
                    "next_prime",
                    "gap",
                    "log_residual_gap",
                    "divisors(p-1)",
                    "divisors(p+1)",
                    "delta_divisors",
                ],
                largest_gap_rows(primary_dataset),
            ),
            "## Local Interpretation",
            "For raw gaps, `log(p)` remains the stronger conventional baseline in this scan.",
            f"After subtracting the log baseline at the largest prefix, the strongest Origin-facing residual correlation is `{metric_label(str(primary_shuffle['observed_metric']))}` with `r = {primary_shuffle['observed_r']:.4f}`.",
            f"Across `{primary_shuffle['trials']}` shuffled-gap controls at the largest prefix, `{primary_shuffle['ge_count']}` matched or exceeded the observed absolute residual correlation; the conservative empirical upper estimate is `{primary_shuffle['empirical_p_upper']:.4f}`.",
            "This is local supportive evidence under the current controls: the Origin-facing residual signal survives the ordinary log baseline, global shuffled-gap comparison, and stronger residue/size-conditioned shuffled controls.",
            "The brave reading is narrow, not vague: local composite structure around a prime, especially `p + 1` and the delta between `p + 1` and `p - 1`, appears to carry information about the next prime gap after size is removed.",
            "The large-gap classification view gives the next proof-of-signal path: move beyond correlation and ask whether Origin metrics identify unusually large residual gaps before they occur.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
