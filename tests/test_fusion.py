import pandas as pd

from bpf.fusion.scorer import compute_fused_scores


def test_compute_fused_scores_returns_expected_columns():
    expression_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3"],
            "BMK1": [1.0, 2.0, 3.0],
            "BMK2": [2.0, 3.0, 4.0],
            "BMK3": [3.0, 4.0, 5.0],
        }
    )

    auc_df = pd.DataFrame(
        {
            "feature": ["BMK1", "BMK2", "BMK3"],
            "auc": [0.9, 0.2, 0.8],
            "abs_auc": [0.9, 0.8, 0.8],
            "direction": ["up_in_case", "down_in_case", "up_in_case"],
        }
    )

    result = compute_fused_scores(
        expression_df,
        auc_df,
        top_features=["BMK1", "BMK2"],
        use_direction_aware_fusion=True,
        use_auc_weights=True,
    )

    assert list(result.columns) == ["sample_id", "fused_raw_score", "fused_probability"]
    assert len(result) == 3


def test_compute_fused_scores_handles_equal_weight_mode():
    expression_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2"],
            "BMK1": [1.0, 2.0],
            "BMK2": [2.0, 1.0],
        }
    )

    auc_df = pd.DataFrame(
        {
            "feature": ["BMK1", "BMK2"],
            "auc": [0.9, 0.1],
            "abs_auc": [0.9, 0.9],
            "direction": ["up_in_case", "down_in_case"],
        }
    )

    result = compute_fused_scores(
        expression_df,
        auc_df,
        top_features=["BMK1", "BMK2"],
        use_direction_aware_fusion=True,
        use_auc_weights=False,
    )

    assert len(result) == 2
    assert "fused_probability" in result.columns