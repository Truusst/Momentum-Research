#Data collection script
#Prices are adjusted for dividends and splits. Data is downloaded from Yahoo Finance using the yfinance library.
#Missing values are dropped only if all values in row are missing. The data is saved as a CSV file in the data directory.
import yfinance as yf
import pandas as pd

tickers = ['SPY', 'XLK', 'XLF', 'XLE', 'XLV', 'XLI', 'XLY', 'XLP', 'XLU', 'XLB', 'TLT', 'GLD', 'EFA', 'EEM', 'IWM']

raw = yf.download(tickers, start="2010-01-01", end="2026-10-08", auto_adjust=True) #end date is set to date this project started to keep consistency in analysis notes. However can but adjusted to be live

prices = raw['Close'].dropna(how='all')
prices_open = raw['Open'].dropna(how='all')

import os
os.makedirs('data', exist_ok=True)
prices.to_csv('data/prices.csv')
prices_open.to_csv('data/open.csv')
