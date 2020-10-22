from data import data
from error import InputError, AccessError
from other import get_active

def message_send(token, channel_id, message):
    '''
    Send a message and create a new entry in the messages database and also inside the channels
    messages database
    '''
    # Could be error if we change what token is, right now it is the stringed version of u_id
    # If the message is too long
    if len(message) > 1000:
        raise InputError

    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # If the user is not part of the channel, and not owner of flockr
    if u_id not in data['channels'][channel_id]['members'] and u_id != 0:
        raise AccessError

    message_id = len(data['messages'])
    new_message = {
        'message_id' : message_id,
        'u_id' : u_id,
        'message' : message,
        'time_created' : 0,
        'channel_id' : channel_id,
    }

    # add to main database
    data['messages'].append(new_message)

    # also add to channels database
    # This puts the new message at the 0th element, as per requirement in channel_messages
    data['channels'][channel_id]['messages'].insert(0, new_message)

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }