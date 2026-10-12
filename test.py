from metrics import summary
import pandas as pd

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