import pandas as pd


def build_auc_weights(
    auc_df: pd.DataFrame,
    features: list[str],
) -> dict[str, float]:
    subset = auc_df[auc_df["feature"].isin(features)].copy()
    if subset.empty:
        raise ValueError("No matching features found for weight construction.")

    weights = {row["feature"]: float(row["abs_auc"]) for _, row in subset.iterrows()}
    total = sum(weights.values())
    if total == 0:
        n = len(weights)
        return {k: 1.0 / n for k in weights}

    return {k: v / total for k, v in weights.items()}