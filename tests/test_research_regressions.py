from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.conjectures import (  # noqa: E402
    block_shuffled_tail_gap_sequence,
    certified_lock_scan,
    consecutive_odd_sequence,
    goldbach_scan,
    markov_gap_sequence,
    odd_arithmetic_after_boundary,
    shuffled_tail_gap_sequence,
)
from emanation_from_1.number_theory import first_n_primes  # noqa: E402
from experiments.goldbach_origin_correlations import (  # noqa: E402
    goldbach_dataset,
    strongest_origin_correlation,
)
from experiments.origin_anchor_echo_fixed_points import (  # noqa: E402
    brute_force_check,
    fixed_point_dataset,
    model_r_squared,
)
from experiments.origin_anchor_residual_transfer import (  # noqa: E402
    ANCHOR_RESIDUALS,
    ZERO_TOLERANCE,
    anchor_residual_transfer_dataset,
    residual_summary,
)
from experiments.origin_pakheta_calculus import (  # noqa: E402
    calculus_dataset,
    formula_check,
    path_control,
)


class ResearchRegressionTests(unittest.TestCase):
    def test_prime_prefix_lock_rows_match_evidence_ledger(self) -> None:
        expected_lock_rows = {
            64: 10,
            128: 15,
            256: 20,
            512: 23,
            1024: 35,
        }

        for prime_count, expected_lock_row in expected_lock_rows.items():
            with self.subTest(prime_count=prime_count):
                scan = certified_lock_scan(first_n_primes(prime_count))
                self.assertIsNone(scan.first_failure)
                self.assertEqual(scan.certified_lock_row, expected_lock_row)

    def test_basic_boundary_controls_keep_gilbreath_claim_constrained(self) -> None:
        odd_scan = certified_lock_scan(consecutive_odd_sequence(64))
        self.assertEqual(odd_scan.certified_lock_row, 1)
        self.assertIsNone(odd_scan.first_failure)

        gap_six_scan = certified_lock_scan(odd_arithmetic_after_boundary(64, gap=6))
        self.assertIsNone(gap_six_scan.certified_lock_row)
        self.assertEqual(gap_six_scan.first_failure, (2, 5))

    def test_prime_gap_order_controls_fail_early_for_fixed_seeds(self) -> None:
        primes = first_n_primes(256)
        controls = [
            (
                "full_shuffle",
                shuffled_tail_gap_sequence(primes, seed=9000),
                (3, 7),
            ),
            (
                "block_shuffle",
                block_shuffled_tail_gap_sequence(primes, block_size=4, seed=15000),
                (2, 9),
            ),
            (
                "markov_gap",
                markov_gap_sequence(primes, seed=40000),
                (3, 3),
            ),
        ]

        for name, sequence, expected_failure in controls:
            with self.subTest(control=name):
                scan = certified_lock_scan(sequence)
                self.assertFalse(scan.certified)
                self.assertEqual(scan.first_failure, expected_failure)

    def test_goldbach_evidence_stays_constrained_after_singular_baseline(self) -> None:
        scan = goldbach_scan(10_000)
        self.assertEqual(scan["failures"], ())
        self.assertEqual(scan["richest_even"], 9240)
        self.assertEqual(scan["richest_pair_count"], 329)

        dataset = goldbach_dataset(10_000)
        normalized = strongest_origin_correlation(dataset, "normalized_pair_density")
        singular = strongest_origin_correlation(dataset, "singular_normalized_density")

        self.assertIsNotNone(normalized)
        self.assertIsNotNone(singular)
        assert normalized is not None
        assert singular is not None

        self.assertEqual(normalized[0], "distinct_factor_depth")
        self.assertAlmostEqual(normalized[1], 0.7110, places=4)
        self.assertEqual(singular[0], "phi_attenuation")
        self.assertAlmostEqual(singular[1], 0.1355, places=4)
        self.assertLess(abs(singular[1]), abs(normalized[1]))

    def test_anchor_echo_fixed_point_mechanisms_match_ledger(self) -> None:
        check = brute_force_check(80)
        self.assertEqual(check["max_idempotent_error"], 0)
        self.assertEqual(check["max_involution_error"], 0)

        dataset = fixed_point_dataset(1000)
        self.assertAlmostEqual(
            model_r_squared(dataset, "log_idempotent_count", ["component_count"]),
            1.0,
        )
        self.assertAlmostEqual(
            model_r_squared(
                dataset,
                "log_involution_count",
                ["odd_component_count", "two_adic_involution_log"],
            ),
            1.0,
        )

    def test_anchor_residual_transfer_has_no_leftover_signal(self) -> None:
        dataset = anchor_residual_transfer_dataset(
            512,
            max_bases=6,
            candidate_base_limit=24,
        )

        for key, _description in ANCHOR_RESIDUALS:
            with self.subTest(residual=key):
                summary = residual_summary(dataset, key)
                self.assertLessEqual(summary["max_abs"], ZERO_TOLERANCE)

    def test_origin_pakheta_calculus_path_identity_matches_ledger(self) -> None:
        check = formula_check(512)
        self.assertEqual(check["compression_return_mismatches"], 0)
        self.assertEqual(check["return_2_mismatches"], 0)
        self.assertEqual(check["return_3_mismatches"], 0)
        self.assertEqual(check["return_5_mismatches"], 0)
        self.assertEqual(check["return_7_mismatches"], 0)
        self.assertEqual(check["gather_2_mismatches"], 0)
        self.assertEqual(check["gather_3_mismatches"], 0)
        self.assertEqual(check["gather_5_mismatches"], 0)

        dataset = calculus_dataset(1000)
        control = path_control(
            dataset,
            "compression_return_log_gap",
            "radical_compression",
            trials=5,
            seed=62226,
        )
        self.assertGreater(control["observed_r"], 0.5)


if __name__ == "__main__":
    unittest.main()
