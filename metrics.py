#library of metric functions
import pandas as pd

def growth_of_one(returns):
    """Turn a series of daily returns in into the growth of $1"""
    return (1 + returns).cumprod()

def annualised_volatility(returns):
    """return, from a series of daily returns, 1 annualised volatility value"""
    return returns.std()*252**0.5

def cagr(returns):
    """return, from a series of daily returns, the CAGR of the series"""
    valid = returns.notna()
    return ((1+returns).prod())**(252/returns[valid].shape[0]) - 1

def sharpe_ratio(returns):
    """return, from a series of daily returns, the sharpe ratio of the series (risk-free rate assumed 0 for now)"""
    return (returns.mean()/returns.std())*252**0.5

def max_drawdown(returns):
    """return, from a series of daily returns, the maximum drawdown the series experiences"""
    return drawdown(returns).min()

def drawdown(returns):
    """Return, from a series of daily returns, the drawdown on each day: the fall from
    the highest value so far (0 at a new high, negative otherwise)."""
    returns_growth = growth_of_one(returns)
    return (returns_growth/returns_growth.cummax() - 1)

def summary(returns):
    """return, from a series of daily returns, a dataframe with a summary of different statistics of the series"""
    summary = pd.Series({"Annualised Return": returns.mean()*252, 
                            "Annualised Volatility": annualised_volatility(returns),
                            "CAGR": cagr(returns),
                            "Sharpe ratio": sharpe_ratio(returns),
                            "Max Drawdown": max_drawdown(returns)})
    return summary




