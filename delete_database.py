import pymysql

# MySQL Database Credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_FitEgg1234_yoga"
DB_NAME = "forex_trading_SS"

def delete_database():
    try:
        # Connect to MySQL Server
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        print("Connected to MySQL Server.")

        # Create a cursor to execute SQL commands
        cursor = connection.cursor()

        # Drop the database
        drop_db_query = f"DROP DATABASE {DB_NAME}"
        cursor.execute(drop_db_query)
        print(f"Database '{DB_NAME}' has been deleted successfully.")

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
    except pymysql.MySQLError as err:
        print(f"Error: {err}")

# Run the function
delete_database()
