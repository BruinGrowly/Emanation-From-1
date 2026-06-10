"""Tests for the Origin-Pakheta commutator catalog."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.number_theory import (  # noqa: E402
    dedekind_psi,
    divisor_sigma,
    factor_counter,
    greatest_prime_factor,
    is_prime,
    radical,
)
from emanation_from_1.origin_pakheta import (  # noqa: E402
    carmichael_lambda_context,
    compression_context,
    dedekind_psi_context,
    divisor_branching_context,
    divisor_sigma_context,
    euler_totient_context,
    gather_context,
    powerful_quotient_context,
    prime_minus_neighborhood_context,
    prime_plus_neighborhood_context,
    return_max_context,
    return_min_context,
    return_prime_context,
)
from experiments.origin_pakheta_commutator_catalog import (  # noqa: E402
    OPERATOR_FUNCTIONS,
    OPERATORS,
    PROVEN_STATUS,
    catalog_pairs,
    run_catalog,
    scan_pair,
    theorem_candidates,
)


CONTEXT_EQUIVALENTS = {
    "C": compression_context,
    "R_min": return_min_context,
    "R_max": return_max_context,
    "R_2": return_prime_context(2),
    "R_3": return_prime_context(3),
    "G_2": gather_context(2),
    "G_3": gather_context(3),
    "Q": powerful_quotient_context,
    "B": divisor_branching_context,
    "T": euler_totient_context,
    "M": carmichael_lambda_context,
    "S": divisor_sigma_context,
    "P": dedekind_psi_context,
    "N-": prime_minus_neighborhood_context,
    "N+": prime_plus_neighborhood_context,
}


class NewContextTests(unittest.TestCase):
    def test_divisor_sigma_examples(self) -> None:
        self.assertEqual(divisor_sigma(1), 1)
        self.assertEqual(divisor_sigma(12), 28)
        self.assertEqual(divisor_sigma(28), 56)

    def test_dedekind_psi_examples(self) -> None:
        self.assertEqual(dedekind_psi(1), 1)
        self.assertEqual(dedekind_psi(12), 24)
        self.assertEqual(dedekind_psi(7), 8)

    def test_greatest_prime_factor_examples(self) -> None:
        self.assertEqual(greatest_prime_factor(12), 3)
        self.assertEqual(greatest_prime_factor(97), 97)
        with self.assertRaises(ValueError):
            greatest_prime_factor(1)

    def test_return_max_and_powerful_quotient(self) -> None:
        self.assertEqual(return_max_context(1), 1)
        self.assertEqual(return_max_context(12), 4)
        self.assertEqual(powerful_quotient_context(12), 2)
        self.assertEqual(powerful_quotient_context(30), 1)


class CatalogOperatorTests(unittest.TestCase):
    def test_roster_is_consistent(self) -> None:
        names = [name for name, _ in OPERATORS]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(OPERATOR_FUNCTIONS))
        self.assertEqual(len(catalog_pairs()), 105)

    def test_cached_operators_match_contexts(self) -> None:
        for name, function in OPERATOR_FUNCTIONS.items():
            context = CONTEXT_EQUIVALENTS[name]
            for n in range(1, 500):
                self.assertEqual(function(n), context(n), (name, n))


class CatalogLemmaTests(unittest.TestCase):
    def commutes(self, left: str, right: str, n: int) -> bool:
        left_op = OPERATOR_FUNCTIONS[left]
        right_op = OPERATOR_FUNCTIONS[right]
        return left_op(right_op(n)) == right_op(left_op(n))

    def test_lemma_c5_compression_powerful_quotient(self) -> None:
        for n in range(2, 400):
            self.assertEqual(self.commutes("C", "Q", n), n == radical(n), n)

    def test_lemma_c8_returns_commute_with_powerful_quotient(self) -> None:
        for n in range(2, 400):
            self.assertTrue(self.commutes("R_2", "Q", n), n)
            self.assertTrue(self.commutes("R_3", "Q", n), n)

    def test_lemma_c9_greatest_return_locus(self) -> None:
        for n in range(2, 400):
            counter = factor_counter(n)
            failing = (
                greatest_prime_factor(n) == 3
                and counter.get(3, 0) == 1
                and len(counter) >= 2
            )
            self.assertEqual(self.commutes("R_max", "R_3", n), not failing, n)
            self.assertTrue(self.commutes("R_max", "R_2", n), n)

    def test_lemma_c11_gather_sigma_never_commutes(self) -> None:
        for n in range(2, 400):
            self.assertFalse(self.commutes("G_2", "S", n), n)
            self.assertFalse(self.commutes("G_3", "N-", n), n)

    def test_lemma_c12_gather_branching_locus(self) -> None:
        for n in range(2, 400):
            self.assertEqual(self.commutes("G_2", "B", n), n % 2 == 1, n)
            self.assertFalse(self.commutes("G_3", "B", n), n)

    def test_lemma_c13_return_min_prime_plus(self) -> None:
        for n in range(2, 400):
            self.assertEqual(self.commutes("R_min", "N+", n), n == 2, n)

    def test_lemma_c14_return_max_sigma(self) -> None:
        for n in range(2, 400):
            self.assertEqual(self.commutes("R_max", "S", n), n == 2, n)

    def test_lemma_c15_return_max_prime_plus(self) -> None:
        for n in range(2, 400):
            self.assertEqual(self.commutes("R_max", "N+", n), n == 2, n)

    def test_corollary_7_1_locus_recovery(self) -> None:
        # C and B commute exactly on n = p^(2^m - 1): primes, p^3, p^7, ...
        expected = {n for n in range(2, 201) if is_prime(n)} | {8, 27, 125, 128}
        observed = {
            n for n in range(2, 201) if self.commutes("C", "B", n)
        }
        self.assertEqual(observed, expected)


class CatalogScanTests(unittest.TestCase):
    def test_scan_pair_fields_and_determinism(self) -> None:
        first = scan_pair("C", "B", 300)
        second = scan_pair("C", "B", 300)
        self.assertEqual(first, second)
        self.assertEqual(first.limit, 300)
        self.assertGreater(first.commute_count, 0)
        self.assertIsNotNone(first.first_noncommuting)
        self.assertTrue(first.checkpoint_counts)

    def test_classifications_are_valid(self) -> None:
        scans = run_catalog(300)
        valid = {"always", "never", "finite?", "sparse", "dense"}
        self.assertEqual(len(scans), 105)
        for scan in scans:
            self.assertIn(scan.classification, valid, (scan.left, scan.right))

    def test_proven_rows_reference_real_pairs(self) -> None:
        pairs = {frozenset(pair) for pair in catalog_pairs()}
        for proven_pair in PROVEN_STATUS:
            self.assertIn(proven_pair, pairs, proven_pair)

    def test_theorem_candidates_exclude_proven_rows(self) -> None:
        scans = run_catalog(300)
        for scan in theorem_candidates(scans):
            self.assertEqual(scan.status, "empirical", (scan.left, scan.right))


if __name__ == "__main__":
    unittest.main()
