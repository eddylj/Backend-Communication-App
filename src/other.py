from data import data
def clear():
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()

'''
Checks if a token is active. Returns the corresponding u_id if it is active,
None otherwise.
'''
def get_active(token):
    if token in data['tokens']:
        # Written in this redundant way because token will be changed in the future
        return data['users'][token]['u_id']
    return None

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