from fractions import Fraction
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.origin_pakheta import (
    compression_context,
    compression_gather_commutator,
    compression_gather_gap_factor,
    compression_prime_return_commutator,
    compression_prime_return_gap_factor,
    compression_return_commutator,
    compression_return_gap_factor,
    gather_context,
    return_min_context,
    return_prime_context,
)


class OriginPakhetaCalculusTests(unittest.TestCase):
    def test_basic_contexts(self) -> None:
        self.assertEqual(compression_context(72), 6)
        self.assertEqual(return_min_context(72), 36)
        self.assertEqual(return_prime_context(3)(72), 24)
        self.assertEqual(return_prime_context(5)(72), 72)
        self.assertEqual(gather_context(5)(72), 360)

    def test_compression_is_idempotent(self) -> None:
        for n in range(1, 100):
            self.assertEqual(
                compression_context(compression_context(n)),
                compression_context(n),
            )

    def test_compression_return_commutator_detects_repeated_least_prime(self) -> None:
        squareful = compression_return_commutator(72)
        squarefree_at_least = compression_return_commutator(30)

        self.assertFalse(squareful.commutes)
        self.assertEqual(squareful.left_after_right, 6)
        self.assertEqual(squareful.right_after_left, 3)
        self.assertEqual(squareful.ratio, Fraction(2, 1))

        self.assertTrue(squarefree_at_least.commutes)
        self.assertEqual(squarefree_at_least.ratio, Fraction(1, 1))

    def test_compression_return_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_return_commutator(n)
            self.assertEqual(
                commutator.ratio,
                Fraction(compression_return_gap_factor(n), 1),
            )

    def test_compression_prime_return_commutator_detects_repeated_prime(self) -> None:
        repeated = compression_prime_return_commutator(72, 3)
        single = compression_prime_return_commutator(18, 2)
        absent = compression_prime_return_commutator(25, 3)

        self.assertFalse(repeated.commutes)
        self.assertEqual(repeated.ratio, Fraction(3, 1))
        self.assertTrue(single.commutes)
        self.assertEqual(single.ratio, Fraction(1, 1))
        self.assertTrue(absent.commutes)
        self.assertEqual(absent.ratio, Fraction(1, 1))

    def test_compression_prime_return_gap_formula(self) -> None:
        for prime in (2, 3, 5, 7):
            for n in range(1, 200):
                commutator = compression_prime_return_commutator(n, prime)
                self.assertEqual(
                    commutator.ratio,
                    Fraction(compression_prime_return_gap_factor(n, prime), 1),
                )

    def test_compression_gather_commutator_detects_existing_prime_facet(self) -> None:
        present = compression_gather_commutator(18, 3)
        absent = compression_gather_commutator(10, 3)

        self.assertFalse(present.commutes)
        self.assertEqual(present.ratio, Fraction(1, 3))
        self.assertTrue(absent.commutes)
        self.assertEqual(absent.ratio, Fraction(1, 1))

    def test_compression_gather_gap_formula(self) -> None:
        for prime in (2, 3, 5):
            for n in range(1, 100):
                commutator = compression_gather_commutator(n, prime)
                self.assertEqual(
                    commutator.ratio,
                    compression_gather_gap_factor(n, prime),
                )


if __name__ == "__main__":
    unittest.main()
