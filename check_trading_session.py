from datetime import datetime, time

def is_trading_session():
    """
    Check if the current UTC time falls into the London or New York trading sessions.

    Returns:
        bool: True if the current time is within either session, False otherwise.
    """
    # Get the current UTC time
    now_utc = datetime.utcnow().time()

    # Define session times
    london_session = (time(8, 0), time(16, 0))  # London: 08:00–16:00 UTC
    new_york_session = (time(13, 0), time(21, 0))  # New York: 13:00–21:00 UTC

    # Check if current UTC time falls into either session
    return london_session[0] <= now_utc <= london_session[1] or \
           new_york_session[0] <= now_utc <= new_york_session[1]

if is_trading_session():
    print("We are within the trading session!")
else:
    print("Outside trading hours.")