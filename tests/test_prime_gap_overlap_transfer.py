from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.prime_gap_origin_prediction import (  # noqa: E402
    attach_external_log_residual_gap,
    evaluate_predictor,
)
from experiments.prime_gap_overlap_transfer import (  # noqa: E402
    PREDICTOR,
    alternate_score_rows,
    analyze_window,
    calibration_baseline,
    overlap_pressure,
    prime_gap_overlap_window,
)


class PrimeGapOverlapTransferTests(unittest.TestCase):
    def test_overlap_pressure_is_zero_for_single_component_cases(self) -> None:
        self.assertAlmostEqual(overlap_pressure(1), 0.0)
        self.assertAlmostEqual(overlap_pressure(9), 0.0)

    def test_prime_gap_overlap_window_adds_predeclared_metric(self) -> None:
        window = prime_gap_overlap_window(start_prime_index=2, gap_count=4)

        self.assertEqual([int(row["p"]) for row in window.rows], [3, 5, 7, 11])
        self.assertIn(PREDICTOR.metric, window.rows[0])
        self.assertIn("adjacent_overlap_delta", window.rows[0])

    def test_predictor_evaluation_is_deterministic(self) -> None:
        window = prime_gap_overlap_window(start_prime_index=1, gap_count=128)
        intercept, slope = calibration_baseline(256)
        attach_external_log_residual_gap(window.rows, intercept, slope)

        first = evaluate_predictor(window.rows, PREDICTOR, large_gap_fraction=0.10)
        second = evaluate_predictor(window.rows, PREDICTOR, large_gap_fraction=0.10)

        self.assertEqual(first["positive_count"], second["positive_count"])
        self.assertEqual(first["hits"], second["hits"])
        self.assertAlmostEqual(first["auc"], second["auc"])

    def test_window_analysis_runs_three_controls(self) -> None:
        analysis = analyze_window(
            start_prime_index=128,
            gap_count=128,
            intercept=0.0,
            slope=1.0,
            large_gap_fraction=0.10,
            trials=3,
            seed=72000,
            size_bins=4,
        )

        controls = analysis["controls"]
        self.assertEqual(
            [control["mode"] for control in controls],
            ["global", "residue30", "residue30_size"],
        )

    def test_alternate_score_rows_are_diagnostics_only(self) -> None:
        window = prime_gap_overlap_window(start_prime_index=1, gap_count=128)
        intercept, slope = calibration_baseline(256)
        attach_external_log_residual_gap(window.rows, intercept, slope)
        rows = alternate_score_rows(window, fraction=0.10)

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[1][0], "p + 1 overlap pressure")


if __name__ == "__main__":
    unittest.main()
