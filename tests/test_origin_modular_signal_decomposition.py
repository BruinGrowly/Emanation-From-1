from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.origin_modular_group_controls import baseline_features_for_target  # noqa: E402
from experiments.origin_modular_signal_decomposition import (  # noqa: E402
    EXACT_GROUPS,
    PROXY_GROUPS,
    TARGET,
    exact_log_contribution_summary,
    model_rows,
    prepared_dataset,
    r_squared_for_keys,
    shapley_r2_attribution,
)
from experiments.origin_modular_shell_transfer import shell_conditioned_residuals  # noqa: E402


class OriginModularSignalDecompositionTests(unittest.TestCase):
    def test_prepared_dataset_adds_exact_log_identity_fields(self) -> None:
        dataset = prepared_dataset(256, max_bases=4, candidate_base_limit=20)

        for row in dataset:
            self.assertAlmostEqual(
                row[TARGET],
                row["log_local_defect"] + row["neg_log_overlap_penalty"],
            )

    def test_exact_contribution_summary_preserves_identity_after_conditioning(self) -> None:
        dataset = prepared_dataset(512, max_bases=4, candidate_base_limit=20)
        baseline_features = baseline_features_for_target("lambda_over_phi")
        summary = exact_log_contribution_summary(dataset, baseline_features)

        self.assertAlmostEqual(summary["share_sum"], 1.0, places=10)
        self.assertLess(summary["max_identity_error"], 1e-10)
        self.assertGreater(summary["overlap_share"], summary["local_defect_share"])

    def test_exact_terms_explain_conditioned_log_target(self) -> None:
        dataset = prepared_dataset(512, max_bases=4, candidate_base_limit=20)
        baseline_features = baseline_features_for_target("lambda_over_phi")
        target_values = shell_conditioned_residuals(dataset, TARGET, baseline_features)

        score = r_squared_for_keys(
            dataset,
            target_values,
            ["log_local_defect", "neg_log_overlap_penalty"],
            baseline_features,
        )

        self.assertAlmostEqual(score, 1.0, places=10)

    def test_model_rows_include_proxy_and_exact_models(self) -> None:
        dataset = prepared_dataset(512, max_bases=4, candidate_base_limit=20)
        baseline_features = baseline_features_for_target("lambda_over_phi")
        rows = model_rows(dataset, baseline_features)
        labels = [row[0] for row in rows]

        self.assertIn("concentration_proxy", labels)
        self.assertIn("exact_local_plus_overlap", labels)

    def test_shapley_attribution_is_deterministic_and_sums_to_model_r2(self) -> None:
        dataset = prepared_dataset(512, max_bases=4, candidate_base_limit=20)
        baseline_features = baseline_features_for_target("lambda_over_phi")
        first = shapley_r2_attribution(dataset, PROXY_GROUPS, baseline_features)
        second = shapley_r2_attribution(dataset, PROXY_GROUPS, baseline_features)

        self.assertEqual(first, second)
        self.assertGreater(sum(row["r2_share"] for row in first), 0.0)

        exact = shapley_r2_attribution(dataset, EXACT_GROUPS, baseline_features)
        self.assertAlmostEqual(sum(row["r2_share"] for row in exact), 1.0, places=10)


if __name__ == "__main__":
    unittest.main()
