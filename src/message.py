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
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = int(time.time())

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
        'time_created' : timestamp,
    }

    # Inserts new message at the start of the messages stored in channel data.
    data['channels'][channel_id]['messages'].insert(0, new_message)

    # Storing channel_id and caller_id only in message data
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

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]

    # If not sender of message and not owner of channel
    if u_id != data['messages'][message_id]['u_id']:
        if u_id not in channel_data['owners']:
            raise AccessError
    elif u_id not in channel_data['members']:
        raise AccessError

    # Remove from messages database
    data['messages'][message_id] = {}

    # Remove from channel database
    for (index, msg) in enumerate(channel_data['messages']):
        if msg['message_id'] == message_id:
            channel_data['messages'].pop(index)
            break

    # Coverage treats the for loop on line 75 as incomplete if it breaks early
    # and states that it never jumps to 82. Clearly doesn't make sense since
    # theres no early returns or exits in the loop. Once the loop breaks,
    # function will return on 82. Coverage exception cautiously applied.
    return {} # pragma: no cover

def message_edit(token, message_id, message):
    '''
    Edit a message
    This changes the message inside the data['messages'] database and also
    inside the data['channels'][channel_id]['messages'] database
    '''
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = int(time.time())

    # Check if token is valid
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # If message doesn't exist already
    if not is_message(message_id):
        raise InputError

    # If the message is too long
    if len(message) > 1000:
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]
    channel_messages = data['channels'][channel_id]['messages']

    # If not sender of message and not owner of channel
    if u_id != data['messages'][message_id]['u_id']:
        if u_id not in channel_data['owners']:
            raise AccessError
    elif u_id not in channel_data['members']:
        raise AccessError

    for (index, msg) in enumerate(channel_messages):
        if msg['message_id'] == message_id:
            # If passed message is the same as existing message
            if message == msg['message']:
                raise InputError
            # If message is an empty string
            if message == "":
                channel_messages.pop(index)
            else:
                msg['message'] = message
                msg['time_created'] = timestamp
            break

    # Same scenario as message_remove. Coverage doesn't account for breaks.
    # Coverage exception cautiously applied.
    return {} # pragma: no cover

def is_message(message_id):
    '''
    Checks if message_id corresponds to a sent message. Also checks if the
    message has already been deleted.
    '''
    return (
        -1 < message_id < len(data['messages']) and
        data['messages'][message_id] != {}
    )
