import threading,queue
#import logging
import ctypes
from Utility import Utility
from ManagerLib import ManagerLib
from dateutil.parser import parse
from FirebaseUtility import FirebaseUtility


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
            t = threading.Thread(target=Engine.ProcessUser,args = (user,))
            t.start()
            th.append(t)

        for x in th: x.join(60)
        for x in th:
            if x.isAlive():
                #logging.error('SynchronizeEvents :: Thread {} alive'.format(str(x.ident)))
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(x.ident), exc)
                if res == 0:
                    #logging.error('SynchronizeEvents :: Thread {} doesnt exist'.format(str(x.ident)))
                    raise ValueError("nonexistent thread id")
                elif res > 1:
                    logging.error('SynchronizeEvents :: Thread {} cant be killed'.format(str(x.ident)))
                    # """if it returns a number greater than one, you're in trouble,
                    # and you should call it again with exc=NULL to revert the effect"""
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(x.ident, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")
                else:
                    #logging.error('SynchronizeEvents :: Thread {} has been killed'.format(str(x.ident)))
                    pass


    @staticmethod
    def ProcessUser(user):
        th = []
        q = queue.Queue()
        count = 0
        if len(user.conditionList) == len(user.subscribeFieldList):
            for condition in user.conditionList:
                    t = threading.Thread(target=Engine.ProcessCondition,args = (user,condition,user.subscribeFieldList[count],q))
                    count+=1
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
            isValidCondtion,retUser,retCondition,retSubscibeFields,fldObj = q.get()
            if isValidCondtion:
                processedFields = Engine.ProcessRegisteredFields(fldObj,retSubscibeFields)
                dth = threading.Thread(target=Engine.RegisterEvent,args = (retUser,retCondition.indice,processedFields,retCondition.triggermessage))
                dth.start()


    @staticmethod
    def ProcessCondition(user,condition,subscribeFlds,q):
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
            #print output
            for conjunction in condition.conjunctions:
                if conjunction == 'AND':
                   retVal = retVal and output[outputcount]
                elif conjunction == 'OR':
                    retVal = retVal or output[outputcount]
                outputcount+=1
            q.put((retVal,user,condition,subscribeFlds.subscribeFieldList,fldObj))
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
        
