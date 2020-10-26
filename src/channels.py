'''
List, listall and create functions
'''
from data import data
from error import InputError, AccessError
from other import get_active

def channels_list(token):
    """
    Provide a list of all channels (and their associated details) that the
    caller is part of.

    Parameters:
        token (str) : Caller's authorisation hash.

    Returns:
        {
            channels: A list of dictionaries with types {channel_id, name} of
                      all channels the caller is part of. If the caller isn't
                      part of any channels, an empty list is returned.
        }

    Raises:
        AccessError: if token is invalid.
    """
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    channel_list = []

    for channel in data['channels']:
        for member in channel['members']:
            if member == u_id:
                details = {
                    'channel_id': channel['channel_id'],
                    'name': channel['name']
                }
                channel_list.append(details)
                break

    return {'channels': channel_list}

def channels_listall(token):
    """
    Provide a list of all channels (and their associated details) in the entire
    flockr server.

    Parameters:
        token (str) : Caller's authorisation hash.

    Returns:
        {
            channels: A list of dictionaries with types {channel_id, name} of
                      all channels. If no channels exists, an empty list is
                      returned.
        }

    Raises:
        AccessError: if token is invalid.
    """
    if get_active(token) is None:
        raise AccessError

    channel_list = []

    for channel in data['channels']:
        details = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channel_list.append(details)

    return {'channels': channel_list}

def channels_create(token, name, is_public):
    """
    Creates a new channel with a specified name that is either a public or
    private.

    Parameters:
        token (str)     : Caller's authorisation hash.
        name (str)      : What the channel will be called.
        is_public (bool): Whether or not the channel will be public.

    Returns:
        {channel_id}: A channel_id corresponding to the newly created channel.

    Raises:
        InputError: if name is more than 20 characters long.
        AccessError: if token is invalid.
    """
    if len(name) > 20:
        raise InputError

    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    channel_id = len(data['channels'])
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'owners' : [u_id],
        'members' : [u_id],
        'is_public' : is_public,
        'messages': [],
    }

    data['channels'].append(new_channel)

    return {'channel_id': channel_id}
