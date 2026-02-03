import pandas as pd
import numpy as np

def compute_log_returns(
    fx_rates: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes log returns of FX rates.

    r_{i,t} = ln(FX_{i,t} / FX_{i,t-1})
    """
    return np.log(fx_rates / fx_rates.shift(1))