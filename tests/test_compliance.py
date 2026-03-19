from bpf.compliance.checkpoint import build_checkpoint_log


def test_build_checkpoint_log_passes_with_valid_inputs():
    result = build_checkpoint_log(
        auc_rows=5,
        fused_rows=10,
        top_features=["BMK1", "BMK2", "BMK4"],
    )

    assert result["status"] == "pass"
    assert result["checks"]["auc_table_nonempty"] is True
    assert result["checks"]["fused_scores_nonempty"] is True
    assert result["checks"]["top_features_present"] is True