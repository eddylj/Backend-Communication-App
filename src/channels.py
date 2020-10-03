from data import data
from error import InputError, AccessError
from other import get_active

# Lists the details of all channels the given user is in
def channels_list(token):
    # Check if the token is active
    u_id = get_active(token)
    if u_id == None:
        raise AccessError

    channel_list = []

    # Looks through the channels database and checks if user is a member in each channel
    # If the user is a member, add the channel to the returned channel_list
    for channel in data['channels']:
        for member in channel['members']:
            if member == u_id:
                details = {
                    'channel_id': channel['channel_id'],
                    'name': channel['name']
                }
                channel_list.append(details)
                break

    return { 'channels' : channel_list }

# Lists the details of all channels in the database
def channels_listall(token):
    # Check if token is active
    if get_active(token) == None:
        raise AccessError

    channel_list = []

    # Goes through the channels database and adds them to the returned channel_list
    for channel in data['channels']:
        details = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channel_list.append(details)

    return {'channels': channel_list}

# Creates a new channel
def channels_create(token, name, is_public):
    # If name of the channel is longer than 20 characters
    if len(name) > 20:
        raise InputError

    # Check if token is active
    u_id = get_active(token)
    if u_id == None:
        raise AccessError
    
    # Inputs details of the new_channel
    channel_id = len(data['channels'])
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'owners' : [u_id],
        'members' : [u_id],
        'is_public' : is_public,
        'messages': [],
    }
    
    # Add to the global variable
    data['channels'].append(new_channel)

    return {'channel_id': channel_id}
