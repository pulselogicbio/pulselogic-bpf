from bpf.fusion.weights import build_auc_weights
import pandas as pd


def test_build_auc_weights_normalizes_to_one():
    auc_df = pd.DataFrame(
        {
            "feature": ["BMK1", "BMK2", "BMK3"],
            "abs_auc": [0.9, 0.8, 0.7],
        }
    )

    weights = build_auc_weights(auc_df, ["BMK1", "BMK2", "BMK3"])

    total = sum(weights.values())
    assert abs(total - 1.0) < 1e-9
    assert set(weights.keys()) == {"BMK1", "BMK2", "BMK3"}