def message_send(token, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    '''
    Edit a message
    - This changes the message inside the data['messages'] database and also inside the 
    data['channels'][channel_id]['messages'] database
    '''
    # If the message is too long
    if len(message) > 1000:
        raise InputError

    u_id = get_active(token)
    if u_id is None:
        raise AccessError

    ogu_id = data['messages'][message_id]['u_id']
    channel_id = data['messages'][message_id]['channel_id']

    # If not original sender, not owner and not owner of flockr
    if u_id != ogu_id and u_id not in data['channels'][channel_id]['owners'] and u_id != 0:
        raise AccessError

    # Delete if message is an empty string
    if message == "":
        data['messages'][message_id] = {}
    else:
        # edit message
        data['messages'][message_id]['message'] = message


    return {
    }
