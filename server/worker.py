import mysql.connector
import datetime
import time

piDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="toor"
    )


mycursor = piDb.cursor()
mycursor.execute("USE piDb")
print(piDb)

while True:

    currentTime = datetime.datetime.now()
    print(currentTime)
    mycursor.execute("SELECT * FROM Zone")
    for x in mycursor:
        print(x[1])
    time.sleep(2)

