import pandas as pd

from bpf.fusion.zscore import zscore_columns
from bpf.fusion.logistic import logistic_transform


def compute_fused_scores(
    expression_df: pd.DataFrame,
    top_features: list[str],
    sample_col: str = "sample_id",
) -> pd.DataFrame:
    working = expression_df[[sample_col] + top_features].copy()
    working = zscore_columns(working, top_features)
    working["fused_raw_score"] = working[top_features].mean(axis=1)
    working["fused_probability"] = logistic_transform(working["fused_raw_score"])
    return working[[sample_col, "fused_raw_score", "fused_probability"]]