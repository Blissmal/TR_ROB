import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(filename='forex_trading.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model(X, y):
    """
    Train a Gradient Boosting Classifier model with hyperparameter tuning.

    Parameters:
    X (DataFrame): Features.
    y (Series): Target variable.

    Returns:
    best_model: Best trained model.
    """
    try:
        model = GradientBoostingClassifier(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.5]
        }
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
        grid_search.fit(X, y)
        best_model = grid_search.best_estimator_
        return best_model
    except Exception as e:
        logging.error(f"Error occurred during model training: {e}")
        raise RuntimeError("Error occurred during model training")

def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) using pandas.

    Parameters:
    data (DataFrame): Historical data including the 'close' price.
    window (int): Window size for RSI calculation (default is 14).

    Returns:
    rsi (Series): Relative Strength Index.
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal(model, current_data, signal_duration):
    """
    Generate a trading signal based on the current data.

    Parameters:
    model: Trained model for prediction.
    current_data (DataFrame): Current data point for prediction.
    signal_duration (int): Duration of the signal in minutes.

    Returns:
    prediction: Predicted trading signal.
    signal_duration: Duration of the signal.
    """
    try:
        # Calculate RSI
        current_data['RSI'] = calculate_rsi(current_data)

        # Make prediction
        X_real_time = current_data[['RSI', 'other_features']].values.reshape(1, -1)
        prediction = model.predict(X_real_time)

        return prediction, signal_duration
    except Exception as e:
        logging.error(f"Error occurred during signal generation: {e}")
        raise RuntimeError("Error occurred during signal generation")

def plot_data_with_expected_movement(data, next_trade_signal, signal_duration):
    """
    Plot historical data with the next trade signal and expected movement direction.

    Parameters:
    data (DataFrame): Historical data.
    next_trade_signal (int): Next trade signal.
    signal_duration (int): Duration of the signal in minutes.
    """
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(data['timestamp'], data['close'], color='blue', label='Close Price')

        # Plot arrow
        if next_trade_signal == 1:
            arrow_color = 'green'
            arrow_direction = 'up'
        elif next_trade_signal == -1:
            arrow_color = 'red'
            arrow_direction = 'down'
        else:
            arrow_color = 'black'
            arrow_direction = 'up'

        plt.annotate(f'{signal_duration} min', xy=(0.5, 0.5), xytext=(0.5, 0.6),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=12, ha='center')

        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.title('Forex Trading Signals with Expected Movement')
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        logging.error(f"Error occurred during visualization: {e}")
        raise RuntimeError("Error occurred during visualization")

def main():
    try:
        # Load and preprocess data
        # (You'll need to replace this with your data loading and preprocessing code)
        data = pd.read_csv("forex_data.csv")
        X = data.drop(columns=["label"])
        y = data["label"]
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = train_model(X_train, y_train)

        # Simulate real-time data
        # Connect to live data feed and continuously receive real-time data
        # For demonstration purposes, let's assume we have a single data point
        current_data = {'timestamp': '2024-02-04 12:00:00', 'close': 1.2345, 'other_features': [0.1, 0.5, 0.2]}  # Add real features based on your data

        # Generate signal for the next trade
        next_trade_signal, signal_duration = generate_signal(model, current_data, 15)  # Signal duration: 15 minutes

        # Plot data with expected movement direction
        plot_data_with_expected_movement(data, next_trade_signal, signal_duration)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred. Please check the log file for details.")

if __name__ == "_main_":
    main()