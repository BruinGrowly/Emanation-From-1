"""Test prime-neighborhood commutator gaps as Goldbach witness density transfer predictors."""

from __future__ import annotations

import argparse
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

from emanation_from_1.conjectures import goldbach_pairs
from emanation_from_1.number_theory import (
    goldbach_singular_factor,
    sieve,
    factor_counter,
    radical,
)
from emanation_from_1.origin_pakheta import (
    compression_prime_minus_neighborhood_commutator,
    compression_prime_plus_neighborhood_commutator,
)
from emanation_from_1.statistics import mean, pearson_correlation
from experiments.origin_modular_shell_transfer import (
    shell_conditioned_residuals,
    shell_groups,
    shuffled_within_shell,
)


METRICS = [
    ("compression_prime_minus_neighborhood_log_gap", "C/N_- path gap"),
    ("compression_prime_plus_neighborhood_log_gap", "C/N_+ path gap"),
]

TRANSFER_TARGETS = [
    ("log_singular_normalized_density", "Goldbach singular-normalized density log(pairs/baseline)"),
]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def goldbach_neighborhood_transfer_dataset(limit: int) -> list[dict[str, float]]:
    """Return dataset of even positive integers with neighborhood gaps and Goldbach targets."""
    if limit < 4:
        raise ValueError("limit must be >= 4")

    primes = sieve(limit)
    rows: list[dict[str, float]] = []
    
    for n in range(4, limit + 1, 2):
        counter = factor_counter(n)
        depth = sum(counter.values())
        c_nm = compression_prime_minus_neighborhood_commutator(n)
        c_np = compression_prime_plus_neighborhood_commutator(n)
        rad_val = radical(n)
        
        pair_count = len(goldbach_pairs(n, primes))
        if pair_count == 0:
            continue  # Safety check
            
        density_baseline = n / (log(n) ** 2)
        singular_factor = goldbach_singular_factor(n)
        singular_baseline = density_baseline * singular_factor
        
        rows.append(
            {
                "n": float(n),
                "log_n": log(n),
                "emanation_depth": float(depth),
                "compression_prime_minus_neighborhood_log_gap": c_nm.log_abs_gap,
                "compression_prime_plus_neighborhood_log_gap": c_np.log_abs_gap,
                "radical_compression": 1.0 - (rad_val / n),
                "log_singular_normalized_density": log(pair_count / singular_baseline),
            }
        )
    return rows


def transfer_control(
    dataset: list[dict[str, float]],
    metric: str,
    target: str,
    trials: int,
    seed: int,
) -> dict[str, object]:
    """Score observed correlation and run shell-conditioned controls."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    # Condition target and metric against log_n
    target_residuals = shell_conditioned_residuals(dataset, target, ["log_n"])
    metric_residuals = shell_conditioned_residuals(dataset, metric, ["log_n"])

    observed_r = pearson_correlation(metric_residuals, target_residuals)
    if observed_r is None:
        observed_r = 0.0

    groups = shell_groups(dataset)
    rng = Random(seed)
    control_abs: list[float] = []

    for _trial in range(trials):
        shuffled = shuffled_within_shell(target_residuals, groups, rng)
        control_abs.append(abs(pearson_correlation(metric_residuals, shuffled) or 0.0))

    ge_count = sum(1 for value in control_abs if value >= abs(observed_r))
    return {
        "metric": metric,
        "target": target,
        "observed_r": observed_r,
        "control_mean_abs": mean(control_abs),
        "control_max_abs": max(control_abs),
        "control_ge_count": ge_count,
        "p_upper": (ge_count + 1) / (trials + 1),
        "trials": trials,
    }


def control_rows(controls: list[dict[str, object]]) -> list[list[object]]:
    return [
        [
            control["metric"],
            control["target"],
            f"{control['observed_r']:.4f}",
            f"{control['control_mean_abs']:.4f}",
            f"{control['control_max_abs']:.4f}",
            f"{control['control_ge_count']}/{control['trials']}",
            f"{control['p_upper']:.4f}",
        ]
        for control in controls
    ]


def write_report(
    report_path: Path,
    dataset: list[dict[str, float]],
    controls: list[dict[str, object]],
    limit: int,
    trials: int,
    seed: int,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Goldbach-Neighborhood Residual Transfer Test (C2)",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                f"**Script:** `experiments/goldbach_neighborhood_transfer.py`",
                f"**Range:** even integers `4..{limit}`",
                f"**Controls:** `{trials}` shell shuffles, seed `{seed}`",
                "",
                "## Purpose",
                "",
                "This report executes an additive C2 (Transfer After Mechanism) target",
                "of the Origin-Pakheta proof program for the prime-neighborhood operators.",
                "",
                "It tests whether the log gaps of the compression commutators ($C/N_-$ and $C/N_+$)",
                "predict the fluctuations of Goldbach witness densities around the classical",
                "Hardy-Littlewood singular series baseline, after removing size and emanation shell depth.",
                "",
                "## Transfer Controls",
                "",
                "All variables are shell-conditioned and residualized against `log(n)`. Controls",
                "shuffle targets within emanation shells to break coordinate alignment.",
                "",
                markdown_table(
                    [
                        "metric",
                        "target",
                        "observed_r",
                        "ctrl_mean_abs",
                        "ctrl_max_abs",
                        "ctrl_ge",
                        "p_upper",
                    ],
                    control_rows(controls),
                ),
                "",
                "## Interpretation",
                "",
                "A successful transfer requires the observed correlation to beat the shuffled",
                "controls significantly ($p < 0.05$).",
                "",
                "If the path gaps predict Goldbach residuals, it proves that the boundary gaps",
                "of $N_-$ and $N_+$ hold information that couples to additive prime distributions,",
                "demonstrating that the calculus has reach in both modular and additive number theory.",
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
    report_path: Path,
) -> dict[str, object]:
    dataset = goldbach_neighborhood_transfer_dataset(limit)
    controls = [
        transfer_control(
            dataset,
            metric,
            target,
            trials=trials,
            seed=seed + (index * 100),
        )
        for index, (metric, _) in enumerate(METRICS)
        for target, _ in TRANSFER_TARGETS
    ]
    write_report(
        report_path,
        dataset,
        controls,
        limit=limit,
        trials=trials,
        seed=seed,
    )
    return {
        "rows": len(dataset),
        "controls": controls,
        "report_path": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--trials", type=int, default=250)
    parser.add_argument("--seed", type=int, default=62426)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "GOLDBACH_NEIGHBORHOOD_TRANSFER.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_experiment(
        limit=args.limit,
        trials=args.trials,
        seed=args.seed,
        report_path=args.report,
    )
    print(f"rows: {result['rows']}")
    print(f"report: {result['report_path']}")


if __name__ == "__main__":
    main()
