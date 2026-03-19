import pandas as pd

from bpf.ranking.auc_ranker import compute_feature_auc_table


def test_compute_feature_auc_table_returns_expected_columns():
    expression_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "BMK1": [9.0, 8.5, 2.0, 1.5],
            "BMK2": [1.0, 1.5, 8.0, 8.5],
        }
    )
    labels_df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3", "S4"],
            "label": [1, 1, 0, 0],
        }
    )

    result = compute_feature_auc_table(expression_df, labels_df)

    assert list(result.columns) == ["feature", "auc", "abs_auc", "direction"]
    assert len(result) == 2