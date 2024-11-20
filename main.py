from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order, place_order_with_pip_sl_tp, check_existing_order,place_order_with_pip_dyamic
from database import log_trade
from monitor_position import monitor_position,initialize_mt5_with_retry
from check_trading_session import  is_trading_session
import time



def main():
    # List of symbols to trade
    SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]  # Add more pairs as needed
    TIMEFRAME = 5  # 1-minute chart
    NUM_BARS = 50
    VOLUME = 1.0  # Lot size
    PIPS_TP = 8  # Take Profit in pips
    PIPS_SL = 5  # Stop Loss in pips

    while True :
        if is_trading_session():
            print(f"We are within the trading session!")
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
                data = apply_scalping_strategy(data,symbol)

                # Check Buy Signal
                if data['Buy_Signal'].iloc[-1]:
                    print(f"Buy signal detected for {symbol}")
                    if check_existing_order(symbol,0) == None:
                        result = place_order_with_pip_dyamic(symbol, "buy", volume=VOLUME,atr_value=data['ATR'].iloc[-1],pips_tp=0,pips_sl=0)
                        #monitor_position(result.order,10)
                        if result is None:
                            time.sleep(1)
                        else:
                            log_trade(symbol, result.order, "buy", VOLUME, data['close'].iloc[-1],data['RSI'].iloc[-1])
                    else:
                        print(f"Orders existed for {symbol}")

                # Check Sell Signal
                if data['Sell_Signal'].iloc[-1]:
                    print(f"Sell signal detected for {symbol}")
                    if check_existing_order(symbol,1) == None:                
                        result = place_order_with_pip_dyamic(symbol, "sell", volume=VOLUME,atr_value=data['ATR'].iloc[-1],pips_tp=0,pips_sl=0)
                        #monitor_position(result.order,10)
                        if result is None:
                            time.sleep(1)
                        else:
                            log_trade(symbol, result.order, "sell", VOLUME, data['close'].iloc[-1],data['RSI'].iloc[-1])
                    else:
                        print(f"Orders existed for {symbol}") 

        else:
            print(f"Outside trading Hours!")    
        # Wait before processing again
        time.sleep(10)

if __name__ == "__main__":
    main()

