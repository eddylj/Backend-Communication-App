"""
Different Functions used throughout the program
"""
import re
import time
import hashlib
import jwt
from data import data
from error import InputError, AccessError

SECRET = hashlib.sha256(str(time.time()).encode()).hexdigest()[:11]

def clear():
    """
    Function to clear the data
    """
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()
    data['messages'].clear()

# To be replaced
def get_active(token):
    """
    Checks if a token is active. Returns the corresponding u_id if it is active,
    None otherwise.

    Parameters:
        token (str) : Caller's authorisation hash.

    Returns:
        u_id (int)  : The corresponding u_id if token is active.
        None        : If token isn't active.
    """
    if token in data['tokens']:
        return jwt.decode(token, SECRET, algorithms='HS256')['u_id']
    return None

# To replace get_active
def validate_token(function):
    def wrapper(*args):
        if args[0] in data['tokens']:
            caller_id = jwt.decode(args[0], SECRET, algorithms='HS256')['u_id']
        else:
            raise AccessError
        return function(caller_id, *args[1:])
    return wrapper

def is_valid_channel(channel_id):
    """
    Checks if the channel_id corresponds to an existing channel stored in the
    database.

    Parameters:
        channel_id (int): Target channel's ID.

    Returns:
        (bool): Whether or not channel_id corresponds to an existing channel.
    """
    return -1 < channel_id < len(data['channels'])

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
    return re.search(regex, email)

def users_all(token):
    """
    Function for returning all the information of the users
    """
    if get_active(token) is None:
        raise AccessError

    users = []
    for info in data['users']:
        users.append(info)

    for user in users:
        del user['password']
        del user['permission_id']

    return {'users': users}

def admin_userpermission_change(token, u_id, permission_id):
    """
    Function for changing admin user permission
    """

    # If token is invalid
    owner_id = get_active(token)
    if owner_id is None:
        raise AccessError

    # Not an owner of flockr
    if data['users'][owner_id]['permission_id'] == 2:
        raise AccessError

    # Invalid u_id
    if not -1 < u_id < len(data['users']):
        raise InputError

    # Invalid permission_id
    if permission_id not in (1, 2):
        raise InputError

    # Change permission_id of u_id
    data['users'][u_id]['permission_id'] = permission_id

    return {}

def search(token, query_str):
    """
    Function to find messages similar to query_str in all channels the caller is
    in. Case insensitive.
    """
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    result = []

    for channel in data['channels']:
        # All channels user is in
        if u_id in channel['members']:
            # Check through all messages
            for message in channel['messages']:
                # Check if current message matches query_str
                if re.search(query_str, message['message'], re.IGNORECASE):
                    result.append(message)

    return {'messages': result}
