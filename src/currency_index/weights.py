import numpy as np
import pandas as pd

def equal_weights(
    currencies: list[str],
) -> pd.Series:
    """
    Assigns equal weights to all currencies.
    """
    n = len(currencies)
    return pd.Series(1 / n, index=currencies)

def fixed_weights(
    weights: dict[str, float],
) -> pd.Series:
    """
    Validates and normalizes fixed user-defined weights.
    """
    w = pd.Series(weights)
    return w / w.sum()
