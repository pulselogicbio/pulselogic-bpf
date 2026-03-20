import argparse

from bpf.constants import DEFAULT_CONFIG_PATH
from bpf.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bpf",
        description="Biomarker Probability Fusion canonical CLI."
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help="Path to run configuration file."
    )
    args = parser.parse_args()

    result = run_pipeline(args.config, invocation_mode="cli")

    print(f"Wrote AUC ranking to: {result['auc_output_path']}")
    print(f"Wrote fused scores to: {result['fused_output_path']}")
    print(f"Wrote audit log to: {result['audit_output_path']}")
    print(f"Wrote checkpoint log to: {result['checkpoint_output_path']}")
    print(f"Wrote run manifest to: {result['manifest_output_path']}")
    print(f"Wrote executive summary to: {result['executive_summary_path']}")
    print(f"Wrote run fingerprint to: {result['fingerprint_output_path']}")
    print(f"Wrote bootstrap summary to: {result['bootstrap_summary_path']}")
    print(f"Top features used: {result['top_features']}")


if __name__ == "__main__":
    main()