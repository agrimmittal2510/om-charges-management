import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    password = "agri2511",
    database = "om_charges_management"
    )
    return conn
