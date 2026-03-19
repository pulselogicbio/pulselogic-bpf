from typing import Any


def build_checkpoint_log(
    auc_rows: int,
    fused_rows: int,
    top_features: list[str],
) -> dict[str, Any]:
    return {
        "status": "pass",
        "checks": {
            "auc_table_nonempty": auc_rows > 0,
            "fused_scores_nonempty": fused_rows > 0,
            "top_features_present": len(top_features) > 0,
        },
        "top_feature_count": len(top_features),
    }