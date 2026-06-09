"""First executable Origin-Pakheta calculus scan."""

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
    divisor_count,
    factor_counter,
    modular_return_decomposition,
    radical,
)
from emanation_from_1.origin_metrics import origin_profile  # noqa: E402
from emanation_from_1.origin_pakheta import (  # noqa: E402
    compression_carmichael_lambda_commutator,
    compression_carmichael_lambda_gap_factor,
    compression_divisor_branching_commutator,
    compression_divisor_branching_gap_factor,
    compression_euler_totient_commutator,
    compression_euler_totient_gap_factor,
    compression_gather_commutator,
    compression_gather_gap_factor,
    compression_prime_minus_neighborhood_commutator,
    compression_prime_minus_neighborhood_gap_factor,
    compression_prime_plus_neighborhood_commutator,
    compression_prime_plus_neighborhood_gap_factor,
    compression_prime_return_commutator,
    compression_prime_return_gap_factor,
    compression_prime_set_return_commutator,
    compression_prime_set_return_gap_factor,
    compression_return_commutator,
    compression_return_gap_factor,
    return_prime_set_divisor_branching_commutator,
    return_prime_set_divisor_branching_gap_factor,
    return_prime_set_prime_minus_neighborhood_commutator,
    return_prime_set_prime_minus_neighborhood_gap_factor,
    return_prime_set_prime_plus_neighborhood_commutator,
    return_prime_set_prime_plus_neighborhood_gap_factor,
)
from emanation_from_1.statistics import mean, pearson_correlation  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    shell_conditioned_residuals,
    shell_groups,
    shuffled_within_shell,
)


GATHER_PRIMES = [2, 3, 5]
RETURN_PRIMES = [2, 3, 5, 7]
RETURN_PRIME_SETS = [(2, 3), (2, 3, 5), (3, 5, 7)]
PATH_TARGETS = [
    ("compression_return_log_gap", "radical_compression"),
    ("return_2_log_gap", "repeated_factor_2"),
    ("return_3_log_gap", "repeated_factor_3"),
    ("return_5_log_gap", "repeated_factor_5"),
    ("return_7_log_gap", "repeated_factor_7"),
    ("gather_2_log_gap", "has_factor_2"),
    ("gather_3_log_gap", "has_factor_3"),
    ("gather_5_log_gap", "has_factor_5"),
    ("compression_divisor_branching_log_gap", "radical_compression"),
    ("compression_carmichael_lambda_log_gap", "radical_compression"),
    ("compression_totient_log_gap", "radical_compression"),
    ("compression_prime_minus_neighborhood_log_gap", "radical_compression"),
    ("compression_prime_plus_neighborhood_log_gap", "radical_compression"),
]


def prime_set_key(primes: tuple[int, ...]) -> str:
    return "_".join(str(prime) for prime in primes)


def prime_set_symbol(primes: tuple[int, ...]) -> str:
    return "{" + ",".join(str(prime) for prime in primes) + "}"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def fraction_log_abs(value: Fraction) -> float:
    if value == 1:
        return 0.0
    return abs(log(value.numerator) - log(value.denominator))


