"""
Different Functions used throughout the program
"""
import os
import glob
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

    images = glob.glob("/src/static/*.jpg")
    for image in images:
        os.remove(image)

# Wrapper.validated attribute to skip validate_token taken from:
# https://stackoverflow.com/questions/41206565/bypassing-a-decorator-for-unit-testing
# EAFP style
def validate_token(function):
    """
    Decorator function to check if a token is valid. Passes the caller_id back
    to the function in place of the token if it is.

    Parameters:
        token (str) : Caller's authorisation hash.
    """
    def wrapper(*args):
        token = args[0]
        # Checking if token is signed properly.
        try:
            caller_id = jwt.decode(token, SECRET, algorithms='HS256')['u_id']
        except jwt.exceptions.DecodeError:
            raise AccessError

        # Checking if token is active.
        try:
            if token != data['tokens'][caller_id]:
                raise AccessError
        except KeyError:
            raise AccessError

        return function(caller_id, *args[1:])

    wrapper.validated = function
    return wrapper

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

@validate_token
def users_all(_, url=None):
    """
    Function for returning all the information of the users
    """
    return {'users': data['users'].list_all_details(url=url)}

@validate_token
def admin_userpermission_change(caller_id, u_id, permission_id):
    """
    Function for changing admin user permission
    """
    caller = data['users'].get_user(caller_id)

    # Not an owner of flockr
    if caller.get_permissions() != 1:
        raise AccessError

    # Invalid permission_id
    if permission_id not in (1, 2):
        raise InputError

    # Get target user. Also checks if they exist.
    target = data['users'].get_user(u_id)

    # Change permission_id of u_id
    target.set_permissions(permission_id)

    return {}

@validate_token
def search(caller_id, query_str):
    """
    Function to find messages similar to query_str in all channels the caller is
    in. Case insensitive.
    """
    if query_str == "":
        raise InputError

    results = []
    channels = data['users'].get_user(caller_id).get_channels()
    for _, channel in channels.list_all().items():
        messages = channel.get_messages()
        results.extend(messages.search_for(query_str))

    return {'messages': results}
