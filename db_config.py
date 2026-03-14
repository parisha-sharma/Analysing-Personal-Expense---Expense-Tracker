import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password="Pari1503", 
        database="expense_tracker"
    )
    return connection