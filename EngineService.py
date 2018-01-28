import time
import threading
from EngineManager import Engine



class EngineService:

    def __init__(self):
        self.engobj = Engine()
        self.status = False


    def EngineRestart(self):
        self.status = True
        threading.Thread(target = self.Run).start()

   
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
           return "Running"
        else:
            return "Stopped"


    def EngineStop(self):
        self.status = False

 
