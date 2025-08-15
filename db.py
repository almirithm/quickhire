import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # ← Replace this
        database="quickhire"
    )
    return connection