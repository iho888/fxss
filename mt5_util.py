import MetaTrader5 as mt5
import time

def initialize_mt5_with_retry(retry_interval=5):
    """
    Initializes MetaTrader 5 with retry logic. 
    Keeps retrying until successful.

    Args:
        retry_interval (int): Time in seconds to wait between retries.
    """
    while not mt5.initialize():
        print("Failed to initialize MetaTrader 5. Retrying in", retry_interval, "seconds...")
        time.sleep(retry_interval)
    
    return mt5
    print("Successfully initialized MetaTrader 5.")

# Example usage
#initialize_mt5_with_retry()
