"""
This module contains tests for message routes in server.py.
"""
import requests
from echo_http_test import url

user = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}
user1 = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}
user2 = {
    'email': 'alsovalid@gmail.com',
    'password': 'aW5Me@l!',
    'name_first': 'Andras',
    'name_last': 'Arato',
}
test_channel = {
    'token': '',
    'name': 'Test Channel',
    'is_public': True
}

def test_message_send_valid_http(url):
    """
    Base case for message_send(). Can't actually compare against
    url/channel/messages since latency makes the timestamp inaccurate, so this
    test only checks that send doesn't raise any errors.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']
    u_id2 = account['u_id']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # Send messages
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    response = requests.post(f"{url}/message/send", json=send_payload)
    assert response.status_code == 200

    send_payload['token'] = token2
    send_payload['message'] = "Goodbye"
    response = requests.post(f"{url}/message/send", json=send_payload)
    assert response.status_code == 200

def test_message_send_too_long_http(url):
    """
    Test case for message_send(), where the passed message exceeds the 1000
    character limit.
    """

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # 1008-character string
    long_message = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
        "commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus "
        "et magnis dis parturient montes, nascetur ridiculus mus. Donec quam "
        "felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla "
        "consequat massa quis enim. Donec pede justo, fringilla vel, aliquet "
        "nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, "
        "venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. "
        "Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. "
        "Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, "
        "consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, "
        "viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus "
        "varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies "
        "nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. "
        "Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem "
        "quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam."
    )

    payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': long_message
    }
    response = requests.post(f"{url}/message/send", json=payload)
    assert response.status_code == 400

def test_message_send_not_member_http(url):
    """
    Test case for message_send(), where the caller is trying to send a message
    to a channel they're not part of.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    response = requests.post(f"{url}/message/send", json=payload)
    assert response.status_code == 400

############################# MESSAGE_REMOVE TESTS #############################

def test_message_remove_valid_http(url):
    """ Base case for message_remove() """

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    send_payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    remove_payload = {
        'token': token,
        'message_id': message['message_id']
    }
    requests.delete(f"{url}/message/remove", json=remove_payload)

    get_payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_remove_nonexistent_http(url):
    """
    Test case for message_remove(), where the message corresponding to the ID
    passed into message_remove() does not exist. e.g. Never been sent or already
    deleted.
    """

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    remove_payload = {
        'token': token,
        'message_id': 12345
    }
    response = requests.delete(f"{url}/message/remove", json=remove_payload)
    assert response.status_code == 400

    # Sending a message, removing it then trying to remove it again.
    payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=payload)
    message = r.json()

    remove_payload['message_id'] = message['message_id']
    requests.delete(f"{url}/message/remove", json=remove_payload)

    response = requests.delete(f"{url}/message/remove", json=remove_payload)
    assert response.status_code == 400

def test_message_remove_not_owner_http(url):
    """
    Test case for message_remove(), where the caller isn't the user who sent the
    message, or an owner of the channel.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']
    u_id2 = account['u_id']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 1 sends a message
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    # User 2 tries to remove it
    remove_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    response = requests.delete(f"{url}/message/remove", json=remove_payload)
    assert response.status_code == 400

def test_message_remove_as_owner_http(url):
    """
    Testing if an owner of the flockr or channel can freely remove messages.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']
    u_id2 = account['u_id']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends a message, then user 1 removes it.
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Goodbye"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    remove_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    requests.delete(f"{url}/message/remove", json=remove_payload)

    get_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_remove_not_member_http(url):
    """
    Edge case for message_remove(), where the caller isn't even in the channel
    where the message is sent. This includes the Flockr owner.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # User 2 creates a channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User 2 sends a message
    payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Goodbye"
    }
    r = requests.post(f"{url}/message/send", json=payload)
    message = r.json()

    # User 1 tries to remove it. Fails despite being Flockr owner.
    remove_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    response = requests.delete(f"{url}/message/remove", json=remove_payload)
    assert response.status_code == 400

############################## MESSAGE_EDIT TESTS ##############################

def test_message_edit_valid_http(url):
    """
    Base case for message_edit(). Editing a message normally and checking
    against channel_messages(). Can't actually compare against
    url/channel/messages since latency makes the timestamp inaccurate, so this
    test only checks that edit doesn't raise any errors.
    """

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=payload)
    message = r.json()

    edit_payload = {
        'token': token,
        'message_id': message['message_id'],
        'message': "Goodbye"
    }
    response = requests.put(f"{url}/message/edit", json=edit_payload)
    assert response.status_code == 200

def test_message_edit_empty_http(url):
    """
    Test case for message_edit(), where the passed string is empty. Should
    delete the message as per specification.
    """

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=payload)
    message = r.json()

    edit_payload = {
        'token': token,
        'message_id': message['message_id'],
        'message': ""
    }
    requests.put(f"{url}/message/edit", json=edit_payload)

    get_payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_edit_not_owner_http(url):
    """
    Test case for message_edit(), where the caller isn't the user who sent the
    message, or an owner of the channel/Flockr.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']
    u_id2 = account['u_id']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 1 sends a message
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    # User 2 tries to edit it
    edit_payload = {
        'token': token2,
        'message_id': message['message_id'],
        'message': "Goodbye"
    }
    response = requests.put(f"{url}/message/edit", json=edit_payload)
    assert response.status_code == 400

