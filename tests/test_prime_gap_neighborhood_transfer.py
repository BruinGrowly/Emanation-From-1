from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.prime_gap_neighborhood_transfer import (
    prime_gap_neighborhood_window,
    calibration_baseline,
    analyze_window,
)


class PrimeGapNeighborhoodTransferTests(unittest.TestCase):
    def test_window_dataset_generation(self) -> None:
        window = prime_gap_neighborhood_window(10, 100)
        self.assertEqual(window.start_prime_index, 10)
        self.assertEqual(window.gap_count, 100)
        self.assertEqual(len(window.rows), 100)
        first = window.rows[0]
        self.assertIn("p_minus_1_log_neighborhood_minus_gap", first)
        self.assertIn("p_plus_1_log_neighborhood_plus_gap", first)
        self.assertIn("adjacent_delta_neighborhood_minus_gap", first)

    def test_calibration_baseline(self) -> None:
        intercept, slope = calibration_baseline(50)
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(slope, float)

    def test_analyze_window_runs(self) -> None:
        intercept, slope = calibration_baseline(50)
        analysis = analyze_window(
            start_prime_index=50,
            gap_count=20,
            intercept=intercept,
            slope=slope,
            large_gap_fraction=0.10,
            trials=3,
            seed=42,
            size_bins=2,
        )
        self.assertEqual(analysis["window"].gap_count, 20)
        self.assertEqual(len(analysis["predictor_rows"]), 2)
        self.assertEqual(len(analysis["alternate_rows"]), 8)


if __name__ == "__main__":
    unittest.main()
