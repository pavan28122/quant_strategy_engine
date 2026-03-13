# Modular Quant Strategy Engine

A robust, modular backtesting framework built in Python. This engine dynamically detects the daily market regime (Trend, Range, Volatile, Low Volatility) and automatically deploys the most suitable trading strategy based on a JSON configuration.

## ✅ Assignment Compliance Checklist

This architecture was specifically designed to meet and exceed the core evaluation criteria:

* **Zero-Touch Engine Modifications:** The framework supports adding Strategy-5 (and beyond) without modifying the core engine code. This is achieved using a dynamic **Registry Pattern** (`@register_strategy`).
* **100% JSON-Driven:** All strategy parameters, regime thresholds, and data source paths are injected via `configs/engine.json`. There are absolutely no hardcoded strategy variables.
* **No Look-Ahead Bias:** Strategy signals are computed using data up to the close of day `t`. Trades are strictly executed using the `Open` price of day `t+1`.
* **CLI Execution:** The engine executes exactly via the required command: `python run_engine.py --config configs/engine.json` using Python's `argparse` module.
* **Strict Architecture:** Adheres exactly to the requested folder structure, dynamically mapping regimes to strategies, and outputting the required `orders.xlsx` log.

---

## 🚀 Features

* **Dynamic Regime Switching:** Evaluates the market state at the start of each day using Moving Averages and Average True Range (ATR) percentiles.
* **Plug-and-Play Architecture:** Uses a Python registry pattern. Adding new strategies requires adding one file and updating the JSON. 
* **Automated Trade Logging:** Outputs a detailed trade log to an Excel file (`orders.xlsx`) including entry/exit dates, prices, PnL, and the specific strategy/regime used.

## 📁 Directory Structure

    project/
    ├── configs/
    │   └── engine.json              # Main configuration file
    ├── data/
    │   ├── ohlc_raw.csv             # Raw data fetched via yfinance
    │   └── ohlc_clean.csv           # Cleaned data used by the engine
    ├── docs/
    │   └── research_notes.md        # Notes on regime logic and edge
    ├── engine/
    │   ├── regimes/
    │   │   └── logic.py             # Regime classification logic
    ├── strategies/
    │   ├── strategy_base.py     # Base abstract class & Registry
    │   ├── trend_following.py   # STRAT_1
    │   ├── mean_reversion.py    # STRAT_2
    │   ├── volatility_breakout.py # STRAT_3
    │   └── range_play.py        # STRAT_4
    └── utils/
        └── data_fetcher.py      # Script to download OHLCV data
    ├── outputs/
    │   ├── validation_report.txt    # Data validation metrics
    │   └── orders.xlsx              # Final backtest trade log
    ├── run_engine.py                # Main execution script
    └── README.md

## ⚙️ Installation & Setup

1. **Ensure you have Python 3.8+ installed.**
2. **Install the required dependencies:**
   ```bash
   pip install pandas numpy yfinance openpyxl
