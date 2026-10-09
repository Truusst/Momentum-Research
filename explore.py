#Most volatile ETF is XLE energy sector ETF. It has the highest annualised volatility among the ETFs in the list. This matches what i would expect given the nature of the energy sector and its sensitivity to market fluctuations and geopolitical events. Least Volatile is XLP consumer staples sector ETF. It has the lowest annualised volatility among the ETFs in the list.
#Multiplied return by 252 to annualise it, and multiplied volatility by the square root of 252 to annualise it. Assuming there are 252 trading days in a year. assumed to be independent and identically distributed (i.i.d) returns hence Var(sum of 252 daily returns) = 252σ² under i.i.d., so annual sd = √252·σ
import pandas as pd
import os
import matplotlib.pyplot as plt

prices = pd.read_csv('data/prices.csv', index_col=0, parse_dates=True)
returns = prices.pct_change().dropna(how='all')



summary = pd.DataFrame({
    'Annualised return': returns.mean()*252,
    'Annualised volatility': returns.std()*252**0.5
})
summary = summary.sort_values(by='Annualised volatility', ascending=False)

print(summary)

#calculating how much $1 invested in each ETF would have grown to by the end of the period. This is done by calculating the cumulative product of (1 + daily returns) for each ETF.
os.makedirs('figures', exist_ok=True)

growth1 = (1 + returns).cumprod()
print(min(growth1.iloc[-1])) # Print the maximum growth value
print(growth1.iloc[-1].idxmin(axis=0)) # Print the minimum growth ticker

growth2 = prices / prices.iloc[0] #also works by normalizing the prices to the first day of the period. This gives the same result as calculating the cumulative product of (1 + daily returns).
print(abs(growth2.iloc[-1] - growth1.iloc[-1]).max()) #checking if the two methods give the same result. They do, as the maximum absolute difference is sufficiently small.

growth1.plot(figsize=(12, 6))
plt.title("Growth of $1 invested in each ETF since 2010")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.legend()
plt.savefig("figures/growth.png")
plt.show()
#XLK grew the most since 2010, and the least growth was seen by TLT. None dropped below $1.