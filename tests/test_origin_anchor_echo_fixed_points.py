from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_anchor_echo_fixed_points import (  # noqa: E402
    PREDECLARED_METRIC,
    brute_force_check,
    fixed_point_dataset,
    model_r_squared,
    target_control,
)


class OriginAnchorEchoFixedPointTests(unittest.TestCase):
    def test_fixed_point_dataset_contains_anchor_targets(self) -> None:
        dataset = fixed_point_dataset(12)
        by_n = {int(row["n"]): row for row in dataset}

        self.assertEqual(by_n[12]["component_count"], 2.0)
        self.assertEqual(by_n[12]["idempotent_count"], 4.0)
        self.assertEqual(by_n[12]["involution_count"], 4.0)
        self.assertIn("log_idempotent_density", by_n[12])
        self.assertIn("overlap_pressure_log", by_n[12])

    def test_brute_force_check_validates_closed_forms(self) -> None:
        check = brute_force_check(50)

        self.assertEqual(check["max_idempotent_error"], 0)
        self.assertEqual(check["max_involution_error"], 0)

    def test_component_count_exactly_explains_idempotent_logs(self) -> None:
        dataset = fixed_point_dataset(256)

        self.assertAlmostEqual(
            model_r_squared(dataset, "log_idempotent_count", ["component_count"]),
            1.0,
        )

    def test_anchor_control_is_seed_deterministic(self) -> None:
        dataset = fixed_point_dataset(512)
        first = target_control(
            dataset,
            "log_idempotent_count",
            trials=5,
            seed=62026,
        )
        second = target_control(
            dataset,
            "log_idempotent_count",
            trials=5,
            seed=62026,
        )

        self.assertEqual(first["predeclared_metric"], PREDECLARED_METRIC)
        self.assertEqual(first["predeclared_ge_count"], second["predeclared_ge_count"])
        self.assertEqual(first["best_metric"], second["best_metric"])
        self.assertAlmostEqual(first["predeclared_r"], second["predeclared_r"])


if __name__ == "__main__":
    unittest.main()
