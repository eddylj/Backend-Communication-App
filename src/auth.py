'''
Login, logout and register functions
'''
from data import data
from error import InputError
from other import get_active, is_valid

def auth_login(email, password):
    """
    Given a registered user's email and password and generates a valid token for
    the user to remain authenticated.

    Parameters:
        email (str)     : User's email
        password (str)  : User's password

    Returns:
        {u_id (int), token (str)}:
            A dictionary containing the user's u_id and a token if the email and
            password can be authenticated against the flockr database.

    Raises:
        InputError:
            When:
                - Email entered is not a valid email.
                - Email entered does not belong to a user.
                - Password is not correct.
    """
    for (index, user) in enumerate(data['users']):
        if user['email'] == email and user['password'] == password:
            if get_active(index) is None:
                data['tokens'].append(str(index))
            return {
                'u_id': index,
                'token': str(index),
            }
    raise InputError

def auth_logout(token):
    """
    Given an active token, invalidates the token to log the user out. If a valid
    token is given, and the user is successfully logged out, it returns true,
    otherwise false.

    Parameters:
        token (str) : User's authorisation hash.

    Returns:
        {is_success (bool)}:
            Whether or not token does correspond to an active token.
    """
    for (index, active_token) in enumerate(data['tokens']):
        if token == active_token:
            data['tokens'].pop(index)
            return {'is_success': True}
    return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password, store a new
    account for them in the flockr database. A handle is generated that is the
    concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters.
    If the handle is already taken, an integer (number of people with the same
    name) is added at the end of the handle. The integer will replace end
    characters if needed to stay within the 20 character limit.

    Parameters:
        email (str)     : User's email
        password (str)  : User's password
        name_first (str): User's first name
        name_last (str) : User's last name

    Returns:
        {u_id (int), token (str)}:
            A dictionary containing the user's new u_id and a token if the
            parameters are valid.

    Raises:
        InputError:
            When:
                - Email entered is not a valid email.
                - Email entered already belongs to a user.
                - Password entered is less than 6 characters long.
                - name_first not is between 1 and 50 characters inclusively
                  in length
                - name_last is not between 1 and 50 characters inclusively
                  in length
    """
    u_id = len(data['users'])
    new_user = {
        'u_id': u_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': (name_first + name_last)[:20].lower()
    }

    if not is_valid(email):
        raise InputError

    number = 0
    for user in data['users']:
        if user['email'] == email:
            raise InputError
        if (user['name_first'] == new_user['name_first'] and
                user['name_last'] == new_user['name_last']):
            number += 1

    if len(new_user['password']) < 6:
        raise InputError

    if not 1 <= len(new_user['name_first']) <= 50:
        raise InputError

    if not 1 <= len(new_user['name_last']) <= 50:
        raise InputError

    if number != 0:
        new_user['handle'] = new_handle(new_user['handle'], number)

    data['users'].append(new_user)
    data['tokens'].append(str(u_id))

    return {
        'u_id': u_id,
        'token': str(u_id),
    }

def new_handle(handle, num):
    """
    Given an existing handle and an integer, generates a new handle by appending
    num to the end of handle. Num will replace end characters if needed to stay
    within the 20 character limit.

    Parameters:
        handle (str): Handle string
        num (int)   : Integer to be appended to handle

    Returns:
        (str): The newly generated handle.
    """
    offset = len(str(num))
    if len(handle) <= (20 - offset):
        return handle + str(num)

    # Workaround method to replace a substring inside a string from:
    # https://stackoverflow.com/questions/49701989/python-replace-character-range-in-a-string-with-new-string/49702020
    return str(num).join([handle[:20 - offset], handle[20:]])
