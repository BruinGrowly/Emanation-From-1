from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.conjectures import (
    block_shuffled_tail_gap_sequence,
    boundary_return_check,
    certified_lock_scan,
    consecutive_odd_sequence,
    difference_rows,
    first_certificate_row,
    gilbreath_check,
    goldbach_pairs,
    markov_gap_sequence,
    odd_arithmetic_after_boundary,
    random_odd_small_gap_sequence,
    row_certificate_defects,
    shuffled_tail_gap_sequence,
)
from emanation_from_1.number_theory import (
    carmichael_lambda,
    divisor_count,
    euler_totient,
    factor,
    goldbach_singular_factor,
    is_prime,
    multiplicative_order,
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

        odd_scan = certified_lock_scan(consecutive_odd_sequence(16))
        self.assertEqual(odd_scan.certified_lock_row, 1)
        self.assertIsNone(odd_scan.first_failure)

        gap_six_scan = certified_lock_scan(odd_arithmetic_after_boundary(16, gap=6))
        self.assertIsNone(gap_six_scan.certified_lock_row)
        self.assertEqual(gap_six_scan.first_failure, (2, 5))

    def test_shuffled_tail_gap_sequence(self) -> None:
        initial = [2, 3, 5, 11, 13, 17]
        shuffled = shuffled_tail_gap_sequence(initial, seed=42)
        self.assertEqual(shuffled[:2], [2, 3])

        initial_gaps = [right - left for left, right in zip(initial, initial[1:])]
        shuffled_gaps = [right - left for left, right in zip(shuffled, shuffled[1:])]
        self.assertEqual(shuffled_gaps[0], initial_gaps[0])
        self.assertEqual(sorted(shuffled_gaps[1:]), sorted(initial_gaps[1:]))

    def test_block_shuffled_tail_gap_sequence(self) -> None:
        initial = [2, 3, 5, 11, 13, 17, 23, 29]
        shuffled = block_shuffled_tail_gap_sequence(initial, block_size=2, seed=7)
        self.assertEqual(shuffled[:2], [2, 3])

        initial_gaps = [right - left for left, right in zip(initial, initial[1:])]
        shuffled_gaps = [right - left for left, right in zip(shuffled, shuffled[1:])]
        self.assertEqual(shuffled_gaps[0], initial_gaps[0])
        self.assertEqual(sorted(shuffled_gaps[1:]), sorted(initial_gaps[1:]))

    def test_markov_gap_sequence(self) -> None:
        initial = [2, 3, 5, 11, 13, 17, 23, 29]
        generated = markov_gap_sequence(initial, seed=11)
        self.assertEqual(len(generated), len(initial))
        self.assertEqual(generated[:2], [2, 3])

        initial_gaps = {right - left for left, right in zip(initial, initial[1:])}
        generated_gaps = [right - left for left, right in zip(generated, generated[1:])]
        self.assertEqual(generated_gaps[0], 1)
        self.assertTrue(set(generated_gaps).issubset(initial_gaps))

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

    def test_modular_return_helpers(self) -> None:
        self.assertEqual(euler_totient(1), 1)
        self.assertEqual(euler_totient(9), 6)
        self.assertEqual(euler_totient(12), 4)

        self.assertEqual(carmichael_lambda(8), 2)
        self.assertEqual(carmichael_lambda(9), 6)
        self.assertEqual(carmichael_lambda(15), 4)
        self.assertEqual(carmichael_lambda(16), 4)

        self.assertEqual(multiplicative_order(2, 9), 6)
        self.assertEqual(multiplicative_order(2, 15), 4)
        self.assertEqual(multiplicative_order(4, 15), 2)

        with self.assertRaises(ValueError):
            multiplicative_order(2, 4)


if __name__ == "__main__":
    unittest.main()
