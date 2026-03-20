def build_feature_selection_policy(
    feature_stability_summary: dict,
    feature_auc_bootstrap_summary: dict,
    *,
    min_stability_frequency: float = 0.80,
    min_auc_margin: float = 0.20,
    max_ci_width: float = 0.25,
    reject_auc_margin: float = 0.05,
) -> dict:
    """
    Build a decision-layer policy for feature selection.

    A feature is selected if:
    - it is frequently selected across bootstrap resamples
    - its mean AUC is meaningfully far from 0.5
    - its bootstrap CI width is reasonably tight

    A feature is rejected if:
    - its mean AUC is too close to 0.5

    Otherwise it is classified as unstable.
    """

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
        auc_margin = abs(mean_auc - 0.5)

        if (
            stability >= min_stability_frequency
            and auc_margin >= min_auc_margin
            and ci_width <= max_ci_width
        ):
            decision = "selected"
            selected_features.append(feature)
        elif auc_margin < reject_auc_margin:
            decision = "rejected"
            rejected_features.append(feature)
        else:
            decision = "unstable"
            unstable_features.append(feature)

        feature_decisions[feature] = {
            "decision": decision,
            "stability_frequency": stability,
            "mean_auc": mean_auc,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "ci_width": ci_width,
            "auc_margin_from_0_5": auc_margin,
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