"""
This module contains basic functionality for standups, a period where users can
send messages that at the end of the period will automatically be collated and
summarised to all other users in the channel.
Available functions include:
    - standup_start()   -> starts a standup
    - standup_active()  -> checks if a standup is currently active
    - standup_send()    -> sends a message during the standup
"""
import time
from data import data
from error import InputError, AccessError
from other import get_active

def standup_start(token, channel_id, length):
    """
    Given a valid channel, starts a standup period lasting the next [length]
    seconds. If any users call standup_send() during this period, their message
    is buffered and collated into a single message at it's conclusion and sent
    as a single message under the user who started the standup.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Destination channel.
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
                - Channel_id does not correspond to an existing channel.
                - There is already an ongoing standup in the channel.
    """
    timestamp = round(time.time())

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if caller_id not in data['channels'][channel_id]['members']:
        raise AccessError

    if length < 1:
        raise InputError

    if standup_active(token, channel_id)['is_actve']:
        raise InputError
