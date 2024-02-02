import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define connection to MetaTrader 5
def connect_to_mt5():
    """Connect to MetaTrader 5."""
    if not mt5.initialize():
        logging.error("Failed to connect to MetaTrader 5.")
        return False
    return True

# Check account balance
def check_account_balance():
    """Check account balance."""
    account_info = mt5.account_info()
    balance = account_info.balance
    if balance < 30:
        logging.error("Insufficient balance for trading.")
        mt5.shutdown()
        exit()
    return balance

# Retrieve historical prices
def retrieve_historical_prices(symbol, timeframe, num_periods):
    """Retrieve historical prices."""
    history = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_periods)
    prices = pd.DataFrame(history)
    return prices

# Calculate ATR (Average True Range) for volatility-based position sizing
def calculate_atr(prices, period=14):
    """Calculate Average True Range (ATR)."""
    high_low_range = prices['high'] - prices['low']
    high_close_range = abs(prices['high'] - prices['close'].shift())
    low_close_range = abs(prices['low'] - prices['close'].shift())
    true_range = pd.concat([high_low_range, high_close_range, low_close_range], axis=1).max(axis=1)
    atr = true_range.rolling(period).mean().iloc[-1]
    return atr

# Open a buy order
def open_buy_order(symbol, lot_size, stop_loss, take_profit):
    """Open a buy order."""
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).bid,
        "sl": stop_loss,
        "tp": take_profit,
        "magic": 123456,
        "comment": "Python EA Buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        logging.info("Buy order executed successfully.")
        return result.order
    else:
        logging.error(f"Order send failed: {result.comment}")
        return None

# Modify an existing order
def modify_order(order, stop_loss, take_profit):
    """Modify an existing order."""
    result = mt5.order_modify(order, sl=stop_loss, tp=take_profit)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        logging.info("Order modified successfully.")
    else:
        logging.error(f"Order modification failed: {result.comment}")

# Backtest the trading strategy
def backtest_strategy(symbol, timeframe, num_periods):
    """Backtest the trading strategy."""
    # Retrieve historical prices
    prices = retrieve_historical_prices(symbol, timeframe, num_periods)

    # Calculate ATR (Average True Range) for volatility-based position sizing
    atr = calculate_atr(prices)

    # Example: Calculate position size based on balance and ATR
    # For backtesting, assume a fixed position size
    position_size = 0.1  # Fixed position size of 0.1 lots

    # Example: Simulate executing the strategy on historical data
    num_trades = 0
    total_profit = 0.0
    for index, row in prices.iterrows():
        # Simulate trade execution based on trade signal conditions
        if row['rsi'] > 70 and row['macd'] > 0:
            # Example: Calculate stop loss and take profit levels
            stop_loss = row['close'] - 2 * atr  # Set stop loss at 2x ATR below entry
            take_profit = row['close'] + 3 * atr  # Set take profit at 3x ATR above entry
            
            # Execute buy order with fixed position size
            order = open_buy_order(symbol, position_size, stop_loss, take_profit)
            if order:
                num_trades += 1
                profit = (take_profit - row['close']) * position_size  # Calculate profit/loss
                total_profit += profit

    # Calculate performance metrics
    win_rate = num_trades / len(prices)
    average_profit_per_trade = total_profit / num_trades if num_trades > 0 else 0.0

    # Print performance metrics
    logging.info(f"Backtest Results for {symbol}:")
    logging.info(f"Number of Trades: {num_trades}")
    logging.info(f"Win Rate: {win_rate:.2%}")
    logging.info(f"Average Profit per Trade: {average_profit_per_trade:.2f}")

# Main function
def ForexStrategyOptimizer():
    # Connect to MetaTrader 5
    if not connect_to_mt5():
        exit()

    # Define timeframes and number of periods for historical data
    timeframe = mt5.TIMEFRAME_M15
    num_periods = 100

    # Backtest the trading strategy for each currency pair
    currency_pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "XAUUSD"]
    for symbol in currency_pairs:
        backtest_strategy(symbol, timeframe, num_periods)

    # Disconnect from MetaTrader 5
    mt5.shutdown()

# Advertisement
print("\nUnlock Your Trading Potential with Our Advanced Forex Trading Robot!\n")
print("Are you ready to take your forex trading to the next level? Introducing our cutting-edge automated trading robot powered by advanced algorithms and state-of-the-art technology.\n")
print("Key Features:\n")
print("1. Intelligent Trade Signal Analysis")
print("2. Dynamic Position Sizing")
print("3. Advanced Order Management\n")
print("Don't miss out on this opportunity to optimize your trading strategy and maximize your profits. Get started today!")

if __name__ == "__main__":
    ForexStrategyOptimizer()