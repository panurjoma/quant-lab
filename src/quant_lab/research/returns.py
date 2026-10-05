from __future__ import annotations

import numpy as np
import pandas as pd


def _prices(prices: pd.Series) -> pd.Series:
    values = prices.astype(float)
    if values.empty:
        return values
    if values.isna().any() or (~np.isfinite(values)).any():
        raise ValueError("prices must be finite and non-missing")
    if (values <= 0).any():
        raise ValueError("prices must be positive")
    return values


def simple_returns(prices: pd.Series) -> pd.Series:
    """Return P_t / P_(t-1) - 1; first observation is NaN by definition."""
    return _prices(prices).pct_change(fill_method=None)


def log_returns(prices: pd.Series) -> pd.Series:
    """Return ln(P_t / P_(t-1)); first observation is NaN by definition."""
    values = _prices(prices)
    return np.log(values / values.shift(1))
