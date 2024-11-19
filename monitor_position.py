import MetaTrader5 as mt5
import threading
import time
from database import log_trade_closure

# Function to close a position based on a timer and ticket number
def close_position_thread(ticket, time_limit_minutes, check_interval_seconds=10):
    """
    Monitors a position and closes it if it is making a profit after the specified time limit.

    Args:
        ticket (int): The ticket number of the position to monitor.
        time_limit_minutes (int): The time limit in minutes to wait before starting to check the position.
        check_interval_seconds (int): The interval in seconds to recheck the position for profit.
    """
    # Connect to MetaTrader 5
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        return

    # Convert time limit to seconds
    time_limit_seconds = time_limit_minutes * 60

    # Wait for the specified time limit
    time.sleep(time_limit_seconds)

    while True:
        # Check the position by ticket number
        positions = mt5.positions_get(ticket=ticket)
        if positions is None or len(positions) == 0:
            print(f"No position found with ticket {ticket}")
            break  # Exit the loop if the position no longer exists

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
                log_trade_closure(position.ticket, "P5")
                print(f"Successfully closed position {position.ticket} on {position.symbol}")
                break  # Exit the loop after successfully closing the position
            else:
                print(f"Failed to close position {position.ticket}. Error: {result.retcode}")

        # Wait for the specified interval before checking again
        time.sleep(check_interval_seconds)

    # Shutdown MetaTrader 5
    mt5.shutdown()

# Function to start the thread
def monitor_position(ticket, time_limit_minutes=5, check_interval_seconds=10):
    """
    Starts a thread to monitor and close a position.

    Args:
        ticket (int): The ticket number of the position to monitor.
        time_limit_minutes (int): The time limit in minutes to wait before starting to check the position.
        check_interval_seconds (int): The interval in seconds to recheck the position for profit.
    """
    thread = threading.Thread(
        target=close_position_thread, 
        args=(ticket, time_limit_minutes, check_interval_seconds)
    )
    thread.start()
    return thread

# Example usage
# Monitor a position with ticket 2318611545 and close it if it's profitable after 5 minutes
# monitor_position(2318611545, 5)