def test_message_edit_as_owner_http(url):
    """
    Testing if an owner of the flockr or channel can freely edit messages.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']
    u_id2 = account['u_id']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends a message, then user 1 edits it.
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    edit_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'message': "Goodbye"
    }
    response = requests.put(f"{url}/message/edit", json=edit_payload)
    assert response.status_code == 200

def test_message_edit_not_member_http(url):
    """
    Edge case for message_edit(), where the caller isn't even in the channel
    where the message is sent. This includes the Flockr owner.
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # User 2 creates a channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User 2 sends a message
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    # User 1 tries to edit it. Fails despite being Flockr owner.
    edit_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'message': "Goodbye"
    }
    response = requests.put(f"{url}/message/edit", json=edit_payload)
    assert response.status_code == 400

# Checking invalid token
def test_message_invalid_token_http(url):
    """
    Test for if token is invalid throughout all message functions
    """

    # Register a user and create a channel with one message in it.
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    payload = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=payload)
    message = r.json()

    # Deactivate token by logging out
    requests.post(f"{url}/auth/logout", json={'token': token})

    # Cannot use when token is invalid
    payload = {
        'token': token,
        'message_id': message['message_id']
    }
    response = requests.delete(f"{url}/message/remove", json=payload)
    assert response.status_code == 400

    payload['message'] = "Goodbye"
    response = requests.put(f"{url}/message/edit", json=payload)
    assert response.status_code == 400

    del payload['message_id']
    payload['channel_id'] = channel['channel_id']
    response = requests.post(f"{url}/message/send", json=payload)
    assert response.status_code == 400

############################## MESSAGE_PIN TESTS ##############################

