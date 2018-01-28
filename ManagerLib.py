from nsetools import Nse
from pprint import pprint
from UserDetails import UserDetails
import json

class ManagerLib(object):

    _instance = None
    def __new__(self):
        if not self._instance:
            self._instance = super(ManagerLib,self).__new__(self)
            self.nse = Nse()
            self.userList = []
        return self._instance
    
    #def __init__(self):
        #self.nse = Nse()
        #self.userList = []


    def GetLiveData(self,key,id,stock):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = self.nse.get_quote(str(stock))
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def CheckStockCode(self,key,id,stock):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = self.nse.is_valid_code(str(stock))
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def GetListOfStocks(self,key,id):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = self.nse.get_stock_codes()
        return json.dumps(ret,ensure_ascii=False, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def AddUser(self,key,firebase_url,firebase_pass):
        firebaseauth={'FIREBASE_URL':firebase_url,'FIREBASE_PWD':firebase_pass}
        userdetailobj = UserDetails(key,firebaseauth)
        self.userList.append(userdetailobj)
        ret = {'message':'User added successfully.','id':userdetailobj.userid}
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)


    def GetUsers(self):
        return json.dumps(self.userList, default=lambda o: o.__dict__,sort_keys=True, indent=4)


    def GetUser(self,key,id):
        userobj = list(x for x in self.userList if x.userid == id)
        if userobj:
            if userobj[0].userkey == key:
                return userobj[0]
            else:
                return {'error':'Id-key mismatch'}
        else:
            return {'error':'Id not found'}

        

    def GetUserDetails(self,key,id):
        ret = self.GetUser(key,id)
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    

    def AddConditionFieldList(self,key,id,indice,attrnames,attrtypes,attrvalues,conjunctions,operations):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.SetConditionList(indice,attrnames,attrtypes,attrvalues,conjunctions,operations)
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    
            
    def AddSubscibeFieldList(self,key,id,conditionid,subscribeFieldlist,triggermessage):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            conditionobjlist = list(condition for condition in ret.conditionList if condition.id == conditionid)
            if conditionobjlist:
                if not any(subscription for subscription in ret.subscribeFieldList if subscription.id == conditionid):
                    ret=ret.SetSubscibeFieldList(conditionobjlist[0].id,conditionobjlist[0].indice,subscribeFieldlist,triggermessage)

                else:
                    ret = {'error':'Subscription for the condition already present.Remove and then try.'}
            else:
                ret = {'error':'Condition id not found.'}
        
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    


    def RemoveFromConditionList(self,key,id,conditionid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.RemoveFromConditionList(conditionid)
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)   


    def RemoveFromSubscriptionList(self,key,id,subscriptionid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.RemoveFromSubscriptionList(subscriptionid)
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def GetConditionList(self,key,userid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.conditionList
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)


    def GetSubscriptionList(self,key,userid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.subscribeFieldList
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)



    def RemoveUser(self,key,id):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            self.userList.remove(ret)
            ret = {'message':'User removed successfully'}
            
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    

    def GetADByStockCode(self,stocklist):
        AllAD = self.nse.get_advances_declines()
        ret = list(x for x in AllAD if x['indice'] in stocklist)
        return ret

        
    def GetAllADStockCode(self):
        AllAD = self.nse.get_advances_declines()
        return list(x['indice'] for x in AllAD)

    def CheckAttrNameOfStock(self,stock,attrname):
        ret = GetAllDetailsOfStock(self,stock)
        if attrname in ret:
            return True
        else:
            return False

    def CheckAttrTypeOfStock(self,stock,attrname,attrtype):
        ret = GetAllDetailsOfStock(self,stock)            
        if attrtype == 'date':
            try:
                parse(ret[attrname])
                return True
            except:
                return False

        elif attrtype == 'number':
            try:
                float(ret[attrname])
                return True
            except:
                return False
        else:
            return True


    def CheckOperation(self,attrtype,operation):
        if attrtype == 'string' and operation != 'equals':
           return False
        else:
           return True
       

    def SetStockList(self,stocklist):
        self.stocklist = stocklist

    def GetStockList(self):
        return self.stocklist

    def AddStock(self,stock):
        self.stocklist.append(stock)

    def RemoveStock(self,stock):
        if len(self.stocklist) > 0 and stock in self.stocklist:
            self.stocklist.remove(stock)        
