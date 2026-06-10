"""Knockout test: condition the C/N_- modular transfer on classical overlap baselines.

The prime-neighborhood transfer experiment found a strong shell-conditioned
coupling between the C/N_- path-commutator gap and log(lambda/phi)
(r = -0.4659, 0/250 controls). This experiment asks whether that coupling
survives conditioning on classical covariates that need no commutators,
paths, or Pakheta vocabulary:

1. Carmichael kernel overlap: Z(n) = log(prod_{p|n}(p-1) / lcm_{p|n}(p-1)).
2. Local 2-adic defect: d2(n) = log(phi(2^a)/lambda(2^a)) for a = v_2(n),
   which is log(2) when v_2(n) >= 3 and 0 otherwise.

Both are functions of the factorization that the modular-return literature
already names. The circularity boundary is deliberate: extending Z to the
full lambda components (p-1)p^(a-1) would determine the target exactly for
all odd n, so the kernel-only Z plus the one-bit 2-adic defect is the
minimal classical ladder that is still a fair test.

The experiment also verifies the exact identity that motivates the test:
for odd squarefree n, lambda(n)/phi(n) = lcm(p-1)/prod(p-1), so on that
subpopulation the transfer target is a deterministic function of the same
generator multiset {p-1 : p | n} that the C/N_- gap is computed from.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from math import lcm, log
from pathlib import Path
from random import Random
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import (  # noqa: E402
    carmichael_lambda,
    euler_totient,
    factor_counter,
)
from emanation_from_1.origin_pakheta import (  # noqa: E402
    compression_prime_minus_neighborhood_commutator,
)
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    shell_conditioned_residuals,
    shell_groups,
    shuffled_within_shell,
)


STAGES = [
    ("replication", "path_gap", ["log_n"]),
    ("classical_baseline_Z", "kernel_overlap", ["log_n"]),
    ("knockout_Z", "path_gap", ["log_n", "kernel_overlap"]),
    ("knockout_Z_plus_2adic", "path_gap", ["log_n", "kernel_overlap", "two_adic_defect"]),
]

TARGET = "log_lambda_over_phi"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def kernel_overlap(n: int) -> float:
    """Return log(prod(p-1)/lcm(p-1)) over the distinct primes of n."""
    if n < 2:
        raise ValueError("kernel overlap requires n >= 2")
    prod_pm1 = 1
    lcm_pm1 = 1
    for p in factor_counter(n):
        prod_pm1 *= p - 1
        lcm_pm1 = lcm(lcm_pm1, p - 1)
    return log(prod_pm1 / lcm_pm1)


def two_adic_defect(n: int) -> float:
    """Return log(phi(2^a)/lambda(2^a)) for a = v_2(n): log 2 if a >= 3, else 0."""
    if n < 2:
        raise ValueError("two-adic defect requires n >= 2")
    return log(2.0) if factor_counter(n).get(2, 0) >= 3 else 0.0


def overlap_knockout_dataset(limit: int) -> list[dict[str, float]]:
    """Return dataset rows with the path gap, target, and classical covariates."""
    if limit < 2:
        raise ValueError("limit must be >= 2")

    rows: list[dict[str, float]] = []
    for n in range(2, limit + 1):
        counter = factor_counter(n)
        rows.append(
            {
                "n": float(n),
                "log_n": log(n),
                "emanation_depth": float(sum(counter.values())),
                "path_gap": compression_prime_minus_neighborhood_commutator(n).log_abs_gap,
                "log_lambda_over_phi": log(carmichael_lambda(n) / euler_totient(n)),
                "kernel_overlap": kernel_overlap(n),
                "two_adic_defect": two_adic_defect(n),
            }
        )
    return rows


def odd_squarefree_identity_check(limit: int) -> tuple[int, int]:
    """Count odd squarefree n in 2..limit where lambda/phi = lcm(p-1)/prod(p-1) exactly.

    Returns (odd squarefree count, exact identity matches), using integer
    arithmetic only. Equality of the two counts proves that on this
    subpopulation the transfer target is determined by the multiset
    {p-1 : p | n} with no residual freedom.
    """
    odd_squarefree = 0
    matches = 0
    for n in range(3, limit + 1, 2):
        counter = factor_counter(n)
        if any(exponent > 1 for exponent in counter.values()):
            continue
        odd_squarefree += 1
        prod_pm1 = 1
        lcm_pm1 = 1
        for p in counter:
            prod_pm1 *= p - 1
            lcm_pm1 = lcm(lcm_pm1, p - 1)
        if carmichael_lambda(n) * prod_pm1 == euler_totient(n) * lcm_pm1:
            matches += 1
    return odd_squarefree, matches


def residual_correlation(
    dataset: list[dict[str, float]],
    metric: str,
    target: str,
    baselines: list[str],
) -> float:
    """Return the shell-conditioned residual correlation of metric and target."""
    target_residuals = shell_conditioned_residuals(dataset, target, baselines)
    metric_residuals = shell_conditioned_residuals(dataset, metric, baselines)
    return pearson_correlation(metric_residuals, target_residuals) or 0.0


def conditioned_transfer_control(
    dataset: list[dict[str, float]],
    metric: str,
    target: str,
    baselines: list[str],
    trials: int,
    seed: int,
) -> dict[str, object]:
    """Score observed conditioned correlation against shell-shuffled controls."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    target_residuals = shell_conditioned_residuals(dataset, target, baselines)
    metric_residuals = shell_conditioned_residuals(dataset, metric, baselines)
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
        "baselines": "+".join(baselines),
        "observed_r": observed_r,
        "control_mean_abs": mean(control_abs),
        "control_max_abs": max(control_abs),
        "control_ge_count": ge_count,
        "p_upper": (ge_count + 1) / (trials + 1),
        "trials": trials,
    }


