from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_anchor_residual_transfer import (  # noqa: E402
    ANCHOR_RESIDUALS,
    ZERO_TOLERANCE,
    anchor_residual_transfer_dataset,
    residual_summary,
    transfer_control,
)


class OriginAnchorResidualTransferTests(unittest.TestCase):
    def test_exact_anchor_residuals_have_no_leftover_variance(self) -> None:
        dataset = anchor_residual_transfer_dataset(
            512,
            max_bases=6,
            candidate_base_limit=24,
        )

        for key, _description in ANCHOR_RESIDUALS:
            with self.subTest(residual=key):
                summary = residual_summary(dataset, key)
                self.assertLessEqual(summary["max_abs"], ZERO_TOLERANCE)
                self.assertFalse(summary["has_leftover_variance"])

    def test_transfer_control_reports_no_leftover_anchor_variance(self) -> None:
        dataset = anchor_residual_transfer_dataset(
            512,
            max_bases=6,
            candidate_base_limit=24,
        )
        control = transfer_control(
            dataset,
            "idempotent_exact_residual",
            "log_lambda_over_phi",
            ["log_n", "phi_over_n", "log_phi", "component_count"],
            trials=5,
            seed=62126,
        )

        self.assertEqual(control["status"], "no_leftover_anchor_variance")
        self.assertIsNone(control["observed_r"])
        self.assertLessEqual(control["anchor_max_abs"], ZERO_TOLERANCE)

    def test_transfer_dataset_contains_independent_targets(self) -> None:
        dataset = anchor_residual_transfer_dataset(
            64,
            max_bases=4,
            candidate_base_limit=16,
        )
        row = dataset[0]

        self.assertIn("log_lambda_over_phi", row)
        self.assertIn("average_order_ratio", row)
        self.assertIn("full_exponent_hit", row)
        self.assertIn("involution_density_exact_residual", row)


if __name__ == "__main__":
    unittest.main()
