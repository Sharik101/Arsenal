pip install requests
pip install yfinance

import requests
import pandas as pd
import yfinance as yf

def get_average_t_bill(api_key):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=TB3MS&api_key={api_key}&file_type=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        observations = data.get('observations', [])
        dates = [obs['date'] for obs in observations]
        values = [obs['value'] for obs in observations]
        df = pd.DataFrame({'Date': dates, 'Value': values})
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        return df['Value'].dropna().tail(5).mean()
    except requests.RequestException as e:
        print("Failed to fetch data:", e)
        return None

def fetch_stock_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    stock_info = ticker.info
    current_price = ticker.history(period="1d")["Close"].iloc[-1]
    full_name = stock_info.get('longName', 'N/A')
    return current_price, full_name
