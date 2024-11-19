import MetaTrader5 as mt5
from mt5_util import initialize_mt5_with_retry

def place_order(symbol, order_type, volume=0.1):
    price = mt5.symbol_info_tick(symbol).ask if order_type == "buy" else mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": "Scalping Strategy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed: {result.retcode}")
    return result


def place_order_with_pip_sl_tp(symbol, order_type, volume, pips_tp, pips_sl):
    """
    Place a limit order with SL/TP calculated in pips.

    :param symbol: Trading symbol (e.g., 'EURUSD')
    :param order_type: 'buy' or 'sell'
    :param volume: Volume of the order (e.g., 0.1 for 0.1 lot)
    :param pips_tp: Take Profit distance in pips
    :param pips_sl: Stop Loss distance in pips
    :return: Result of the order placement
    """
    # Retrieve symbol information
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Failed to retrieve symbol info for {symbol}")
    
    # Ensure the symbol is active
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise ValueError(f"Failed to activate symbol {symbol}")
    
    # Get the current price
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        raise ValueError(f"Failed to retrieve tick data for {symbol}")
    
    point = symbol_info.point  # Symbol's point value (e.g., 0.0001 for EURUSD)
    pip_value = 10 * point  # 1 pip = 10 points for most forex pairs

    # Calculate SL and TP levels
    if order_type == "buy":
        price = tick.ask  # Entry price for buy orders
        take_profit = price + (pips_tp * pip_value)
        stop_loss = price - (pips_sl * pip_value)
    elif order_type == "sell":
        price = tick.bid  # Entry price for sell orders
        take_profit = price - (pips_tp * pip_value)
        stop_loss = price + (pips_sl * pip_value)
    else:
        raise ValueError("Invalid order type. Use 'buy' or 'sell'.")

    # Prepare the order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": stop_loss,  # Stop Loss level
        "tp": take_profit,  # Take Profit level
        "deviation": 1,  # Maximum allowed slippage in points
        "magic": 131313,  # Unique identifier for the order
        "comment": "Order with pip-based SL/TP",
        "type_time": mt5.ORDER_TIME_GTC,  # Good Till Cancelled
        "type_filling": mt5.ORDER_FILLING_FOK,  # Immediate or Cancel
    }

    # Send the order
    result = mt5.order_send(request)

    # Check the result
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.retcode}")
    else:
        print(f"Order placed successfully: {result}")

    return result

def check_existing_order(symbol):
    if not initialize_mt5_with_retry():
        print("Failed to initialize MetaTrader5")
        return
    orders = mt5.positions_get()
    if orders is None:
        print("Error:", mt5.last_error())
        return None
    if orders == None:
        print("No orders found, error code =", mt5.last_error())
        return None
    elif len(orders) > 0:
        for order in orders:
            print(f"Order {order.ticket}, Symbol: {order.symbol}")
            if order.symbol == symbol:
                return order.ticket
    else:
        print("No active orders.")
        return None


