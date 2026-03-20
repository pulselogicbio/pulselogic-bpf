import pandas as pd

from bpf.validation.bootstrap import build_feature_auc_bootstrap_summary


def test_build_feature_auc_bootstrap_summary_returns_expected_keys():
    expression_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "BMK1": [1.0, 2.0, 3.0, 4.0],
            "BMK2": [4.0, 3.0, 2.0, 1.0],
        }
    )

    labels_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "label": [1, 1, 0, 0],
        }
    )

    result = build_feature_auc_bootstrap_summary(
        expression_df,
        labels_df,
        iterations=25,
        ci_percentiles=(2.5, 97.5),
        sample_col="sample_id",
        label_col="label",
        random_seed=42,
    )

    assert "iterations" in result
    assert "random_seed" in result
    assert "ci_percentiles" in result
    assert "feature_auc_summary" in result
    assert "BMK1" in result["feature_auc_summary"]