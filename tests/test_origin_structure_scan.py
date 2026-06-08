from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_structure_scan import (  # noqa: E402
    branching_hotspots,
    first_depth_occurrences,
    origin_rows,
    shell_summaries,
)


class OriginStructureScanTests(unittest.TestCase):
    def test_origin_rows_capture_direct_emanation_depths(self) -> None:
        rows = origin_rows(8)
        depths = [row["depth"] for row in rows]

        self.assertEqual(depths, [0, 1, 1, 2, 1, 2, 1, 3])
        self.assertTrue(rows[0]["is_origin"])
        self.assertTrue(rows[1]["is_prime_layer"])
        self.assertTrue(rows[7]["is_prime_power"])
        self.assertEqual(rows[7]["return_path"], (8, 4, 2, 1))

    def test_shell_summaries_group_by_factor_layer(self) -> None:
        summaries = {item["depth"]: item for item in shell_summaries(origin_rows(12))}

        self.assertEqual(summaries[0]["count"], 1)
        self.assertEqual(summaries[1]["prime_layer_count"], 5)
        self.assertEqual(summaries[2]["count"], 4)
        self.assertEqual(summaries[3]["count"], 2)
        self.assertEqual(summaries[3]["first_n"], 8)

    def test_first_depth_occurrences_match_binary_stacks(self) -> None:
        firsts = first_depth_occurrences(origin_rows(32))

        self.assertEqual(
            [(item["depth"], item["first_n"], item["minimal_binary_stack"]) for item in firsts],
            [(0, 1, 1), (1, 2, 2), (2, 4, 4), (3, 8, 8), (4, 16, 16), (5, 32, 32)],
        )
        self.assertTrue(all(item["matches_binary_stack"] for item in firsts))

    def test_branching_hotspots_rank_high_divisor_counts(self) -> None:
        hotspots = branching_hotspots(origin_rows(32), count=3)

        self.assertEqual(hotspots[0][0], 24)
        self.assertEqual(hotspots[0][3], 8)
        self.assertIn("24 -> 12 -> 6 -> 3 -> 1", hotspots[0][-1])


if __name__ == "__main__":
    unittest.main()
