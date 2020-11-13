"""
Login, logout and register functions
"""
from time import time
import hashlib
import jwt
from data import data
from error import InputError
from other import is_valid, SECRET

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
        if user['email'] == email and validate_pw(user, password):
            for token in data['tokens']:
                if jwt.decode(token, SECRET, algorithms='HS256')['u_id'] == index:
                    return {
                        'u_id': index,
                        'token': token,
                    }
            payload = {'u_id': index, 'session': time()}
            token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
            data['tokens'].append(token)
            return {
                'u_id': index,
                'token': token,
            }
    raise InputError

def validate_pw(user, password):
    """
    Hashes the provided password with SHA256 and compares the result with the
    password hash stored in the specified user's data.

    Parameters:
        user (dict)     : User's stored data.
        password (str)  : Password being checked against data.

    Returns:
        (bool): Whether or not the entered password's hash matches the stored
                hash.
    """
    password = hashlib.sha256(password.encode())
    return password.digest() == user['password'].digest()

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
    try:
        data['tokens'].remove(token)
        return {'is_success': True}
    except ValueError:
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

    if not is_valid(email):
        raise InputError

    number = 0
    for user in data['users']:
        if user['email'] == email:
            raise InputError
        if (user['name_first'] == name_first and
                user['name_last'] == name_last):
            number += 1

    if len(password) < 6:
        raise InputError

    if not 1 <= len(name_first) <= 50:
        raise InputError

    if not 1 <= len(name_last) <= 50:
        raise InputError

    new_user = {
        'u_id': u_id,
        'email': email,
        'password': hashlib.sha256(password.encode()),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': (name_first + name_last)[:20].lower(),
        'permission_id' : 2,
    }

    # Permission_id for owner (automatically for u_id 0)
    if u_id == 0:
        new_user['permission_id'] = 1

    if number != 0:
        new_user['handle_str'] = new_handle(new_user['handle_str'], number)

    data['users'].append(new_user)

    payload = {'u_id': u_id, 'session': time()}
    token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
    data['tokens'].append(token)

    return {
        'u_id': u_id,
        'token': token,
    }

def auth_passwordreset_request():
    """
    Request a password reset, by sending a confirmation email to the provided email
    """

    return {}

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
