import pandas as pd


def validate_sample_alignment(
    expression_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    sample_col: str = "sample_id",
) -> None:
    if sample_col not in expression_df.columns:
        raise ValueError(f"Expression data missing required column: {sample_col}")

    if sample_col not in labels_df.columns:
        raise ValueError(f"Labels data missing required column: {sample_col}")

    if expression_df[sample_col].duplicated().any():
        raise ValueError("Expression data contains duplicate sample IDs")

    if labels_df[sample_col].duplicated().any():
        raise ValueError("Labels data contains duplicate sample IDs")

    overlap = set(expression_df[sample_col]).intersection(set(labels_df[sample_col]))
    if not overlap:
        raise ValueError("No overlapping sample IDs found between expression data and labels")