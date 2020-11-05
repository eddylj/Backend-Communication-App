import time
from data import data
from error import InputError, AccessError
from other import get_active

def validatetoken(function):
    def wrapper(*args):
        caller_id = get_active(args[0])
        if caller_id is None:
            raise AccessError
        return message_send(caller_id, *args[1:])
    return wrapper

@validatetoken
def message_send(caller_id, channel_id, message):
    # If the user is not part of the channel
    if caller_id not in data['channels'][channel_id]['members']:
        raise AccessError

    # Rest of the code
