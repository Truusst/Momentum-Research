import pandas as pd

def run_backtest(weights, returns, cost=0.0):
    if isinstance(weights, pd.Series):
        weights = weights.to_frame()
    if isinstance(returns, pd.Series):
        returns = returns.to_frame()
    weights = weights.shift(1).fillna(0)
    portfolio_daily_returns = (weights*returns).sum(axis=1, numeric_only=True)
    #only for now
    turnover = weights.diff().abs().sum(axis=1)
    adjusted_daily_returns = portfolio_daily_returns - turnover*cost
    return adjusted_daily_returns