def test_message_pin_valid_http(url):
    '''
    Base Test for message_pin. Owner pinning a message and checking with channel_messages()
    '''

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']
    u_id1 = account['u_id']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 1 into the channel
    invite_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'u_id': u_id1
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends two messages, then user 1(flockr owner) and user 2 pins it.
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message1 = r.json()

    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message2 = r.json()

    pin_payload = {
        'token': token2,
        'message_id': message1['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    pin_payload = {
        'token': token1,
        'message_id': message2['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_pin_invalid_message_id_http(url):
    '''
    Test case for an invalid message ID of a message that doesn't exist in the channel
    when an owner is pinning a message.
    '''

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    pin_payload = {
        'token': token1,
        'message_id': 12345
    }
    response = requests.post(f"{url}/message/pin", json=pin_payload)
    assert response.status_code == 400

    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    pin_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    response = requests.post(f"{url}/message/pin", json=pin_payload)
    assert response.status_code == 400

def test_message_pin_not_member(url):
    '''
    Test Case for when the user is pinning a message when they are not a member of the
    channel and are owners
    '''

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "KOOLL"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    pin_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/pin", json=pin_payload)
    assert response.status_code == 400

    leave_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
    }

    requests.post(f"{url}/channel/leave", json=leave_payload)

    pin_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/pin", json=pin_payload)
    assert response.status_code == 400

def test_message_pin_not_owner(url):
    '''
    Test case for messages being pinned by non-owners or not by the flockr owner 
    who must be in the channel
    '''

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'u_id': u_id1
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    pin_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/pin", json=pin_payload)
    assert response.status_code == 400

############################## MESSAGE_UNPIN TESTS ##############################
def test_message_unpin_valid_http(url):
    '''
    Base Test for message_unpin. Owner pinning a message and checking with channel_messages()
    ''' 
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 1 into the channel
    invite_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'u_id': u_id1
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends two messages
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message1 = r.json()

    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "what it do"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message2 = r.json()

    pin_payload = {
        'token': token1,
        'message_id': message1['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    pin_payload = {
        'token': token2,
        'message_id': message2['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

    unpin_payload = {
        'token': token1,
        'message_id': message2['message_id']
    }
    requests.post(f"{url}/message/unpin", json=unpin_payload)

    unpin_payload = {
        'token': token2,
        'message_id': message1['message_id']
    }
    requests.post(f"{url}/message/unpin", json=unpin_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_unpin_invalid_message_id(url): 
    '''
    Test case for an invalid message ID of a message that doesn't exist in the channel
    '''

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    unpin_payload = {
        'token': token1,
        'message_id': 12345
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400

    # User 1 sends two messages
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message1 = r.json()

    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "what it do"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message2 = r.json()

    pin_payload = {
        'token': token1,
        'message_id': message1['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    unpin_payload = {
        'token': token1,
        'message_id': message1['message_id']
    }
    requests.post(f"{url}/message/unpin", json=unpin_payload)

    unpin_payload = {
        'token': token1,
        'message_id': message1['message_id']
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400

    unpin_payload = {
        'token': token1,
        'message_id': message2['message_id']
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400

def test_message_unpin_not_member(url):
    '''
    Test Case for messages being pinned by non-members of the channel that are owners
    '''
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User 2 sends a message
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "Hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()    

    pin_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    unpin_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400   

    leave_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
    }

    requests.post(f"{url}/channel/leave", json=leave_payload)

    unpin_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400 


def test_message_unpin_not_owner(url):
    '''
    Test case for the non-owner or non-flockr owner unpinning messages in the channel
    '''

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # Invite user 2 into the channel
    invite_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'u_id': u_id2
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends a message
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()

    pin_payload = {
        'token': token1,
        'message_id': message['message_id']
    }
    requests.post(f"{url}/message/pin", json=pin_payload)

    unpin_payload = {
        'token': token2,
        'message_id': message['message_id']
    }
    response = requests.post(f"{url}/message/unpin", json=unpin_payload)
    assert response.status_code == 400 


############################## MESSAGE_REACT TESTS ##############################

def test_message_react_valid_http(url):
    '''
    Base test for message react. Owner reacting to a message and checking with channel_messages()
    '''
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()    

    # Invite user 1 into the channel
    invite_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'u_id': u_id1
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends a message
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()   

    react_payload = {
        'token': token2,
        'message_id': message['message_id'],
        'react_id': 1 # 1 for now as only have 1 react so far
    }

    r = requests.post(f"{url}/message/react", json=react_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_react_invalid_message_id_http(url):
    '''
    Test case for having an invalid message id to a non-existent message in the channel
    '''
    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    react_payload = {
        'token': token1,
        'message_id': 12345,
        'react_id': 1
    }
    
    response = requests.post(f"{url}/message/react", json=react_payload)
    assert response.status_code == 400

def test_message_react_invalid_react_id_http(url):
    '''
    Test case for having an invalid react id to a non-existent react available in the channel
    '''
    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User sends a message
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()   

    react_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'react_id': 123415
    }
    
    response = requests.post(f"{url}/message/react", json=react_payload)
    assert response.status_code == 400

def test_message_react_already_active_react_id():
    '''
    Test case for when the react id is already being used on a message
    '''
    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User sends a message
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()   

    react_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'react_id': 1,
    }
    
    r = requests.post(f"{url}/message/react", json=react_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

    react_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'react_id': 1
    }
    
    response = requests.post(f"{url}/message/react", json=react_payload)
    assert response.status_code == 400

############################## MESSAGE_UNREACT TESTS ##############################

def test_message_unreact_valid_http(url): 
    '''
    Base test for message unreact. Owner unreacting to a message and checking with channel_messages()
    ''' 

     # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    r = requests.post(f"{url}/auth/register", json=user2)
    account = r.json()
    token2 = account['token']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()    

    # Invite user 1 into the channel
    invite_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'u_id': u_id1
    }
    requests.post(f"{url}/channel/invite", json=invite_payload)

    # User 2 sends a message
    send_payload = {
        'token': token2,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json() 

    react_payload = {
        'token': token2,
        'message_id': message['message_id'],
        'react_id': 1 # 1 for now as only have 1 react so far
    }

    r = requests.post(f"{url}/message/react", json=react_payload)
   

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

    unreact_payload = {
        'token': token2,
        'message_id': message['message_id'],
        'react_id': 1 # 1 for now as only have 1 react so far
    }

    r = requests.post(f"{url}/message/unreact", json=unreact_payload)
    message = r.json()  

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_unreact_invalid_message_id_http(url):
    '''
    Test case for when the message id is invalid and does not correspond to a message in the channel
    '''
    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    unreact_payload = {
        'token': token1,
        'message_id': 12345,
        'react_id': 1
    }
    
    response = requests.post(f"{url}/message/unreact", json=unreact_payload)
    assert response.status_code == 400

def test_message_unreact_invalid_react_id_http(url):
    '''
    Test case for having an invalid react id to a non-existent react available in the channel
    '''

    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User sends a message
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message = r.json()   

    unreact_payload = {
        'token': token1,
        'message_id': message['message_id'],
        'react_id': 123415
    }
    
    response = requests.post(f"{url}/message/unreact", json=unreact_payload)
    assert response.status_code == 400

def test_message_unreact_already_active_react_id():
    '''
    Test case for when the react id is already being used on a message
    '''
    # Create a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token1 = account['token']

    # Create channel
    test_channel['token'] = token1
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # User sends two messages
    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "that one"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message1 = r.json()  

    send_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'message': "hello"
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    message2 = r.json()    

    react_payload = {
        'token': token1,
        'message_id': message1['message_id'],
        'react_id': 1
    }
    
    r = requests.post(f"{url}/message/react", json=react_payload)

    get_payload = {
        'token': token1,
        'channel_id': channel['channel_id'],
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=get_payload)
    messages = r.json()
    assert messages == {
        'messages': [],
        'start': 0,
        'end': -1
    }

    unreact_payload = {
        'token': token1,
        'message_id': message2['message_id'],
        'react_id': 1
    }
    
    response = requests.post(f"{url}/message/unreact", json=unreact_payload)
    assert response.status_code == 400
