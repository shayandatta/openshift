#!/usr/bin/env python
import os

app = Flask(__name__)


@app.route("/")
def index():
    return 'Hello World'


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()
    app.run(
        debug=True
    )
