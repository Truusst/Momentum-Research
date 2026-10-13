import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

prices = pd.read_csv('data/prices.csv', index_col=0, parse_dates=True)
returns = prices.pct_change().dropna(how='all')



summary = pd.DataFrame({
    'Annualised return': returns.mean()*252,
    'Annualised volatility': returns.std()*252**0.5
})
summary = summary.sort_values(by='Annualised volatility', ascending=False)
print(summary)
#Most volatile ETF is XLE energy sector ETF. It has the highest annualised volatility among the ETFs in the list. This matches what i would expect given the nature of the energy sector and its sensitivity to market fluctuations and geopolitical events. Least Volatile is XLP consumer staples sector ETF. It has the lowest annualised volatility among the ETFs in the list.
#Multiplied return by 252 to annualise it, and multiplied volatility by the square root of 252 to annualise it. Assuming there are 252 trading days in a year. assumed to be independent and identically distributed (i.i.d) returns hence Var(sum of 252 daily returns) = 252σ² under i.i.d., so annual sd = √252·σ

#calculating how much $1 invested in each ETF would have grown to by the end of the period. This is done by calculating the cumulative product of (1 + daily returns) for each ETF.
os.makedirs('figures', exist_ok=True)

growth1 = (1 + returns).cumprod()
print(growth1.iloc[-1].sort_values()) #Seeing maximum and minimum growth of $1 invested in each ETF since 2010. 

growth2 = prices / prices.iloc[0] #also works by normalizing the prices to the first day of the period. This gives the same result as calculating the cumulative product of (1 + daily returns).
print(f"max absolute difference: {abs(growth2.iloc[-1] - growth1.iloc[-1]).max()}") #checking if the two methods give the same result. They do, as the maximum absolute difference is sufficiently small (1e-13).

growth1.plot(figsize=(12, 6))
plt.title("Growth of $1 invested in each ETF since 2010")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.legend()
plt.savefig("figures/growth.png")
plt.show()
#XLK grew the most since 2010, and the least growth was seen by TLT. None dropped below $1.

print(returns["SPY"].nsmallest(5))
#The five worst daily returns for SPY include:
#2020-03-16,2020-03-12,2020-03-09: caused by the COVID-19 pandemic 
#2011-08-08: caused by the Black Monday 2011 stock market crash
#2025-04-04: caused by the 2025 stock market crash (US tariff announcements) 

worst_ticker = returns.min().idxmin()           # ticker with the lowest return
worst_date = returns[worst_ticker].idxmin()     # date of that ticker's lowest return
worst_return = returns[worst_ticker].min()      # the return itself
print(f"Worst single day: {worst_ticker} returned {worst_return:.1%} on {worst_date:%Y-%m-%d}")
#The ETF with the single worst day is also the ETF with the highest annualised volatility, XLE. However higher volatility doesnt guarantee the worst single day. 

#calculating the correlation matrix of the returns of the ETFS
corr = returns.corr() 
print(corr)

plt.figure(figsize=(10, 8))
plt.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(label='Correlation')
plt.title('Correlation Matrix of ETF Returns')
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)), corr.index, rotation=0)
plt.tight_layout()
plt.savefig('figures/correlation_matrix.png')
plt.show()


corr_no_diag = corr.mask(np.eye(len(corr), dtype=bool))
pair_col = corr_no_diag.max().idxmax()          # column containing the overall max
pair_row = corr_no_diag[pair_col].idxmax()      # row of the max within that column
max_corr = corr_no_diag[pair_col].max()

print(f"Highest correlation: {pair_row} and {pair_col}, {max_corr:.2f}")
#The two ETFs with the highest correlation are XLK and SPY, with a correlation coefficient of 0.92.

print(corr['SPY'].sort_values(ascending=True))
#The ETF with the lowest correlation with SPY is TLT, with a correlation coefficient of -0.28. This indicates that TLT tends to move in the opposite direction of SPY, which is consistent with the fact that TLT is a bond ETF and bonds often have an inverse relationship with stocks.

#The strategy ranks ETFs on returns, so it only adds value when the winners and losers actually behave differently. 
#Most of these ETFs are highly correlated with SPY (around 0.5-0.9), largely because the sector ETFs are slices of the S&P 500, so in most months the ranking is choosing between assets that move together. 
#The main diversifiers are TLT (-0.28) and GLD (0.07), which give the strategy a way out of stocks in long downturns. So I’d expect only a modest edge over SPY, driven mainly by the periods when those low-correlation assets mattered.

monthly = prices.resample('ME').last().pct_change().dropna(how='all')

march_from_daily = (1+returns.loc['2020-03']).prod() - 1
march_from_monthly = monthly.loc['2020-03']
print(abs(march_from_monthly - march_from_daily).max().max()) #check that the monthly returns are consistent with the daily returns. The maximum absolute difference is sufficiently small (7.77e-16), indicating that the monthly returns are consistent with the daily returns.

#final month of data is incomplete, so the last row is dropped when calculating monthly returns. 

past_12m = prices.resample('ME').last().pct_change(12).dropna(how='all')
most_recent_ranking = past_12m.iloc[-2].sort_values(ascending=False) #-2 iloc because the last row is incomplete. 
print(most_recent_ranking)
#The strategy wouldve held the following 3 ETFs in the most recent complete month: XLE, XLK, and EEM.
