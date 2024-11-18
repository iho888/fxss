from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order, place_order_with_pip_sl_tp
from database import log_trade
import time

from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order_with_pip_sl_tp
from database import log_trade
import time


def main():
    # List of symbols to trade
    SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]  # Add more pairs as needed
    TIMEFRAME = 1  # 1-minute chart
    NUM_BARS = 50
    VOLUME = 0.1  # Lot size
    PIPS_TP = 8  # Take Profit in pips
    PIPS_SL = 8  # Stop Loss in pips

    while True:
        for symbol in SYMBOLS:
            print(f"Processing {symbol}...")

            # Fetch data for the symbol
            data = fetch_mt5_data(symbol, TIMEFRAME, NUM_BARS)
            if data is None or data.empty:
                print(f"No data available for {symbol}")
                continue

            # Rename columns if necessary
            data.rename(columns={"tick_volume": "volume"}, inplace=True)

            # Validate required columns
            required_columns = {'close', 'high', 'low', 'volume'}
            if not required_columns.issubset(data.columns):
                print(f"Data is missing required columns for {symbol}: {required_columns - set(data.columns)}")
                continue

            # Apply scalping strategy
            data = apply_scalping_strategy(data)

            # Check Buy Signal
            if data['Buy_Signal'].iloc[-1]:
                print(f"Buy signal detected for {symbol}")
                place_order_with_pip_sl_tp(symbol, "buy", volume=VOLUME, pips_tp=PIPS_TP, pips_sl=PIPS_SL)
                log_trade(symbol, "buy", VOLUME, data['close'].iloc[-1])

            # Check Sell Signal
            if data['Sell_Signal'].iloc[-1]:
                print(f"Sell signal detected for {symbol}")
                place_order_with_pip_sl_tp(symbol, "sell", volume=VOLUME, pips_tp=PIPS_TP, pips_sl=PIPS_SL)
                log_trade(symbol, "sell", VOLUME, data['close'].iloc[-1])

        # Wait before processing again
        time.sleep(10)

if __name__ == "__main__":
    main()

