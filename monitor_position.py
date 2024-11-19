import MetaTrader5 as mt5
from datetime import datetime, timedelta
import threading
import argparse
from database import log_trade_closure

# Function to close a position based on timedelta and ticket number
def close_position_thread(ticket, time_limit_minutes):
    """
    Monitors a position and closes it if it has been open for more than the specified time limit and is making a profit.
    
    Args:
        ticket (int): The ticket number of the position to monitor.
        time_limit_minutes (int): The time limit in minutes to check before closing the position.
    """
    # Connect to MetaTrader 5
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        return

    # Define the time limit as a timedelta
    time_limit = timedelta(minutes=time_limit_minutes).total_seconds()

    while True:
        # Get the position by ticket number
        positions = mt5.positions_get(ticket=ticket)
        if positions is None or len(positions) == 0:
            print(f"No position found with ticket {ticket}")
            break

        # There should only be one position with this ticket
        position = positions[0]

        # Get position details
        #open_time = datetime.fromtimestamp(position.time)
        open_time = datetime.utcfromtimestamp(position.time)
        current_time = datetime.now()
        diff_time = current_time - open_time
        diff_time_sec = diff_time.total_seconds()

        profit = position.profit

        # Check if position has been open for more than the time limit and is profitable
        if (diff_time_sec) > time_limit and profit > 0:
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
                log_trade_closure(result.order,"P5")
                print(f"Successfully closed position {ticket} on {position.symbol}")
                break  # Exit the loop after closing the position
            else:
                print(f"Failed to close position {ticket}. Error: {result.retcode}")
                break

    # Shutdown MetaTrader 5
    mt5.shutdown()

# Function to start the thread
def monitor_position(ticket, time_limit_minutes=5):
    """
    Starts a thread to monitor and close a position.

    Args:
        ticket (int): The ticket number of the position to monitor.
        time_limit_minutes (int): The time limit in minutes to check before closing the position.
    """
    thread = threading.Thread(target=close_position_thread, args=(ticket, time_limit_minutes))
    thread.start()
    return thread

# Example usage
# Monitor a position with ticket 123456 and close it if it's been open for more than 5 minutes
monitor_position(2318611545, 5)
