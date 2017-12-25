from flask import Flask
from nsetools import Nse
import json

app = Flask(__name__)
nse = Nse()


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/show/<stock>', methods = ['GET'])
def get_key(stock):
    print (type(stock))
    st_details = nse.get_quote(str(stock))
    return json.dumps(st_details, default=lambda o: o.__dict__,sort_keys=True, indent=4)

if __name__ == '__main__':
    app.run()
