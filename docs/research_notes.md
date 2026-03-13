# Research Notes: Regime-Based Strategy Switching

### How Regime Logic Works
The regime classifier uses a dynamic approach rather than static thresholds. It calculates the 50-day Simple Moving Average (SMA) to establish basic trend direction, and an Average True Range (ATR) over 14 days to measure volatility. To adapt to changing market conditions, it compares the current ATR against a rolling 60-day 30th and 70th percentile threshold. 
- **Trending:** Price > 50 SMA.
- **Volatile:** Current ATR > 70th percentile of recent history.
- **Low Vol:** Current ATR < 30th percentile of recent history.
- **Ranging:** Default state when none of the extreme conditions are met.

### When Each Strategy is Effective
- **Trend Following (MA Crossover):** Best in directional markets (Trending regime) where momentum overrides mean reversion tendencies.
- **Mean Reversion (RSI):** Highly effective in Low Volatility regimes where the market behaves like a spring, reacting predictably to short-term overbought/oversold levels.
- **Volatility Breakout:** Best triggered during high Volatility regimes where massive range expansions occur, capturing momentum spikes.
- **Range Play:** Effective in Ranging regimes where price action is choppy and bounded.

### Edge in Dynamic Switching
Static strategies suffer massive drawdowns when the market environment changes (e.g., trend followers get chopped up in sideways markets). Dynamic switching limits capital exposure to suboptimal market conditions, improving the overall Sharpe ratio by aligning the mathematical logic of the strategy with current market physics.

### Risks of Regime Switching
- **Whipsawing:** Rapid changes in regimes can cause the engine to swap strategies too frequently, accumulating transaction costs and false starts.
- **Lag:** MA and ATR are lagging indicators. By the time a "Trend" regime is detected, the move may already be halfway over.

### Suggested Improvements
1. **Regime Smoothing:** Apply a hidden Markov model (HMM) or an exponential moving average to the regime state to prevent flickering between states day-to-day.
2. **Position Sizing:** Currently fixed at `qty=1`. Integrating Kelly Criterion or ATR-based position sizing based on account equity would drastically improve risk management.