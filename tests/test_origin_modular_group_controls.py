from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.statistics import pearson_correlation  # noqa: E402
from experiments.origin_modular_group_controls import (  # noqa: E402
    add_group_baseline_fields,
    baseline_features_for_target,
    group_control,
    grouped_indices,
    regression_residuals,
)
from experiments.origin_modular_return import modular_return_dataset  # noqa: E402


class OriginModularGroupControlTests(unittest.TestCase):
    def test_group_baseline_fields_are_attached(self) -> None:
        dataset = modular_return_dataset(32, max_bases=4, candidate_limit=12)
        add_group_baseline_fields(dataset)

        row = next(item for item in dataset if int(item["n"]) == 9)
        self.assertAlmostEqual(row["phi_over_n"], 6 / 9)
        self.assertIn("log_phi", row)
        self.assertIn("log_lambda", row)

    def test_baseline_features_avoid_target_circularity(self) -> None:
        self.assertNotIn("lambda_over_phi", baseline_features_for_target("lambda_over_phi"))
        self.assertIn("lambda_over_phi", baseline_features_for_target("average_order_ratio"))

    def test_regression_residuals_remove_feature_correlation(self) -> None:
        dataset = modular_return_dataset(256, max_bases=4, candidate_limit=20)
        add_group_baseline_fields(dataset)
        residuals = regression_residuals(
            dataset,
            "lambda_over_phi",
            baseline_features_for_target("lambda_over_phi"),
        )

        correlation = pearson_correlation(
            [row["log_n"] for row in dataset],
            residuals,
        )
        self.assertIsNotNone(correlation)
        assert correlation is not None
        self.assertAlmostEqual(correlation, 0.0, places=12)

    def test_grouped_indices_partition_rows(self) -> None:
        dataset = modular_return_dataset(128, max_bases=4, candidate_limit=20)
        add_group_baseline_fields(dataset)
        groups = grouped_indices(dataset, ["log_n", "phi_over_n"], bins_per_feature=3)

        self.assertEqual(sum(len(indices) for indices in groups.values()), len(dataset))
        self.assertTrue(all(isinstance(key, tuple) for key in groups))
        self.assertGreaterEqual(len(groups), 3)

    def test_group_control_is_seed_deterministic(self) -> None:
        dataset = modular_return_dataset(256, max_bases=4, candidate_limit=20)
        add_group_baseline_fields(dataset)
        first = group_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=64000,
            bins_per_feature=3,
        )
        second = group_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=64000,
            bins_per_feature=3,
        )

        self.assertEqual(first["predeclared_ge_count"], second["predeclared_ge_count"])
        self.assertEqual(first["best_metric"], second["best_metric"])
        self.assertAlmostEqual(first["predeclared_r"], second["predeclared_r"])


if __name__ == "__main__":
    unittest.main()
