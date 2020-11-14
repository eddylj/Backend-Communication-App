'''
Invite, details, messages, leave, join, addowner and removeowner functions.
Further functions such as is_valid_channel, is_member and is_owner used to help the
above functions.
'''
from data import data
from error import InputError, AccessError
from other import validate_token

@validate_token
def channel_invite(caller_id, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately.

    Parameters:
        token       (str)   : Caller's authorisation hash.
        channel_id  (int)   : Target channel's ID.
        u_id        (int)   : Invitee's user ID

    Returns:
        {}: An empty dictionary if the user was successfully invited to the
            channel.

    Raises:
        InputError:
            When:
                - channel_id does not refer to a valid channel.
                - u_id does not refer to a valid user.
                - you try to invite someone that's already in the channel.
                - you try to invite yourself.
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
    """
    channel = data['channels'].get_channel(channel_id)
    user = data['users'].get_user(u_id)

    if not channel.is_member(caller_id):
        raise AccessError

    if channel.is_member(u_id):
        raise InputError

    channel.join(user)

    return {}

@validate_token
def channel_details(caller_id, channel_id, url=None):
    """
    Given a Channel with ID channel_id that the caller is part of, provide basic
    details about the channel.

    Parameters:
        token       (str)   : Caller's authorisation hash.
        channel_id  (int)   : Target channel's ID.

    Returns:
        {name, owner_members, all_members}:
            A dictionary containing the name, a list of owners and a list of
            members ordered by joining date.

    Raises:
        InputError:
            When channel_id does not refer to a valid channel.
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
    """
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    return {
        'name': channel.get_name(),
        'owner_members': channel.get_owners().list_all_details(url=url),
        'all_members': channel.get_members().list_all_details(url=url)
    }

@validate_token
def channel_messages(caller_id, channel_id, start):
    """
    Given a Channel with ID channel_id that the caller is part of, return up to
    50 messages between index "start" and "start + 50". Message with index 0 is
    the most recent message in the channel. This function returns a new index
    "end" which is the value of "start + 50", or, if this function has returned
    the least recent messages in the channel, returns -1 in "end" to indicate
    there are no more messages to load after this return.Negative start values
    are invalid.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.
        start (int)     : Index of first message to be shown.

    Returns:
        {messages, start, end}:
            A dictionary of messages in the format:
                {message_id, u_id, message, time_created, reacts, is_pinned}
            as well as the start index given by the user and the end index (-1
            if all messages have been returned, start + 50 otherwise).

    Raises:
        InputError:
            When:
                - channel_id does not refer to a valid channel.
                - start is greater than the total number of messages in the
                  channel.
                - start is negative.
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
    """
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    messages = channel.get_messages()
    num_sent_messages = messages.num_messages(sent=True)
    if not 0 <= start <= num_sent_messages:
        raise InputError

    if start + 50 < num_sent_messages:
        end = start + 50
    else:
        end = -1

    return {
        'messages': messages.get_details(start, end),
        'start': start,
        'end': end
    }

@validate_token
def channel_leave(caller_id, channel_id):
    """
    Given a channel ID, the user leaves the corresponding channel. The last
    member of a channel may leave, however the channel still remains and can
    be accessed with the same channel_id.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.

    Returns:
        {}: An empty dictionary if the user left the channel successfully.

    Raises:
        InputError:
            When channel_id does not refer to a valid channel.
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
    """
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_member(caller_id):
        raise AccessError

    channel.leave(caller_id)
    return {}

@validate_token
def channel_join(caller_id, channel_id):
    """
    Given a channel_id of a channel that the caller can join, adds them to that
    channel. Flockr owner (first account created) can join private channels.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.

    Returns:
        {}: An empty dictionary if the user joined the channel successfully.

    Raises:
        InputError:
            When:
                - channel_id does not refer to a valid channel.
                - caller is already part of the channel specified.
        AccessError:
            When:
                - the channel specified is set to private and the caller isn't
                  the flockr owner.
                - token is invalid.
    """
    user = data['users'].get_user(u_id=caller_id)
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_public() and user.get_permissions() != 1:
        raise AccessError

    if channel.is_member(caller_id):
        raise InputError

    channel.join(user)

    return {}

@validate_token
def channel_addowner(caller_id, channel_id, u_id):
    """
    Make the user corresponding to u_id an owner of the channel corresponding to
    channel_id.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.
        u_id (int)      : User to be added as an owner.

    Returns:
        {}: An empty dictionary if the user was added as an owner successfully.

    Raises:
        InputError:
            When:
                - channel_id does not refer to a valid channel.
                - User is already an owner of the channel specified.
        AccessError:
            When:
                - the caller isn't an owner of the channel, and isn't the flockr
                  owner.
                - token is invalid.
    """
    caller = data['users'].get_user(u_id=caller_id)
    channel = data['channels'].get_channel(channel_id)

    if not channel.is_owner(caller_id) and caller.get_permissions() != 1:
        raise AccessError

    if channel.is_owner(u_id):
        raise InputError

    user = data['users'].get_user(u_id=u_id)
    channel.get_owners().add_user(user)

    return {}

@validate_token
def channel_removeowner(caller_id, channel_id, u_id):
    """
    Remove the user corresponding to u_id from owners of the channel
    corresponding to channel_id.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.
        u_id (int)      : User to be added as an owner.

    Returns:
        {}: An empty dictionary if the user was removed as an owner successfully.

    Raises:
        InputError:
            When:
                - channel_id does not refer to a valid channel.
                - User is not an owner of the channel specified.
        AccessError:
            When:
                - the caller isn't an owner of the channel, and isn't the flockr
                  owner.
                - token is invalid.
    """
    if caller_id == u_id:
        raise InputError

    channel = data['channels'].get_channel(channel_id)
    user = data['users'].get_user(caller_id)

    if not channel.is_owner(caller_id) and user.get_permissions() != 1:
        raise AccessError

    if not channel.is_owner(u_id):
        raise InputError

    channel.get_owners().remove_user(u_id=u_id)

    return {}

def is_member(channel_id, u_id):
    """
    Checks if a user (u_id) is a member of a specified channel (channel_id).

    Parameters:
        channel_id (int): Channel's ID.
        u_id (int)      : User's ID.

    Returns:
        (bool): Whether or not user is in the specifiec channel.
    """
    return u_id in data['channels'][channel_id]['members']

def is_owner(channel_id, u_id):
    """
    Checks if a user (u_id) is an owner of a specified channel (channel_id).

    Parameters:
        channel_id (int): Channel's ID.
        u_id (int)      : User's ID.

    Returns:
        (bool): Whether or not user is an owner in the specifiec channel.
    """
    return u_id in data['channels'][channel_id]['owners']
