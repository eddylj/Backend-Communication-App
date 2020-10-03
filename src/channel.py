from data import data
from error import InputError, AccessError
from other import get_active

def channel_invite(token, channel_id, u_id):

    inviter = get_active(token)

    # Invalid user
    if inviter == None or get_active(u_id) == None:
        raise InputError
    

    # Invalid channel
    if not is_valid_channel(channel_id):
        raise InputError
    
    # CHANGE IN FUTURE IF GET_ACTIVE CHANGES
    # Inviter is not a member of the channel
    if is_member(channel_id, inviter):
        raise AccessError


    # Invite user to the channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['members'].append(u_id)

    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    u_id = get_active(token)
    if u_id == None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError
    
    messages = data['channels'][channel_id]['messages']
    if start > len(messages) or start < 0:
        raise InputError

    if not is_member(channel_id, u_id):
        raise AccessError

    if start + 50 < len(messages):
        end = start + 50
    else:
        end = -1
    
    # Provided example kept for records. Might be useful in later iterations.
    # 'messages': [
    #     {
    #         'message_id': 1,
    #         'u_id': 1,
    #         'message': 'Hello world',
    #         'time_created': 1582426789,
    #     }
    # ],
    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):

    user = get_active(token)

    # Invalid user
    if user == None:
        raise InputError

    # Invalid channel
    if not is_valid_channel(channel_id):
        raise InputError

    # Channel is private
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if channel['is_public'] == False:
                raise AccessError
            else:
                channel['members'].append(user)

    return {
    }

def channel_addowner(token, channel_id, u_id):
    caller_id = get_active(token)
    if caller_id == None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if is_owner(channel_id, u_id):
        raise InputError

    if not is_owner(channel_id, caller_id) and caller_id != 0:
        raise AccessError

    data['channels'][channel_id]['owners'].append(u_id)
    return {}

def channel_removeowner(token, channel_id, u_id):
    caller_id = get_active(token)
    if caller_id == None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if not is_owner(channel_id, u_id):
        raise InputError

    if not is_owner(channel_id, caller_id) and caller_id != 0:
        raise AccessError

    data['channels'][channel_id]['owners'].remove(u_id)
    return {}

def is_valid_channel(channel_id):
    return len(data['channels']) <= channel_id

def is_member(channel_id, u_id):
    return u_id in data['channels'][channel_id]['members']

def is_owner(channel_id, u_id):
    return u_id in data['channels'][channel_id]['owners']
