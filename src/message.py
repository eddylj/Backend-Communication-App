from data import data
from error import InputError, AccessError
from other import get_active

def message_send(token, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove(token, message_id):
    '''
    Remove a message inside the messages database and channels database
    '''
    # For now, removing a message is making the messages dictionary it belongs to to {}
    u_id = get_active(token)

    # The message is already empty
    if data['messages'][message_id] == {}:
        raise InputError

    # If not sender of message / not owner of flockr
    if u_id not in (data['messages'][message_id]['u_id'], 0):
        raise AccessError


    channel_id = data['messages'][message_id]['channel_id']

    # Remove from messages database
    data['messages'][message_id] = {}

    # Remove from channel database
    data['channels'][channel_id]['messages'].pop(0)

    return {
    }

def message_edit(token, message_id, message):
    return {
    }
