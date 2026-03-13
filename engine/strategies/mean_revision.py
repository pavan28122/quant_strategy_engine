import pandas as pd
import numpy as np
from .strategy_base import StrategyBase, register_strategy

@register_strategy("STRAT_2")
class MeanReversion(StrategyBase):
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        rsi_window = self.params.get("rsi_window", 14)
        rsi_buy = self.params.get("rsi_buy", 30)
        rsi_sell = self.params.get("rsi_sell", 70)
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        signals = np.where(rsi < rsi_buy, 1, np.where(rsi > rsi_sell, -1, 0))
        return pd.Series(signals, index=df.index).fillna(0)
