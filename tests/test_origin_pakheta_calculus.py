from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_pakheta_calculus import (  # noqa: E402
    calculus_dataset,
    formula_check,
    path_control,
    run_experiment,
)


class OriginPakhetaCalculusScanTests(unittest.TestCase):
    def test_formula_check_has_no_mismatches(self) -> None:
        check = formula_check(256)

        self.assertEqual(check["compression_return_mismatches"], 0)
        self.assertEqual(check["return_2_mismatches"], 0)
        self.assertEqual(check["return_3_mismatches"], 0)
        self.assertEqual(check["return_5_mismatches"], 0)
        self.assertEqual(check["return_7_mismatches"], 0)
        self.assertEqual(check["return_set_2_3_mismatches"], 0)
        self.assertEqual(check["return_set_2_3_5_mismatches"], 0)
        self.assertEqual(check["return_set_3_5_7_mismatches"], 0)
        self.assertEqual(check["gather_2_mismatches"], 0)
        self.assertEqual(check["gather_3_mismatches"], 0)
        self.assertEqual(check["gather_5_mismatches"], 0)

    def test_calculus_dataset_exposes_path_gaps(self) -> None:
        dataset = calculus_dataset(12)
        by_n = {int(row["n"]): row for row in dataset}

        self.assertGreater(by_n[4]["compression_return_log_gap"], 0.0)
        self.assertEqual(by_n[6]["compression_return_log_gap"], 0.0)
        self.assertGreater(by_n[4]["return_2_log_gap"], 0.0)
        self.assertEqual(by_n[6]["return_2_log_gap"], 0.0)
        self.assertGreater(by_n[9]["return_3_log_gap"], 0.0)
        self.assertGreater(by_n[6]["gather_2_log_gap"], 0.0)
        self.assertEqual(by_n[7]["gather_2_log_gap"], 0.0)

    def test_path_control_is_seed_deterministic(self) -> None:
        dataset = calculus_dataset(512)
        first = path_control(
            dataset,
            "compression_return_log_gap",
            "radical_compression",
            trials=5,
            seed=62226,
        )
        second = path_control(
            dataset,
            "compression_return_log_gap",
            "radical_compression",
            trials=5,
            seed=62226,
        )

        self.assertEqual(first["control_ge_count"], second["control_ge_count"])
        self.assertAlmostEqual(first["observed_r"], second["observed_r"])

    def test_run_experiment_writes_report(self) -> None:
        report_path = ROOT / "_test_origin_pakheta_calculus_report.md"
        try:
            result = run_experiment(
                limit=128,
                trials=3,
                seed=62226,
                report_path=report_path,
            )

            self.assertEqual(result["rows"], 127)
            self.assertTrue(report_path.exists())
            self.assertIn("Origin-Pakheta Calculus", report_path.read_text())
        finally:
            report_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
