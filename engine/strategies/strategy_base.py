from abc import ABC, abstractmethod
import pandas as pd

STRATEGY_REGISTRY = {}

def register_strategy(logic_id: str):
    """Decorator to automatically register strategies to the engine."""
    def decorator(cls):
        STRATEGY_REGISTRY[logic_id] = cls
        return cls
    return decorator

class StrategyBase(ABC):
    def __init__(self, params: dict):
        self.params = params

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Takes OHLCV dataframe, returns a pandas Series of signals 
        (1 for Buy, -1 for Sell, 0 for Hold) for each row.
        """
        pass
