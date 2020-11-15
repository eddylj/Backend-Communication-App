'''
List, listall and create functions
'''
from data import data, Users, Channel
from error import InputError
from other import validate_token

@validate_token
def channels_list(caller_id):
    """
    Provide a list of all channels (and their associated details) that the
    caller is part of.

    Parameters:
        token   (str)   : Caller's authorisation hash.

    Returns:
        {
            channels: A list of dictionaries with types {channel_id, name} of
                      all channels the caller is part of. If the caller isn't
                      part of any channels, an empty list is returned.
        }

    Raises:
        AccessError: if token is invalid.
    """
    user = data['users'].get_user(u_id=caller_id)

    return {'channels': user.get_channels().list_all_details()}

@validate_token
def channels_listall(*_):
    """
    Provide a list of all channels (and their associated details) in the entire
    flockr server.

    Parameters:
        token (str): Caller's authorisation hash.

    Returns:
        {
            channels: A list of dictionaries with types {channel_id, name} of
                      all channels. If no channels exists, an empty list is
                      returned.
        }

    Raises:
        AccessError: if token is invalid.
    """
    return {'channels': data['channels'].list_all_details()}

@validate_token
def channels_create(caller_id, name, is_public):
    """
    Creates a new channel with a specified name that is either a public or
    private.

    Parameters:
        token       (str) : Caller's authorisation hash.
        name        (str) : What the channel will be called.
        is_public   (bool): Whether or not the channel will be public.

    Returns:
        {channel_id}: A channel_id corresponding to the newly created channel.

    Raises:
        InputError: if name is more than 20 characters long.
        AccessError: if token is invalid.
    """
    if len(name) > 20:
        raise InputError

    channel_id = data['channels'].num_channels()
    caller = data['users'].get_user(u_id=caller_id)
    new_channel = Channel(caller, channel_id, name, is_public)

    data['channels'].add_channel(new_channel)

    return {'channel_id': channel_id}
