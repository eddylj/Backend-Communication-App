'''
Functions to send, remove and edit messages
'''
import time
from data import data
from error import InputError, AccessError
from other import get_active

def message_send(token, channel_id, message):
    '''
    Send a message and create a new entry in the messages database and also inside the channels
    messages database
    '''
    # Check if token is valid
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # If the user is not part of the channel
    if caller_id not in data['channels'][channel_id]['members']:
        raise AccessError

    # If the message is too long
    if not 0 < len(message) < 1000:
        raise InputError

    message_id = len(data['messages'])
    new_message = {
        'message_id' : message_id,
        'u_id' : caller_id,
        'message' : message,
        'time_created' : int(time.time()),
    }

    # Adds to channel data WITHOUT channel_id, since output demands that.
    # This puts the new message at the 0th element, as per requirement in channel_messages
    data['channels'][channel_id]['messages'].insert(0, new_message)

    # Storing channel_id and caller_id only in message data
    # The others aren't relevant and only take up space + need to be updated.
    data['messages'].append({'channel_id': channel_id, 'u_id': caller_id})

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    '''
    Remove a message inside the messages database and channels database
    '''
    # Check if token is valid
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # If message doesn't exist already
    if not is_message(message_id):
        raise InputError

    # The message is already deleted
    if data['messages'][message_id] == {}:
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']

    # If not sender of message / not owner of flockr
    if u_id not in (data['messages'][message_id]['u_id'], 0):
        if u_id not in data['channels'][channel_id]['owners']:
            raise AccessError

    # If not owner of the channel

        #raise AccessError

    # Remove from messages database
    data['messages'][message_id] = {}

    # Remove from channel database
    data['channels'][channel_id]['messages'].pop(0)

    return {
    }

def message_edit(token, message_id, message):
    '''
    Edit a message
    This changes the message inside the data['messages'] database and also
    inside the data['channels'][channel_id]['messages'] database
    '''

    # If message doesn't exist already
    if not is_message(message_id):
        raise InputError

    # If the message is too long
    if len(message) > 1000:
        raise InputError

    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    ogu_id = data['messages'][message_id]['u_id']
    channel_id = data['messages'][message_id]['channel_id']

    # If not original sender, not owner and not owner of flockr
    if u_id != ogu_id and u_id not in data['channels'][channel_id]['owners'] and u_id != 0:
        raise AccessError

    # Delete if message is an empty string
    if message == "":
        data['messages'][message_id] = {}
    else:
        # edit message
        data['messages'][message_id]['message'] = message


    return {
    }

def is_message(message_id):
    '''
    Checks if the message with 'message_id' has been sent before
    '''
    return -1 < message_id < len(data['messages'])
