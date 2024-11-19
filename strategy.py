from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

def apply_scalping_strategy(data):
    # Ensure the required columns are present in the data (e.g., 'close', 'high', 'low', 'volume')
    if not {'close', 'high', 'low', 'volume'}.issubset(data.columns):
        raise ValueError("Data is missing required columns: 'close', 'high', 'low', or 'volume'.")

    # Calculate EMA9 and EMA21
    data['EMA9'] = EMAIndicator(data['close'], window=5).ema_indicator()
    data['EMA21'] = EMAIndicator(data['close'], window=10).ema_indicator()

    # Compare EMA9 and EMA21 with proper handling of NaN
    data['Trend'] = data['EMA9'] > data['EMA21']

    # Calculate RSI
    data['RSI'] = RSIIndicator(data['close'], window=14).rsi()

    # Calculate ATR
    data['ATR'] = AverageTrueRange(data['high'], data['low'], data['close'], window=14).average_true_range() * 10000

    # Calculate On-Balance Volume (OBV)
    data['OBV'] = OnBalanceVolumeIndicator(data['close'], data['volume']).on_balance_volume()

    # print indicators
    print (f"EMA9 =  {data['EMA9'].iloc[-1]}")
    print (f"EMA21=  {data['EMA21'].iloc[-1]}")
    print (f"RSI=  {data['RSI'].iloc[-1]}")
    print (f"ATR=  {data['ATR'].iloc[-1]}")
    #print (f"OBV=  {data['OBV'].iloc[-1]}")


    # Define Buy Signal
    #data['Buy_Signal'] = (
    #    ((data['EMA9'] > data['EMA21']) & (data['EMA9'].shift(1) <= data['EMA21'].shift(1))
    #    ).fillna(False) &  # Bullish EMA crossover
    #    (data['RSI'] < 40) &  # Oversold RSI
    #    (data['ATR'] > data['ATR'].rolling(3).mean())  # ATR above average (increased volatility)
    #)

    data['Buy_Signal'] = (
        ((data['EMA9'] > data['EMA21']) & (data['EMA9'].shift(1) <= data['EMA21'].shift(1))
        ).fillna(False)  &          # Bullish trend
        ((data['RSI'] > 55) & (data['RSI'] < 70)) &           # Neutral RSI
        (data['ATR'] < data['ATR'].rolling(5).mean()) # Stable volatility
    )

    data['Sell_Signal'] = (
        ((data['EMA9'] < data['EMA21']) & (data['EMA9'].shift(1) >= data['EMA21'].shift(1))
        ).fillna(False) &        # Bearish trend
        ((data['RSI'] < 45) & (data['RSI'] > 30) ) &           # Neutral RSI
        (data['ATR'] < data['ATR'].rolling(5).mean()) # Stable volatility
    )

    return data

