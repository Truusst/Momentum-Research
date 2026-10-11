# Cross-Sectional Momentum in Sector ETFs

Research study testing whether ranking ETFs by past returns and holding
the winners beats simply holding the S&P 500, after realistic costs.

## Research question
Does cross-sectional momentum outperform buy-and-hold SPY on a
risk-adjusted basis across 15 US sector and cross-asset ETFs (2010–present)?

## Data
- Daily adjusted closing prices from Yahoo Finance via `yfinance`
- 15 ETFs: 10 US sector ETFs, plus SPY, IWM, EFA, EEM, TLT and GLD
- Prices adjusted for dividends and splits; empty rows dropped

## Hypotheses (written before backtesting)
1. Most ETFs are highly correlated with SPY, so the strategy will
   behave much like the market most of the time.
2. Any edge will come mainly from reduced losses in long downturns,
   when low-correlation assets like TLT and GLD rank highly.
3. Results may depend heavily on a few key periods.

## Project structure
- `data.py`: downloads and cleans price data
- `explore.py`: summary statistics, growth and correlation charts

## Status
In progress: data exploration complete, backtester next.