from Metadata import Condition,SubscibeField
import json
import uuid

class UserDetails:

    def __init__(self,key,firebaseauth):
        self.userkey = key
        self.firebaseauth = firebaseauth 
        self.userid = str(uuid.uuid4()).upper()
        self.conditionList=[]
        self.subscribeFieldList=[]


    def SetConditionList(self,indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage):
        conditionobj = Condition()
        error = conditionobj.CreateCondition(indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage)
        if len(error) > 0 :
            return error

        else:
            self.conditionList.append(conditionobj)
            return conditionobj.id

    def RemoveFromConditionList(self,id):
        conditionobj = list(x for x in self.conditionList if x.id==id)
        if conditionobj:
            self.conditionList.remove(conditionobj[0])
            return 'Removed successfully'
        else:
            return 'Id not found'


    def GetConditionList(self):
        return json.dumps(self.conditionList, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def SetSubscibeFieldList(self,indice,subscribeFieldlist):
        subscibefieldobj = SubscibeField()
        #print ('inside userdetails')
        error = subscibefieldobj.CreateSubscribeFieldList(indice,subscribeFieldlist)
     
        if len(error) > 0 :
            return error
        else:
            self.subscribeFieldList.append(subscibefieldobj)
            return subscibefieldobj.id


    def RemoveFromSubscriptionList(self,id):
        subscribeobj = list(x for x in self.subscribeFieldList if x.id==id)
        if subscribeobj:
            self.subscribeFieldList.remove(subscribeobj[0])
            return 'Removed successfully'
        else:
            return 'Id not found'


    def GetSubscibeFieldList(self):
        return json.dumps(self.subscribeFieldList, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        

        

    
    

