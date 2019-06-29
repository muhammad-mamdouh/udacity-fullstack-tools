#!/usr/bin/env python3
#


from flask import Flask
app = Flask(__name__)


# @app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World!"


if __name__ == '__main__':
    # By making this True, the server will reload itself each time it
    # notices a code change
    app.debug = True

    # host = '0.0.0.0' This tells the web server to listen on all public
    # Ip addresses
    app.run(host='0.0.0.0', port=8000)
