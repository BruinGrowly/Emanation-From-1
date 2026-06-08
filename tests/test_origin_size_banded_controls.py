from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_size_banded_controls import (  # noqa: E402
    SHELL_METRICS,
    origin_size_dataset,
    residuals_after_log_size,
    size_bin_groups,
    target_control,
)
from emanation_from_1.statistics import pearson_correlation  # noqa: E402


class OriginSizeBandedControlTests(unittest.TestCase):
    def test_origin_size_dataset_starts_after_origin(self) -> None:
        dataset = origin_size_dataset(8)

        self.assertEqual([int(row["n"]) for row in dataset], [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual([row["emanation_depth"] for row in dataset], [1, 1, 2, 1, 2, 1, 3])
        self.assertEqual(dataset[2]["divisor_count"], 3.0)
        self.assertEqual(dataset[-1]["radical_compression"], 0.75)
        self.assertEqual(dataset[-1]["squarefree_flag"], 0.0)

    def test_log_residuals_remove_linear_log_correlation(self) -> None:
        dataset = origin_size_dataset(128)
        residuals = residuals_after_log_size(dataset, "divisor_count")

        correlation = pearson_correlation(
            [row["log_n"] for row in dataset],
            residuals,
        )
        self.assertIsNotNone(correlation)
        assert correlation is not None
        self.assertAlmostEqual(correlation, 0.0, places=12)

    def test_size_bin_groups_partition_dataset(self) -> None:
        dataset = origin_size_dataset(21)
        groups = size_bin_groups(dataset, size_bins=4)

        self.assertEqual(sorted(groups), [0, 1, 2, 3])
        self.assertEqual(sum(len(indices) for indices in groups.values()), len(dataset))
        self.assertEqual(groups[0][0], 0)
        self.assertEqual(groups[3][-1], len(dataset) - 1)

    def test_target_control_is_seed_deterministic(self) -> None:
        dataset = origin_size_dataset(256)
        first = target_control(
            dataset,
            "divisor_count",
            SHELL_METRICS,
            trials=5,
            seed=51000,
            size_bins=4,
        )
        second = target_control(
            dataset,
            "divisor_count",
            SHELL_METRICS,
            trials=5,
            seed=51000,
            size_bins=4,
        )

        self.assertEqual(first["observed_metric"], second["observed_metric"])
        self.assertEqual(first["control_ge_count"], second["control_ge_count"])
        self.assertAlmostEqual(first["observed_r"], second["observed_r"])
        self.assertIn(first["observed_metric"], SHELL_METRICS)


if __name__ == "__main__":
    unittest.main()
