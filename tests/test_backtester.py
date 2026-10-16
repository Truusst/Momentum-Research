import pandas as pd
import pytest
from backtester import run_backtest

dates = pd.date_range("2020-01-01", periods=5, freq="B")
returns = pd.DataFrame({"SPY": [0.01] * 5}, index=dates)
weights = pd.DataFrame({"SPY": [0, 0, 1, 1, 1]}, index=dates)  # decide to buy at day 2's close


def test_no_look_ahead():
    """A decision made at day 2's close must only start earning from day 3."""
    result = run_backtest(weights, returns)
    assert result.iloc[2] == pytest.approx(0.0)    # decision day: nothing earned yet
    assert result.iloc[3] == pytest.approx(0.01)   # first day actually holding SPY


def test_cost_charged_on_entry():
    """Buying 100% of the portfolio is a turnover of 1, so the first day held pays the cost."""
    result = run_backtest(weights, returns, cost=0.001)
    assert result.iloc[3] == pytest.approx(0.01 - 0.001)
    assert result.iloc[4] == pytest.approx(0.01)   # no trade that day, so no cost