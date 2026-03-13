import json
import pandas as pd
import importlib
import pkgutil
import argparse
import os
from engine.regimes.logic import detect_regime
import engine.strategies as strategies
from engine.strategies.strategy_base import STRATEGY_REGISTRY
from engine.utils.data_fetcher import fetch_data

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def import_all_strategies():
    """Dynamically imports all modules in the strategies package to trigger registry."""
    package = strategies
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"engine.strategies.{module_name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/engine.json")
    args = parser.parse_args()

    config = load_config(args.config)
    
    # 1. Fetch data if it doesn't exist
    if not os.path.exists(config['data_file']):
        fetch_data()
        
    df = pd.read_csv(config['data_file'], index_col='Date', parse_dates=True)
    
    # 2. Setup dynamic strategies
    import_all_strategies()
    active_strategies = {}
    
    for strat_name, strat_config in config['strategies'].items():
        if strat_config.get('enabled', False):
            logic_id = strat_config['logic_id']
            if logic_id in STRATEGY_REGISTRY:
                active_strategies[strat_name] = STRATEGY_REGISTRY[logic_id](strat_config['params'])
            else:
                print(f"Warning: {logic_id} not found in registry.")

    # 3. Precompute signals for performance (Vectorized)
    # This does NOT introduce look-ahead bias because we only read index `t` at time `t`.
    signals_df = pd.DataFrame(index=df.index)
    for name, strategy in active_strategies.items():
        signals_df[name] = strategy.generate_signals(df)
        
    # 4. Detect Regimes
    regime_series = detect_regime(df, config)
    
    # Regime to Strategy Mapping mapping
    regime_mapping = {
        "trend": "trend_following",
        "range": "range_play",
        "volatile": "volatility_breakout",
        "low_vol": "mean_reversion"
    }

    # 5. Engine Flow (Simulating Time)
    open_position = None  # Dict to store entry details
    trades = []
    
    # Iterate through days up to the second to last day (since we trade on t+1 open)
    for i in range(len(df) - 1):
        current_date = df.index[i]
        next_date = df.index[i+1]
        
        current_regime = regime_series.iloc[i]
        active_strat_name = regime_mapping.get(current_regime)
        
        if not active_strat_name or active_strat_name not in active_strategies:
            continue
            
        # Get signal generated at close of day t
        signal = signals_df.loc[current_date, active_strat_name]
        
        # 6. Execute Trades on Next Day Open (No look-ahead bias)
        next_open = df.iloc[i+1]['Open']
        
        if open_position is not None:
            # Check for exit (If signal flips or goes to 0, or regime changes radically)
            # For simplicity: close position if signal is opposite or 0
            if (open_position['side'] == 'LONG' and signal <= 0) or \
               (open_position['side'] == 'SHORT' and signal >= 0):
                
                # Calculate PnL
                if open_position['side'] == 'LONG':
                    pnl = next_open - open_position['entry_price']
                else:
                    pnl = open_position['entry_price'] - next_open
                    
                bars_held = (i+1) - open_position['entry_idx']
                
                trades.append({
                    "entry_dt": open_position['entry_dt'],
                    "entry_price": open_position['entry_price'],
                    "qty": 1,
                    "side": open_position['side'],
                    "strategy_used": open_position['strategy_used'],
                    "regime": open_position['regime'],
                    "exit_dt": next_date,
                    "exit_price": next_open,
                    "pnl": pnl,
                    "bars_held": bars_held
                })
                open_position = None
                
        # Open new position
        if open_position is None and signal != 0:
            open_position = {
                "entry_dt": next_date,
                "entry_price": next_open,
                "side": "LONG" if signal == 1 else "SHORT",
                "strategy_used": active_strat_name,
                "regime": current_regime,
                "entry_idx": i+1
            }

    # 7. Output to Excel
    trades_df = pd.DataFrame(trades)
    if not trades_df.empty:
        trades_df.sort_values(by='entry_dt', inplace=True)
        out_path = "outputs/orders.xlsx"
        trades_df.to_excel(out_path, index=False)
        print(f"Backtest complete. {len(trades_df)} trades logged to {out_path}.")
    else:
        print("Backtest complete. No trades executed.")

if __name__ == "__main__":
    main()