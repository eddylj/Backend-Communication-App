import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import message
import user
import other
from data import data

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register", methods=['POST'])
def register():
    data = request.get_json('data')

    return dumps(
        auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last'])
    )

@APP.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json('data')

    return dumps(
        auth.auth_login(data['email'], data['password'])
    )

@APP.route("/auth/logout", methods=['POST'])
def logout():
    data = request.get_json('data')

    return dumps(
        auth.auth_logout(data['token'])
    )




if __name__ == "__main__":
    APP.run(port=9557) # Do not edit this port
