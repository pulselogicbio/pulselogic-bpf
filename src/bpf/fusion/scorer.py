import pandas as pd

from bpf.fusion.zscore import zscore_columns
from bpf.fusion.logistic import logistic_transform
from bpf.fusion.weights import build_auc_weights


def compute_fused_scores(
    expression_df: pd.DataFrame,
    auc_df: pd.DataFrame,
    top_features: list[str],
    *,
    sample_col: str = "sample_id",
    use_direction_aware_fusion: bool = True,
    use_auc_weights: bool = True,
) -> pd.DataFrame:
    working = expression_df[[sample_col] + top_features].copy()
    working = zscore_columns(working, top_features)

    feature_meta = (
        auc_df[auc_df["feature"].isin(top_features)][["feature", "direction", "abs_auc"]]
        .drop_duplicates()
        .set_index("feature")
    )

    adjusted = working.copy()

    if use_direction_aware_fusion:
        for feature in top_features:
            direction = feature_meta.loc[feature, "direction"]
            if direction == "down_in_case":
                adjusted[feature] = -1.0 * adjusted[feature]

    if use_auc_weights:
        weights = build_auc_weights(auc_df, top_features)
    else:
        n = len(top_features)
        weights = {feature: 1.0 / n for feature in top_features}

    adjusted["fused_raw_score"] = 0.0
    for feature in top_features:
        adjusted["fused_raw_score"] += adjusted[feature] * weights[feature]

    adjusted["fused_probability"] = logistic_transform(adjusted["fused_raw_score"])

    return adjusted[[sample_col, "fused_raw_score", "fused_probability"]]