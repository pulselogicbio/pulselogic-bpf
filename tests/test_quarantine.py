from pathlib import Path
import pytest
import yaml

from bpf.pipeline import run_pipeline


def test_run_pipeline_writes_quarantine_on_invalid_config(tmp_path):
    bad_config = {
        "canonical_version": "v1.0.0",
        "run_label": "bad_run",
        "random_seed": 42,
        "inputs": {
            "expression_matrix": "examples/toy_expression.csv",
            "labels": "examples/toy_labels.csv",
        },
        "analysis": {
            "top_n_features": 3,
        },
        "outputs": {
            "base_dir": str(tmp_path),
            "auc_table": "demo_auc_ranking.csv",
            "fused_scores": "demo_fused_scores.csv",
            "audit_json": "demo_run_audit.json",
            "checkpoint_json": "demo_checkpoint_log.json",
            "manifest_json": "demo_run_manifest.json",
            "executive_summary_txt": "EXECUTIVE_SUMMARY.txt",
            "quarantine_json": "QUARANTINE.json",
            "run_fingerprint_json": "RUN_FINGERPRINT.json",
            "bootstrap_summary_json": "BOOTSTRAP_SUMMARY.json",
            "feature_stability_json": "FEATURE_STABILITY.json",
            "feature_auc_bootstrap_json": "FEATURE_AUC_BOOTSTRAP.json",
        },
    }

    del bad_config["inputs"]["labels"]

    config_path = tmp_path / "bad_config.yaml"
    config_path.write_text(yaml.safe_dump(bad_config), encoding="utf-8")

    with pytest.raises(ValueError):
        run_pipeline(config_path)

    quarantine_path = tmp_path / "QUARANTINE.json"
    assert quarantine_path.exists()
    text = quarantine_path.read_text(encoding="utf-8")
    assert '"status": "quarantined"' in text