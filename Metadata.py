from Utility import Utility
import uuid


class SubscibeField:

    error = []
        
    def CreateSubscribeFieldList(self,conditionid,indice,subscribeFieldlist,triggermessage):
        error = SubscibeField.check(indice,subscribeFieldlist,triggermessage)
        if len(error) == 0:
            self.id =conditionid
            self.fieldlist = subscribeFieldlist
            self.triggermessage = triggermessage
        return error

    
    @staticmethod
    def check(indice,subscribeFieldlist,triggermessage):
        
        utility = Utility()
        error = []

        if not triggermessage:
            error.append({'error':'Message cannot be empty'})
      
        if utility.CheckStockCode(indice) is False:
            error.append({'error':'Wrong index code'})

        else:
            if not utility.CheckAttrNamesOfStock(indice,subscribeFieldlist):
                error.append({'error':'Field name doesnot exist'})

        return error
            


class Condition:

    error = []

    def CreateCondition(self,indice,attrnames,attrtypes,attrvalues,conjunctions,operations):
        error = Condition.check(indice,attrnames,attrtypes,attrvalues,conjunctions,operations)
        if len(error) == 0:

            self.id = str(uuid.uuid4()).upper()
            self.indice = indice
            self.attrnames = attrnames
            self.attrtypes = attrtypes
            self.attrvalues = [str(attrvalue) for attrvalue in attrvalues]
            self.conjunctions = conjunctions
            self.operations = operations

        return error


    @staticmethod
    def check(indice,attrnames,attrtypes,attrvalues,conjunctions,operations):
    
        utility = Utility()
        error = []
        
        if not set(conjunctions).issubset(set(['AND','OR'])):
            error.append({'error':'Conjuntion must be AND/OR'})
        
        if utility.CheckStockCode(indice) is False:
            error.append({'error':'Wrong index code'})

        else:
            if not set(attrtypes).issubset(set(['string','date','number'])):
                error.append({'error':'Type not in string/date/number'})
                
            else:
                if utility.CheckAttrNamesOfStock(indice,attrnames):

                    if utility.CheckAttrTypesOfStock(indice,attrnames,attrtypes,attrvalues):
    
                        #operation check
                        if  set(operations).issubset(set(['equals','greater','lesser'])) and all(utility.CheckOperation(attrtypes[i],operations[i]) for i in range(len(attrtypes))):
                            pass
 
                        else:
                            error.append({'error':'Operation not in equals/greater/lesser.Note :String can have equals operation only'})                     

                    else:
                        error.append({'error':'Attribute type mismatch or value is null'})

                else:
                    error.append({'error':'Attribute name doesnot exist'})


        return error

            
    
