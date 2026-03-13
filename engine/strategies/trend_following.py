import pandas as pd
import numpy as np
from .strategy_base import StrategyBase, register_strategy

@register_strategy("STRAT_1")
class TrendFollowing(StrategyBase):
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        fast_ma = self.params.get("fast_ma", 20)
        slow_ma = self.params.get("slow_ma", 50)
        
        fast = df['Close'].rolling(window=fast_ma).mean()
        slow = df['Close'].rolling(window=slow_ma).mean()
        
        # 1 when fast > slow, -1 when fast < slow
        signals = np.where(fast > slow, 1, np.where(fast < slow, -1, 0))
        return pd.Series(signals, index=df.index).fillna(0)
    
