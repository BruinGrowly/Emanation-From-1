from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.statistics import pearson_correlation  # noqa: E402
from experiments.prime_gap_origin_profiles import (  # noqa: E402
    analyze_prime_count,
    attach_log_residual_gap,
    metric_label,
    prime_gap_dataset,
)


class PrimeGapOriginProfileTests(unittest.TestCase):
    def test_prime_gap_dataset_contains_origin_sources(self) -> None:
        dataset = prime_gap_dataset(8)
        self.assertEqual(len(dataset), 7)

        first = dataset[0]
        self.assertEqual(first["prime_index"], 1.0)
        self.assertEqual(first["p"], 2.0)
        self.assertEqual(first["next_prime"], 3.0)
        self.assertEqual(first["gap"], 1.0)
        self.assertEqual(first["p_minus_1_emanation_depth"], 0.0)
        self.assertEqual(first["p_plus_1_emanation_depth"], 1.0)
        self.assertEqual(first["index_emanation_depth"], 0.0)
        self.assertEqual(first["adjacent_delta_emanation_depth"], 1.0)

    def test_log_residual_gap_removes_linear_log_baseline(self) -> None:
        dataset = prime_gap_dataset(128)
        attach_log_residual_gap(dataset)

        correlation = pearson_correlation(
            [row["log_p"] for row in dataset],
            [row["log_residual_gap"] for row in dataset],
        )
        self.assertIsNotNone(correlation)
        assert correlation is not None
        self.assertAlmostEqual(correlation, 0.0, places=12)

    def test_analysis_keeps_log_baseline_stronger_than_residual_origin_signal(self) -> None:
        analysis = analyze_prime_count(512, shuffle_trials=5, seed=24000)
        best_residual = analysis["best_residual"]
        self.assertIsNotNone(best_residual)
        assert best_residual is not None

        self.assertEqual(analysis["gap_count"], 511)
        self.assertEqual(best_residual[0], "adjacent_delta_divisor_count")
        self.assertGreater(abs(analysis["log_gap_r"]), abs(best_residual[1]))

    def test_shuffle_control_is_seed_deterministic(self) -> None:
        first = analyze_prime_count(128, shuffle_trials=5, seed=24000)["shuffle"]
        second = analyze_prime_count(128, shuffle_trials=5, seed=24000)["shuffle"]

        self.assertEqual(first["observed_metric"], second["observed_metric"])
        self.assertEqual(first["ge_count"], second["ge_count"])
        self.assertAlmostEqual(first["mean_abs_best"], second["mean_abs_best"])
        self.assertEqual(metric_label(str(first["observed_metric"])), "p + 1.divisor_count")


if __name__ == "__main__":
    unittest.main()
