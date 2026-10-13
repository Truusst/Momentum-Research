#backtesting cross-sectional momentum strategy
import pandas as pd
from backtester import run_backtest
prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)

def momentum_strategy(prices, lookback=12, top_n=3):
    "Build daily portfolio weights for a cross-sectional momentum strategy."
    dates = prices.index.to_series()
    month_end_dates = dates.groupby(prices.index.to_period("M")).max()
    monthly_prices = prices.loc[month_end_dates]
    monthly_prices = monthly_prices.iloc[:-1] if monthly_prices.index[-1] + pd.offsets.BMonthEnd(0) != monthly_prices.index[-1] else monthly_prices
    yearly_return = monthly_prices.pct_change(lookback)


    def momentum_weights(signal, top_n):
        """returns the weights of a signal for the top n highest return every 12 months (cross-sectional momentum strategy for top n ETFs)"""
        weights = ((signal.rank(axis=1, method='max', na_option='keep'))>(signal.shape[1]-top_n)).astype(int)
        return (weights/top_n).fillna(0) 


    monthly_weights = momentum_weights(yearly_return, top_n) 
    daily_weights = monthly_weights.reindex(prices.index, method="ffill") #reindex the days of the months and fill it with the signal for that month
    return daily_weights

#sanity checks
if __name__ == "__main__":
    daily_weights = momentum_strategy(prices)
    backtest_run = run_backtest(daily_weights, prices.pct_change())
    print(daily_weights.sum(axis=1).value_counts())
    print(backtest_run.tail(10))
    row = daily_weights.loc["2022-02-28"]
    print(row[row>0])
    print(daily_weights.loc["2022-02-23":"2022-03-02"])
    print(backtest_run.isna().sum())
    