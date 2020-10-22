'''
Database for all users, channels, tokens and messages, stored in the global variable
'data'
'''
data = {
    # Stores registered users
    # Could also store tokens per user? I think having an active tokens list
    # would be more efficient though.
    'users': [],
    # Stores active channels
    'channels': [],
    # Stores active tokens
    'tokens': [],
    # Stores messages
    'messages' : [],
}
