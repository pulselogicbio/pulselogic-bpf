import pytest

from bpf.io.manifests import validate_run_config


def test_validate_run_config_accepts_valid_config():
    config = {
        "canonical_version": "v1.0.0",
        "run_label": "test",
        "random_seed": 42,
        "inputs": {
            "expression_matrix": "examples/toy_expression.csv",
            "labels": "examples/toy_labels.csv",
        },
        "analysis": {
            "top_n_features": 3,
            "use_direction_aware_fusion": True,
            "use_auc_weights": True,
            "bootstrap_enabled": True,
            "bootstrap_iterations": 100,
            "bootstrap_ci_percentiles": [2.5, 97.5],
        },
        "outputs": {
            "base_dir": "outputs",
            "auc_table": "demo_auc_ranking.csv",
            "fused_scores": "demo_fused_scores.csv",
            "audit_json": "demo_run_audit.json",
            "checkpoint_json": "demo_checkpoint_log.json",
            "manifest_json": "demo_run_manifest.json",
            "executive_summary_txt": "EXECUTIVE_SUMMARY.txt",
            "quarantine_json": "QUARANTINE.json",
            "run_fingerprint_json": "RUN_FINGERPRINT.json",
            "bootstrap_summary_json": "BOOTSTRAP_SUMMARY.json",
        },
    }

    validate_run_config(config)


def test_validate_run_config_raises_on_missing_key():
    config = {
        "run_label": "test",
        "random_seed": 42,
        "inputs": {},
        "analysis": {},
        "outputs": {},
    }

    with pytest.raises(ValueError, match="Missing required config key: canonical_version"):
        validate_run_config(config)