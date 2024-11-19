from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order, place_order_with_pip_sl_tp, check_existing_order
from database import log_trade
import time

from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order_with_pip_sl_tp
from monitor_position import close_position_thread, monitor_position
from database import log_trade
import time


def main():
    # List of symbols to trade
    SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]  # Add more pairs as needed
    TIMEFRAME = 1  # 1-minute chart
    NUM_BARS = 50
    VOLUME = 1.0  # Lot size
    PIPS_TP = 6  # Take Profit in pips
    PIPS_SL = 6  # Stop Loss in pips

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
                if check_existing_order(symbol) == None:
                    result = place_order_with_pip_sl_tp(symbol, "buy", volume=VOLUME, pips_tp=PIPS_TP, pips_sl=PIPS_SL)
                    monitor_position(result.order,5)
                    log_trade(symbol, result.order, "buy", VOLUME, data['close'].iloc[-1],data['RSI'].iloc[-1])
                else:
                    print(f"Orders existed for {symbol}")

            # Check Sell Signal
            if data['Sell_Signal'].iloc[-1]:
                print(f"Sell signal detected for {symbol}")
                if check_existing_order(symbol) == None:                
                    result = place_order_with_pip_sl_tp(symbol, "sell", volume=VOLUME, pips_tp=PIPS_TP, pips_sl=PIPS_SL)
                    monitor_position(result.order,5)
                    log_trade(symbol, result.order, "sell", VOLUME, data['close'].iloc[-1],data['RSI'].iloc[-1])
                else:
                    print(f"Orders existed for {symbol}") 

        # Wait before processing again
        time.sleep(10)

if __name__ == "__main__":
    main()

