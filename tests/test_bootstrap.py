import pandas as pd

from bpf.validation.bootstrap import build_bootstrap_summary


def test_build_bootstrap_summary_returns_expected_keys():
    expression_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "BMK1": [1.0, 2.0, 3.0, 4.0],
            "BMK2": [4.0, 3.0, 2.0, 1.0],
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

    result = build_bootstrap_summary(
        expression_df,
        auc_df,
        top_features=["BMK1", "BMK2"],
        iterations=25,
        ci_percentiles=(2.5, 97.5),
        use_direction_aware_fusion=True,
        use_auc_weights=True,
        random_seed=42,
    )

    assert "iterations" in result
    assert "mean_fused_raw_score" in result
    assert "std_fused_raw_score" in result
    assert "ci_lower" in result
    assert "ci_upper" in result
    assert result["iterations"] == 25