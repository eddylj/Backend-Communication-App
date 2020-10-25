'''
Functions used to return and change information regarding user's data
'''
from data import data
from error import InputError, AccessError
from other import get_active, is_valid

def user_profile(token, u_id):
    '''
    Return information on the user (u_id, email, first name, last name, handle)
    '''

    # Why would you change it to InputError? Token's going to get changed but error handling won't.
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Invalid user
    if not is_user(u_id):
        raise InputError

    user = data['users'][u_id]

    return_user = {
        'u_id' : user['u_id'],
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle'],
    }

    return {'user': return_user}

def user_profile_setname(token, name_first, name_last):
    '''
    Change first or last name of the user if valid
    '''

    # InputError as this only confirms that the token exists, not necessarily active or not
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # name_first invalid length
    if not 1 <= len(name_first) <= 50:
        raise InputError

    # name_last invalid length
    if not 1 <= len(name_last) <= 50:
        raise InputError

    # # Don't use get_active function as user doesn't have to be active
    # u_id = int(token)
    # Where did you get this from? Because assignment specs say in 6.3:
    # "for all functions except auth/register and auth/login, an AccessError is
    # thrown when the token passed in is not a valid token."

    # Proposed change: have InputError be thrown if passed name is the same as
    # existing. This keeps the code consistent to the logic for the other
    # profile_set functions.
    # data['users'][caller_id]['name_first'] = name_first
    # data['users'][caller_id]['name_last'] = name_last

    if data['users'][caller_id]['name_first'] == name_first:
        if data['users'][caller_id]['name_last'] == name_last:
            raise InputError
    else:
        data['users'][caller_id]['name_first'] = name_first
        data['users'][caller_id]['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    '''
    Change email of the user
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Check if valid email
    if not is_valid(email):
        raise InputError

    # Not used by another account
    for user in data['users']:
        if user['email'] == email:
            raise InputError

    # Don't use get_active function as user doesn't have to be active
    # lines 53-55
    # u_id = int(token)

    data['users'][caller_id]['email'] = email

    return {}

def user_profile_sethandle(token, handle_str):
    '''
    Change handle of the user
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Invalid length
    if not 3 <= len(handle_str) <= 20:
        raise InputError

    # Check for uppercase letters.
    if not handle_str.islower():
        raise InputError

    # Not used by another account
    for user in data['users']:
        if user['handle'] == handle_str:
            raise InputError

    data['users'][caller_id]['handle'] = handle_str

    return {}

def is_user(u_id):
    '''
    Check for valid user ID
    '''
    return -1 < u_id < len(data['users'])
