from bpf.selection.policy import build_feature_selection_policy


def test_build_feature_selection_policy_classifies_features():
    stability = {
        "feature_frequency": {
            "BMK1": 0.95,
            "BMK2": 0.90,
            "BMK3": 0.30,
            "BMK4": 0.10,
        }
    }

    auc_bootstrap = {
        "feature_auc_summary": {
            "BMK1": {"mean_auc": 0.95, "ci_lower": 0.90, "ci_upper": 0.98},
            "BMK2": {"mean_auc": 0.10, "ci_lower": 0.05, "ci_upper": 0.18},
            "BMK3": {"mean_auc": 0.70, "ci_lower": 0.40, "ci_upper": 0.95},
            "BMK4": {"mean_auc": 0.52, "ci_lower": 0.49, "ci_upper": 0.55},
        }
    }

    result = build_feature_selection_policy(
        stability,
        auc_bootstrap,
        min_stability_frequency=0.80,
        min_auc_margin=0.20,
        max_ci_width=0.25,
        reject_auc_margin=0.05,
    )

    assert "BMK1" in result["selected_features"]
    assert "BMK2" in result["selected_features"]
    assert "BMK3" in result["unstable_features"]
    assert "BMK4" in result["rejected_features"]