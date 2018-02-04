import json
from flask import Flask,request
from ManagerLib import ManagerLib
from EngineService import EngineService
from flask import jsonify

app = Flask(__name__)
manager = ManagerLib()
engine = EngineService()


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route('/nimbus/v1/stocks/<key>', methods = ['GET'])
def getListOfStocks(key):
    userid = request.headers.get("userid")
    if userid is not None:
        try:
            return manager.GetListOfStocks(key,userid)
        except:
            raise InvalidUsage('Data not found', status_code=504)
    else:
        raise InvalidUsage('Userid is missing', status_code=406)


@app.route('/nimbus/v1/checkstock/<key>/<indice>', methods = ['GET'])
def checkStockCode(key,indice):
    userid = request.headers.get("userid")
    if userid is not None:
        try:
            return manager.CheckStockCode(key,userid,indice)
        except:
            raise InvalidUsage('data not found', status_code=504)
    else:
        raise InvalidUsage('userid is missing', status_code=406)



@app.route('/nimbus/v1/livedata/<key>/<indice>', methods = ['GET'])
def getLiveData(key,indice):
    userid = request.headers.get("userid")
    if userid is not None:
        try:
            return manager.GetLiveData(key,userid,indice)
        except:
            raise InvalidUsage('Data not found', status_code=504)
    else:
        raise InvalidUsage('Userid is missing', status_code=406)



@app.route('/nimbus/v1/user/<key>', methods = ['GET'])
def getUserDetails(key):
    userid = request.headers.get("userid")
    if userid is not None:
        ret = manager.GetUserDetails(str(key),str(userid))
        return ret
    else:
        raise InvalidUsage('Userid missing', status_code=406)


@app.route('/nimbus/v1/users', methods = ['GET'])
def getUsers():
    authkey = request.headers.get("authkey")
    if authkey is not None and authkey=="ADMIN":
        return manager.GetUsers()
    else:
        raise InvalidUsage('Invalid authkey', status_code=401)



@app.route('/nimbus/v1/newuser/<key>', methods = ['POST'])
def addUser(key):

    data = request.data
    if data is not None:
        try:
            dataDict = json.loads(data.decode('utf-8'))
            return manager.AddUser(key,dataDict['FIREBASE_URL'],dataDict['FIREBASE_PWD'])
        except:
            raise InvalidUsage('Data send is not in correct format', status_code=400)
    else:
        raise InvalidUsage('No data found', status_code=406)


@app.route('/nimbus/v1/setcondition/<key>', methods = ['POST'])
def addConditionFieldList(key):
    userid = request.headers.get("userid")
    data = request.data
    if data and userid is not None:
        try:
            dataDict = json.loads(data.decode('utf-8'))
            return manager.AddConditionFieldList(key,userid,dataDict['indice'],dataDict['attrnames'],dataDict['attrtypes'],dataDict['attrvalues'],dataDict['conjunctions'],dataDict['operations'])
        except:
            raise InvalidUsage('Data send is not in correct format', status_code=400)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)



@app.route('/nimbus/v1/setsubscibelist/<key>', methods = ['POST'])
def addSubscibeFieldList(key):
    userid = request.headers.get("userid")
    data = request.data
    if data and userid is not None:
        try:
            dataDict = json.loads(data.decode('utf-8'))
            return manager.AddSubscibeFieldList(key,userid,dataDict['id'],dataDict['fieldlist'],dataDict['triggermessage'])
        except:
            raise InvalidUsage('Data send is not in correct format', status_code=400)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)



@app.route('/nimbus/v1/delcondition/<key>', methods = ['DELETE'])
def delConditionFieldList(key):
    userid = request.headers.get("userid")
    data = request.data
    if data and userid is not None:
        try:
            dataDict = json.loads(data.decode('utf-8'))
            return manager.RemoveFromConditionList(key,userid,dataDict['id'])
        except:
            raise InvalidUsage('Data send is not in correct format', status_code=400)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)



@app.route('/nimbus/v1/delsubscibelist/<key>', methods = ['DELETE'])
def delSubscibeFieldList(key):
    userid = request.headers.get("userid")
    data = request.data
    if data and userid is not None:
        try:
            dataDict = json.loads(data.decode('utf-8'))
            return manager.RemoveFromSubscriptionList(key,userid,dataDict['id'])
        except:
            raise InvalidUsage('Data send is not in correct format', status_code=400)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)



@app.route('/nimbus/v1/deluser/<key>', methods = ['DELETE'])
def delUser(key):
    userid = request.headers.get("userid")
    if userid is not None:
        return manager.RemoveUser(key,userid)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)


@app.route('/nimbus/v1/getconditionlist/<key>', methods = ['GET'])
def getConditionList(key):
    userid = request.headers.get("userid")
    if userid is not None:
        return manager.GetConditionList(key,userid)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)


@app.route('/nimbus/v1/getsubscriptionlist/<key>', methods = ['GET'])
def getSubscriptionList(key):
    userid = request.headers.get("userid")
    if userid is not None:
        return manager.GetSubscriptionList(key,userid)
    else:
        raise InvalidUsage('Userid or data is missing', status_code=406)

    

###### Engine API's ######
    
@app.route('/nimbus/v1/enginestatus', methods = ['GET'])
def engineStatus():
    authkey = request.headers.get("authkey")
    if authkey is not None and authkey=="ADMIN":
        return engine.GetStatus()
    else:
        raise InvalidUsage('invalid authkey', status_code=401)


@app.route('/nimbus/v1/enginerestart', methods = ['GET'])
def engineRestart():
    authkey = request.headers.get("authkey")
    if authkey is not None and authkey=="ADMIN":
        return engine.EngineRestart()
    else:
        raise InvalidUsage('invalid authkey', status_code=401)


@app.route('/nimbus/v1/enginestop', methods = ['GET'])
def engineStop():
    authkey = request.headers.get("authkey")
    if authkey is not None and authkey=="ADMIN":
        return engine.EngineStop()
    else:
        raise InvalidUsage('invalid authkey', status_code=401)

      

if __name__=='__main__':
    app.run()
