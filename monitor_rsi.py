import MetaTrader5 as mt5
from datetime import datetime, timedelta
import threading
import pandas as pd
from ta.momentum import RSIIndicator
from database import log_trade_closure
import time 

def fetch_latest_rsi(symbol, timeframe, window=14):
    """
    Fetch the latest RSI value for the given symbol and timeframe.
    
    Args:
        symbol (str): The trading symbol (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., mt5.TIMEFRAME_M1).
        window (int): RSI calculation window (default is 14).

    Returns:
        float: The latest RSI value.
    """
    # Fetch the latest 100 bars for RSI calculation
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, window + 1)
    if rates is None:
        print(f"Failed to fetch data for {symbol}")
        return None

    # Convert rates to DataFrame
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)

    # Calculate RSI
    data['RSI'] = RSIIndicator(data['close'], window=window).rsi()
    return data['RSI'].iloc[-1]  # Return the latest RSI value


def monitor_rsi(symbol,ticket, timeframe, rsi_overbought=70, rsi_oversold=30, check_interval=5):
    """
    Thread function to monitor RSI and raise a signal if oversold/overbought.

    Args:
        symbol (str): The trading symbol (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., mt5.TIMEFRAME_M1).
        rsi_overbought (int): RSI overbought threshold (default is 70).
        rsi_oversold (int): RSI oversold threshold (default is 30).
        check_interval (int): Interval in seconds between RSI checks.
    """
    while True:
        # Fetch the latest RSI
        rsi = fetch_latest_rsi(symbol, timeframe)
        if rsi is None:
            print("Error fetching RSI. Retrying...")
            continue

        # Check RSI thresholds
        if rsi >= rsi_overbought:
            print(f"RSI Alert: Overbought ({rsi:.2f}) on {symbol}")
            close_position(symbol,ticket)
        elif rsi <= rsi_oversold:
            print(f"RSI Alert: Oversold ({rsi:.2f}) on {symbol}")
            close_position(symbol,ticket)
        # Wait for the next check
        threading.Event().wait(check_interval)


def start_rsi_monitoring_thread(symbol, ticket,timeframe, rsi_overbought=70, rsi_oversold=30, check_interval=5):
    """
    Start a thread to monitor RSI for a given symbol and timeframe.

    Args:
        symbol (str): The trading symbol (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., mt5.TIMEFRAME_M1).
        rsi_overbought (int): RSI overbought threshold.
        rsi_oversold (int): RSI oversold threshold.
        check_interval (int): Interval in seconds between RSI checks.
    """
    thread = threading.Thread(
        target=monitor_rsi, 
        args=(symbol, ticket,timeframe, rsi_overbought, rsi_oversold, check_interval),
        daemon=True  # Set daemon so the thread ends with the program
    )
    thread.start()
    return thread

from mt5_util import initialize_mt5_with_retry

# Function to close a position based on a timer and ticket number
def close_position(symbol,ticket):
    """
    Monitors a position and closes it if it is making a profit after the specified time limit.

    Args:
        ticket (int): The ticket number of the position to monitor.
        time_limit_minutes (int): The time limit in minutes to wait before starting to check the position.
        check_interval_seconds (int): The interval in seconds to recheck the position for profit.
    """
    # Connect to MetaTrader 5
    if not initialize_mt5_with_retry():
        print("Failed to initialize MetaTrader 5")
        return

    
    # Check the position by ticket number
    positions = mt5.positions_get(ticket=ticket)
    if positions is None or len(positions) == 0:
        print(f"No position found with ticket {ticket}")
        return   # Exit the loop if the position no longer exists

    # There should only be one position with this ticket
    position = positions[0]

    # Get position details
    profit = position.profit

    # Check if the position is profitable
    if profit > 0:
        # Close the position
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_BUY if position.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL,
            "position": position.ticket,
            "magic": position.magic,
            "comment": "Closing profitable position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            log_trade_closure(position.ticket, "P_RSI")
            print(f"Successfully closed position {position.ticket} on {position.symbol}")
            return  # Exit the loop after successfully closing the position
        else:
            log_trade_closure(position.ticket, "P_RSI_F")
            print(f"Failed to close position {position.ticket}. Error: {result.retcode}")


    # Shutdown MetaTrader 5
    mt5.shutdown()





# Example Usage
# if __name__ == "__main__":
#    if not mt5.initialize():
#        print("Failed to initialize MetaTrader 5")
#        quit()

#    # Start monitoring RSI for EURUSD on a 1-minute chart
#    symbol = "EURUSD"
#    timeframe = mt5.TIMEFRAME_M1
#    rsi_thread = start_rsi_monitoring_thread(symbol, 123456, timeframe)

#    # Let the main program continue running
#    try:
#        while True:
#            pass  # Keep the main program alive
#    except KeyboardInterrupt:
#        print("Stopping RSI monitoring...")
#        mt5.shutdown()
