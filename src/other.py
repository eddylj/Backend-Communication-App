'''
Different Functions used throughout the program
'''
import re
import time
import hashlib
import jwt
from data import data

SECRET = hashlib.sha256(str(time.time()).encode()).hexdigest()[:11]

def clear():
    '''
    Function to clear the data
    '''
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()
    data['messages'].clear()

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
    '''
    Function for returning all the information of the users
    '''
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

# def admin_userpermission_change(token, u_id, permission_id):
#     '''
#     Function for changing admin user permission
#     '''
#     pass

def search(token, query_str):
    '''
    Function to find the information about messages
    '''
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
