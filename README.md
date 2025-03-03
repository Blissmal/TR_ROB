# Forex Trading Bot

## Overview
The Forex Trading Bot is an automated trading system that integrates with MetaTrader 5 (MT5). It analyzes market data, calculates moving averages, executes trades based on predefined strategies, and dynamically manages risk.

## Features
- Seamless integration with the MetaTrader 5 platform
- Utilizes fast and slow moving averages for trade signals
- Automates buy and sell trade execution
- Implements risk management with stop-loss and take-profit orders
- Includes a trailing stop feature for better risk management
- Continuously monitors trades and adjusts stop-loss levels
- Ensures trading occurs only within specified hours

## Prerequisites
- Python 3.x installed
- MetaTrader 5 installed
- `MetaTrader5` Python package installed (`pip install MetaTrader5`)

## Installation
1. Clone or download this repository.
2. Install the required Python package:
   ```bash
   pip install MetaTrader5
   ```
3. Ensure your MetaTrader 5 platform is running and your account details are correctly configured.

## Usage
1. Update the `your_login` and `your_password` variables with your MT5 demo or real account credentials.
2. Configure the trading parameters:
   - **Symbol** (e.g., "USDJPY")
   - **Timeframe** (e.g., `mt5.TIMEFRAME_M1` for 1-minute charts)
   - **Fast and slow moving average periods**
   - **Maximum risk percentage per trade**
   - **Take-profit and trailing-stop ratios**
3. Run the bot:
   ```bash
   python trading_bot.py
   ```

## Parameters
| Parameter | Description |
|-----------|-------------|
| `symbol` | The trading symbol (e.g., USDJPY) |
| `timeframe` | The timeframe for market analysis |
| `fast_ma_period` | The fast moving average period |
| `slow_ma_period` | The slow moving average period |
| `max_risk_percent` | The maximum risk percentage per trade |
| `take_profit_ratio` | The take-profit ratio |
| `trailing_stop_ratio` | The trailing-stop ratio |

## Functionality
- **`get_market_data()`**: Retrieves market data.
- **`calculate_moving_averages()`**: Computes moving averages.
- **`calculate_position_size()`**: Determines trade size based on risk percentage.
- **`is_within_trading_hours()`**: Ensures trades are executed within active market hours.
- **`execute_trade()`**: Places buy or sell orders based on market conditions.
- **`adjust_stop_loss()`**: Dynamically adjusts the stop-loss based on price movement.
- **`monitor_trades()`**: Continuously monitors open trades and applies necessary adjustments.
- **`main()`**: Runs the trading loop continuously, with a 60-second delay between cycles.

## Notes
- The bot executes trades every hour if a valid signal is detected.
- It operates only within trading hours to minimize unnecessary risk.
- Built-in error handling ensures robustness and stability.

## Disclaimer
**This bot is intended for educational purposes only. Trading carries significant financial risk, and past performance does not guarantee future results. Use at your own discretion.**

