from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.conjectures import gilbreath_check, goldbach_pairs
from emanation_from_1.number_theory import divisor_count, factor, is_prime, radical, sieve
from emanation_from_1.origin_metrics import origin_profile, return_path_to_one


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


if __name__ == "__main__":
    unittest.main()

