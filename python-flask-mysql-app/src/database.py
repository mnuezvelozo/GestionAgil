import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='flask',
    password='flask',
    database='flaskproduct'
)