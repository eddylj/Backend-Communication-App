'''
Functions used to return and change information regarding user's data
'''
import re
from data import data
from error import InputError
from other import get_active

def user_profile(token, u_id):
    '''
    Return information on the user (u_id, email, first name, last name, handle)
    '''

    # Invalid user
    if not is_user(u_id):
        raise InputError

    # InputError as this only confirms that the token exists, not necessarily active or not
    u_id = get_active(token)
    if u_id is None:
        raise InputError


    user = data['users'][u_id]

    return_user = {
        'u_id' : user['u_id'],
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle'],
    }

    return {
        'user': return_user,
    }

def user_profile_setname(token, name_first, name_last):
    '''
    Change first or last name of the user if valid
    '''

    # InputError as this only confirms that the token exists, not necessarily active or not
    u_id = get_active(token)
    if u_id is None:
        raise InputError

    # name_first invalid length
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError

    # name_last invalid length
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError

    # Don't use get_active function as user doesn't have to be active
    u_id = int(token)

    data['users'][u_id]['name_first'] = name_first
    data['users'][u_id]['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    '''
    Change email of the user
    '''

    # InputError as this only confirms that the token exists, not necessarily active or not
    u_id = get_active(token)
    if u_id is None:
        raise InputError

    # Check if valid email
    if not is_valid(email):
        raise InputError

    # Not used by another account
    for user in data['users']:
        if user['email'] == email:
            raise InputError
    # Don't use get_active function as user doesn't have to be active
    u_id = int(token)

    data['users'][u_id]['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Change handle of the user
    '''

    # Invalid length
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError
    # Not used by another account
    for user in data['users']:
        if user['handle'] == handle_str:
            raise InputError

    # Don't use get_active function as user doesn't have to be active
    u_id = int(token)

    data['users'][u_id]['handle'] = handle_str

    return {
    }


def is_valid(email):
    """
    Code provided in project specs, from:
    https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    Checks if email is valid against a regular expression.

    Parameters:
        email (str) : User's email

    Returns:
        (bool): Whether or not the email entered is invalid according to the
                regex standards.
    """
    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
    if re.search(regex, email):
        return True
    return False

def is_user(u_id):
    '''
    Check for valid user ID
    '''
    return u_id < len(data['users'])
