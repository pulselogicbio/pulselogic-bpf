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

    result = compute_fused_scores(expression_df, top_features=["BMK1", "BMK2"])

    assert list(result.columns) == ["sample_id", "fused_raw_score", "fused_probability"]
    assert len(result) == 3