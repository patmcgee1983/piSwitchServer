import mysql.connector

piDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="toor"
    )

print(piDb)
