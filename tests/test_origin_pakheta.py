from fractions import Fraction
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emanation_from_1.origin_pakheta import (
    carmichael_lambda_context,
    compression_carmichael_lambda_commutator,
    compression_carmichael_lambda_gap_factor,
    compression_context,
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
    divisor_branching_context,
    euler_totient_context,
    gather_context,
    prime_minus_neighborhood_context,
    prime_plus_neighborhood_context,
    return_min_context,
    return_prime_context,
    return_prime_set_context,
    return_prime_set_divisor_branching_commutator,
    return_prime_set_divisor_branching_gap_factor,
    return_prime_set_prime_minus_neighborhood_commutator,
    return_prime_set_prime_minus_neighborhood_gap_factor,
    return_prime_set_prime_plus_neighborhood_commutator,
    return_prime_set_prime_plus_neighborhood_gap_factor,
)


class OriginPakhetaCalculusTests(unittest.TestCase):
    def test_basic_contexts(self) -> None:
        self.assertEqual(compression_context(72), 6)
        self.assertEqual(return_min_context(72), 36)
        self.assertEqual(return_prime_context(3)(72), 24)
        self.assertEqual(return_prime_context(5)(72), 72)
        self.assertEqual(return_prime_set_context((2, 3, 5))(72), 12)
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

    def test_compression_prime_set_return_commutator_multiplies_repeated_layers(
        self,
    ) -> None:
        both_repeated = compression_prime_set_return_commutator(72, (2, 3, 5))
        one_repeated = compression_prime_set_return_commutator(18, (2, 3))
        squarefree = compression_prime_set_return_commutator(30, (2, 3, 5))

        self.assertFalse(both_repeated.commutes)
        self.assertEqual(both_repeated.ratio, Fraction(6, 1))
        self.assertFalse(one_repeated.commutes)
        self.assertEqual(one_repeated.ratio, Fraction(3, 1))
        self.assertTrue(squarefree.commutes)
        self.assertEqual(squarefree.ratio, Fraction(1, 1))

    def test_compression_prime_set_return_gap_formula(self) -> None:
        for prime_set in ((2, 3), (2, 5), (2, 3, 5), (3, 5, 7)):
            for n in range(1, 300):
                commutator = compression_prime_set_return_commutator(n, prime_set)
                self.assertEqual(
                    commutator.ratio,
                    Fraction(
                        compression_prime_set_return_gap_factor(n, prime_set),
                        1,
                    ),
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

    def test_new_contexts(self) -> None:
        self.assertEqual(divisor_branching_context(12), 6)
        self.assertEqual(carmichael_lambda_context(12), 2)
        self.assertEqual(euler_totient_context(12), 4)

    def test_compression_divisor_branching_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_divisor_branching_commutator(n)
            self.assertEqual(
                commutator.ratio,
                compression_divisor_branching_gap_factor(n),
            )

    def test_return_prime_set_divisor_branching_gap_formula(self) -> None:
        for prime_set in ((2, 3), (2, 5), (2, 3, 5), (3, 5, 7)):
            for n in range(1, 200):
                commutator = return_prime_set_divisor_branching_commutator(n, prime_set)
                self.assertEqual(
                    commutator.ratio,
                    return_prime_set_divisor_branching_gap_factor(n, prime_set),
                )

    def test_compression_carmichael_lambda_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_carmichael_lambda_commutator(n)
            self.assertEqual(
                commutator.ratio,
                compression_carmichael_lambda_gap_factor(n),
            )

    def test_compression_euler_totient_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_euler_totient_commutator(n)
            self.assertEqual(
                commutator.ratio,
                compression_euler_totient_gap_factor(n),
            )

    def test_prime_neighborhood_contexts(self) -> None:
        self.assertEqual(prime_minus_neighborhood_context(12), 1 * 2)  # (2-1)*(3-1) = 2
        self.assertEqual(prime_plus_neighborhood_context(12), 3 * 4)   # (2+1)*(3+1) = 12

    def test_compression_prime_minus_neighborhood_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_prime_minus_neighborhood_commutator(n)
            self.assertEqual(
                commutator.ratio,
                compression_prime_minus_neighborhood_gap_factor(n),
            )

    def test_return_prime_set_prime_minus_neighborhood_gap_formula(self) -> None:
        for prime_set in ((2, 3), (2, 5), (2, 3, 5), (3, 5, 7)):
            for n in range(1, 200):
                commutator = return_prime_set_prime_minus_neighborhood_commutator(n, prime_set)
                self.assertEqual(
                    commutator.ratio,
                    return_prime_set_prime_minus_neighborhood_gap_factor(n, prime_set),
                )

    def test_compression_prime_plus_neighborhood_gap_formula(self) -> None:
        for n in range(1, 200):
            commutator = compression_prime_plus_neighborhood_commutator(n)
            self.assertEqual(
                commutator.ratio,
                compression_prime_plus_neighborhood_gap_factor(n),
            )

    def test_return_prime_set_prime_plus_neighborhood_gap_formula(self) -> None:
        for prime_set in ((2, 3), (2, 5), (2, 3, 5), (3, 5, 7)):
            for n in range(1, 200):
                commutator = return_prime_set_prime_plus_neighborhood_commutator(n, prime_set)
                self.assertEqual(
                    commutator.ratio,
                    return_prime_set_prime_plus_neighborhood_gap_factor(n, prime_set),
                )


if __name__ == "__main__":
    unittest.main()
