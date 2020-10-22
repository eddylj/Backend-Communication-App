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
    '''
    Remove a message inside the messages database and channels database
    '''
    # For now, removing a message is making the messages dictionary it belongs to to {}
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # The message is already empty
    if data['messages'][message_id] == {}:
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']

    # If not sender of message / not owner of flockr / owner of channel
    if u_id not in (data['messages'][message_id]['u_id'], 0, data['channels'][channel_id]['owners']):
        raise AccessError

    # Remove from messages database
    data['messages'][message_id] = {}

    # Remove from channel database
    data['channels'][channel_id]['messages'].pop(0)

    return {
    }

def message_edit(token, message_id, message):
    '''
    Edit a message
    - This changes the message inside the data['messages'] database and also inside the 
    data['channels'][channel_id]['messages'] database
    '''
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
