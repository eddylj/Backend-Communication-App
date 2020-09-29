from data import data
def clear():
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()

'''
Loops through list of active tokens checking if provided token is already
active. If not, adds the token to the list.
'''
def is_active(token):
    for active_token in data['tokens']:
        if token == active_token:
            return True
    return False

def users_all(token):
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

def search(token, query_str):
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