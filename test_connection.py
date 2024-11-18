import MetaTrader5 as mt5
import pandas as pd

if not mt5.initialize():
    print("MetaTrader5 initialization failed")
    quit()

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M1
num_bars = 10

# Activate the symbol
if not mt5.symbol_select(symbol, True):
    print(f"Failed to activate symbol {symbol}")
else:
    print(f"Symbol {symbol} is activated.")

# Fetch data
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
if rates is None:
    print(f"No data retrieved for symbol {symbol} on timeframe {timeframe}.")
else:
    # Convert to DataFrame for easier inspection
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df)
