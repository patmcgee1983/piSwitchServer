#
# PI Web Server
# made 2018 by Pat McGee
# This takes in http requests, and responds with a json string to the client the switch states
# Works in conjuntion with the client file
#

import json
from pathlib import Path
import pickle
from flask import Flask
from flask import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

    
# a Zone is a virtual representation of a switch
# It contains the current state, name, description, and schedule
class Zone:
    def __init__(self,id):
        self.id = id
        self.name = "Zone"+str(id)
        self.state = 0
        self.startTime = ""
        self.endTime = ""
        self.days = [0,0,0,0,0,0,0]

        print("Created " + self.name)

class CustomEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, Zone):
            return { "name" : obj.name, "id" : obj.id, "startTime" : obj.startTime, "endTime" : obj.endTime, "state" : obj.state, "days" : obj.days }
        
        return json.JSONEncoder.default(self,obj)


# SaveZone takes in the id of the zone and saves the
# Zone of that ID to file
def SaveZone(i):
    zonePath = Path("zone"+str(i))
    file = open(str(zonePath),"wb")
    obj.append(Zone(i))
    print(obj[i].name)
    pickle.dump(obj[i],file)
    file.close()


# Entry point for main program
print("Started program...")

numberOfSwitches = 5
obj = []

for i in range(0,numberOfSwitches):

    zonePath = Path("zone"+str(i))
    if zonePath.is_file():
        print(str(zonePath) + " is a file")
        file = open(str(zonePath),"rb")
        obj.append(pickle.load(file))
        file.close()
    else:
        print(str(zonePath) + " is a not a file")
        file = open(str(zonePath),"wb")
        obj.append(Zone(i))
        print(obj[i].name)
        pickle.dump(obj[i],file)
        file.close()

#obj[2].name = "Some other name"
#SaveZone(2);

@app.route("/")

def webServer():

    #zoneList = obj
    

    switch  = request.args.get('switch', None)
    position  = request.args.get('position', None)

    return json.dumps(obj,cls=CustomEncoder)

if __name__ == "__main__":

    app.run(host='0.0.0.0')
    

