from pathlib import Path
import yaml

from bpf.io.loaders import load_csv
from bpf.ranking.auc_ranker import compute_feature_auc_table
from bpf.fusion.scorer import compute_fused_scores


def main() -> None:
    config_path = Path("configs/canonical_v1_0_0.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    expression_path = config["inputs"]["expression_matrix"]
    labels_path = config["inputs"]["labels"]
    top_n_features = int(config["analysis"]["top_n_features"])

    output_dir = Path(config["outputs"]["base_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    auc_output_path = output_dir / config["outputs"]["auc_table"]
    fused_output_path = output_dir / config["outputs"]["fused_scores"]

    expression_df = load_csv(expression_path)
    labels_df = load_csv(labels_path)

    auc_df = compute_feature_auc_table(expression_df, labels_df)
    auc_df.to_csv(auc_output_path, index=False)

    top_features = auc_df["feature"].head(top_n_features).tolist()
    fused_df = compute_fused_scores(expression_df, top_features=top_features)
    fused_df.to_csv(fused_output_path, index=False)

    print(f"Wrote AUC ranking to: {auc_output_path}")
    print(f"Wrote fused scores to: {fused_output_path}")
    print(f"Top features used: {top_features}")


if __name__ == "__main__":
    main()