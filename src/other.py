'''
Different Functions used throughout the program
'''

from data import data
def clear():
    '''
    Function to clear the data
    '''
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()

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

def users_all(token):
    '''
    Function for returning all the information of the users
    '''
    users = []
    for info in data['users']:
        users.append(info)
    
    for user in users:
        del user['password']
    return {
        'users': users
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
