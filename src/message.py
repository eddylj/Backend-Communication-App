"""
Functions to send, remove and edit messages
"""
import threading
import time
from data import data, Message
from error import InputError, AccessError
from other import validate_token

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

    channel.get_messages().add_message(new_message, message_id)
    data['messages'].add_message(new_message, message_id)

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
    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    if not message.is_sender(caller_id):
        if not channel.is_owner(caller_id):
            raise AccessError
    elif not channel.is_member(caller_id):
        raise AccessError

    data['messages'].remove_message(message_id)
    channel.get_messages().remove_message(message_id)

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

    # Also checks if message has been deleted
    stored_message = data['messages'].get_message(message_id)
    channel = stored_message.get_channel()

    # If the message is too long
    if len(message) > 1000:
        raise InputError

    # If not sender of message and not owner of channel
    if not stored_message.is_sender(caller_id):
        if not channel.is_owner(caller_id):
            raise AccessError
    elif not channel.is_member(caller_id):
        raise AccessError

    if stored_message.compare(message):
        raise InputError
    if message == "":
        data['messages'].remove_message(message_id)
        channel.get_messages().remove_message(message_id)
    else:
        stored_message.set_time(timestamp)
        stored_message.set_message(message)

    return {}

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

    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    is_valid_message(message)

    message_id = data['messages'].num_messages()
    data['messages'].add_message(None, message_id)

    args = [caller_id, message_id, channel, message]
    threading.Timer(countdown, send_later_resolve, args).start()

    return {'message_id': message_id}

def send_later_resolve(sender_id, message_id, channel, message):
    """
    Function which sends a message with a predetermined message_id. Works
    similar to message_send(), just without any checks since the only time this
    function is expected to be used is in message_send_later(), which has error
    handling.
    """
    timestamp = round(time.time())

    new_message = Message(message_id, channel, sender_id, message, timestamp)
    data['messages'].add_message(new_message, message_id)
    channel.get_messages().add_message(new_message, message_id)

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
    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    if not is_valid_react(react_id):
        raise InputError

    if not channel.is_member(caller_id):
        raise AccessError

    try:
        reacts = message.get_reacts(react_id)
    except KeyError:
        message.add_react(caller_id, react_id)
        return {}

    if message.is_sender(caller_id) and reacts['is_the_user_reacted']:
        raise InputError
    if message.already_reacted(caller_id, react_id) is not None:
        raise InputError

    message.add_react(caller_id, react_id)
    return {}

@validate_token
def message_unreact(caller_id, message_id, react_id):
    """
    Given a valid message_id, the reaction with react_id from the caller is
    removed from the message.
    """
    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    if not is_valid_react(react_id):
        raise InputError

    if not channel.is_member(caller_id):
        raise AccessError

    message.remove_react(caller_id, react_id)

@validate_token
def message_pin(caller_id, message_id):
    """
    Function to pin a message in a channel
    """
    # Also checks if the message exists
    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    # User is not an owner in the channel where message was sent
    if not channel.is_owner(caller_id):
        raise AccessError

    if message.is_pinned():
        raise InputError
    message.pin()

    return {}

@validate_token
def message_unpin(caller_id, message_id):
    """
    Function to unpin a message in a channel
    """
    # Also checks if the message exists
    message = data['messages'].get_message(message_id)
    channel = message.get_channel()

    # User is not an owner in the channel where message was sent
    if not channel.is_owner(caller_id):
        raise AccessError

    if not message.is_pinned():
        raise InputError
    message.unpin()

    return {}

def is_valid_message(message):
    """ Checks if a message is between 1 and 1000, raise InputError if not. """
    if not 0 < len(message) <= 1000:
        raise InputError
    return True

def is_valid_react(react_id):
    """ Checks if a react_id is valid. """
    # Currently useless since theres only 1 react. May add more on frontend.
    return react_id in [1]
