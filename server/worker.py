#!/usr/bin/python3.5

#Number of Zones Hard wired into the PI
numberOfZones = 8

# Statically identify GPIO mapping for zones
class Zone:
    def __init__(self, number):
        self.id = number
    
        if number == 1:
            self.gpio = 2
            self.pin = 3
            
        if number == 2:
            self.gpio = 3
            self.pin = 5

        if number == 3:
            self.gpio = 4
            self.pin = 7

        if number == 4:
            self.gpio = 17
            self.pin = 11

        if number == 5:
            self.gpio = 27
            self.pin = 13

        if number == 6:
            self.gpio = 22
            self.pin = 15

        if number == 7:
            self.gpio = 23
            self.pin = 16

        #self.led = LED(self.gpio)
                   
zones = []
i=0

# Create number of zones as defined
while i < numberOfZones:
    zones.append(Zone(i))
    i+=1

print("Program Start...")
import mysql.connector
import datetime
import time
#from gpiozero import LED


piDb = mysql.connector.connect(
host="localhost",
user="root",
passwd="toor"
)



mycursor = piDb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS piDb")
mycursor.execute("USE piDb")

mycursor.execute("CREATE TABLE IF NOT EXISTS Zone(Id INT AUTO_INCREMENT, ForceOn BIT(1) DEFAULT 0, Name VARCHAR(60), State BIT(1) DEFAULT 0, StartTime TIME, EndTime TIME, GPIO INT, DAYS BIT(7) DEFAULT 45, SchedulerState BIT(1) DEFAULT 0,  constraint id_key PRIMARY KEY(Id));")
                     
#Create the Zones if they do not exist already
mycursor.execute("SELECT * FROM Zone")
myresult = mycursor.fetchall()

zonesCounted = 0
for i in myresult:
    zonesCounted+=1

print(str(zonesCounted) + " Zones Counted")

# If the number of Zones defined does not match how many are in the table we'll recreate them
if zonesCounted != numberOfZones:
    print("\nZone count mismatch... recreating Zones")
    mycursor.execute("DROP TABLE Zone")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Zone(Id INT AUTO_INCREMENT, ForceOn BIT(1) DEFAULT 0, Name VARCHAR(60), State BIT(1) DEFAULT 0, StartTime TIME, EndTime TIME, GPIO INT, DAYS BIT(7) DEFAULT 0000000, SchedulerState BIT(1) DEFAULT 0,  constraint id_key PRIMARY KEY(Id));")

i=0
while i<numberOfZones:
    print("\nCreating Zone "+str(i))
    mycursor.execute("INSERT INTO Zone (Name) VALUES ('Zone "+str(i)+"')")
    i+=1

piDb.commit()
mycursor.close()
piDb.close()

print("Entering loop...")

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

    print("Fetching results...")
    print(myresult)
          
    for i in myresult:
        #print(i)
        print(str(i))
        # if the state is ON, trun on the GPIO for that Zone
        if i[2] == 1:
            print("turning on GPIO "+str(i[6])+" on Zone Id "+ str(i[0]))
            #gpio.on()
        else:
            print("turning off GPIO "+str(i[6])+" on Zone Id "+ str(i[0]))
            #gpio.off()

    mycursor.close()
    piDb.close()
    
    time.sleep(2)