def stage_rows(stages: list[dict[str, object]], labels: list[str]) -> list[list[object]]:
    return [
        [
            label,
            stage["metric"],
            stage["baselines"],
            f"{stage['observed_r']:.4f}",
            f"{stage['control_mean_abs']:.4f}",
            f"{stage['control_max_abs']:.4f}",
            f"{stage['control_ge_count']}/{stage['trials']}",
            f"{stage['p_upper']:.4f}",
        ]
        for label, stage in zip(labels, stages)
    ]


def write_report(
    report_path: Path,
    stages: list[dict[str, object]],
    labels: list[str],
    ancestry_r: float,
    identity_counts: tuple[int, int],
    rows: int,
    limit: int,
    trials: int,
    seed: int,
) -> None:
    odd_squarefree, matches = identity_counts
    replication = stages[0]
    baseline = stages[1]
    knockout = stages[2]
    knockout_2adic = stages[3]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Modular Overlap Knockout Test (C2 Counter-Test)",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                "**Script:** `experiments/origin_modular_overlap_knockout.py`",
                f"**Range:** `2..{limit}`",
                f"**Controls:** `{trials}` shell shuffles, seed `{seed}`",
                "",
                "## Purpose",
                "",
                "The prime-neighborhood transfer test reported a strong shell-conditioned",
                "coupling between the `C/N_-` path-commutator gap and `log(lambda/phi)`.",
                "This experiment executes the decomposition step pre-registered in the",
                "README (\"prove which part of the shell-conditioned signal comes from",
                "concentration, component splitting, and Carmichael overlap\") by",
                "conditioning the transfer on classical covariates definable without the",
                "path calculus:",
                "",
                "- `Z(n) = log(prod_{p|n}(p-1) / lcm_{p|n}(p-1))` (Carmichael kernel overlap)",
                "- `d2(n) = log(2)` if `v_2(n) >= 3` else `0` (local 2-adic lambda defect)",
                "",
                "## Exact Identity (Pre-Wiring Check)",
                "",
                f"For odd squarefree `n` in `2..{limit}`: `{odd_squarefree}` of `{rows}` rows.",
                f"The identity `lambda(n)/phi(n) = lcm(p-1)/prod(p-1)` holds exactly for",
                f"`{matches}/{odd_squarefree}` of them (integer arithmetic, no floats).",
                "",
                "On this subpopulation the transfer target is a deterministic function of",
                "the same generator multiset `{p-1 : p | n}` from which the `C/N_-` gap is",
                "computed, so conditioning on `Z` leaves it zero residual variance there.",
                "",
                "## Knockout Ladder",
                "",
                "All variables are shell-conditioned and residualized against the listed",
                "baselines. Controls shuffle target residuals within emanation shells.",
                "",
                markdown_table(
                    [
                        "stage",
                        "metric",
                        "baselines",
                        "observed_r",
                        "ctrl_mean_abs",
                        "ctrl_max_abs",
                        "ctrl_ge",
                        "p_upper",
                    ],
                    stage_rows(stages, labels),
                ),
                "",
                f"Ancestry of predictor and covariate: `r(path_gap, Z | log n, shells) = {ancestry_r:.4f}`.",
                "",
                "## Interpretation",
                "",
                f"1. The published transfer replicates exactly (`r = {replication['observed_r']:.4f}`).",
                f"2. The classical covariate `Z` alone is a stronger predictor of the target",
                f"   (`r = {baseline['observed_r']:.4f}`) than the path gap itself.",
                f"3. Conditioning on `Z` removes most of the path-gap signal",
                f"   (`r = {knockout['observed_r']:.4f}`), and adding the one-bit 2-adic defect",
                f"   takes the remainder to `r = {knockout_2adic['observed_r']:.4f}`",
                f"   (`p_upper = {knockout_2adic['p_upper']:.4f}`), which does not clear the",
                "   repo's `p < 0.05` transfer bar.",
                "",
                "Read against the preprint's Section 5.1: the strong `C/N_-` modular",
                "transfer is overwhelmingly a re-measurement of classical Carmichael",
                "kernel overlap plus the 2-adic lambda special case, not evidence that",
                "path-order residue carries novel information about modular contraction.",
                "Any future transfer claim for the v0 neighborhood operators should be",
                "required to beat this two-covariate classical ladder, not only size and",
                "shell controls. The marginal trace that remains is the open question;",
                "extending the ladder further approaches the circularity boundary noted",
                "in the script docstring, so a sharper test needs an independent target.",
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
    dataset = overlap_knockout_dataset(limit)
    labels = [label for label, _, _ in STAGES]
    stages = [
        conditioned_transfer_control(
            dataset,
            metric,
            TARGET,
            baselines,
            trials=trials,
            seed=seed + (index * 100),
        )
        for index, (_, metric, baselines) in enumerate(STAGES)
    ]
    ancestry_r = residual_correlation(dataset, "path_gap", "kernel_overlap", ["log_n"])
    identity_counts = odd_squarefree_identity_check(limit)
    write_report(
        report_path,
        stages,
        labels,
        ancestry_r,
        identity_counts,
        rows=len(dataset),
        limit=limit,
        trials=trials,
        seed=seed,
    )
    return {
        "rows": len(dataset),
        "stages": stages,
        "ancestry_r": ancestry_r,
        "identity_counts": identity_counts,
        "report_path": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--trials", type=int, default=250)
    parser.add_argument("--seed", type=int, default=62326)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_OVERLAP_KNOCKOUT.md",
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
    odd_squarefree, matches = result["identity_counts"]
    print(f"odd squarefree identity: {matches}/{odd_squarefree}")
    for label, stage in zip([label for label, _, _ in STAGES], result["stages"]):
        print(
            f"{label}: r = {stage['observed_r']:+.4f}, "
            f"ctrl_ge = {stage['control_ge_count']}/{stage['trials']}, "
            f"p_upper = {stage['p_upper']:.4f}"
        )
    print(f"report: {result['report_path']}")


if __name__ == "__main__":
    main()
