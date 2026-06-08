from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_shell_scaling import (  # noqa: E402
    parse_csv_ints,
    primary_summary_rows,
    scaling_analyses,
    scaling_reading,
)


class OriginModularShellScalingTests(unittest.TestCase):
    def test_parse_csv_ints_rejects_empty_or_nonpositive_values(self) -> None:
        self.assertEqual(parse_csv_ints("8, 16,32", "limits"), [8, 16, 32])
        with self.assertRaises(ValueError):
            parse_csv_ints("", "limits")
        with self.assertRaises(ValueError):
            parse_csv_ints("8,0", "limits")

    def test_scaling_analysis_runs_for_small_limits(self) -> None:
        analyses = scaling_analyses(
            limits=[128, 256],
            max_bases=4,
            candidate_base_limit=20,
            trials=3,
            seed=68000,
        )

        self.assertEqual([analysis["limit"] for analysis in analyses], [128, 256])
        self.assertEqual(len(analyses[0]["controls"]), 4)
        self.assertGreater(analyses[0]["rows_scored"], 0)

    def test_primary_summary_rows_and_reading_are_stable(self) -> None:
        analyses = scaling_analyses(
            limits=[128],
            max_bases=4,
            candidate_base_limit=20,
            trials=3,
            seed=68000,
        )

        rows = primary_summary_rows(analyses)
        reading = scaling_reading(analyses)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 128)
        self.assertIn("within-shell signal", reading)


if __name__ == "__main__":
    unittest.main()
