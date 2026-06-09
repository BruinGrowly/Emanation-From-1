"""Probe theorem candidates behind modular return compression."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import (  # noqa: E402
    carmichael_lambda,
    factor_counter,
    lambda_phi_ratio as exact_lambda_phi_ratio,
    modular_return_decomposition,
    radical,
)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def factor_shape(n: int) -> str:
    counter = factor_counter(n)
    if not counter:
        return "1"
    return " * ".join(
        str(prime) if exponent == 1 else f"{prime}^{exponent}"
        for prime, exponent in sorted(counter.items())
    )


def lambda_phi_ratio(n: int) -> Fraction:
    return exact_lambda_phi_ratio(n)


def component_formula_ratio(n: int) -> Fraction:
    decomposition = modular_return_decomposition(n)
    return decomposition.local_defect_ratio / decomposition.overlap_penalty


def distinct_odd_prime_bound(n: int) -> Fraction:
    return modular_return_decomposition(n).odd_distinct_prime_bound


def verify_component_formula(limit: int) -> tuple[int, int | None]:
    checked = 0
    for n in range(1, limit + 1):
        expected = lambda_phi_ratio(n)
        formula = component_formula_ratio(n)
        checked += 1
        if expected != formula:
            return checked, n
    return checked, None


def verify_odd_bound(limit: int) -> tuple[int, int | None]:
    checked = 0
    for n in range(3, limit + 1, 2):
        checked += 1
        if lambda_phi_ratio(n) > distinct_odd_prime_bound(n):
            return checked, n
    return checked, None


def verify_coprime_product_law(limit: int) -> tuple[int, tuple[int, int] | None]:
    checked = 0
    for a in range(2, limit + 1):
        for b in range(2, limit + 1):
            if gcd(a, b) != 1:
                continue
            checked += 1
            left = lambda_phi_ratio(a * b)
            right = lambda_phi_ratio(a) * lambda_phi_ratio(b) / gcd(
                carmichael_lambda(a),
                carmichael_lambda(b),
            )
            if left != right:
                return checked, (a, b)
    return checked, None


def monotonicity_counterexamples(limit: int, max_shell: int) -> list[list[object]]:
    examples: list[list[object]] = []
    for shell in range(2, max_shell + 1):
        values: list[tuple[float, float, int]] = []
        for n in range(2, limit + 1):
            if sum(factor_counter(n).values()) != shell:
                continue
            compression = 1 - (radical(n) / n)
            values.append((compression, lambda_phi_ratio(n), n))

        values.sort()
        best_ratio = -1.0
        best_item: tuple[float, float, int] | None = None
        for compression, ratio, n in values:
            if best_item is not None and best_ratio > ratio + 1e-12:
                examples.append(
                    [
                        shell,
                        best_item[2],
                        f"{best_item[0]:.4f}",
                        f"{float(best_item[1]):.4f}",
                        n,
                        f"{compression:.4f}",
                        f"{float(ratio):.4f}",
                    ]
                )
                break
            if ratio > best_ratio:
                best_ratio = ratio
                best_item = (compression, ratio, n)
    return examples


def endpoint_rows(max_shell: int) -> list[list[object]]:
    rows: list[list[object]] = []
    for shell in range(2, max_shell + 1):
        odd_prime_power = 3**shell
        odd_squarefree = 1
        prime = 3
        while sum(factor_counter(odd_squarefree).values()) < shell:
            odd_squarefree *= prime
            prime += 2
            while any(prime % divisor == 0 for divisor in range(3, int(prime**0.5) + 1, 2)):
                prime += 2
        rows.append(
            [
                shell,
                odd_prime_power,
                f"{1 - radical(odd_prime_power) / odd_prime_power:.4f}",
                f"{float(lambda_phi_ratio(odd_prime_power)):.4f}",
                odd_squarefree,
                f"{1 - radical(odd_squarefree) / odd_squarefree:.4f}",
                f"{float(lambda_phi_ratio(odd_squarefree)):.4f}",
                f"{float(distinct_odd_prime_bound(odd_squarefree)):.4f}",
            ]
        )
    return rows


def pressure_decomposition_rows(values: list[int]) -> list[list[object]]:
    rows: list[list[object]] = []
    for n in values:
        decomposition = modular_return_decomposition(n)
        rows.append(
            [
                n,
                factor_shape(n),
                decomposition.shell_depth,
                decomposition.component_count,
                decomposition.odd_component_count,
                f"{float(decomposition.radical_compression):.4f}",
                format_fraction(decomposition.local_defect_ratio),
                format_fraction(decomposition.overlap_penalty),
                format_fraction(decomposition.lambda_phi_ratio),
                format_fraction(decomposition.odd_distinct_prime_bound),
            ]
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument("--pair-limit", type=int, default=100)
    parser.add_argument("--max-shell", type=int, default=8)
    parser.add_argument(
        "--pressure-examples",
        default="8,9,12,30,63,105,210,7560",
        help="Comma-separated n values for the pressure decomposition table.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "ORIGIN_MODULAR_THEOREM_PROBE.md",
    )
    return parser.parse_args()


def parse_csv_ints(value: str, label: str) -> list[int]:
    values = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not values or any(item < 1 for item in values):
        raise ValueError(f"{label} must be a comma-separated list of positive integers")
    return values


def main() -> None:
    args = parse_args()
    if args.limit < 2:
        raise ValueError("limit must be >= 2")
    if args.pair_limit < 2:
        raise ValueError("pair-limit must be >= 2")
    if args.max_shell < 2:
        raise ValueError("max-shell must be >= 2")
    pressure_examples = parse_csv_ints(args.pressure_examples, "pressure-examples")

    component_checked, component_failure = verify_component_formula(args.limit)
    odd_bound_checked, odd_bound_failure = verify_odd_bound(args.limit)
    pair_checked, pair_failure = verify_coprime_product_law(args.pair_limit)
    counterexamples = monotonicity_counterexamples(args.limit, args.max_shell)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = "\n\n".join(
        [
            "# Origin Modular Theorem Probe",
            f"Generated: `{generated}`",
            "This report is generated by `experiments/origin_modular_theorem_probe.py`.",
            "It separates what is already theorem-level from what remains empirical in the modular return line.",
            "The next proof move is now explicit: decompose return-exponent compression into concentration, splitting, and Carmichael-overlap pressure.",
            "## Verified Identities And Bounds",
            markdown_table(
                ["claim", "checked", "first_failure"],
                [
                    [
                        "`lambda(n)/phi(n)` equals local-defect divided by lcm-overlap penalty",
                        component_checked,
                        "none" if component_failure is None else component_failure,
                    ],
                    [
                        "For odd `n`, `lambda(n)/phi(n) <= 2^(1-omega(n))`",
                        odd_bound_checked,
                        "none" if odd_bound_failure is None else odd_bound_failure,
                    ],
                    [
                        "For coprime `a,b`, ratio(ab)=ratio(a)ratio(b)/gcd(lambda(a),lambda(b))",
                        pair_checked,
                        "none" if pair_failure is None else pair_failure,
                    ],
                ],
            ),
            "## Three-Term Pressure Decomposition",
            "For `n = product p_i^a_i`, set `c_i = lambda(p_i^a_i)` and `d_i = c_i / phi(p_i^a_i)`. Then:",
            "```text\nlambda(n) / phi(n) = product(d_i) / (product(c_i) / lcm(c_i))\n```",
            "The Origin-facing reading is: concentration pressure is tracked by radical compression, splitting pressure by the number of coprime prime-power components, and overlap pressure exactly by the product-to-lcm penalty.",
            markdown_table(
                [
                    "n",
                    "factor_shape",
                    "Omega",
                    "components",
                    "odd_components",
                    "radical_compression",
                    "local_defect",
                    "overlap_penalty",
                    "lambda_phi",
                    "odd_bound",
                ],
                pressure_decomposition_rows(pressure_examples),
            ),
            "## Endpoint Comparison Inside Shells",
            "Odd prime powers are maximally concentrated; odd squarefree products are maximally split.",
            markdown_table(
                [
                    "shell",
                    "prime_power",
                    "prime_power_compression",
                    "prime_power_lambda_phi",
                    "squarefree",
                    "squarefree_compression",
                    "squarefree_lambda_phi",
                    "odd_bound",
                ],
                endpoint_rows(args.max_shell),
            ),
            "## Counterexamples To Naive Monotonicity",
            "These show why the theorem cannot simply say higher radical compression always implies higher `lambda/phi` inside a shell.",
            markdown_table(
                [
                    "shell",
                    "lower_compression_n",
                    "lower_compression",
                    "higher_ratio",
                    "higher_compression_n",
                    "higher_compression",
                    "lower_ratio",
                ],
                counterexamples,
            ),
            "## Local Interpretation",
            "The provable core is the coprime product/lcm law: every new coprime component introduces a return-exponent compression factor controlled by Carmichael lcm overlap.",
            "Radical compression is not a total ordering of `lambda/phi`. It is a proxy for concentration versus splitting of a fixed shell, while prime-minus-one overlap can override it locally.",
            "The proof target should therefore be framed as a structural mechanism and bounded endpoint theorem, not as a universal monotonicity theorem.",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
