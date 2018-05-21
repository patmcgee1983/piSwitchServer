import json
from pathlib import Path
import pickle

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
    
# Entry point for main program
print("Started program...")

numberOfSwitches = 5
obj = []

for i in range(0,numberOfSwitches):

    zonePath = Path("zone"+str(i))
    if zonePath.is_file():
        print(str(zonePath) + " is a file")
        file = open(zonePath,"rb")
        obj.append(pickle.load(file))
        file.close()
    else:
        print(str(zonePath) + " is a not a file")
        file = open(zonePath,"wb")
        obj.append(Zone(i))
        print(obj[i].name)
        pickle.dump(obj[i],file)
        file.close()

print(json.dumps(obj,cls=CustomEncoder))