def calculus_dataset(limit: int) -> list[dict[str, float]]:
    """Return rows for the first Origin-Pakheta calculus scan."""
    if limit < 2:
        raise ValueError("limit must be >= 2")

    rows: list[dict[str, float]] = []
    for n in range(2, limit + 1):
        counter = dict(factor_counter(n))
        least_prime = min(counter)
        profile = origin_profile(n)
        decomposition = modular_return_decomposition(n)
        compression_return = compression_return_commutator(n)

        row = {
            "n": float(n),
            "log_n": log(n),
            "emanation_depth": float(profile.emanation_depth),
            "component_count": float(decomposition.component_count),
            "divisor_count": float(divisor_count(n)),
            "radical_compression": 1.0 - (radical(n) / n),
            "least_prime": float(least_prime),
            "least_prime_log": log(least_prime),
            "least_prime_exponent": float(counter[least_prime]),
            "least_prime_repeated": 1.0 if counter[least_prime] > 1 else 0.0,
            "overlap_pressure_log": log(float(decomposition.overlap_penalty)),
            "compression_return_log_gap": compression_return.log_abs_gap,
            "compression_return_commutes": 1.0 if compression_return.commutes else 0.0,
        }
        for prime in RETURN_PRIMES:
            commutator = compression_prime_return_commutator(n, prime)
            exponent = counter.get(prime, 0)
            row[f"factor_{prime}_exponent"] = float(exponent)
            row[f"repeated_factor_{prime}"] = 1.0 if exponent > 1 else 0.0
            row[f"return_{prime}_log_gap"] = commutator.log_abs_gap
            row[f"return_{prime}_commutes"] = 1.0 if commutator.commutes else 0.0
        for prime in GATHER_PRIMES:
            commutator = compression_gather_commutator(n, prime)
            row[f"has_factor_{prime}"] = 1.0 if n % prime == 0 else 0.0
            row[f"gather_{prime}_log_gap"] = commutator.log_abs_gap
            row[f"gather_{prime}_commutes"] = 1.0 if commutator.commutes else 0.0
        
        c_b = compression_divisor_branching_commutator(n)
        row["compression_divisor_branching_log_gap"] = c_b.log_abs_gap
        row["compression_divisor_branching_commutes"] = 1.0 if c_b.commutes else 0.0
        
        c_m = compression_carmichael_lambda_commutator(n)
        row["compression_carmichael_lambda_log_gap"] = c_m.log_abs_gap
        row["compression_carmichael_lambda_commutes"] = 1.0 if c_m.commutes else 0.0
        
        c_t = compression_euler_totient_commutator(n)
        row["compression_totient_log_gap"] = c_t.log_abs_gap
        row["compression_totient_commutes"] = 1.0 if c_t.commutes else 0.0

        c_nm = compression_prime_minus_neighborhood_commutator(n)
        row["compression_prime_minus_neighborhood_log_gap"] = c_nm.log_abs_gap
        row["compression_prime_minus_neighborhood_commutes"] = 1.0 if c_nm.commutes else 0.0

        c_np = compression_prime_plus_neighborhood_commutator(n)
        row["compression_prime_plus_neighborhood_log_gap"] = c_np.log_abs_gap
        row["compression_prime_plus_neighborhood_commutes"] = 1.0 if c_np.commutes else 0.0

        rows.append(row)
    return rows


def formula_check(limit: int) -> dict[str, int]:
    """Return formula mismatch counts for the v0 commutator identities."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    compression_return_mismatches = 0
    selected_return_mismatches = {prime: 0 for prime in RETURN_PRIMES}
    selected_set_return_mismatches = {
        prime_set: 0 for prime_set in RETURN_PRIME_SETS
    }
    gather_mismatches = {prime: 0 for prime in GATHER_PRIMES}
    compression_divisor_branching_mismatches = 0
    return_prime_set_divisor_branching_mismatches = {
        prime_set: 0 for prime_set in RETURN_PRIME_SETS
    }
    compression_carmichael_lambda_mismatches = 0
    compression_totient_mismatches = 0
    compression_prime_minus_neighborhood_mismatches = 0
    return_prime_set_prime_minus_neighborhood_mismatches = {
        prime_set: 0 for prime_set in RETURN_PRIME_SETS
    }
    compression_prime_plus_neighborhood_mismatches = 0
    return_prime_set_prime_plus_neighborhood_mismatches = {
        prime_set: 0 for prime_set in RETURN_PRIME_SETS
    }
    for n in range(1, limit + 1):
        compression_return = compression_return_commutator(n)
        expected_return = Fraction(compression_return_gap_factor(n), 1)
        if compression_return.ratio != expected_return:
            compression_return_mismatches += 1

        for prime in RETURN_PRIMES:
            selected_return = compression_prime_return_commutator(n, prime)
            expected_selected = Fraction(
                compression_prime_return_gap_factor(n, prime),
                1,
            )
            if selected_return.ratio != expected_selected:
                selected_return_mismatches[prime] += 1

        for prime_set in RETURN_PRIME_SETS:
            selected_set_return = compression_prime_set_return_commutator(
                n,
                prime_set,
            )
            expected_selected_set = Fraction(
                compression_prime_set_return_gap_factor(n, prime_set),
                1,
            )
            if selected_set_return.ratio != expected_selected_set:
                selected_set_return_mismatches[prime_set] += 1

        for prime in GATHER_PRIMES:
            gather = compression_gather_commutator(n, prime)
            if gather.ratio != compression_gather_gap_factor(n, prime):
                gather_mismatches[prime] += 1

        c_b = compression_divisor_branching_commutator(n)
        if c_b.ratio != compression_divisor_branching_gap_factor(n):
            compression_divisor_branching_mismatches += 1

        for prime_set in RETURN_PRIME_SETS:
            r_s_b = return_prime_set_divisor_branching_commutator(n, prime_set)
            if r_s_b.ratio != return_prime_set_divisor_branching_gap_factor(n, prime_set):
                return_prime_set_divisor_branching_mismatches[prime_set] += 1

        c_m = compression_carmichael_lambda_commutator(n)
        if c_m.ratio != compression_carmichael_lambda_gap_factor(n):
            compression_carmichael_lambda_mismatches += 1

        c_t = compression_euler_totient_commutator(n)
        if c_t.ratio != compression_euler_totient_gap_factor(n):
            compression_totient_mismatches += 1

        c_nm = compression_prime_minus_neighborhood_commutator(n)
        if c_nm.ratio != compression_prime_minus_neighborhood_gap_factor(n):
            compression_prime_minus_neighborhood_mismatches += 1

        for prime_set in RETURN_PRIME_SETS:
            r_s_nm = return_prime_set_prime_minus_neighborhood_commutator(n, prime_set)
            if r_s_nm.ratio != return_prime_set_prime_minus_neighborhood_gap_factor(n, prime_set):
                return_prime_set_prime_minus_neighborhood_mismatches[prime_set] += 1

        c_np = compression_prime_plus_neighborhood_commutator(n)
        if c_np.ratio != compression_prime_plus_neighborhood_gap_factor(n):
            compression_prime_plus_neighborhood_mismatches += 1

        for prime_set in RETURN_PRIME_SETS:
            r_s_np = return_prime_set_prime_plus_neighborhood_commutator(n, prime_set)
            if r_s_np.ratio != return_prime_set_prime_plus_neighborhood_gap_factor(n, prime_set):
                return_prime_set_prime_plus_neighborhood_mismatches[prime_set] += 1

    return {
        "limit": limit,
        "compression_return_mismatches": compression_return_mismatches,
        **{
            f"return_{prime}_mismatches": selected_return_mismatches[prime]
            for prime in RETURN_PRIMES
        },
        **{
            f"return_set_{prime_set_key(prime_set)}_mismatches": (
                selected_set_return_mismatches[prime_set]
            )
            for prime_set in RETURN_PRIME_SETS
        },
        **{
            f"gather_{prime}_mismatches": gather_mismatches[prime]
            for prime in GATHER_PRIMES
        },
        "compression_divisor_branching_mismatches": compression_divisor_branching_mismatches,
        **{
            f"return_set_divisor_branching_{prime_set_key(prime_set)}_mismatches": (
                return_prime_set_divisor_branching_mismatches[prime_set]
            )
            for prime_set in RETURN_PRIME_SETS
        },
        "compression_carmichael_lambda_mismatches": compression_carmichael_lambda_mismatches,
        "compression_totient_mismatches": compression_totient_mismatches,
        "compression_prime_minus_neighborhood_mismatches": compression_prime_minus_neighborhood_mismatches,
        **{
            f"return_set_prime_minus_neighborhood_{prime_set_key(prime_set)}_mismatches": (
                return_prime_set_prime_minus_neighborhood_mismatches[prime_set]
            )
            for prime_set in RETURN_PRIME_SETS
        },
        "compression_prime_plus_neighborhood_mismatches": compression_prime_plus_neighborhood_mismatches,
        **{
            f"return_set_prime_plus_neighborhood_{prime_set_key(prime_set)}_mismatches": (
                return_prime_set_prime_plus_neighborhood_mismatches[prime_set]
            )
            for prime_set in RETURN_PRIME_SETS
        },
    }


def path_summary_rows(dataset: list[dict[str, float]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for target, _metric in PATH_TARGETS:
        values = [row[target] for row in dataset]
        nonzero = [value for value in values if value > 0]
        rows.append(
            [
                target,
                f"{len(nonzero)}/{len(values)}",
                f"{len(nonzero) / len(values):.4f}",
                f"{mean(values):.4f}",
                f"{max(values):.4f}",
            ]
        )
    return rows


def path_control(
    dataset: list[dict[str, float]],
    target: str,
    metric: str,
    trials: int,
    seed: int,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be >= 1")

    target_values = shell_conditioned_residuals(dataset, target, ["log_n"])
    metric_values = shell_conditioned_residuals(dataset, metric, ["log_n"])
    observed_r = pearson_correlation(metric_values, target_values)
    if observed_r is None:
        raise ValueError(f"undefined path correlation for {target}")

    groups = shell_groups(dataset)
    rng = Random(seed)
    control_abs: list[float] = []
    for _trial in range(trials):
        shuffled = shuffled_within_shell(target_values, groups, rng)
        control_abs.append(abs(pearson_correlation(metric_values, shuffled) or 0.0))

    ge_count = sum(1 for value in control_abs if value >= abs(observed_r))
    return {
        "target": target,
        "metric": metric,
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
            control["target"],
            control["metric"],
            f"{control['observed_r']:.4f}",
            f"{control['control_mean_abs']:.4f}",
            f"{control['control_max_abs']:.4f}",
            f"{control['control_ge_count']}/{control['trials']}",
            f"{control['p_upper']:.4f}",
        ]
        for control in controls
    ]


def example_rows(dataset: list[dict[str, float]], count: int) -> list[list[object]]:
    ranked = sorted(
        dataset,
        key=lambda row: (
            row["compression_return_log_gap"],
            row["least_prime_repeated"],
            row["radical_compression"],
            -row["n"],
        ),
        reverse=True,
    )
    return [
        [
            int(row["n"]),
            int(row["emanation_depth"]),
            int(row["least_prime"]),
            int(row["least_prime_exponent"]),
            f"{row['radical_compression']:.4f}",
            f"{row['compression_return_log_gap']:.4f}",
            f"{row['gather_2_log_gap']:.4f}",
            f"{row['gather_3_log_gap']:.4f}",
        ]
        for row in ranked[:count]
    ]


def formula_rows(check: dict[str, int]) -> list[list[object]]:
    return [
        [
            "C/R_min",
            "`C(R_min(n)) / R_min(C(n)) = spf(n) if v_{spf(n)}(n) > 1 else 1`",
            check["compression_return_mismatches"],
        ],
        *[
            [
                f"C/R_{prime}",
                f"`C(R_{prime}(n)) / R_{prime}(C(n)) = {prime} if v_{prime}(n) > 1 else 1`",
                check[f"return_{prime}_mismatches"],
            ]
            for prime in RETURN_PRIMES
        ],
        *[
            [
                f"C/R_{prime_set_symbol(prime_set)}",
                "`C(R_S(n)) / R_S(C(n)) = product of selected repeated primes`",
                check[f"return_set_{prime_set_key(prime_set)}_mismatches"],
            ]
            for prime_set in RETURN_PRIME_SETS
        ],
        *[
            [
                f"C/G_{prime}",
                f"`C(G_{prime}(n)) / G_{prime}(C(n)) = 1/{prime} if {prime} divides n else 1`",
                check[f"gather_{prime}_mismatches"],
            ]
            for prime in GATHER_PRIMES
        ],
        [
            "C/B",
            "`C(B(n)) / B(C(n)) = rad(d(n)) / 2^omega(n)`",
            check["compression_divisor_branching_mismatches"],
        ],
        *[
            [
                f"R_{prime_set_symbol(prime_set)}/B",
                "`R_S(B(n)) / B(R_S(n)) = formula with rad_S(d(n))`",
                check[f"return_set_divisor_branching_{prime_set_key(prime_set)}_mismatches"],
            ]
            for prime_set in RETURN_PRIME_SETS
        ],
        [
            "C/M",
            "`C(M(n)) / M(C(n)) = lcm formula`",
            check["compression_carmichael_lambda_mismatches"],
        ],
        [
            "C/T",
            "`C(T(n)) / T(C(n)) = rad(phi(n)) / phi(rad(n))`",
            check["compression_totient_mismatches"],
        ],
        [
            "C/N_-",
            "`C(N_-(n)) / N_-(C(n)) = rad(N_-(n)) / N_-(n)`",
            check["compression_prime_minus_neighborhood_mismatches"],
        ],
        *[
            [
                f"R_{prime_set_symbol(prime_set)}/N_-",
                "`R_S(N_-(n)) / N_-(R_S(n)) = formula with rad_S(N_-(n))`",
                check[f"return_set_prime_minus_neighborhood_{prime_set_key(prime_set)}_mismatches"],
            ]
            for prime_set in RETURN_PRIME_SETS
        ],
        [
            "C/N_+",
            "`C(N_+(n)) / N_+(C(n)) = rad(N_+(n)) / N_+(n)`",
            check["compression_prime_plus_neighborhood_mismatches"],
        ],
        *[
            [
                f"R_{prime_set_symbol(prime_set)}/N_+",
                "`R_S(N_+(n)) / N_+(R_S(n)) = formula with rad_S(N_+(n))`",
                check[f"return_set_prime_plus_neighborhood_{prime_set_key(prime_set)}_mismatches"],
            ]
            for prime_set in RETURN_PRIME_SETS
        ],
    ]


def write_report(
    report_path: Path,
    dataset: list[dict[str, float]],
    check: dict[str, int],
    controls: list[dict[str, object]],
    limit: int,
    trials: int,
    seed: int,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Origin-Pakheta Calculus v0 Scan",
                "",
                f"**Generated (UTC):** {datetime.now(timezone.utc).date().isoformat()}",
                f"**Script:** `experiments/origin_pakheta_calculus.py`",
                f"**Range:** `2..{limit}`",
                f"**Controls:** `{trials}` shell shuffles, seed `{seed}`",
                "",
                "## Purpose",
                "",
                "This is the first executable Origin-Pakheta calculus. It treats",
                "positive integers as relationship-fields and exact arithmetic",
                "maps as contexts. The first usable object is a path commutator:",
                "",
                "```text",
                "Delta(A, B; n) = A(B(n)) / B(A(n))",
                "```",
                "",
"If `Delta = 1`, the two contexts commute at `n`. If not, the",
                "integer field remembers the path order.",
                "",
                "## v0 Operators",
                "",
                "| Symbol | Definition | Pakheta reading |",
                "| --- | --- | --- |",
                "| `C(n)` | `rad(n)` | compression / squarefree field skeleton |",
                "| `R_min(n)` | remove one least-prime factor | return one layer toward `1` |",
                "| `R_p(n)` | remove one selected `p` layer if present | selected return context |",
                "| `G_p(n)` | `p * n` for prime `p` | gather one prime facet into the field |",
                "| `B(n)` | `divisor_count(n)` | divisor-branching context |",
                "| `M(n)` | `carmichael_lambda(n)` | modular-return exponent/period context |",
                "| `T(n)` | `euler_totient(n)` | modular-return size/density context |",
                "| `Delta(A,B;n)` | `A(B(n)) / B(A(n))` | path-order residue |",
                "",
                "## Exact Formula Checks",
                "",
                markdown_table(
                    ["commutator", "identity", "mismatches"],
                    formula_rows(check),
                ),
                "",
                "## Path-Sensitivity Summary",
                "",
                markdown_table(
                    ["path_gap", "nonzero", "rate", "mean_log_gap", "max_log_gap"],
                    path_summary_rows(dataset),
                ),
                "",
                "## Shell-Controlled Signals",
                "",
                "Targets and metrics are shell-centered and residualized against",
                "`log(n)`. Controls shuffle target residuals within emanation shells.",
                "",
                markdown_table(
                    [
                        "target",
                        "metric",
                        "observed_r",
                        "ctrl_mean_abs",
                        "ctrl_max_abs",
                        "ctrl_ge",
                        "p_upper",
                    ],
                    control_rows(controls),
                ),
                "",
                "## Largest C/R_min Path Gaps",
                "",
                markdown_table(
                    [
                        "n",
                        "Omega",
                        "spf",
                        "v_spf",
                        "radical_compression",
                        "C_R_gap",
                        "C_G2_gap",
                        "C_G3_gap",
                    ],
                    example_rows(dataset, 12),
                ),
                "",
                "## Interpretation",
                "",
                "This is new math in the working sense: we now have named operators,",
                "an exact commutator, theorem candidates, executable scans, and",
                "controls. The strongest v0 result is simple but useful:",
                "",
                "```text",
                "compress then return != return then compress",
                "exactly when the least-prime return layer is repeated",
                "```",
                "",
                "The selected-prime return family generalizes this:",
                "",
                "```text",
                "compress then R_p != R_p then compress",
                "exactly when the chosen p-layer is repeated",
                "```",
                "",
                "That gives the Origin-Pakheta program a first path-sensitive",
                "calculus. It does not prove the full Origin Reframe, but it creates",
                "a usable formal surface where Pakheta ideas become exact arithmetic.",
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
    dataset = calculus_dataset(limit)
    check = formula_check(limit)
    controls = [
        path_control(
            dataset,
            target,
            metric,
            trials=trials,
            seed=seed + index,
        )
        for index, (target, metric) in enumerate(PATH_TARGETS)
    ]
    write_report(
        report_path,
        dataset,
        check,
        controls,
        limit=limit,
        trials=trials,
        seed=seed,
    )
    return {
        "rows": len(dataset),
        "check": check,
        "controls": controls,
        "report_path": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--trials", type=int, default=250)
    parser.add_argument("--seed", type=int, default=62226)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_PAKHETA_CALCULUS.md",
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
