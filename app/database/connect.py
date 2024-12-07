import os
import mysql.connector

connection = None

def connect():
    global connection
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'), 
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        if connection.is_connected():
            print('Connected to MySQL database')

    except mysql.connector.Error as e:
        print(e)
