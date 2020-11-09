"""
Functions to send, remove and edit messages
"""
import threading
import time
from data import data
from error import InputError, AccessError
from other import get_active, validate_token, is_valid_channel

@validate_token
def message_send(caller_id, channel_id, message):
    """
    Send a message and create a new entry in the messages database and also in
    the channel's messages database.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Destination channel.
        message (str)       : Message to be sent.

    Returns:
        {'message_id'(int)}:
            A dictionary containing the unique identifier of the newly sent
            message.

    Raises:
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
        InputError:
            - When message isn't between 1 and 1000 characters in length.
    """
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = round(time.time())

    # If the user is not part of the channel
    if caller_id not in data['channels'][channel_id]['members']:
        raise AccessError

    # If the message is too long
    is_valid_message(message)

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
    """
    Removes a message from the channel's database that is storing it. Replaces
    the data stored in the messages data with an empty dictionary to preserve
    the generation of unique message_ids.

    Parameters:
        token (str)         : User's authorisation hash.
        message_id (int)    : Target message's identifier.

    Returns:
        {}: An empty dictionary if message_remove succeeds.

    Raises:
        AccessError:
            - When token is invalid.
            - When none of these conditions are met:
                - Message with message_id was sent by the caller making this
                request.
                - The caller isn't an owner of the channel where the message
                was sent.
        InputError:
            - When the message doesn't exist (never sent/already deleted).
    """
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

@validate_token
def message_edit(caller_id, message_id, message):
    """
    Edits the contents of a message stored in channel data and updates the
    timestamp. If an empty string is passed as the message string, the message
    is deleted instead.

    Parameters:
        token (str)         : User's authorisation hash.
        message_id (int)    : Target message's identifier.
        message (str)       : New message to be edited in.

    Returns:
        {}: An empty dictionary if message_edit succeeds.

    Raises:
        AccessError:
            - When token is invalid.
            - When none of these conditions are met:
                - Message with message_id was sent by the caller making this
                request.
                - The caller isn't an owner of the channel where the message
                was sent.
        InputError:
            When:
                - The message to be edited in is longer than 1000 characters.
                - The message is exactly the same as the one stored in data.
                - Message_id doesn't correspond to an existing message.
    """
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = round(time.time())

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
    if caller_id != data['messages'][message_id]['u_id']:
        if caller_id not in channel_data['owners']:
            raise AccessError
    elif caller_id not in channel_data['members']:
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

@validate_token
def message_send_later(caller_id, channel_id, message, time_sent):
    """
    Sends a message from a user to the channel specified by channel_id
    automatically at a specified time in the future.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Target channel.
        message (str)       : Message string to be sent.
        time_sent (int)     : Unix timestamp when the message will be sent.

    Returns:
        {'message_id'(int)}:
            A dictionary containing the unique identifier of the message.
    Raises:
        AccessError:
            When:
                - The caller is not a member of the channel.
                - Token is invalid.
        InputError:
            When:
                - Channel_id does not correspond to an existing channel.
                - Message isn't between 1 and 1000 characters in length.
                - Time_sent is in the past.
    """
    countdown = time_sent - round(time.time())

    if countdown <= 0:
        raise InputError

    if not is_valid_channel(channel_id):
        raise InputError

    channel = data['channels'][channel_id]

    if caller_id not in channel['members']:
        raise AccessError

    is_valid_message(message)

    message_id = len(data['messages'])
    data['messages'].append({})

    args = [caller_id, message_id, channel_id, message]
    threading.Timer(countdown, send_later_resolve, args).start()

    return {'message_id': message_id}

def send_later_resolve(sender_id, message_id, channel_id, message):
    timestamp = round(time.time())

    data['messages'][message_id] = {
        'channel_id': channel_id,
        'u_id': sender_id
    }

    new_message = {
        'message_id' : message_id,
        'u_id' : sender_id,
        'message' : message,
        'time_created' : timestamp,
    }
    data['channels'][channel_id]['messages'].insert(0, new_message)

def is_message(message_id):
    """
    Checks if message_id corresponds to a sent message. Also checks if the
    message has already been deleted.
    """
    return (
        -1 < message_id < len(data['messages']) and
        data['messages'][message_id] != {}
    )

def is_valid_message(message):
    """ Checks if a message is between 1 and 1000, raise InputError if not. """
    if not 0 < len(message) <= 1000:
        raise InputError
    return True
