import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

def log_trade(symbol, order_type, volume, price):
    with connection.cursor() as cursor:
        sql = "INSERT INTO trades (symbol, order_type, volume, price, timestamp) VALUES (%s, %s, %s, %s, NOW())"
        cursor.execute(sql, (symbol, order_type, volume, price))
        connection.commit()
