from Utility import Utility
import uuid


class SubscibeField:

    error = []
        
    def CreateSubscribeFieldList(self,indice,subscribeFieldlist):

        error = SubscibeField.check(indice,subscribeFieldlist)
        
        if len(error) == 0:
            self.id =str(uuid.uuid4()).upper()
            self.subscribeFieldList = subscribeFieldlist
        return error

    
    @staticmethod
    def check(indice,subscribeFieldlist):
        
        utility = Utility()
        error = []
        
        if utility.CheckStockCode(indice) is False:
            error.append('Wrong index code')

        else:
            if not utility.CheckAttrNamesOfStock(indice,subscribeFieldlist):
                error.append('field name doesnt exist')

        return error
            


class Condition:

    error = []

    def CreateCondition(self,indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage):
        #print ("inside metadata")
        error = Condition.check(indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage)
        #print ("inside metadata error "+str(error))
        if len(error) == 0:

            self.id = str(uuid.uuid4()).upper()
            self.indice = indice
            self.attrnames = attrnames
            self.attrtypes = attrtypes
            self.attrvalues = [str(attrvalue) for attrvalue in attrvalues]
            self.conjunctions = conjunctions
            self.operations = operations
            self.triggermessage = triggermessage

        return error


    @staticmethod
    def check(indice,attrnames,attrtypes,attrvalues,conjunctions,operations,triggermessage):
    
        utility = Utility()
        error = []

        if not set(conjunctions).issubset(set(['AND','OR'])):
            error.append('Conjuntion must be AND/OR')
        

        if utility.CheckStockCode(indice) is False:
            error.append('Wrong index code')

        else:
            if not set(attrtypes).issubset(set(['string','date','number'])):
                error.append('Type not in string/date/number')

            else:
                if utility.CheckAttrNamesOfStock(indice,attrnames):

                    if utility.CheckAttrTypesOfStock(indice,attrnames,attrtypes,attrvalues):
    
                        #operation check
                        if  set(operations).issubset(set(['equals','greater','lesser'])) and all(utility.CheckOperation(attrtypes[i],operations[i]) for i in range(len(attrtypes))):

                            if not triggermessage:

                                error.append('Message cannot be empty')
                        
                        else:
                            error.append('Operation not in equals/greater/lesser.Note :String can have equals operation only')                     

                    else:
                        error.append('Attribute type mismatch or value is null')

                else:
                    error.append('Attribute name doesnot exist')


        return error

            
    
