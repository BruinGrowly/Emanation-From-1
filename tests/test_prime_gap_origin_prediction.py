from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.prime_gap_origin_prediction import (  # noqa: E402
    PREDICTORS,
    analyze_window,
    evaluate_predictor,
    prime_gap_window_dataset,
    roc_auc,
)
from experiments.prime_gap_origin_profiles import attach_log_residual_gap  # noqa: E402


class PrimeGapOriginPredictionTests(unittest.TestCase):
    def test_prime_gap_window_dataset_uses_one_based_prime_index(self) -> None:
        dataset = prime_gap_window_dataset(start_prime_index=2, gap_count=4)

        self.assertEqual([int(row["prime_index"]) for row in dataset], [2, 3, 4, 5])
        self.assertEqual([int(row["p"]) for row in dataset], [3, 5, 7, 11])
        self.assertEqual([int(row["gap"]) for row in dataset], [2, 2, 4, 2])
        self.assertIn("adjacent_delta_divisor_count", dataset[0])

    def test_roc_auc_handles_ties_with_average_ranks(self) -> None:
        auc = roc_auc([0.2, 0.2, 0.9, 0.1], [0.0, 1.0, 1.0, 0.0])

        self.assertIsNotNone(auc)
        assert auc is not None
        self.assertAlmostEqual(auc, 0.875)

    def test_predictor_evaluation_is_deterministic(self) -> None:
        dataset = prime_gap_window_dataset(start_prime_index=1, gap_count=128)
        attach_log_residual_gap(dataset)

        first = evaluate_predictor(dataset, PREDICTORS[0], large_gap_fraction=0.10)
        second = evaluate_predictor(dataset, PREDICTORS[0], large_gap_fraction=0.10)

        self.assertEqual(first["positive_count"], second["positive_count"])
        self.assertEqual(first["hits"], second["hits"])
        self.assertAlmostEqual(first["auc"], second["auc"])
        self.assertGreaterEqual(first["enrichment"], 0.0)

    def test_window_analysis_runs_conditioned_controls(self) -> None:
        calibration = prime_gap_window_dataset(start_prime_index=1, gap_count=128)
        attach_log_residual_gap(calibration)
        # A tiny fixed baseline is sufficient here; this test checks plumbing, not evidence.
        analysis = analyze_window(
            start_prime_index=128,
            gap_count=128,
            predictors=PREDICTORS[:1],
            intercept=0.0,
            slope=1.0,
            large_gap_fraction=0.10,
            trials=3,
            seed=28000,
            size_bins=4,
        )

        predictor_rows = analysis["predictor_rows"]
        self.assertEqual(len(predictor_rows), 1)
        controls = predictor_rows[0]["controls"]
        self.assertEqual([control["mode"] for control in controls], ["global", "residue30", "residue30_size"])


if __name__ == "__main__":
    unittest.main()
