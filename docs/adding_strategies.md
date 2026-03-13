# Guide: Adding a New Strategy to the Engine

One of the core architectural requirements of this backtesting framework is that **adding a new strategy must require zero changes to the core engine**. 

This is achieved using a **Registry Pattern** in Python. The engine automatically scans the `engine/strategies/` directory and loads any class that registers itself.

Follow these 2 simple steps to add a new strategy (e.g., `STRAT_5`).

---

## Step 1: Create the Strategy Class

1. Create a new Python file inside the `engine/strategies/` folder. For example: `engine/strategies/macd_crossover.py`.
2. Import `StrategyBase` and `register_strategy`.
3. Create your class, inherit from `StrategyBase`, and add the `@register_strategy("YOUR_LOGIC_ID")` decorator above it.
4. Implement the `generate_signals(self, df)` method. 
   - **Input:** A pandas DataFrame (`df`) containing OHLCV data.
   - **Output:** A pandas Series of integers where `1` = Buy, `-1` = Sell, and `0` = Hold.

### Example Code (`macd_crossover.py`):

```python
import pandas as pd
import numpy as np
from .strategy_base import StrategyBase, register_strategy

# 1. Register the strategy with a unique logic_id
@register_strategy("STRAT_5")
class MACDCrossover(StrategyBase):
    
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        # 2. Fetch parameters dynamically from JSON
        fast_period = self.params.get("fast_period", 12)
        slow_period = self.params.get("slow_period", 26)
        signal_period = self.params.get("signal_period", 9)
        
        # 3. Calculate your indicators
        ema_fast = df['Close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow_period, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        
        # 4. Generate Long (1) / Short (-1) / Hold (0) signals
        signals = np.where(macd_line > signal_line, 1, 
                           np.where(macd_line < signal_line, -1, 0))
                           
        return pd.Series(signals, index=df.index).fillna(0)
