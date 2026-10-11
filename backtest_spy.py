# Backtest SPY with 200-day moving average strategy
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/prices.csv', index_col=0, parse_dates=True)
spy = df["SPY"]

rolling_days = 200

ma200 = spy.rolling(rolling_days).mean()
valid = ma200.notna()  # Only consider dates where the 200-day moving average is valid

signal = (spy>ma200).astype(int)[valid]  # 1 if SPY > MA200, else 0
print(f"Percentage of time SPY is above its 200-day moving average: {signal.mean()*100:.2f}%")

#The backtest
spy_returns = spy.pct_change()[valid]  # Daily returns of SPY
strategy_returns = signal * spy_returns
strategy_returns_growth = (1 + strategy_returns).cumprod()
spy_returns_growth = (1 + spy_returns).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(strategy_returns_growth, label='Strategy Growth')
plt.plot(spy_returns_growth, label='SPY Growth')
plt.xlabel("Date")
plt.ylabel("Growth")
plt.legend()
plt.title('Backtest of SPY with 200-day Moving Average Strategy')
plt.savefig("figures/ma_backtest_v1.png")   
plt.show()

print(strategy_returns)
print(f"Final growth of the strategy: {strategy_returns_growth.iloc[-1]:.2f}")
print(f"Final growth of SPY: {spy_returns_growth.iloc[-1]:.2f}")
#The backtest has look ahead bias, as the strategy uses the current day's price to determine whether to be in or out of the market. In reality, one would only know the current day's price at the end of the day, so the decision to be in or out of the market should be made based on the previous day's price.

strategy_returnsV2 = signal.shift(1).fillna(0) * spy_returns #fixing look ahead bias
strategy_returns_growthV2 = (1 + strategy_returnsV2).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(strategy_returns_growthV2, label='Strategy Growth (V2)')
plt.plot(spy_returns_growth, label='SPY Growth')
plt.xlabel("Date")
plt.ylabel("Growth")
plt.legend()
plt.title('Backtest of SPY with 200-day Moving Average Strategy (V2)')
plt.savefig("figures/ma_backtest_v2.png")
plt.show()

print(f"Final growth of the strategy (V2): {strategy_returns_growthV2.iloc[-1]:.2f}")
print(f"Final growth of SPY: {spy_returns_growth.iloc[-1]:.2f}")
#Clear large drop in performance of the strategy in V2 compared to V1. Drop of around 15 from 20.31 to 5.19. Buy and hold 8.75
#The strategy does not beat buy and hold in V2. 
#However during drops in the market (for example COVID), the strategy does not drop as much as buy and hold. This is because the strategy is out of the market during these drops, while buy and hold is still in the market. The strategy is able to avoid some of the losses during these drops, which is a positive aspect of the strategy.
#However during the drops it also stays out during the rebound which it missed a lot of.

percentage_in_market = signal.mean()*100
switches_in_market = signal.diff().abs().sum()
print(f"number of switches with strategy: {switches_in_market}")

v2_summary = {"Annualised return": strategy_returnsV2.mean()*252, "Annualised volatility": strategy_returnsV2.std()*252**0.5, "Drawdown": (strategy_returns_growthV2 / strategy_returns_growthV2.cummax() -1).min() }
spy_summary = {"Annualised return": spy_returns.mean()*252, "Annualised volatility": spy_returns.std()*252**0.5, "Drawdown": (spy_returns_growth / spy_returns_growth.cummax() - 1).min()}

v2_summary_table = pd.DataFrame({"v2": v2_summary, "SPY": spy_summary})

print(v2_summary_table)
StrategyV2_return_over_risk = v2_summary_table.loc["Annualised return", "v2"]/v2_summary_table.loc["Annualised volatility", "v2"]
spy_return_over_risk = v2_summary_table.loc["Annualised return", "SPY"]/v2_summary_table.loc["Annualised volatility", "SPY"]
print(StrategyV2_return_over_risk, spy_return_over_risk)
#The strategy has a higher return/risk value than spy (0.94 compared to 0.89) indicating its lower retunr is compensated by its lower risk as the values are close.


#with 200, the final growth of V2 was 5.19
#with 150, the final growth of v2 was 4.58
#with 100, the final growth of V2 was 4.57
#with 50, the final growth of V2 was 3.11
#appears to decrease with lower values for the rolling window with return/risk also decreasing


