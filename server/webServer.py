#
# PI Web Server
# made 2018 by Pat McGee
# This takes in http requests, and responds with a json string to the client the switch states
# Works in conjunction with the client file
#

import json
from pathlib import Path
import pickle
from flask import Flask
from flask import request
from flask_cors import CORS
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
#from multiprocessing import Process, Value
#from celery import task
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


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

zones = []
app = Flask(__name__)


    
# a Zone is a virtual representation of a switch
# It contains the current state, name, description, and schedule
class Zone:
    def __init__(self,obj):
        print("Creating Zone Object")
        
        self.id = obj[0]
        self.name = obj[1]
        self.state = obj[2]
        self.force = obj[3]
        self.startTime = str(obj[4])
        self.endTime = str(obj[5])
        self.gpio = obj[6] 
        self.days = obj[7]
        
        print("Created " + self.name + ", State = " + str(self.state))
        print(type(obj[7]))

              
              

class CustomEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, Zone):
            return { "name" : obj.name, "id" : obj.id, "startTime" : obj.startTime, "endTime" : obj.endTime, "state" : obj.state, "days" : obj.days, "gpio" : obj.gpio }
        
        return json.JSONEncoder.default(self,obj)


# SaveZone takes in the id of the zone and saves the
# Zone of that ID to file
def NewZone():
    print("New Zone")
    sql = "insert into Zone(0,0,0,0,0)"
    mycursor.execute(sql)

    RefreshZones()
    

def UpdateZone(id,name,days,startTime,endTime):
    print("Update Zone")
    sql = "UPDATE Zone SET Name='"+name+"', Gpio='"+str(0)+"', Days='"+str(days)+"', StartTime='"+startTime+"', EndTime ='"+endTime+"' WHERE Id="+str(id)
    print(sql)
    mycursor.execute(sql)

# GetZones clears the global zones
def GetZones():
    zones.clear()
    
    print("Called GetZones")
    sql = "SELECT Id,Name,State,ForceOn,StartTime,EndTime,Gpio,Days FROM Zone"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    zoneCounter = 0
    
    for i in myresult:
        print(i)
        zones.insert(zoneCounter,Zone(i))
        print(zones[zoneCounter])
        zoneCounter = zoneCounter + 1

    return zones



# Entry point for main program
print("Started program...")



#obj[2].name = "Some other name"
#SaveZone(2);

@app.route("/", methods=['GET', 'POST'])
@crossdomain(origin='*')


def webServer():

    #zoneList = obj
    
    cmd = request.form.get('cmd')
    
    print("Received Request...")
    print(str(request.form))
    
    if cmd == 'update':
        print("Updating...")
        
        name = request.form.get('name')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        days = request.form.get('days')
        id = request.form.get('id')
        
        if id == "" or name == "":
            return "{ \"status\" : \"fail\", \"msg\" : \"Not all information received to update\"}"
        
        else:
                        
            UpdateZone(id,name,days,startTime,endTime)
            
            return "{ \"status\" : \"success\", \"msg\" : \"Updated Zone\"}"
        
    else:
        print("Returning PI Info")
        deviceDesc = "My PI"
        deviceIp = "192.168.1.100"
        deviceName = "192.168.1.100"
        deviceTime = "192.168.1.100"
        #resp = flask.Response(json.dumps(obj,cls=CustomEncoder))
        #resp.headers['Access-Control-Allow-Origin'] = '*'
        # Creating a JSON string from the device properties and the Zone array properties
        jsonStr = "{ \"deviceName\" : \""+deviceName+"\", \"deviceDesc\" : \""+deviceDesc+"\", \"deviceIp\" : \""+deviceIp+"\", \"deviceTime\" : \""+deviceTime+"\", \"Zones\" : "
        obj = GetZones()
        jsonStr += json.dumps(obj,cls=CustomEncoder)
        jsonStr += "}"
        return jsonStr
    


#@task
#while True:
#    print("loop running")
#    time.sleep(1)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, use_reloader=False)
  
    

