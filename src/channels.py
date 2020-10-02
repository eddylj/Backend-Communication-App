from data import data
from error import InputError

def channels_list(token):
    
    token_user = ''

    for user in data['users']:
        if user['email'] == token:
            token_user = 




    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):

    return data['channels']

def channels_create(token, name, is_public):
    
    # If name of the channel is longer than 20 characters
    if len(name) > 20:
        raise InputError

    # Finding the creator/owner of the channel
    owner = {}

    for user in data['users']:
        # For now, the token is the equivalent to the user's email
        if user['email'] == token:
            owner = user


    new_channel = {
        'id' : len(data['channels']) + 1,
        'name' : name,
        # 'is_public' : is_public,
        # 'owner' : owner,
        # 'members' : [owner],
    }
    
    # Add to the global variable
    data['channels'].append(new_channel)

    return {
        'id': len(data['channels']),
    }
