def build_model_assembly(
    auc_df,
    feature_selection_policy: dict,
) -> dict:
    selected_features = feature_selection_policy.get("selected_features", [])
    feature_decisions = feature_selection_policy.get("feature_decisions", {})

    selected_auc_df = auc_df[auc_df["feature"].isin(selected_features)].copy()

    if selected_auc_df.empty:
        return {
            "selected_features": [],
            "feature_spec": {},
            "normalized_weights": {},
            "assembly_status": "empty",
        }

    abs_auc_map = {
        row["feature"]: float(row["abs_auc"])
        for _, row in selected_auc_df.iterrows()
    }

    total = sum(abs_auc_map.values())
    if total == 0:
        n = len(abs_auc_map)
        normalized_weights = {k: 1.0 / n for k in abs_auc_map}
    else:
        normalized_weights = {k: v / total for k, v in abs_auc_map.items()}

    feature_spec = {}
    for feature in selected_features:
        decision_meta = feature_decisions.get(feature, {})
        direction = decision_meta.get("direction", "positive")
        sign = 1.0 if direction == "positive" else -1.0

        feature_spec[feature] = {
            "direction": direction,
            "sign": sign,
            "abs_auc": float(abs_auc_map.get(feature, 0.0)),
            "normalized_weight": float(normalized_weights.get(feature, 0.0)),
        }

    return {
        "selected_features": selected_features,
        "feature_spec": feature_spec,
        "normalized_weights": normalized_weights,
        "assembly_status": "ready",
    }