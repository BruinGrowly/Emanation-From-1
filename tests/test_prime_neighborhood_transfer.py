from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.prime_neighborhood_transfer import (
    prime_neighborhood_transfer_dataset,
    transfer_control,
    run_experiment,
)


class PrimeNeighborhoodTransferTests(unittest.TestCase):
    def test_dataset_generation(self) -> None:
        dataset = prime_neighborhood_transfer_dataset(100)
        self.assertEqual(len(dataset), 99)  # 2..100
        first = dataset[0]
        self.assertEqual(first["n"], 2.0)
        self.assertIn("compression_prime_minus_neighborhood_log_gap", first)
        self.assertIn("compression_prime_plus_neighborhood_log_gap", first)
        self.assertIn("log_lambda_over_phi", first)

    def test_transfer_control_determinism(self) -> None:
        dataset = prime_neighborhood_transfer_dataset(100)
        first = transfer_control(
            dataset,
            "compression_prime_minus_neighborhood_log_gap",
            "log_lambda_over_phi",
            trials=5,
            seed=42,
        )
        second = transfer_control(
            dataset,
            "compression_prime_minus_neighborhood_log_gap",
            "log_lambda_over_phi",
            trials=5,
            seed=42,
        )
        self.assertEqual(first["observed_r"], second["observed_r"])
        self.assertEqual(first["p_upper"], second["p_upper"])

    def test_run_experiment_writes_report(self) -> None:
        report_path = ROOT / "_test_prime_neighborhood_transfer_report.md"
        try:
            result = run_experiment(
                limit=50,
                trials=3,
                seed=42,
                report_path=report_path,
            )
            self.assertEqual(result["rows"], 49)
            self.assertTrue(report_path.exists())
            self.assertIn("Prime-Neighborhood Residual Transfer Test", report_path.read_text())
        finally:
            report_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
