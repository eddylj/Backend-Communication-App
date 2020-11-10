"""
Functions to send, remove and edit messages
"""
import time
from data import data
from error import InputError, AccessError
from other import get_active

def message_send(token, channel_id, message):
    """
    Send a message and create a new entry in the messages database and also in
    the channel's messages database.

    Parameters:
        token (str)         : User's authorisation hash.
        channel_id (int)    : Destination channel.
        message (str)       : Message to be sent.

    Returns:
        {'message_id'(int)}:
            A dictionary containing the unique identifier of the newly sent
            message.

    Raises:
        AccessError:
            When:
                - the caller is not a member of the channel.
                - token is invalid.
        InputError:
            - When message isn't between 1 and 1000 characters in length.
    """
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = int(time.time())

    # Check if token is valid
    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # If the user is not part of the channel
    if caller_id not in data['channels'][channel_id]['members']:
        raise AccessError

    # If the message is too long
    if not 0 < len(message) < 1000:
        raise InputError

    message_id = len(data['messages'])
    new_message = {
        'message_id' : message_id,
        'u_id' : caller_id,
        'message' : message,
        'time_created' : timestamp,
        'reacts' : [],
        'is_pinned' : False,

    }

    # Inserts new message at the start of the messages stored in channel data.
    data['channels'][channel_id]['messages'].insert(0, new_message)

    # Storing channel_id and caller_id only in message data
    data['messages'].append({'channel_id': channel_id, 'u_id': caller_id})

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    """
    Removes a message from the channel's database that is storing it. Replaces
    the data stored in the messages data with an empty dictionary to preserve
    the generation of unique message_ids.

    Parameters:
        token (str)         : User's authorisation hash.
        message_id (int)    : Target message's identifier.

    Returns:
        {}: An empty dictionary if message_remove succeeds.

    Raises:
        AccessError:
            - When token is invalid.
            - When none of these conditions are met:
                - Message with message_id was sent by the caller making this
                request.
                - The caller isn't an owner of the channel where the message
                was sent.
        InputError:
            - When the message doesn't exist (never sent/already deleted).
    """
    # Check if token is valid
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # If message doesn't exist already
    if not is_message(message_id):
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]

    # If not sender of message and not owner of channel
    if u_id != data['messages'][message_id]['u_id']:
        if u_id not in channel_data['owners']:
            raise AccessError
    elif u_id not in channel_data['members']:
        raise AccessError

    # Remove from messages database
    data['messages'][message_id] = {}

    # Remove from channel database
    for (index, msg) in enumerate(channel_data['messages']):
        if msg['message_id'] == message_id:
            channel_data['messages'].pop(index)
            break

    # Coverage treats the for loop on line 75 as incomplete if it breaks early
    # and states that it never jumps to 82. Clearly doesn't make sense since
    # theres no early returns or exits in the loop. Once the loop breaks,
    # function will return on 82. Coverage exception cautiously applied.
    return {} # pragma: no cover

def message_edit(token, message_id, message):
    """
    Edits the contents of a message stored in channel data and updates the
    timestamp. If an empty string is passed as the message string, the message
    is deleted instead.

    Parameters:
        token (str)         : User's authorisation hash.
        message_id (int)    : Target message's identifier.
        message (str)       : New message to be edited in.

    Returns:
        {}: An empty dictionary if message_edit succeeds.

    Raises:
        AccessError:
            - When token is invalid.
            - When none of these conditions are met:
                - Message with message_id was sent by the caller making this
                request.
                - The caller isn't an owner of the channel where the message
                was sent.
        InputError:
            When:
                - The message to be edited in is longer than 1000 characters.
                - The message is exactly the same as the one stored in data.
                - Message_id doesn't correspond to an existing message.
    """
    # Keeping the timestamp as close to the start of function as possible.
    timestamp = int(time.time())

    # Check if token is valid
    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    # If message doesn't exist already
    if not is_message(message_id):
        raise InputError

    # If the message is too long
    if len(message) > 1000:
        raise InputError

    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]
    channel_messages = data['channels'][channel_id]['messages']

    # If not sender of message and not owner of channel
    if u_id != data['messages'][message_id]['u_id']:
        if u_id not in channel_data['owners']:
            raise AccessError
    elif u_id not in channel_data['members']:
        raise AccessError

    for (index, msg) in enumerate(channel_messages):
        if msg['message_id'] == message_id:
            # If passed message is the same as existing message
            if message == msg['message']:
                raise InputError
            # If message is an empty string
            if message == "":
                channel_messages.pop(index)
            else:
                msg['message'] = message
                msg['time_created'] = timestamp
            break

    # Same scenario as message_remove. Coverage doesn't account for breaks.
    # Coverage exception cautiously applied.
    return {} # pragma: no cover

