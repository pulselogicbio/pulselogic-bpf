import pandas as pd
from sklearn.metrics import roc_auc_score

def compute_feature_auc_table(
    expression_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    sample_col: str = "sample_id",
    label_col: str = "label",
) -> pd.DataFrame:
    merged = labels_df.merge(expression_df, on=sample_col, how="inner")
    if merged.empty:
        raise ValueError("No overlapping samples found between labels and expression data.")

    y = merged[label_col]
    feature_cols = [c for c in merged.columns if c not in {sample_col, label_col}]
    rows = []

    for feature in feature_cols:
        x = merged[feature]
        auc = roc_auc_score(y, x)
        direction = "up_in_case" if auc >= 0.5 else "down_in_case"
        rows.append(
            {
                "feature": feature,
                "auc": float(auc),
                "abs_auc": float(max(auc, 1 - auc)),
                "direction": direction,
            }
        )

    result = pd.DataFrame(rows).sort_values(["abs_auc", "feature"], ascending=[False, True])
    result.reset_index(drop=True, inplace=True)
    return result