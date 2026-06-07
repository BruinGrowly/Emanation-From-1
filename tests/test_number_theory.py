from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.conjectures import (
    boundary_return_check,
    consecutive_odd_sequence,
    difference_rows,
    first_certificate_row,
    gilbreath_check,
    goldbach_pairs,
    odd_arithmetic_after_boundary,
    random_odd_small_gap_sequence,
    row_certificate_defects,
    shuffled_tail_gap_sequence,
)
from emanation_from_1.number_theory import (
    divisor_count,
    factor,
    goldbach_singular_factor,
    is_prime,
    radical,
    sieve,
)
from emanation_from_1.origin_metrics import origin_profile, return_path_to_one
from emanation_from_1.statistics import pearson_correlation


class NumberTheoryTests(unittest.TestCase):
    def test_sieve_and_primality(self) -> None:
        self.assertEqual(sieve(20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertTrue(is_prime(97))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(99))

    def test_factor_profile(self) -> None:
        self.assertEqual(factor(1), [])
        self.assertEqual(factor(60), [2, 2, 3, 5])
        self.assertEqual(radical(60), 30)
        self.assertEqual(divisor_count(60), 12)
        self.assertEqual(return_path_to_one(60), [60, 30, 15, 5, 1])

        profile = origin_profile(60)
        self.assertEqual(profile.emanation_depth, 4)
        self.assertEqual(profile.distinct_factor_depth, 3)

    def test_finite_conjecture_scans(self) -> None:
        self.assertTrue(gilbreath_check(32).verified)
        self.assertIn((5, 23), goldbach_pairs(28))
        self.assertIn((11, 17), goldbach_pairs(28))

    def test_gilbreath_control_sequences(self) -> None:
        odd_check = boundary_return_check(consecutive_odd_sequence(16))
        self.assertTrue(odd_check.verified)

        gap_six_check = boundary_return_check(odd_arithmetic_after_boundary(16, gap=6))
        self.assertFalse(gap_six_check.verified)
        self.assertEqual(gap_six_check.first_failure, (2, 5))

        random_sequence = random_odd_small_gap_sequence(
            length=16,
            max_gap_units=4,
            seed=1000,
        )
        self.assertEqual(random_sequence[:4], [2, 3, 11, 13])

    def test_gilbreath_certificate_rows(self) -> None:
        self.assertEqual(row_certificate_defects([1, 0, 2, 2]), 0)
        self.assertEqual(row_certificate_defects([1, 1, 2]), 1)
        self.assertEqual(row_certificate_defects([3, 0, 2]), 1)

        odd_rows = difference_rows(consecutive_odd_sequence(16))
        self.assertEqual(first_certificate_row(odd_rows), 1)

        gap_six_rows = difference_rows(odd_arithmetic_after_boundary(16, gap=6))
        self.assertIsNone(first_certificate_row(gap_six_rows))

    def test_shuffled_tail_gap_sequence(self) -> None:
        initial = [2, 3, 5, 11, 13, 17]
        shuffled = shuffled_tail_gap_sequence(initial, seed=42)
        self.assertEqual(shuffled[:2], [2, 3])

        initial_gaps = [right - left for left, right in zip(initial, initial[1:])]
        shuffled_gaps = [right - left for left, right in zip(shuffled, shuffled[1:])]
        self.assertEqual(shuffled_gaps[0], initial_gaps[0])
        self.assertEqual(sorted(shuffled_gaps[1:]), sorted(initial_gaps[1:]))

    def test_pearson_correlation(self) -> None:
        self.assertAlmostEqual(
            pearson_correlation([1, 2, 3], [2, 4, 6]),
            1.0,
        )
        self.assertAlmostEqual(
            pearson_correlation([1, 2, 3], [6, 4, 2]),
            -1.0,
        )
        self.assertIsNone(pearson_correlation([1, 1, 1], [2, 3, 4]))

    def test_goldbach_singular_factor(self) -> None:
        self.assertEqual(goldbach_singular_factor(8), 1.0)
        self.assertAlmostEqual(goldbach_singular_factor(6), 2.0)
        self.assertAlmostEqual(goldbach_singular_factor(30), 8 / 3)


if __name__ == "__main__":
    unittest.main()
