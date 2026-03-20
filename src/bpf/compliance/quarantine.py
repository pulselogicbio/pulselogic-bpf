from pathlib import Path
from typing import Any
import json


def write_quarantine_record(
    path: str | Path,
    *,
    timestamp_utc: str,
    invocation_mode: str,
    config_path: str,
    error_type: str,
    error_message: str,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "status": "quarantined",
        "timestamp_utc": timestamp_utc,
        "invocation_mode": invocation_mode,
        "config_path": config_path,
        "error_type": error_type,
        "error_message": error_message,
    }

    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")