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


def build_feature_stability_summary(
    expression_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    *,
    iterations: int = 100,
    top_n_features: int = 3,
    sample_col: str = "sample_id",
    label_col: str = "label",
    random_seed: int = 42,
) -> dict:
    from collections import Counter
    from bpf.ranking.auc_ranker import compute_feature_auc_table

    if sample_col not in expression_df.columns:
        raise ValueError(f"Expression data missing required column: {sample_col}")

    if sample_col not in labels_df.columns:
        raise ValueError(f"Labels data missing required column: {sample_col}")

    if label_col not in labels_df.columns:
        raise ValueError(f"Labels data missing required column: {label_col}")

    if iterations <= 0:
        raise ValueError("iterations must be > 0")

    if top_n_features <= 0:
        raise ValueError("top_n_features must be > 0")

    rng = np.random.default_rng(random_seed)
    feature_counter = Counter()

    for _ in range(iterations):
        sample_idx = rng.choice(len(expression_df), size=len(expression_df), replace=True)
        boot_expression_df = expression_df.iloc[sample_idx].reset_index(drop=True)

        boot_labels_df = labels_df.merge(
            boot_expression_df[[sample_col]],
            on=sample_col,
            how="inner",
        )

        auc_df = compute_feature_auc_table(
            boot_expression_df,
            boot_labels_df,
            sample_col=sample_col,
            label_col=label_col,
        )

        selected_features = auc_df["feature"].head(top_n_features).tolist()
        feature_counter.update(selected_features)

    sorted_items = sorted(feature_counter.items(), key=lambda x: (-x[1], x[0]))

    feature_counts = {feature: int(count) for feature, count in sorted_items}
    feature_frequency = {
        feature: float(count / iterations) for feature, count in sorted_items
    }

    return {
        "iterations": int(iterations),
        "top_n_features": int(top_n_features),
        "random_seed": int(random_seed),
        "feature_counts": feature_counts,
        "feature_frequency": feature_frequency,
    }


def build_feature_auc_bootstrap_summary(
    expression_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    *,
    iterations: int = 100,
    ci_percentiles: tuple[float, float] = (2.5, 97.5),
    sample_col: str = "sample_id",
    label_col: str = "label",
    random_seed: int = 42,
) -> dict:
    from collections import defaultdict
    from bpf.ranking.auc_ranker import compute_feature_auc_table

    if sample_col not in expression_df.columns:
        raise ValueError(f"Expression data missing required column: {sample_col}")

    if sample_col not in labels_df.columns:
        raise ValueError(f"Labels data missing required column: {sample_col}")

    if label_col not in labels_df.columns:
        raise ValueError(f"Labels data missing required column: {label_col}")

    if iterations <= 0:
        raise ValueError("iterations must be > 0")

    rng = np.random.default_rng(random_seed)
    lower_p, upper_p = ci_percentiles
    auc_store: dict[str, list[float]] = defaultdict(list)

    for _ in range(iterations):
        sample_idx = rng.choice(len(expression_df), size=len(expression_df), replace=True)
        boot_expression_df = expression_df.iloc[sample_idx].reset_index(drop=True)

        boot_labels_df = labels_df.merge(
            boot_expression_df[[sample_col]],
            on=sample_col,
            how="inner",
        )

        auc_df = compute_feature_auc_table(
            boot_expression_df,
            boot_labels_df,
            sample_col=sample_col,
            label_col=label_col,
        )

        for _, row in auc_df.iterrows():
            auc_store[str(row["feature"])].append(float(row["auc"]))

    feature_summaries = {}
    for feature in sorted(auc_store.keys()):
        values = np.array(auc_store[feature], dtype=float)
        feature_summaries[feature] = {
            "n": int(len(values)),
            "mean_auc": float(np.mean(values)),
            "std_auc": float(np.std(values, ddof=0)),
            "ci_percentiles": [lower_p, upper_p],
            "ci_lower": float(np.percentile(values, lower_p)),
            "ci_upper": float(np.percentile(values, upper_p)),
        }

    return {
        "iterations": int(iterations),
        "random_seed": int(random_seed),
        "ci_percentiles": [lower_p, upper_p],
        "feature_auc_summary": feature_summaries,
    }