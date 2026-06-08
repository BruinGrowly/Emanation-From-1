from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_return import (  # noqa: E402
    modular_return_dataset,
    residuals_after_log_size,
    sampled_unit_bases,
    target_control,
)
from emanation_from_1.statistics import pearson_correlation  # noqa: E402


class OriginModularReturnTests(unittest.TestCase):
    def test_sampled_unit_bases_returns_coprime_candidates(self) -> None:
        self.assertEqual(sampled_unit_bases(10, max_bases=4, candidate_limit=12), [3, 7, 9])
        self.assertEqual(sampled_unit_bases(11, max_bases=3, candidate_limit=12), [2, 3, 4])

    def test_modular_return_dataset_contains_return_ratios(self) -> None:
        dataset = modular_return_dataset(12, max_bases=4, candidate_limit=12)
        by_n = {int(row["n"]): row for row in dataset}

        self.assertNotIn(2, by_n)
        self.assertEqual(by_n[9]["phi"], 6.0)
        self.assertEqual(by_n[9]["lambda"], 6.0)
        self.assertEqual(by_n[9]["max_order_ratio"], 1.0)
        self.assertEqual(by_n[8]["lambda_over_phi"], 0.5)
        self.assertEqual(by_n[8]["emanation_depth"], 3.0)

    def test_log_residuals_remove_size_correlation(self) -> None:
        dataset = modular_return_dataset(128, max_bases=4, candidate_limit=20)
        residuals = residuals_after_log_size(dataset, "lambda_over_phi")

        correlation = pearson_correlation(
            [row["log_n"] for row in dataset],
            residuals,
        )
        self.assertIsNotNone(correlation)
        assert correlation is not None
        self.assertAlmostEqual(correlation, 0.0, places=12)

    def test_target_control_is_seed_deterministic(self) -> None:
        dataset = modular_return_dataset(256, max_bases=4, candidate_limit=20)
        first = target_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=62000,
            size_bins=4,
        )
        second = target_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=62000,
            size_bins=4,
        )

        self.assertEqual(first["predeclared_metric"], "emanation_depth")
        self.assertEqual(first["predeclared_ge_count"], second["predeclared_ge_count"])
        self.assertEqual(first["best_metric"], second["best_metric"])
        self.assertAlmostEqual(first["predeclared_r"], second["predeclared_r"])


if __name__ == "__main__":
    unittest.main()
