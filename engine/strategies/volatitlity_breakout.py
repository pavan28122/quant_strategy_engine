import pandas as pd
import numpy as np
from .strategy_base import StrategyBase, register_strategy

@register_strategy("STRAT_3")
class VolatilityBreakout(StrategyBase):
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        atr_window = self.params.get("atr_window", 14)
        multiplier = self.params.get("multiplier", 1.5)
        
        # Simple ATR calculation
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=atr_window).mean()
        
        prev_high = df['High'].shift(1)
        prev_low = df['Low'].shift(1)
        
        buy_threshold = prev_high + (atr.shift(1) * multiplier)
        sell_threshold = prev_low - (atr.shift(1) * multiplier)
        
        signals = np.where(df['High'] > buy_threshold, 1, 
                           np.where(df['Low'] < sell_threshold, -1, 0))
        return pd.Series(signals, index=df.index).fillna(0)