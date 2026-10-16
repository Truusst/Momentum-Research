import pandas as pd

def run_backtest(weights, returns, cost=0.0):
    """runs a backtest on specific weights and returns. returns an adjusted daily returns series with turnover accounted"""
    if isinstance(weights, pd.Series):
        weights = weights.to_frame()
    if isinstance(returns, pd.Series):
        returns = returns.to_frame()
    weights = weights.shift(1).fillna(0)
    portfolio_daily_returns = (weights*returns).sum(axis=1, numeric_only=True)
    turnover = weights.diff().abs().sum(axis=1)
    adjusted_daily_returns = portfolio_daily_returns - turnover*cost
    return adjusted_daily_returns

def run_backtest_open(weights, closes, opens, cost=0.0):
    """runs a backtest on specific weights and open/close prices. returns an adjusted daily returns series with turnover accounted"""
    if isinstance(weights, pd.Series):
        weights = weights.to_frame()
    if isinstance(closes, pd.Series):
        closes = closes.to_frame()
    if isinstance(opens, pd.Series):
        opens = opens.to_frame()

    overnight = opens / closes.shift(1) - 1
    intraday = closes / opens - 1

    overnight_weights = weights.shift(2).fillna(0)
    intraday_weights = weights.shift(1).fillna(0)

    overnights_returns = (overnight*overnight_weights).sum(axis=1, numeric_only=True)
    intraday_returns = (intraday*intraday_weights).sum(axis=1, numeric_only=True)
    portfolio_daily_returns = (1+overnights_returns)*(1+intraday_returns) - 1

    turnover = intraday_weights.diff().abs().sum(axis=1)
    adjusted_daily_returns = portfolio_daily_returns - turnover*cost
    return adjusted_daily_returns

        

