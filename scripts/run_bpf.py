from pathlib import Path
import yaml

from bpf.io.loaders import load_csv
from bpf.ranking.auc_ranker import compute_feature_auc_table


def main() -> None:
    config_path = Path("configs/canonical_v1_0_0.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    expression_path = config["inputs"]["expression_matrix"]
    labels_path = config["inputs"]["labels"]

    output_dir = Path(config["outputs"]["base_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    auc_filename = config["outputs"]["auc_table"]
    auc_output_path = output_dir / auc_filename

    expression_df = load_csv(expression_path)
    labels_df = load_csv(labels_path)

    auc_df = compute_feature_auc_table(expression_df, labels_df)
    auc_df.to_csv(auc_output_path, index=False)

    print(f"Wrote AUC ranking to: {auc_output_path}")


if __name__ == "__main__":
    main()