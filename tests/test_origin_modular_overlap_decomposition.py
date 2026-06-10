"""Tests for the modular overlap decomposition experiment."""

from __future__ import annotations

from math import log
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_overlap_decomposition import (  # noqa: E402
    TARGET,
    conditioned_transfer_control,
    kernel_overlap,
    odd_squarefree_identity_check,
    overlap_decomposition_dataset,
    power_kernel_overlap,
    two_adic_defect,
)


class OverlapDecompositionTests(unittest.TestCase):
    def test_dataset_shape_and_keys(self) -> None:
        dataset = overlap_decomposition_dataset(300)
        self.assertEqual(len(dataset), 299)
        expected_keys = {
            "n",
            "log_n",
            "emanation_depth",
            "path_gap",
            "log_lambda_over_phi",
            "kernel_overlap",
            "two_adic_defect",
            "power_kernel_overlap",
        }
        self.assertEqual(set(dataset[0]), expected_keys)

    def test_kernel_overlap_examples(self) -> None:
        # n = 15: primes {3, 5}, prod(p-1) = 8, lcm(p-1) = 4
        self.assertAlmostEqual(kernel_overlap(15), log(2.0))
        # prime n: single term, prod = lcm
        self.assertEqual(kernel_overlap(7), 0.0)

    def test_two_adic_defect_threshold(self) -> None:
        self.assertEqual(two_adic_defect(4), 0.0)
        self.assertAlmostEqual(two_adic_defect(8), log(2.0))
        self.assertEqual(two_adic_defect(12), 0.0)
        self.assertAlmostEqual(two_adic_defect(24), log(2.0))
        self.assertEqual(two_adic_defect(15), 0.0)

    def test_power_kernel_overlap_examples(self) -> None:
        # n = 20 = 2^2 * 5: the 2-power channel overlaps v_2(5-1) = 2,
        # truncated by a - 1 = 1
        self.assertAlmostEqual(power_kernel_overlap(20), log(2.0))
        # n = 12 = 2^2 * 3: v_2(3-1) = 1, a - 1 = 1
        self.assertAlmostEqual(power_kernel_overlap(12), log(2.0))
        # n = 63 = 3^2 * 7: v_3(7-1) = 1, a - 1 = 1
        self.assertAlmostEqual(power_kernel_overlap(63), log(3.0))
        # n = 18 = 2 * 3^2: v_3(2-1) = 0, no overlap
        self.assertEqual(power_kernel_overlap(18), 0.0)
        # n = 45 = 3^2 * 5: v_3(5-1) = 0, no overlap
        self.assertEqual(power_kernel_overlap(45), 0.0)
        # squarefree n has no power channels
        self.assertEqual(power_kernel_overlap(30), 0.0)

    def test_odd_squarefree_identity_is_exact(self) -> None:
        odd_squarefree, matches = odd_squarefree_identity_check(1000)
        self.assertEqual(odd_squarefree, 403)
        self.assertEqual(matches, odd_squarefree)

    def test_decomposition_reduces_correlation(self) -> None:
        dataset = overlap_decomposition_dataset(300)
        replication = conditioned_transfer_control(
            dataset, "path_gap", TARGET, ["log_n"], trials=5, seed=62326
        )
        decomposition_control = conditioned_transfer_control(
            dataset,
            "path_gap",
            TARGET,
            ["log_n", "kernel_overlap"],
            trials=5,
            seed=62326,
        )
        self.assertLess(
            abs(decomposition_control["observed_r"]),
            abs(replication["observed_r"]),
        )

    def test_controls_are_deterministic(self) -> None:
        dataset = overlap_decomposition_dataset(200)
        first = conditioned_transfer_control(
            dataset, "path_gap", TARGET, ["log_n"], trials=10, seed=99
        )
        second = conditioned_transfer_control(
            dataset, "path_gap", TARGET, ["log_n"], trials=10, seed=99
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
