from nsetools import Nse
from dateutil.parser import parse

class Utility:

    def __init__(self):
        self.nse = Nse()

    def CheckStockCode(self,stock):
        return self.nse.is_valid_code(stock)


    def GetAllDetailsOfStock(self,stock):
        return self.nse.get_quote(str(stock))
            

    def GetAllAttrNamesOfStock(self,stock):
        return self.nse.get_quote(stock).keys()
    

    def CheckAttrNamesOfStock(self,stock,attrnames):
        ret = self.GetAllDetailsOfStock(stock)
        if set(attrnames).issubset(set(ret.keys())):
            return True
        else:
            return False

    def CheckAttrTypesOfStock(self,stock,attrnames,attrtypes,attrvalues):
        ret = self.GetAllDetailsOfStock(stock)
        flag = False
        for i in range(len(attrtypes)):
            if str(attrtypes[i]) == 'date':
                try:
                    parse(ret[attrnames[i]])
                    parse(str(attrvalues[i]))
                    flag = True
                except:
                    flag = False
                    break

            elif str(attrtypes[i]) == 'number':
                try:
                    float(ret[attrnames[i]]) 
                    float(str(attrvalues[i]))
                    flag = True
                except:
                    flag = False
                    break
            else:
                flag = True

        return flag

    def CheckOperation(self,attrtype,operation):
        
        if attrtype == 'string' and operation != 'equals':
           return False
        else:
           return True

