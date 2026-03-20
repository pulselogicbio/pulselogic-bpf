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

    required_analysis_keys = ["top_n_features"]
    for key in required_analysis_keys:
        if key not in config["analysis"]:
            raise ValueError(f"Missing required analysis config key: analysis.{key}")

    required_output_keys = [
        "base_dir",
        "auc_table",
        "fused_scores",
        "audit_json",
        "checkpoint_json",
        "manifest_json",
        "executive_summary_txt",
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
]