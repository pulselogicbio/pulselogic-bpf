from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

from bpf.io.loaders import load_csv
from bpf.io.writers import write_json
from bpf.ranking.auc_ranker import compute_feature_auc_table
from bpf.fusion.scorer import compute_fused_scores
from bpf.compliance.audit import build_run_audit
from bpf.compliance.checkpoint import build_checkpoint_log
from bpf.reports.executive import write_executive_summary
from bpf.version import __version__


def run_pipeline(config_path: str | Path, invocation_mode: str = "script") -> dict[str, Any]:
    config_path = Path(config_path)
    timestamp_utc = datetime.now(timezone.utc).isoformat()

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    expression_path = Path(config["inputs"]["expression_matrix"])
    labels_path = Path(config["inputs"]["labels"])
    top_n_features = int(config["analysis"]["top_n_features"])

    output_dir = Path(config["outputs"]["base_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    auc_output_path = output_dir / config["outputs"]["auc_table"]
    fused_output_path = output_dir / config["outputs"]["fused_scores"]
    audit_output_path = output_dir / config["outputs"]["audit_json"]
    checkpoint_output_path = output_dir / config["outputs"]["checkpoint_json"]
    manifest_output_path = output_dir / config["outputs"]["manifest_json"]
    executive_summary_path = output_dir / config["outputs"]["executive_summary_txt"]

    expression_df = load_csv(expression_path)
    labels_df = load_csv(labels_path)

    auc_df = compute_feature_auc_table(expression_df, labels_df)
    auc_df.to_csv(auc_output_path, index=False)

    top_features = auc_df["feature"].head(top_n_features).tolist()
    fused_df = compute_fused_scores(expression_df, top_features=top_features)
    fused_df.to_csv(fused_output_path, index=False)

    audit = build_run_audit(
        config_path=config_path,
        expression_path=expression_path,
        labels_path=labels_path,
        top_features=top_features,
    )
    write_json(audit, audit_output_path)

    checkpoint = build_checkpoint_log(
        auc_rows=len(auc_df),
        fused_rows=len(fused_df),
        top_features=top_features,
    )
    write_json(checkpoint, checkpoint_output_path)

    manifest = {
        "package_version": __version__,
        "canonical_version": config["canonical_version"],
        "run_label": config["run_label"],
        "timestamp_utc": timestamp_utc,
        "invocation_mode": invocation_mode,
        "config_path": str(config_path),
        "manifest_path": str(manifest_output_path),
        "random_seed": config["random_seed"],
        "top_n_features": top_n_features,
        "selected_top_features": top_features,
        "row_counts": {
            "expression_rows": len(expression_df),
            "labels_rows": len(labels_df),
            "auc_rows": len(auc_df),
            "fused_rows": len(fused_df),
        },
        "outputs": {
            "auc_table": str(auc_output_path),
            "fused_scores": str(fused_output_path),
            "audit_json": str(audit_output_path),
            "checkpoint_json": str(checkpoint_output_path),
            "executive_summary_txt": str(executive_summary_path),
        },
    }
    write_json(manifest, manifest_output_path)

    write_executive_summary(
        executive_summary_path,
        package_version=__version__,
        canonical_version=config["canonical_version"],
        run_label=config["run_label"],
        random_seed=config["random_seed"],
        timestamp_utc=timestamp_utc,
        config_path=str(config_path),
        invocation_mode=invocation_mode,
        top_features=top_features,
        expression_rows=len(expression_df),
        labels_rows=len(labels_df),
        auc_rows=len(auc_df),
        fused_rows=len(fused_df),
        checkpoint_status=checkpoint["status"],
        auc_output_path=str(auc_output_path),
        fused_output_path=str(fused_output_path),
        audit_output_path=str(audit_output_path),
        checkpoint_output_path=str(checkpoint_output_path),
        manifest_output_path=str(manifest_output_path),
    )

    return {
        "auc_output_path": auc_output_path,
        "fused_output_path": fused_output_path,
        "audit_output_path": audit_output_path,
        "checkpoint_output_path": checkpoint_output_path,
        "manifest_output_path": manifest_output_path,
        "executive_summary_path": executive_summary_path,
        "top_features": top_features,
    }