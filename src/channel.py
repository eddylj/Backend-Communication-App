'''
Invite, details, messages, leave, join, addowner and removeowner functions.
Further functions such as is_valid_channel, is_member and is_owner used to help the
above functions.
'''
from data import data
from error import InputError, AccessError
from other import get_active, is_valid_channel

def channel_invite(token, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.
        u_id (int)      : Invitee's user ID

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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not 0 <= u_id < len(data['users']):
        raise InputError

    if is_member(channel_id, u_id):
        raise InputError

    if not is_member(channel_id, caller_id):
        raise AccessError

    data['channels'][channel_id]['members'].append(u_id)
    if data['users'][u_id]['permission_id'] == 1:
        data['channels'][channel_id]['owners'].append(u_id)
    return {}

def channel_details(token, channel_id):
    """
    Given a Channel with ID channel_id that the caller is part of, provide basic
    details about the channel.

    Parameters:
        token (str)     : Caller's authorisation hash.
        channel_id (int): Target channel's ID.

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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not is_member(channel_id, caller_id):
        raise AccessError

    owners = []
    for user in data['channels'][channel_id]['owners']:
        user_details = {}
        user_details['u_id'] = data['users'][user]['u_id']
        user_details['name_first'] = data['users'][user]['name_first']
        user_details['name_last'] = data['users'][user]['name_last']
        user_details['profile_img_url'] = f"{data['users'][user]['u_id']}.jpg"
        owners.append(user_details)

    members = []
    for user in data['channels'][channel_id]['members']:
        user_details = {}
        user_details['u_id'] = data['users'][user]['u_id']
        user_details['name_first'] = data['users'][user]['name_first']
        user_details['name_last'] = data['users'][user]['name_last']
        user_details['profile_img_url'] = f"{data['users'][user]['u_id']}.jpg"
        members.append(user_details)

    return {
        'name': data['channels'][channel_id]['name'],
        'owner_members': owners,
        'all_members': members,
    }

def channel_messages(token, channel_id, start):
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
                {message_id, u_id, message, time_created}
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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    messages = data['channels'][channel_id]['messages']
    if start > len(messages) or start < 0:
        raise InputError

    if not is_member(channel_id, caller_id):
        raise AccessError

    if start + 50 < len(messages):
        end = start + 50
        messages = messages[start:end]
    else:
        end = -1

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not is_member(channel_id, caller_id):
        raise AccessError

    if is_owner(channel_id, caller_id):
        data['channels'][channel_id]['owners'].remove(caller_id)
    data['channels'][channel_id]['members'].remove(caller_id)
    return {}

def channel_join(token, channel_id):
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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not data['channels'][channel_id]['is_public'] and caller_id != 0:
        raise AccessError

    if is_member(channel_id, caller_id):
        raise InputError

    data['channels'][channel_id]['members'].append(caller_id)
    if data['users'][caller_id]['permission_id'] == 1:
        data['channels'][channel_id]['owners'].append(caller_id)
    return {}

def channel_addowner(token, channel_id, u_id):
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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if is_owner(channel_id, u_id):
        raise InputError

    if not is_owner(channel_id, caller_id) and data['users'][caller_id]['permission_id'] != 1:
        raise AccessError

    data['channels'][channel_id]['owners'].append(u_id)
    return {}

def channel_removeowner(token, channel_id, u_id):
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
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not is_owner(channel_id, u_id):
        raise InputError

    if not is_owner(channel_id, caller_id) and data['users'][caller_id]['permission_id'] != 1:
        raise AccessError

    if caller_id == u_id:
        raise InputError

    data['channels'][channel_id]['owners'].remove(u_id)
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
