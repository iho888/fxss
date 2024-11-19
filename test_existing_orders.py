import MetaTrader5 as mt5
from data_fetcher import fetch_mt5_data
from strategy import apply_scalping_strategy
from trade_executor import place_order, place_order_with_pip_sl_tp, check_existing_order
from database import log_trade
import time

def test_existing_order():
    if not mt5.initialize():
        print("Failed to initialize MetaTrader5")
    check_existing_order("USDCHF")
    return



if __name__ == "__main__":
    test_existing_order()