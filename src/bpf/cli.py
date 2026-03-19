import argparse
from bpf.constants import DEFAULT_CONFIG_PATH

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
    print(f"BPF CLI initialized. Config: {args.config}")

if __name__ == "__main__":
    main()