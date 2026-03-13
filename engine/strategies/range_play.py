import pandas as pd
import numpy as np
from .strategy_base import StrategyBase, register_strategy

@register_strategy("STRAT_4")
class RangePlay(StrategyBase):
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = self.params.get("lookback", 10)
        
        rolling_high = df['High'].rolling(window=lookback).max().shift(1)
        rolling_low = df['Low'].rolling(window=lookback).min().shift(1)
        
        # Buy near bottom (e.g. within 2% of low), Sell near top
        buffer = (rolling_high - rolling_low) * 0.10
        
        buy_zone = rolling_low + buffer
        sell_zone = rolling_high - buffer
        
        signals = np.where(df['Close'] <= buy_zone, 1, 
                           np.where(df['Close'] >= sell_zone, -1, 0))
        return pd.Series(signals, index=df.index).fillna(0)