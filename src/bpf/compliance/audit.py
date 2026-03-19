from pathlib import Path
from typing import Any

from bpf.io.hashing import sha256_file


def build_run_audit(
    config_path: str | Path,
    expression_path: str | Path,
    labels_path: str | Path,
    top_features: list[str],
) -> dict[str, Any]:
    return {
        "config_path": str(config_path),
        "expression_path": str(expression_path),
        "labels_path": str(labels_path),
        "config_sha256": sha256_file(config_path),
        "expression_sha256": sha256_file(expression_path),
        "labels_sha256": sha256_file(labels_path),
        "top_features": top_features,
    }