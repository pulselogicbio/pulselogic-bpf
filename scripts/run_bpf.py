from bpf.constants import DEFAULT_CONFIG_PATH
from bpf.pipeline import run_pipeline


def main() -> None:
    result = run_pipeline(DEFAULT_CONFIG_PATH, invocation_mode="script")

    print(f"Wrote AUC ranking to: {result['auc_output_path']}")
    print(f"Wrote fused scores to: {result['fused_output_path']}")
    print(f"Wrote audit log to: {result['audit_output_path']}")
    print(f"Wrote checkpoint log to: {result['checkpoint_output_path']}")
    print(f"Wrote run manifest to: {result['manifest_output_path']}")
    print(f"Wrote executive summary to: {result['executive_summary_path']}")
    print(f"Top features used: {result['top_features']}")


if __name__ == "__main__":
    main()