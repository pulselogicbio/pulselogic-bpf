import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: str | Path) -> str:
    path = Path(path)
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json_dumps(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def build_run_fingerprint(payload: dict[str, Any]) -> dict[str, Any]:
    canonical_payload = canonical_json_dumps(payload)
    fingerprint = sha256_text(canonical_payload)

    return {
        "fingerprint_payload": payload,
        "canonical_payload_sha256": fingerprint,
    }