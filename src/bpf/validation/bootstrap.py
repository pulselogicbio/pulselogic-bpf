import numpy as np
import pandas as pd

from bpf.fusion.scorer import compute_fused_scores


def build_bootstrap_summary(
    expression_df: pd.DataFrame,
    auc_df: pd.DataFrame,
    top_features: list[str],
    *,
    iterations: int = 100,
    ci_percentiles: tuple[float, float] = (2.5, 97.5),
    use_direction_aware_fusion: bool = True,
    use_auc_weights: bool = True,
    sample_col: str = "sample_id",
    random_seed: int = 42,
) -> dict:
    rng = np.random.default_rng(random_seed)
    bootstrap_means = []

    for _ in range(iterations):
        sample_idx = rng.choice(len(expression_df), size=len(expression_df), replace=True)
        boot_expression_df = expression_df.iloc[sample_idx].reset_index(drop=True)

        fused_df = compute_fused_scores(
            boot_expression_df,
            auc_df,
            top_features=top_features,
            sample_col=sample_col,
            use_direction_aware_fusion=use_direction_aware_fusion,
            use_auc_weights=use_auc_weights,
        )

        bootstrap_means.append(float(fused_df["fused_raw_score"].mean()))

    lower_p, upper_p = ci_percentiles

    return {
        "iterations": iterations,
        "random_seed": random_seed,
        "top_features": top_features,
        "mean_fused_raw_score": float(np.mean(bootstrap_means)),
        "std_fused_raw_score": float(np.std(bootstrap_means, ddof=0)),
        "ci_percentiles": [lower_p, upper_p],
        "ci_lower": float(np.percentile(bootstrap_means, lower_p)),
        "ci_upper": float(np.percentile(bootstrap_means, upper_p)),
    }