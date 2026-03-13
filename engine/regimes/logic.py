import pandas as pd
import numpy as np

def detect_regime(df: pd.DataFrame, config: dict) -> pd.Series:
    """
    Returns a pandas Series of regime names corresponding to the DataFrame index.
    """
    params = config.get("regime_classifier", {})
    trend_ma = params.get("trend_ma", 50)
    atr_window = params.get("atr_window", 14)
    
    # Calculate MA and ATR
    df['MA'] = df['Close'].rolling(window=trend_ma).mean()
    
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(window=atr_window).mean()
    
    # Calculate ATR quantiles dynamically based on an expanding window or lookback
    # Using a 60-day rolling quantile to adapt to changing market conditions
    df['ATR_30_pct'] = df['ATR'].rolling(60, min_periods=atr_window).quantile(0.3)
    df['ATR_70_pct'] = df['ATR'].rolling(60, min_periods=atr_window).quantile(0.7)
    
    regimes = pd.Series("range", index=df.index) # Default
    
    # Conditions
    is_trending = df['Close'] > df['MA']
    is_volatile = df['ATR'] >= df['ATR_70_pct']
    is_low_vol = df['ATR'] <= df['ATR_30_pct']
    
    # Apply logic (Hierarchy: Volatile/Low Vol overrides Trend/Range if extreme)
    regimes = np.where(is_trending, "trend", "range")
    regimes = np.where(is_volatile, "volatile", regimes)
    regimes = np.where(is_low_vol, "low_vol", regimes)
    
    return pd.Series(regimes, index=df.index)
