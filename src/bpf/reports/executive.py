from pathlib import Path


def write_executive_summary(
    path: str | Path,
    *,
    package_version: str,
    canonical_version: str,
    run_label: str,
    random_seed: int,
    timestamp_utc: str,
    config_path: str,
    invocation_mode: str,
    top_features: list[str],
    expression_rows: int,
    labels_rows: int,
    auc_rows: int,
    fused_rows: int,
    checkpoint_status: str,
    auc_output_path: str,
    fused_output_path: str,
    audit_output_path: str,
    checkpoint_output_path: str,
    manifest_output_path: str,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "PulseLogic BPF - Executive Summary",
        "==================================",
        "",
        f"Package version: {package_version}",
        f"Canonical version: {canonical_version}",
        f"Run label: {run_label}",
        f"Timestamp (UTC): {timestamp_utc}",
        f"Invocation mode: {invocation_mode}",
        f"Config path: {config_path}",
        f"Random seed: {random_seed}",
        "",
        "Selected top features:",
        ", ".join(top_features) if top_features else "(none)",
        "",
        "Row counts:",
        f"- expression rows: {expression_rows}",
        f"- labels rows: {labels_rows}",
        f"- auc rows: {auc_rows}",
        f"- fused rows: {fused_rows}",
        "",
        f"Checkpoint status: {checkpoint_status}",
        "",
        "Outputs:",
        f"- AUC table: {auc_output_path}",
        f"- Fused scores: {fused_output_path}",
        f"- Audit log: {audit_output_path}",
        f"- Checkpoint log: {checkpoint_output_path}",
        f"- Run manifest: {manifest_output_path}",
        "",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")