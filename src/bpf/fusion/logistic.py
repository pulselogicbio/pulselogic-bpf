import numpy as np
import pandas as pd


def logistic_transform(x: pd.Series) -> pd.Series:
    return 1.0 / (1.0 + np.exp(-x))