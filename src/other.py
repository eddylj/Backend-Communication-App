'''
Different Functions used throughout the program
'''
import re
from data import data
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
        # Written in this redundant way because token will be changed in the future
        return data['users'][int(token)]['u_id']
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
    u_id = get_active(token)
    if u_id is None:
        raise InputError
    
    result = []

    for channel in data['channels']:
        # All channels user is in
        if u_id in channel['members']:
            # Check through all messages
            for message in channel['messages']:
                # Check if in the current message
                if query_str in message['message']: 
                    # append if query_str is in
                    result.append(message)

    return {
        'messages': result
    }
