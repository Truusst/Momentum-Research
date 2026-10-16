import pandas as pd
import pytest
from metrics import cagr, max_drawdown


def test_cagr_constant_returns():
    """252 days of +0.1% should compound to exactly 1.001^252 - 1 over one year."""
    returns = pd.Series([0.001] * 252)
    assert cagr(returns) == pytest.approx(1.001 ** 252 - 1)


def test_max_drawdown_simple_path():
    """Growth path 1.10 -> 0.88 -> 0.924: the worst fall from a peak is 0.88/1.10 - 1 = -20%."""
    returns = pd.Series([0.10, -0.20, 0.05])
    assert max_drawdown(returns) == pytest.approx(-0.20)