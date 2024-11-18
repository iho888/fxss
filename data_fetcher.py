import MetaTrader5 as mt5
import pandas as pd

def fetch_mt5_data(symbol, timeframe, num_bars):
    
    if not mt5.initialize():
        print("MetaTrader5 initialization failed")
        quit()

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    print("Fetched data:", rates)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
