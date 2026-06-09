from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.goldbach_neighborhood_transfer import (
    goldbach_neighborhood_transfer_dataset,
    transfer_control,
    run_experiment,
)


class GoldbachNeighborhoodTransferTests(unittest.TestCase):
    def test_dataset_generation(self) -> None:
        dataset = goldbach_neighborhood_transfer_dataset(50)
        # 4, 6, 8, ..., 50 -> 24 even numbers
        self.assertEqual(len(dataset), 24)
        first = dataset[0]
        self.assertEqual(first["n"], 4.0)
        self.assertIn("compression_prime_minus_neighborhood_log_gap", first)
        self.assertIn("compression_prime_plus_neighborhood_log_gap", first)
        self.assertIn("log_singular_normalized_density", first)

    def test_dataset_generation_invalid_limit(self) -> None:
        with self.assertRaises(ValueError):
            goldbach_neighborhood_transfer_dataset(2)

    def test_transfer_control_determinism(self) -> None:
        dataset = goldbach_neighborhood_transfer_dataset(50)
        first = transfer_control(
            dataset,
            "compression_prime_minus_neighborhood_log_gap",
            "log_singular_normalized_density",
            trials=5,
            seed=42,
        )
        second = transfer_control(
            dataset,
            "compression_prime_minus_neighborhood_log_gap",
            "log_singular_normalized_density",
            trials=5,
            seed=42,
        )
        self.assertEqual(first["observed_r"], second["observed_r"])
        self.assertEqual(first["p_upper"], second["p_upper"])

    def test_run_experiment_writes_report(self) -> None:
        report_path = ROOT / "_test_goldbach_neighborhood_transfer_report.md"
        try:
            result = run_experiment(
                limit=30,
                trials=3,
                seed=42,
                report_path=report_path,
            )
            self.assertEqual(result["rows"], 14)  # 4..30 -> 14 evens
            self.assertTrue(report_path.exists())
            self.assertIn("Goldbach-Neighborhood Residual Transfer Test", report_path.read_text(encoding="utf-8"))
        finally:
            report_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
