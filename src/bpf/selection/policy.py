def build_feature_selection_policy(
    feature_stability_summary: dict,
    feature_auc_bootstrap_summary: dict,
    *,
    min_stability_frequency: float = 0.80,
    min_auc_margin: float = 0.20,
    max_ci_width: float = 0.25,
    reject_auc_margin: float = 0.05,
) -> dict:
    stability_freq = feature_stability_summary.get("feature_frequency", {})
    auc_summary = feature_auc_bootstrap_summary.get("feature_auc_summary", {})

    all_features = sorted(set(stability_freq.keys()) | set(auc_summary.keys()))

    selected_features = []
    rejected_features = []
    unstable_features = []
    feature_decisions = {}

    for feature in all_features:
        stability = float(stability_freq.get(feature, 0.0))
        auc_info = auc_summary.get(feature)

        if auc_info is None:
            feature_decisions[feature] = {
                "decision": "unstable",
                "reason": "missing_auc_summary",
                "stability_frequency": stability,
            }
            unstable_features.append(feature)
            continue

        mean_auc = float(auc_info["mean_auc"])
        ci_lower = float(auc_info["ci_lower"])
        ci_upper = float(auc_info["ci_upper"])
        ci_width = ci_upper - ci_lower

        direction = "positive" if mean_auc >= 0.5 else "inverse"
        adjusted_auc = max(mean_auc, 1.0 - mean_auc)
        adjusted_auc_margin = adjusted_auc - 0.5

        if (
            stability >= min_stability_frequency
            and adjusted_auc_margin >= min_auc_margin
            and ci_width <= max_ci_width
        ):
            decision = "selected"
            selected_features.append(feature)
        elif adjusted_auc_margin < reject_auc_margin:
            decision = "rejected"
            rejected_features.append(feature)
        else:
            decision = "unstable"
            unstable_features.append(feature)

        feature_decisions[feature] = {
            "decision": decision,
            "direction": direction,
            "stability_frequency": stability,
            "mean_auc": mean_auc,
            "adjusted_auc": adjusted_auc,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "ci_width": ci_width,
            "adjusted_auc_margin_from_0_5": adjusted_auc_margin,
        }

    return {
        "policy_thresholds": {
            "min_stability_frequency": float(min_stability_frequency),
            "min_auc_margin": float(min_auc_margin),
            "max_ci_width": float(max_ci_width),
            "reject_auc_margin": float(reject_auc_margin),
        },
        "selected_features": selected_features,
        "rejected_features": rejected_features,
        "unstable_features": unstable_features,
        "feature_decisions": feature_decisions,
    }