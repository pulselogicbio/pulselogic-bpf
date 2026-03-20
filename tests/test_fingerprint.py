from bpf.io.hashing import build_run_fingerprint


def test_build_run_fingerprint_returns_sha256():
    payload = {
        "config_sha256": "abc",
        "input_hashes": {"expression_matrix": "def"},
        "output_hashes": {"auc_table": "ghi"},
    }

    result = build_run_fingerprint(payload)

    assert "fingerprint_payload" in result
    assert "canonical_payload_sha256" in result
    assert len(result["canonical_payload_sha256"]) == 64