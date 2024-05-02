import numpy as np
import pandas as pd
import yfinance as yf

def get_stock_data(ticker_symbol, period="1y"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period=period)

def calculate_volatility(data):
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    return log_returns.std() * np.sqrt(252)

def get_option_chain(ticker_symbol, expiration_dates):
    ticker = yf.Ticker(ticker_symbol)
    option_chain = {}
    for date in expiration_dates:
        try:
            opts = ticker.option_chain(date)
            option_chain[date] = {'calls': opts.calls[['strike', 'lastPrice', 'bid', 'ask']].head(), 'puts': opts.puts[['strike', 'lastPrice', 'bid', 'ask']].head()}
        except ValueError as e:
            print(f"No options data for {date}: {e}")
    return option_chain
