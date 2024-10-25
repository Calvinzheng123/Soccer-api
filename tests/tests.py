import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='soccer-api.c9sauo86m8mu.us-east-2.rds.amazonaws.com',
            user='root',    
            password='Zheng123!',  
            database='soccer_api'      
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
create_connection()