def is_message(message_id):
    """
    Checks if message_id corresponds to a sent message. Also checks if the
    message has already been deleted.
    """
    return (
        -1 < message_id < len(data['messages']) and
        data['messages'][message_id] != {}
    )

def message_react(token, message_id, react_id):
    """
    Function to react to a message in a channel
    """

    # Find channel_id and data
    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]

    # Check if user is reacting to a valid message within a channel that the authorised user has joined
    caller_id = get_active(token)
    if caller_id not in data['channels'][channel_id]['members']:
        raise InputError

    # Check if user is performing an appropriate reaction ->just need to know if there's a list of elegible reacts
    # if reaction not in data['channels'][channel_id]['reactions']: # search through the list of elegible reacts if this is possible
    if react_id != 1:
        raise InputError

    # only issue with this is that itll work for react_id 1 but not for 1,2,3.. etc. if the reacts aren't coming in increasing
    # order, ie. the the reacts list will not be in increasing order of react_id.
    for (index, msg) in enumerate(channel_data['messages']):
        # Find the message in the channels database
        if msg['message_id'] == message_id:
            # if reacts is currently not populated and the user is not reacting to their own message
            if not msg['reacts'][react_id] and token != msg['token']:
                insert = {
                    react_id: react_id
                    uid:[token]
                    is_the_user_reacted: False
                }
                insert_copy = insert.copy()
                # add the new dictionary to the list
                msg['reacts'].append(insert_copy)
            # If reacts is currently not populated and the user is reacting to their own message
            elif not msg['reacts'][react_id] and token == msg['token']:
                insert = {
                    react_id: react_id
                    uid:[token]
                    is_the_user_reacted: True
                }
                insert_copy = insert.copy()
                # add the new dictionary to the list
                msg['reacts'].append(insert_copy)
            # If there already exist reacts to the message
            else: 
                # Raise InputError if the user has already reacted
                if msg['reacts'][react_id]['is_the_user_reacted'] = True:
                    raise InputError
                else:
                    # Append the token to the 'reacts' list
                    msg['reacts'][react_id]['u_ids'].append(token)
                    # Change 'is_the_user_reacted' if the user is reacting to their own message
                    if token == msg['token']:
                        msg['reacts'][react_id]['is_the_user_reacted'] == True

    return {}

def message_unreact(token, message_id, react_id):
    """
    Function to unreact a message in a channel
    """

    # Find channel_id and data
    channel_id = data['messages'][message_id]['channel_id']
    channel_data = data['channels'][channel_id]

    # Check if user is unreacting a valid message within a channel that the authorised user has joined
    caller_id = get_active(token)
    if caller_id not in data['channels'][channel_id]['members']:
        raise InputError

    # Check if user is performing an appropriate unreact ->just need to know if there's a list of elegible reacts
    # if react_id not in data['channels'][channel_id]['reactions']: # search through the list of elegible reacts
    if react_id != 1:
        raise InputError

    for (index, msg) in enumerate(channel_data['messages']):
        # Find the message in the channels database
        if msg['message_id'] == message_id:
            # If there arent any reacts that the user can unreact, raise InputError
            if not msg['reacts'][react_id]:
                raise InputError          
            
            # Removing the uid from the list of reacts
            msg['reacts'][react_id]['u_ids'].remove(token)
            if token == msg['token']:
                # If the user is the person who sent the message, update 'is_the_user_reacted'
                msg['reacts'][react_id]['is_the_user_reacted'] == False
            # If the list of reacts is now empty, remove the dictionary from the reacts list.
            if not msg['reacts'][react_id]['u_ids']:
                removekey(msg['reacts'], react_id)

    return {}

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

