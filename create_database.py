import pymysql

# MySQL database credentials
DB_HOST = "localhost" #MySQL80
DB_USER = "root"
DB_PASSWORD = "your_FitEgg1234_yoga"
DB_NAME = "forex_trading_SS"

def create_database_and_tables():
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = connection.cursor()

        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Database '{DB_NAME}' created or already exists.")

        # Select the database
        cursor.execute(f"USE {DB_NAME};")

        # Create the 'trades' table
        create_trades_table_query = """
        CREATE TABLE IF NOT EXISTS trades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticket BIGINT NOT NULL,  -- Add ticket column as NOT NULL
            symbol VARCHAR(10),
            order_type VARCHAR(4),
            volume FLOAT,
            price FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

                # SQL Query to Create `trade_metrics` Table
        create_trade_metrics_table = """
        CREATE TABLE IF NOT EXISTS trade_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trade_id INT NOT NULL,
            rsi FLOAT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trade_id) REFERENCES trades(id)
        );
        """

        # SQL Query to Create `trade_closures` Table
        create_trade_closures_table = """
        CREATE TABLE IF NOT EXISTS trade_closures (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trade_id INT NOT NULL,
            close_reason VARCHAR(50) NOT NULL,
            close_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trade_id) REFERENCES trades(id)
        );
        """
        cursor.execute(create_trades_table_query)
        cursor.execute(create_trade_metrics_table)
        cursor.execute(create_trade_closures_table)
        print("Table 'trades' created or already exists.")

        # Commit changes and close connection
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_database_and_tables()
