'''
Functions used to return and change information regarding user's data
'''
from data import data
from error import InputError, AccessError
from other import get_active, is_valid

def user_profile(token, u_id):
    '''
    For a valid user, returns information about their user_id, email,
    first name, last name, and handle.

    Parameters:
        token(str): User's authorisation hash.
        u_id(int): User's unique identification number
    Returns:
        {user(dict)}:
            A dictionary that contains all the user details including their
            user id, email, first name and last name.
    Raises:
        InputError:
            When:
                - user id entered is invalid
        AccessError:
            When:
                - the token is invalid and is inactive

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
        'handle_str' : user['handle_str'],
    }

    return {'user': return_user}

def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name.

    Parameters:
        token(str): User's authorisation hash.
        name_first(str): User's first name.
        name_last(str): User's last name.
    Returns:
        {}: empty dictionary if the user's name was successfully changed in their profile
    Raises:
        InputError:
            When:
                - the first name exceeds the length of 50 letters
                - the last name exceeds the length of 50 letters
                - if the changed name is exactly the same as the previous name
        AccessError:
            When:
                - the token is invalid and is inactive
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

    if (data['users'][caller_id]['name_first'] == name_first and
            data['users'][caller_id]['name_last'] == name_last):
        raise InputError

    data['users'][caller_id]['name_first'] = name_first
    data['users'][caller_id]['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address.

    Parameters:
        token(str): User's authorisation hash
        email(str): User's email address
    Returns:
        {}: empty dictionary if the user's email was successfully changed in their profile
    Raises:
        InputError:
            When:
                - the email is invalid
                - the email is already used by another account
        AccessError:
            When:
                - the token is invalid and inactive
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
    Update the authorised user's handle (i.e. display name).

    Parameters:
        token(str): User's authorisation hash
        handle_str(str): User's name displayed on flockr
    Returns:
        {}: empty dictionary if the user's handle was successfully changed in their profile
    Raises:
        InputError:
            When:
                - the handle exceeds the length of 20 letters or less than 3 letters
                - the handle has upper case letters
                - if the handle is already used by another account/user
        AccessError:
            When:
                - the token is invalid and inactive

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
        if user['handle_str'] == handle_str:
            raise InputError

    data['users'][caller_id]['handle_str'] = handle_str

    return {}

def is_user(u_id):
    '''
    Checks for a valid user ID

    Parameters:
        u_id(int): User's unique identification number
    Returns:
        (bool): whether or not the user id is valid or not
    '''
    return -1 < u_id < len(data['users'])
