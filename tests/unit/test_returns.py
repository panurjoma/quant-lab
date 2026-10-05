import math

import pandas as pd
import pytest

from quant_lab.research import log_returns, simple_returns


def test_simple_returns_are_hand_checkable() -> None:
    result = simple_returns(pd.Series([100.0, 110.0, 99.0]))
    assert math.isnan(result.iloc[0])
    assert result.iloc[1] == pytest.approx(0.10)
    assert result.iloc[2] == pytest.approx(-0.10)


def test_log_returns_are_hand_checkable() -> None:
    result = log_returns(pd.Series([100.0, 110.0]))
    assert result.iloc[1] == pytest.approx(math.log(1.1))


def test_returns_reject_nonpositive_prices() -> None:
    with pytest.raises(ValueError, match="positive"):
        simple_returns(pd.Series([100.0, 0.0]))
