#testing metric functions
from metrics import summary, growth_of_one
import pandas as pd
from backtester import run_backtest

prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
spy = prices["SPY"].pct_change()

print(summary(spy))
# SPY: annualised return = 0.147, CAGR = 0.142, volatility = 0.170.
# CAGR is lower than the annualised mean because of volatility drag: compounding
# punishes swings (e.g. -10% then +10% leaves you at 0.99), so the geometric average
# is always below the arithmetic one (AM-GM).
# Check: ln(1 + CAGR) ≈ μ - σ²/2. Here ln(1.142) = 0.1328 vs 0.147 - 0.170²/2 = 0.1328,
# an almost exact match. So two strategies with equal average returns can end with very
# different wealth. Lower volatility compounds better, which is why I should judge strategies
# on CAGR and Sharpe rather than average return.


#Regressiontesting backtester
df = pd.read_csv('data/prices.csv', index_col=0, parse_dates=True)
spy = df["SPY"]

rolling_days = 200

ma200 = spy.rolling(rolling_days).mean()
valid = ma200.notna()  # Only consider dates where the 200-day moving average is valid

signal = (spy>ma200).astype(int)[valid]  # 1 if SPY > MA200, else 0
print(f"Percentage of time SPY is above its 200-day moving average: {signal.mean()*100:.2f}%")

#The backtest
spy_returns = spy.pct_change()[valid]  # Daily returns of SPY
strategy_returns = signal.shift(1) * spy_returns
strategy_returns_growth = (1 + strategy_returns).cumprod()
spy_returns_growth = (1 + spy_returns).cumprod()
#comparing values to see if function works
print(strategy_returns_growth.iloc[-1])
print(growth_of_one(run_backtest(signal, spy_returns, cost=20*0.0001)).iloc[-1])
#both output 5.19 correct
print(summary(spy_returns))
table = pd.DataFrame({"0": summary(run_backtest(signal, spy_returns)), 
                      "5": summary(run_backtest(signal, spy_returns, cost=5*0.0001)),
                      "10": summary(run_backtest(signal, spy_returns, cost=10*0.0001)),
                      "20": summary(run_backtest(signal, spy_returns, cost=20*0.0001)),})
print(table)
#With an increase in bps, it is clear that annualised return and CAGR decrease. This is clearly due to cost of entering and exiting
#This tells me that with a strategy that trades more often, if the bp>0, it will have worse CAGR, sharpe ratio and Drawdown