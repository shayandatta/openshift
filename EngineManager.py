import threading,queue
#import logging
import ctypes
from Utility import Utility
from ManagerLib import ManagerLib
from dateutil.parser import parse
from FirebaseUtility import FirebaseUtility
import datetime


class Engine:

    utility = Utility()

    def __init__(self):
        self.manager = ManagerLib()   
        self.subscriptionList = self.manager.userList
        #logging.basicConfig(filename='error.log',level=logging.ERROR,
                            #format='%(asctime)s :: %(message)s')


    def RefreshSubscriptionList(self):
        self.subscriptionList = self.manager.userList


    def SynchronizeEvents(self):
        th = []
        for user in self.subscriptionList:
            Engine.ProcessUser(user)



    @staticmethod
    def ProcessUser(user):
        th = []
        q = queue.Queue()
        count = 0
        for conditionobj in user.conditionList:
            subscriptionobj = list(subscribedFlds for subscribedFlds in user.subscribeFieldList if subscribedFlds.id == conditionobj.id)
            if subscriptionobj:
                t = threading.Thread(target=Engine.ProcessCondition,args = (user,conditionobj,subscriptionobj[0],q))
                t.start()
                th.append(t)

        for x in th: x.join(20)
        for x in th:
            if x.isAlive():
                #logging.error('ProcessUser :: Thread {} alive'.format(str(x.ident)))
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(x.ident), exc)
                if res == 0:
                    #logging.error('ProcessUser :: Thread {} doesnt exist'.format(str(x.ident)))
                    raise ValueError("nonexistent thread id")
                elif res > 1:
                    #logging.error('ProcessUser :: Thread {} cant be killed'.format(str(x.ident)))
                    # """if it returns a number greater than one, you're in trouble,
                    # and you should call it again with exc=NULL to revert the effect"""
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(x.ident, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")
                else:
                    #logging.error('ProcessUser :: Thread {} has been killed'.format(str(x.ident)))
                    pass
        for i in range(len(th)):
            isValidCondtion,retUser,retCondition,retSubscribeFldobj,fldObj = q.get()
            if isValidCondtion:
                processedFields = Engine.ProcessRegisteredFields(fldObj,retSubscribeFldobj.fieldlist)
                dth = threading.Thread(target=Engine.RegisterEvent,args = (retUser,retCondition.indice,processedFields,retSubscribeFldobj.triggermessage))
                dth.start()


    @staticmethod
    def ProcessCondition(user,condition,subscribeFldobj,q):
        try:
            output = []
            fldObj = []
            if Engine.utility.CheckStockCode(condition.indice):
               fldObj = Engine.utility.GetAllDetailsOfStock(condition.indice)
               if set(condition.attrnames).issubset(set(fldObj.keys())):
                   for i in range(len(condition.attrnames)):
                       currentvalue = fldObj[condition.attrnames[i]]
                       if currentvalue is not None:
                           if condition.attrtypes[i] == 'number':
                               attrvalue = float(condition.attrvalues[i])
                               currentvalue = float(currentvalue)
                           elif condition.attrtypes[i] == 'date':
                               attrvalue = parse(condition.attrvalues[i])
                               currentvalue = parse(currentvalue)
                           else:
                               attrvalue = condition.attrvalues[i]

                               
                           if ((condition.operations[i] == 'equals' and currentvalue == attrvalue) or
                              (condition.operations[i] == 'greater' and currentvalue > attrvalue) or
                              (condition.operations[i] == 'lesser' and currentvalue < attrvalue)):
                               output.append(True)
                           else:
                               output.append(False)

            retVal = output[0]
            outputcount = 1
            for conjunction in condition.conjunctions:
                if conjunction == 'AND':
                   retVal = retVal and output[outputcount]
                elif conjunction == 'OR':
                    retVal = retVal or output[outputcount]
                outputcount+=1
            q.put((retVal,user,condition,subscribeFldobj,fldObj))
        except Exception as e:
            #logging.error('ProcessCondition :: Error occured. Message : {}'.format(str(e.getMessage())))
            pass
        finally:
            return q   



    @staticmethod
    def RegisterEvent(userDtl,indice,fldDict,triggermessage):
        try:
            firebaseobj = FirebaseUtility(userDtl.firebaseauth)
            #firebaseobj = FirebaseUtility("https://test-project-f8976.firebaseio.com/")
            fldDict.update({'triggermessage':triggermessage})
            return firebaseobj.insertdata(userDtl.userid,indice,fldDict)

        except:
            #logging.error('RegisterEvent :: Error occured. Message : {}'.format(str(e.getMessage())))
            pass
        


    @staticmethod
    def ProcessRegisteredFields(fldObj,subscribeFlds):
        processedFields = {subscribeFld:fldObj[subscribeFld] for subscribeFld in subscribeFlds}
        return processedFields
        
