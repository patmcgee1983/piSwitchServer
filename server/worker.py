#!/usr/bin/python3.5

print("Program Start...")
import mysql.connector
import datetime
import time
from gpiozero import LED

gpio = LED(2)


while True:

    piDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="toor"
    )


    mycursor = piDb.cursor()
    mycursor.execute("USE piDb")

    currentTime = datetime.datetime.now()
    #print(currentTime)
    sql = "SELECT Id,Name,State,ForceOn,StartTime,EndTime,Gpio,Days,SchedulerState FROM Zone"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    for i in myresult:
        #print(i)
        
        # if the state is ON, trun on the GPIO for that Zone
        
        if i[2] == 1:
            print("turning on GPIO "+str(i[6])+" on Zone Id "+ str(i[0]))
            gpio.on()
        else:
            print("turning off GPIO "+str(i[6])+" on Zone Id "+ str(i[0]))
            gpio.off()

    mycursor.close()
    piDb.close()
    
    time.sleep(2)

