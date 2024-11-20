from trade_executor import place_order_with_pip_sl_tp, place_order_with_pip_dyamic
import MetaTrader5 as mt5

def test_place_order():
    # Initialize MetaTrader5
    if not mt5.initialize():
        print("Failed to initialize MetaTrader5")
        return

    # Test parameters
    symbol = "EURUSD"  # Replace with the symbol you want to test
    order_type = "buy"  # Test with "buy" or "sell"
    volume = 0.1  # Lot size
    pips_tp = 8  # Take Profit in pips
    pips_sl = 8  # Stop Loss in pips

    symbol = "EURUSD"  # Replace with your symbol
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(f"Symbol {symbol} not found.")
    else:
        print(f"Supported filling modes for {symbol}: {symbol_info.filling_mode}")

    # Place the order
    try:
        print(f"Testing {order_type} order for {symbol} with {pips_tp} TP and {pips_sl} SL...")
        result = place_order_with_pip_dyamic(symbol, "sell", volume=1,atr_value=4/10000,pips_tp=0,pips_sl=0)

        # Print the result
        if result:
            print("Order placed successfully!")
            print(f"Details: {result}")
        else:
            print("Order placement failed. Check the function for issues.")
    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        # Shutdown MetaTrader5
        mt5.shutdown()

if __name__ == "__main__":
    test_place_order()
