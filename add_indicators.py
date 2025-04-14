import pandas as pd
import ta

def add_indicator_data(input_file, output_file):
    # Read the CSV file. Make sure the CSV has columns: Date, Open, High, Low, Close, Volume.
    data = pd.read_csv(input_file, parse_dates=["Date"])
    
    # Set the Date column as the index (like a row label).
    data.set_index("Date", inplace=True)
    
    # Convert the key columns to numbers (if they're not already).
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    
    # Remove rows that are missing data.
    data.dropna(inplace=True)
    
    # Calculate RSI using a 14-day window.
    data["RSI"] = ta.momentum.RSIIndicator(close=data["Close"], window=14).rsi()
    
    # Calculate MACD and its signal line (using default parameters: fast=12, slow=26, signal=9).
    macd_obj = ta.trend.MACD(close=data["Close"])
    data["MACD"] = macd_obj.macd()
    data["MACD_Signal"] = macd_obj.macd_signal()
    
    # Calculate Bollinger Bands (window of 20, multiplier 2).
    bb_obj = ta.volatility.BollingerBands(close=data["Close"], window=20, window_dev=2)
    data["BB_High"] = bb_obj.bollinger_hband()
    data["BB_Low"] = bb_obj.bollinger_lband()
    
    # Save the augmented data to a new CSV file.
    data.to_csv(output_file)
    print(f"Indicator data has been saved to {output_file}")

if __name__ == "__main__":
    # Use the exact name of the file you uploaded.
    add_indicator_data("Download Data - FUND_US_XNAS_QQQ.csv", "augmented_data.csv")
