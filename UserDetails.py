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


    def SetConditionList(self,indice,attrnames,attrtypes,attrvalues,conjunctions,operations):
        conditionobj = Condition()
        error = conditionobj.CreateCondition(indice,attrnames,attrtypes,attrvalues,conjunctions,operations)
        if len(error) > 0 :
            return error

        else:
            self.conditionList.append(conditionobj)
            return {'message':'Condition added successfully.','id':conditionobj.id}

    def RemoveFromConditionList(self,id):
        conditionobj = list(x for x in self.conditionList if x.id==id)
        subscribeobj = list(x for x in self.subscribeFieldList if x.id==id)
        if subscribeobj:
            self.subscribeFieldList.remove(subscribeobj[0])
            
        if conditionobj:
            self.conditionList.remove(conditionobj[0])
            return {'message':'Removed successfully'}
        else:
            return {'message':'Id not found'}


    def SetSubscibeFieldList(self,conditionid,indice,subscribeFieldlist,triggermessage):
        subscibefieldobj = SubscibeField()
        error = subscibefieldobj.CreateSubscribeFieldList(conditionid,indice,subscribeFieldlist,triggermessage)
        if len(error) > 0 :
            return error
        else:
            self.subscribeFieldList.append(subscibefieldobj)
            return {'message':'Fields subscribbed successfully.'}


    def RemoveFromSubscriptionList(self,id):
        subscribeobj = list(x for x in self.subscribeFieldList if x.id==id)
        if subscribeobj:
            self.subscribeFieldList.remove(subscribeobj[0])
            return {'message':'Removed successfully'}
        else:
            return {'message':'Id not found'}

    

    
    

