from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

def apply_scalping_strategy(data):
    # Ensure the required columns are present in the data (e.g., 'close', 'high', 'low', 'volume')
    if not {'close', 'high', 'low', 'volume'}.issubset(data.columns):
        raise ValueError("Data is missing required columns: 'close', 'high', 'low', or 'volume'.")

    # Calculate EMA
    data['EMA9'] = EMAIndicator(data['close'], window=9).ema_indicator()
    data['EMA21'] = EMAIndicator(data['close'], window=21).ema_indicator()

    # Calculate RSI
    data['RSI'] = RSIIndicator(data['close'], window=14).rsi()

    # Calculate ATR
    data['ATR'] = AverageTrueRange(data['high'], data['low'], data['close'], window=14).average_true_range()

    # Calculate On-Balance Volume (OBV)
    data['OBV'] = OnBalanceVolumeIndicator(data['close'], data['volume']).on_balance_volume()

    # Define Buy Signal
    data['Buy_Signal'] = (
        (data['EMA9'] > data['EMA21']) &  # Bullish EMA crossover
        (data['RSI'] < 30) &  # Oversold RSI
        (data['ATR'] > data['ATR'].rolling(5).mean())  # ATR above average (increased volatility)
    )

    # Define Sell Signal
    data['Sell_Signal'] = (
        (data['EMA9'] < data['EMA21']) &  # Bearish EMA crossover
        (data['RSI'] > 70) &  # Overbought RSI
        (data['ATR'] > data['ATR'].rolling(5).mean())  # ATR above average (increased volatility)
    )

    return data

