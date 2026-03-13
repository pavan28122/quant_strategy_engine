import yfinance as yf
import pandas as pd
import os

def fetch_data(symbol="SPY", period="6mo"):
    print(f"Fetching {period} data for {symbol}...")
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval="1d")
    
    if df.empty:
        raise ValueError("No data fetched. Check your internet connection or symbol.")
    
    df.index = df.index.tz_localize(None) # Clean timezone for ease of use
    
    # Save Raw
    raw_path = "data/ohlc_raw.csv"
    df.to_csv(raw_path)
    
    # Clean Data (Drop unused columns, handle NAs)
    clean_df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    clean_path = "data/ohlc_clean.csv"
    clean_df.to_csv(clean_path)
    
    # Validation Report
    with open("outputs/validation_report.txt", "w") as f:
        f.write(f"Validation Report for {symbol}\n")
        f.write(f"Total Rows: {len(clean_df)}\n")
        f.write(f"Start Date: {clean_df.index.min()}\n")
        f.write(f"End Date: {clean_df.index.max()}\n")
        f.write(f"Missing Values: {clean_df.isnull().sum().sum()}\n")
        
    print(f"Data saved to {clean_path}")
    return clean_path

if __name__ == "__main__":
    fetch_data()