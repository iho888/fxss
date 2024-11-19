import MetaTrader5 as mt5
import pandas as pd
from mt5_util import initialize_mt5_with_retry

def fetch_mt5_data(symbol, timeframe, num_bars):
    
    mt5 = initialize_mt5_with_retry()
    if not mt5:
        print("MetaTrader5 initialization failed")
        quit()

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    # print("Fetched data:", rates)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
