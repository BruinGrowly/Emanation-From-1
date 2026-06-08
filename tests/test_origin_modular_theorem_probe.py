from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_theorem_probe import (  # noqa: E402
    component_formula_ratio,
    distinct_odd_prime_bound,
    lambda_phi_ratio,
    monotonicity_counterexamples,
    verify_component_formula,
    verify_coprime_product_law,
    verify_odd_bound,
)


class OriginModularTheoremProbeTests(unittest.TestCase):
    def test_component_formula_matches_direct_ratio(self) -> None:
        for n in (8, 9, 12, 15, 45, 63, 210):
            with self.subTest(n=n):
                self.assertAlmostEqual(component_formula_ratio(n), lambda_phi_ratio(n))

    def test_odd_distinct_prime_bound(self) -> None:
        self.assertEqual(distinct_odd_prime_bound(9), 1.0)
        self.assertEqual(distinct_odd_prime_bound(15), 0.5)
        self.assertEqual(distinct_odd_prime_bound(105), 0.25)
        self.assertLessEqual(lambda_phi_ratio(105), distinct_odd_prime_bound(105))

    def test_verification_helpers_find_no_small_failures(self) -> None:
        self.assertIsNone(verify_component_formula(256)[1])
        self.assertIsNone(verify_odd_bound(255)[1])
        self.assertIsNone(verify_coprime_product_law(32)[1])

    def test_naive_monotonicity_has_counterexamples(self) -> None:
        examples = monotonicity_counterexamples(limit=5000, max_shell=5)

        self.assertTrue(any(row[0] == 3 for row in examples))
        shell_three = next(row for row in examples if row[0] == 3)
        self.assertEqual(shell_three[1], 30)
        self.assertEqual(shell_three[4], 63)


if __name__ == "__main__":
    unittest.main()
