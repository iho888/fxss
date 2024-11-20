from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

def apply_scalping_strategy(data,symbol):
    # Ensure the required columns are present in the data (e.g., 'close', 'high', 'low', 'volume')
    if not {'close', 'high', 'low', 'volume'}.issubset(data.columns):
        raise ValueError("Data is missing required columns: 'close', 'high', 'low', or 'volume'.")

    # Calculate EMA9 and EMA21
    data['EMA9'] = EMAIndicator(data['close'], window=9).ema_indicator()
    data['EMA21'] = EMAIndicator(data['close'], window=21).ema_indicator()

    # Compare EMA9 and EMA21 with proper handling of NaN
    data['Trend'] = data['EMA9'] > data['EMA21']

    # Calculate RSI
    data['RSI'] = RSIIndicator(data['close'], window=14).rsi()

    # Calculate ATR
    if symbol == 'USDJPY':

        data['ATR'] = AverageTrueRange(data['high'], data['low'], data['close'], window=14).average_true_range() * 100
    else:
        data['ATR'] = AverageTrueRange(data['high'], data['low'], data['close'], window=14).average_true_range() * 10000

    # Calculate On-Balance Volume (OBV)
    data['OBV'] = OnBalanceVolumeIndicator(data['close'], data['volume']).on_balance_volume()

    # Calculate OBV trend (using difference between current and previous OBV)
    data['OBV_Trend'] = data['OBV'].diff()

    # Print indicators for debugging
    print(f"EMA9 =  {data['EMA9'].iloc[-1]}")
    print(f"EMA21 = {data['EMA21'].iloc[-1]}")
    print(f"RSI =   {data['RSI'].iloc[-1]}")
    print(f"ATR =   {data['ATR'].iloc[-1]}")
    #print(f"VOLUME =   {data['VOLUME'].iloc[-1]}")
    print(f"OBV =   {data['OBV'].iloc[-1]}")
    print(f"OBV Trend = {data['OBV_Trend'].iloc[-1]}")

    #print(data[['close', 'volume', 'OBV', 'OBV_Trend']].head(10))  # Inspect the first rows
    #print(data['OBV'].diff().describe())  # Examine the trend distribution
    #print((data['OBV'] < data['OBV'].shift()).any())  # Check if OBV ever decreases

    # Define Buy Signal (with OBV confirmation)
    data['Buy_Signal'] = (
        ((data['EMA9'] > data['EMA21']) & (data['EMA9'].shift(1) <= data['EMA21'].shift(1))
        ).fillna(False) &  # Bullish EMA crossover
        ((data['RSI'] > 50) & (data['RSI'] < 70)) &  # Neutral RSI
        (data['ATR'] < data['ATR'].rolling(5).mean()) #&  # Stable volatility
        #(data['OBV_Trend'] > 0)  # OBV rising (buying pressure)
    )

    # Define Sell Signal (with OBV confirmation)
    data['Sell_Signal'] = (
        ((data['EMA9'] < data['EMA21']) & (data['EMA9'].shift(1) >= data['EMA21'].shift(1))
        ).fillna(False) &  # Bearish EMA crossover
        ((data['RSI'] < 50) & (data['RSI'] > 30)) &  # Neutral RSI
        (data['ATR'] < data['ATR'].rolling(5).mean()) #&  # Stable volatility
        #(data['OBV_Trend'] < 0)  # OBV falling (selling pressure)
    )

    return data
