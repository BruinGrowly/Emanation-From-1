from collections import defaultdict
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_group_controls import add_group_baseline_fields  # noqa: E402
from experiments.origin_modular_return import modular_return_dataset  # noqa: E402
from experiments.origin_modular_shell_transfer import (  # noqa: E402
    PREDECLARED_METRIC,
    shell_centered_values,
    shell_conditioned_residuals,
    shell_groups,
    shell_transfer_control,
)


class OriginModularShellTransferTests(unittest.TestCase):
    def test_shell_groups_partition_dataset_by_emanation_depth(self) -> None:
        dataset = modular_return_dataset(128, max_bases=4, candidate_limit=20)
        groups = shell_groups(dataset)

        self.assertEqual(sum(len(indices) for indices in groups.values()), len(dataset))
        for shell, indices in groups.items():
            self.assertTrue(
                all(int(dataset[index]["emanation_depth"]) == shell for index in indices)
            )

    def test_shell_centered_values_have_zero_shell_means(self) -> None:
        dataset = modular_return_dataset(128, max_bases=4, candidate_limit=20)
        centered = shell_centered_values(dataset, "lambda_over_phi")
        values_by_shell: dict[int, list[float]] = defaultdict(list)
        for row, value in zip(dataset, centered):
            values_by_shell[int(row["emanation_depth"])].append(value)

        for values in values_by_shell.values():
            self.assertAlmostEqual(sum(values) / len(values), 0.0, places=12)

    def test_shell_conditioned_residuals_keep_length(self) -> None:
        dataset = modular_return_dataset(256, max_bases=4, candidate_limit=20)
        add_group_baseline_fields(dataset)
        residuals = shell_conditioned_residuals(
            dataset,
            "lambda_over_phi",
            ["log_n", "phi_over_n", "log_phi"],
        )

        self.assertEqual(len(residuals), len(dataset))
        self.assertGreater(max(residuals), min(residuals))

    def test_shell_transfer_control_is_seed_deterministic(self) -> None:
        dataset = modular_return_dataset(256, max_bases=4, candidate_limit=20)
        add_group_baseline_fields(dataset)
        first = shell_transfer_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=66000,
        )
        second = shell_transfer_control(
            dataset,
            "lambda_over_phi",
            trials=5,
            seed=66000,
        )

        self.assertEqual(first["predeclared_metric"], PREDECLARED_METRIC)
        self.assertEqual(first["predeclared_ge_count"], second["predeclared_ge_count"])
        self.assertEqual(first["best_metric"], second["best_metric"])
        self.assertAlmostEqual(first["predeclared_r"], second["predeclared_r"])


if __name__ == "__main__":
    unittest.main()
