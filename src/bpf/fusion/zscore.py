import pandas as pd


def zscore_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result = df.copy()
    for col in columns:
        mean = result[col].mean()
        std = result[col].std(ddof=0)
        if std == 0:
            result[col] = 0.0
        else:
            result[col] = (result[col] - mean) / std
    return result