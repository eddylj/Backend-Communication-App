"""
This module contains basic functionality for standups, a period where users can
send messages that at the end of the period will automatically be collated and
summarised to all other users in the channel.
User functions include:
    - standup_start()   -> starts a standup
    - standup_active()  -> checks if a standup is currently active
    - standup_send()    -> sends a message during the standup
"""
import threading
import time
from data import data
from message import is_valid_message
from error import InputError, AccessError
from other import validate_token

# def standup_resolve(sender_id, channel_id):
#     """
#     Sends the standup buffer string as a message into a given channel. Ignores
#     length limitations and access rules unlike message_send. The standup key
#     in channel data is then removed entirely, signifying the end of the standup.
#     """
#     timestamp = round(time.time())
#     channel = data['channels'][channel_id]
#     if len(channel['standup']['buffer']) != 0:
#         message_id = len(data['messages'])
#         new_message = {
#             'message_id' : message_id,
#             'u_id' : sender_id,
#             'message' : channel['standup']['buffer'],
#             'time_created' : timestamp,
#         }

#         channel['messages'].insert(0, new_message)
#         data['messages'].append({'channel_id': channel_id, 'u_id': sender_id})

#     del channel['standup']

@validate_token
def standup_start(caller_id, channel_id, length):
    """
    Given a valid channel, starts a standup period lasting the next [length]
    seconds. If any users call standup_send() during this period, their message
    is buffered and collated into a single message at it's conclusion and sent
    as a single message under the user who started the standup.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Target channel.
        length (int)        : Length of standup in seconds.

    Returns:
        {time_finish}:
            A dictionary containing the Unix timestamp when the standup is
            scheduled to finish.

    Raises:
        AccessError:
            When:
                - The caller is not a member of the channel.
                - Token is invalid.
        InputError:
            When:
                - Length parameter is less than 1.
                - Channel_id does not correspond to an existing channel.
                - There is already an ongoing standup in the channel.
    """
    length = int(length)
    if length <= 0:
        raise InputError

    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    if channel.has_standup():
        raise InputError

    time_finish = round(time.time()) + length
    channel.start_standup(time_finish)
    threading.Timer(length, channel.end_standup, [caller_id]).start()

    return {'time_finish': time_finish}

@validate_token
def standup_active(caller_id, channel_id):
    """
    For a given channel, return whether a standup is active in it, and what time
    the standup finishes. If no standup is active, then time_finish returns None

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Target channel.

    Returns:
        {'is_active': (bool), 'time_finish': (int)}
            A dictionary containing whether or not there is an active standup,
            and the Unix timestamp the standup is scheduled to end at.

    Raises:
        AccessError:
            When:
                - The caller is not a member of the channel.
                - Token is invalid.
        InputError:
            When channel_id does not correspond to an existing channel.
    """
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    is_active = channel.has_standup()
    time_finish = channel.standup_time_finish()

    return {'is_active': is_active, 'time_finish': time_finish}

@validate_token
def standup_send(caller_id, channel_id, message):
    """
    Adds a message to the standup buffer, provided there is an active standup in
    the specified channel.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Target channel.
        message (str)       : Message string to be sent.

    Returns:
        {}: An empty dictionary if the message was sent successfully.

    Raises:
        AccessError:
            When:
                - The caller is not a member of the channel.
                - Token is invalid.
        InputError:
            When:
                - Channel_id does not correspond to an existing channel.
                - There isn't an active standup in the channel.
                - The message exceeds 1000 characters in length.
    """
    channel = data['channels'].get_channel(channel_id)
    user = data['users'].get_user(caller_id)

    if not channel.is_member(caller_id):
        raise AccessError

    is_valid_message(message)

    if not channel.has_standup():
        raise InputError

    message = user.get_handle() + ": " + message
    channel.standup_buffer(message)

    return {}
