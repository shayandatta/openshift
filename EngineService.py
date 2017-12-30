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



'''  
cnt=0
while(True):
    engobj.RefreshSubscriptionList()
    engobj.SynchronizeEvents()
    if cnt%2==0:
        manager = ManagerLib()
        id = manager.AddUser("SHAYAN",'https://test-project-f8976.firebaseio.com/','')
        print(manager.GetUserDetails("SHAYAN",id))
        print(manager.AddConditionFieldList("SHAYAN",id,'ICICIBANK',['basePrice','totalTradedVolume','cm_adj_low_dt'],['number','number','date'],['304.0','6602231.0','28-DEC-16'],['OR','AND'],['greater','equals','lesser'],'hello'))
        print(manager.AddConditionFieldList("SHAYAN",id,'BAJAJ-AUTO',['lastPrice','bcEndDate'],['number','date'],['3202.2','22-JUL-17'],['AND'],['lesser','lesser'],'Hit'))
        print(manager.AddSubscibeFieldList("SHAYAN",id,'ICICIBANK',['basePrice','bcEndDate','css_status_desc']))
        print(manager.AddSubscibeFieldList("SHAYAN",id,'BAJAJ-AUTO',['securityVar','extremeLossMargin','lastPrice']))

    print("done")

'''
 
