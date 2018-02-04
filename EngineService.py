import time
import json
import threading
from EngineManager import Engine



class EngineService:

    def __init__(self):
        self.engobj = Engine()
        self.status = False


    def EngineRestart(self):
        self.status = True
        threading.Thread(target = self.Run).start()
        return json.dumps({'message':'Engine Restarted'}, default=lambda o: o.__dict__,sort_keys=True, indent=4)

   
    def Run(self):
        #print (self.status)
        while self.status:
            try:
                self.engobj.RefreshSubscriptionList()
                self.engobj.SynchronizeEvents()
                
            except Exception as e:
                # log file
                self.status = False
                print (str(e))


        self.status = False


    def GetStatus(self):
        if self.status:
            ret = {'message':'Engine Running'}
        else:
            ret = {'message':'Engine Stopped'}
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)


    def EngineStop(self):
        self.status = False
        return json.dumps({'message':'Engine Stopped'}, default=lambda o: o.__dict__,sort_keys=True, indent=4)

 
