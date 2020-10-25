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


# AUTH FUNCTIONS
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


# CHANNEL FUNCTIONS
@APP.route("/channel/invite", methods=['POST'])
def invite():
    data = request.get_json('data')

    return dumps(
        channel.channel_invite(data['token'], data['channel_id'], data['u_id'])
    )

@APP.route("/channel/details", methods=['GET'])
def details():
    # token = request.args.get('token')
    # channel_id = request.args.get('channel_id')

    return dumps(
        channel.channel_details(request.args.get('token'), int(request.args.get('channel_id')))
    )

@APP.route("/channel/messages", methods=['GET'])
def messages():
    # token = request.args.get('token')
    # channel_id = request.args.get('channel_id')
    # start = request.args.get('start')

    return dumps(
        channel.channel_messages(request.args.get('token'), request.args.get('channel_id'),request.args.get('start'))
    )


@APP.route("/channel/leave", methods=['POST'])
def leave():
    data = request.get_json('data')

    return dumps(
        channel.channel_leave(data['token'], data['channel_id'])
    )

@APP.route("/channel/join", methods=['POST'])
def join():
    data = request.get_json('data')

    return dumps(
        channel.channel_leave(data['token'], data['channel_id'])
    )

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    data = request.get_json('data')

    return dumps(
        channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    )

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    data = request.get_json('data')

    return dumps(
        channel.channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    )


# CHANNELS FUNCTIONS
@APP.route("/channels/list", methods=['GET'])
def clist():
    # token = request.args.get('token')

    return dumps(
        channels.channels_list(request.args.get('token'))
    )

@APP.route("/channels/listall", methods=['GET'])
def listall():
    # token = request.args.get('token')

    return dumps(
        channels.channels_listall(request.args.get('token'))
    )

@APP.route("/channels/create", methods=['POST'])
def create():
    data = request.get_json('data')

    return dumps(
        channels.channels_create(data['token'], data['name'], data['is_public'])
    )


# MESSAGES FUNCTIONS


# USER FUNCTIONS
@APP.route("/user/profile", methods=['GET'])
def profile():
    # token = request.args.get('token')
    # u_id = request.args.get('u_id')

    return dumps(
        user.user_profile(request.args.get('token'), int(request.args.get('u_id')))
    )

@APP.route("/user/profile/setname", methods=['PUT'])
def setname():
    data = request.get_json('data')

    return dumps(
        user.user_profile_setname(data['token'], data['name_first'], data['name_last'])
    )

@APP.route("/user/profile/setemail", methods=['PUT'])
def setemail():
    data = request.get_json('data')

    return dumps(
        user.user_profile_setemail(data['token'], data['email'])
    )

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle():
    data = request.get_json('data')

    return dumps(
        user.user_profile_sethandle(data['token'], data['handle_str'])
    )

@APP.route("/users/all", methods=['GET'])
def usersall():
    # token = request.args.get('token')

    return dumps(
        other.users_all(request.args.get('token'))
    )


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
