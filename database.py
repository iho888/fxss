import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)



# Function to log trade closures into the trade_closures table
def log_trade_closure(ticket, close_reason):
    """
    Logs a trade closure event into the trade_closures table.

    Args:
        ticket (int): The ticket number of the position.
        close_reason (str): The reason why the trade was closed.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        # Step 1: Find the trade_id from the trades table using the ticket
        find_trade_id_query = "SELECT id FROM trades WHERE ticket = %s"
        cursor.execute(find_trade_id_query, (ticket,))
        trade_row = cursor.fetchone()

        if trade_row is None:
            print(f"No matching trade found for ticket {ticket}. Closure not logged.")
            return

        trade_id = trade_row[0]  # Extract trade_id from the result

        # Step 2: Insert the closure details into trade_closures
        log_closure_query = """
            INSERT INTO trade_closures (trade_id, close_reason, close_timestamp)
            VALUES (%s, %s, NOW());
        """
        cursor.execute(log_closure_query, (trade_id, close_reason))
        connection.commit()
        print(f"Logged closure for trade ID {trade_id} with reason '{close_reason}'.")

        cursor.close()
        connection.close()
    except pymysql.MySQLError as err:
        print(f"Database error: {err}")

def log_trade(symbol, ticket, order_type, volume, price, rsi):
    with connection.cursor() as cursor:
        sql = "INSERT INTO trades (symbol,ticket, order_type, volume, price, timestamp) VALUES (%s, %s, %s, %s, %s, NOW())"
        cursor.execute(sql, (symbol,ticket, order_type, volume, price))
        
        # Get the ID of the newly inserted trade
        trade_id = cursor.lastrowid

        # Insert into trade_metrics table
        sql_rsi = "INSERT INTO trade_metrics (trade_id, rsi, timestamp) VALUES (%s, %s, NOW())"
        cursor.execute(sql_rsi, (trade_id, rsi))

        connection.commit()
