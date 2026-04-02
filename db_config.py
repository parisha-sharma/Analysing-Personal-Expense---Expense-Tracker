import mysql.connector

def get_connection():    #Creating a function to connect to SQL
    password = input("Enter your DB password: ")    #input password from the user
    connection = mysql.connector.connect(    #connecting with SQL
        host="localhost",
        user="root",
        password=password,
        database="expense_tracker"    #Database name
    )
    return connection
