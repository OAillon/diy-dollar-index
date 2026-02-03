import pandas as pd
import numpy as np

def aggregate_returns(
    returns: pd.DataFrame,
    weights: pd.Series,
) -> pd.Series:
    """
    Weighted sum of log returns.
    """
    aligned_returns = returns[weights.index] # Ensures the index is in the same order
    return aligned_returns.dot(weights)
