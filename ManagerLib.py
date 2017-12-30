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
        try:
            ret = self.GetUser(key,id)
            if isinstance(ret, UserDetails):
                ret = self.nse.get_stock_codes()
            return json.dumps(ret,ensure_ascii=False, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        except Exception as e:
            print (str(e))



    def AddUser(self,key,firebase_url,firebase_pass):
        firebaseauth={'FIREBASE_URL':firebase_url,'FIREBASE_PWD':firebase_pass}
        userdetailobj = UserDetails(key,firebaseauth)
        self.userList.append(userdetailobj)
        return userdetailobj.userid


    def GetUsers(self):
        return json.dumps(self.userList, default=lambda o: o.__dict__,sort_keys=True, indent=4)


    def GetUser(self,key,id):
        userobj = list(x for x in self.userList if x.userid == id)
        if userobj:
            if userobj[0].userkey == key:
                return userobj[0]
            else:
                return "Id-key mismatch"
        else:
            return "Id not found"

        

    def GetUserDetails(self,key,id):
        ret = self.GetUser(key,id)
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    

    def AddConditionFieldList(self,key,id,indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret=ret.SetConditionList(indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage)
        
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    
            
    def AddSubscibeFieldList(self,key,id,stockname,subscribeFieldlist):
        #print(subscribeFieldlist)
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret=ret.SetSubscibeFieldList(stockname,subscribeFieldlist)
        
        return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    


    def RemoveFromConditionList(self,key,id,conditionid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.RemoveFromConditionList(conditionid)
            return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)   
        else:
            return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)   


    def RemoveFromSubscriptionList(self,key,id,subscriptionid):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            ret = ret.RemoveFromSubscriptionList(subscriptionid)
            return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)   
        else:
            return json.dumps(ret, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        return get_index_quote(stock)



    def RemoveUser(self,key,id):
        ret = self.GetUser(key,id)
        if isinstance(ret, UserDetails):
            self.userList.remove(ret)
            return "removed successfully"
        else:
            return ret

    

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

    def GetConditionList(self):
        return json.dumps(self.conditionList, default=lambda o: o.__dict__,sort_keys=True, indent=4)


        
#print(ManagerLib().GetAllDetailsOfStock('ICICIBANK'))
#CreateCondition(indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage):
#manager = ManagerLib()
#print(manager.userDetails.SetConditionList('ICICIBANK',['buyPrice1'],['number'],['256'],['AND'],['greater'],'hello'))
#print(manager.userDetails.GetConditionList())
#print (manager.userDetails.SetSubscibeFieldList('ICICIBANK',['buyPrice1']))
#print (manager.userDetails.GetSubscibeFieldList())
#print(manager.RemoveFromConditionList('45'))
#print (manager.GetUserDetails(5))
#id = manager.AddUser("SHAYAN")
#print(manager.GetUserDetails("SHAYAN",id))
#print(manager.AddConditionFieldList("SHAYAN",id,'ICICIBANK',['basePrice'],['number'],['256'],['AND'],['greater'],'hello'))
#print(manager.AddSubscibeFieldList("SHAYAN",id,'ICICIBANK',['basePrice']))
#print(manager.GetUserDetails("SHAYAN",id))
