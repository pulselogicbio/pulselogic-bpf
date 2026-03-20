from typing import Any


def validate_run_config(config: dict[str, Any]) -> None:
    required_top_keys = ["canonical_version", "run_label", "random_seed", "inputs", "analysis", "outputs"]
    for key in required_top_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    required_input_keys = ["expression_matrix", "labels"]
    for key in required_input_keys:
        if key not in config["inputs"]:
            raise ValueError(f"Missing required input config key: inputs.{key}")

    required_analysis_keys = [
    "top_n_features",
    "use_direction_aware_fusion",
    "use_auc_weights",
    "bootstrap_enabled",
    "bootstrap_iterations",
    "bootstrap_ci_percentiles",
    "selection_min_stability_frequency",
    "selection_min_auc_margin",
    "selection_max_ci_width",
    "selection_reject_auc_margin",
]

    required_output_keys = [
    "base_dir",
    "auc_table",
    "fused_scores",
    "audit_json",
    "checkpoint_json",
    "manifest_json",
    "executive_summary_txt",
    "quarantine_json",
    "run_fingerprint_json",
    "bootstrap_summary_json",
    "feature_stability_json",
    "feature_auc_bootstrap_json",
    "feature_selection_policy_json",
    "model_assembly_json",
]
    for key in required_output_keys:
        required_output_keys = [
    "base_dir",
    "auc_table",
    "fused_scores",
    "audit_json",
    "checkpoint_json",
    "manifest_json",
    "executive_summary_txt",
    "quarantine_json",
    "run_fingerprint_json",
    "bootstrap_summary_json",
]