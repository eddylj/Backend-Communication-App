"""
Functions to send, remove and edit messages
"""
import threading
import bisect
import time
from data import data, Message
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

    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    # If the message is too long
    is_valid_message(message)

    message_id = data['messages'].num_messages()
    new_message = Message(message_id, channel, caller_id, message, timestamp)

    channel.get_messages().add_message(new_message)
    data['messages'].add_message(new_message)

    return {'message_id': message_id,}

@validate_token
def message_remove(caller_id, message_id):
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
    # If message doesn't exist already
    if not data['messages'].is_message(message_id):
        raise InputError

    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    if not message.is_sender(caller_id):
        if not channel.is_owner(caller_id):
            raise AccessError
    elif not channel.is_member(caller_id):
        raise AccessError

    data['messages'].remove_message(message_id)

    return {}

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

    data['messages'].get_message(message_id)

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
                - Token is invalid.
                - The caller is not a member of the channel.
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

@validate_token
def message_react(caller_id, message_id, react_id):
    """
    Given a valid message_id, a reaction from the caller is added to the
    corresponding message.

    Parameters:
        token (str)         : User's authorisation hash.
        message_id (int)    : ID of the target message.
        react_id (int)      : Type of reaction to be added to the message.

    Returns:
        {}: An empty dictionary if a reaction was added successfully.

    Raises:
        AccessError:
            When:
                - Token is invalid.
                - The user isn't in the channel where the message was posted.
        InputError:
            When:
                - No message with that message_id exists.
                - React_id doesn't correspond to a valid reaction.
                - The caller has already reacted with the same reaction to a
                  message.
    """
    if not is_message(message_id):
        raise InputError

    if not is_valid_react(react_id):
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]
    channel_messages = data['channels'][channel_id]['messages']

    if caller_id not in channel_data['members']:
        raise AccessError

    for msg in channel_messages:
        if msg['message_id'] == message_id:
            # Maybe change react_ids to start from 0
            try:
                reacts = msg['reacts'][react_id - 1]
            except IndexError:
                raise InputError

            # Extra computation for small numbers of reactions, but potentially
            # faster for more reactions.
            # If caller has already reacted.
            is_sender = caller_id == msg['u_id']
            if is_sender and reacts['is_this_user_reacted']:
                raise InputError
            if caller_id in reacts['u_ids']:
                raise InputError

            bisect.insort(reacts['u_ids'], caller_id)
            if is_sender:
                reacts['is_this_user_reacted'] = True
            return {}

    raise InputError

@validate_token
def message_unreact(caller_id, message_id, react_id):
    """
    Given a valid message_id, the reaction with react_id from the caller is
    removed from the message.
    """
    if not is_message(message_id):
        raise InputError

    if not is_valid_react(react_id):
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]
    channel_messages = data['channels'][channel_id]['messages']

    if caller_id not in channel_data['members']:
        raise AccessError

    for msg in channel_messages:
        if msg['message_id'] == message_id:
            # Maybe change react_ids to start from 0
            try:
                reacts = msg['reacts'][react_id - 1]
            except IndexError:
                raise InputError

            # Could change to binary search
            try:
                index = reacts['u_ids'].index(caller_id)
            except ValueError:
                raise InputError

            is_sender = caller_id == msg['u_id']
            if is_sender and reacts['is_this_user_reacted']:
                reacts['is_this_user_reacted'] = False
            reacts['u_ids'].pop(index)

            return {}

    raise InputError

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

def is_valid_react(react_id):
    """ Checks if a react_id is valid. """
    # Currently useless since theres only 1 react. May add more on frontend.
    return react_id in [1]
