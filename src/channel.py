from data import data
from error import InputError, AccessError
from other import get_active

def channel_invite(token, channel_id, u_id):
    caller_id = get_active(token)
    if caller_id == None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError

    if len(data['users']) <= u_id:
        raise InputError

    if is_member(channel_id, u_id):
        raise InputError

    if not is_member(channel_id, caller_id):
        raise AccessError

    data['channels'][channel_id]['members'].append(u_id)
    return {
    }

def channel_details(token, channel_id):
    caller_id = get_active(token)
    if caller_id == None:
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
        owners.append(user_details)
    
    members = []
    for user in data['channels'][channel_id]['members']:
        user_details = {}
        user_details['u_id'] = data['users'][user]['u_id']
        user_details['name_first'] = data['users'][user]['name_first']
        user_details['name_last'] = data['users'][user]['name_last']
        members.append(user_details)

    return {
        'name': data['channels'][channel_id]['name'],
        'owner_members': owners,
        'all_members': members,
    }

def channel_messages(token, channel_id, start):
    caller_id = get_active(token)
    if caller_id == None:
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
    caller_id = get_active(token)
    if caller_id == None:
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
    caller_id = get_active(token)
    if caller_id == None:
        raise AccessError

    if not is_valid_channel(channel_id):
        raise InputError
    
    if not data['channels'][channel_id]['is_public'] and caller_id != 0:
        raise AccessError

    if is_member(channel_id, caller_id):
        raise InputError

    data['channels'][channel_id]['members'].append(caller_id)
    return {}

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

    if caller_id == u_id:
        raise InputError

    data['channels'][channel_id]['owners'].remove(u_id)
    return {}

def is_valid_channel(channel_id):
    return len(data['channels']) > channel_id

def is_member(channel_id, u_id):
    return u_id in data['channels'][channel_id]['members']

def is_owner(channel_id, u_id):
    return u_id in data['channels'][channel_id]['owners']
