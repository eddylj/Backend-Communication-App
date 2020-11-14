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

def test_message_pin_base_http(url):
    """
    Base test to make sure message_pin works
    """

    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account1 = r.json()
    token1 = account1['token']
    u_id1 = account1['u_id']

    r = requests.post(f"{url}/auth/register", json=user2)
    account2 = r.json()
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invite user 1 into the channel
    invite_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u_id1
    }

    requests.post(f"{url}/channels/create", json=invite_payload)

    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']


    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "goodnight",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']


    # Owner of Channel pinning
    pin_payload = {
        'token' : token2,
        'message_id' : msg_id1,
    }
    r = requests.post(f"{url}/message/pin", json=pin_payload)
    assert r.status_code == 200


    # Owner of Flockr pinning
    pin_payload = {
        'token' : token1,
        'message_id' : msg_id2,
    }
    r = requests.post(f"{url}/message/pin", json=pin_payload)
    assert r.status_code == 200


def test_message_pin_inputerror_http(url):

    """
    Test http server outputs error
    """

    # Create user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token = account['token']
    u_id = account['u_id']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']


    # Error with non existent message_id
    pin_payload = {
        'token' : token,
        'message_id' : 123415,
    }
    r = requests.post(f"{url}/message/pin", json=pin_payload)

    assert r.status_code == 400

    # Message is already pinned
    send_payload = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id = r.json()['message_id']


    pin_payload = {
        'token' : token,
        'message_id' : msg_id,
    }
    requests.post(f"{url}/message/pin", json=pin_payload)


    pin_payload = {
        'token' : token,
        'message_id' : msg_id,
    }
    r = requests.post(f"{url}/message/pin", json=pin_payload)
    assert r.status_code == 400


############################## MESSAGE_UNPIN TESTS ##############################

def test_message_unpin_base_http(url):
    """
    Unpin tests for http
    """
    
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account1 = r.json()
    token1 = account1['token']
    u_id1 = account1['u_id']

    r = requests.post(f"{url}/auth/register", json=user2)
    account2 = r.json()
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invite user 1 into the channel
    invite_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u_id1
    }

    requests.post(f"{url}/channels/create", json=invite_payload)

    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']


    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "goodnight",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']


    # Owner of Channel pinning
    pin_payload = {
        'token' : token2,
        'message_id' : msg_id1,
    }
    requests.post(f"{url}/message/pin", json=pin_payload)


    # Owner of Flockr pinning
    pin_payload = {
        'token' : token1,
        'message_id' : msg_id2,
    }
    requests.post(f"{url}/message/pin", json=pin_payload)


    # Flockr Owner unpinning
    pin_payload = {
        'token' : token1,
        'message_id' : msg_id2,
    }
    requests.post(f"{url}/message/unpin", json=pin_payload)

    # Channel Owner unpinning
    pin_payload = {
        'token' : token2,
        'message_id' : msg_id1,
    }
    requests.post(f"{url}/message/unpin", json=pin_payload)

def test_message_unpin_inputerror_http():
    """
    Unpin tests to test that the server gives errors
    """

    # Create user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token = account['token']
    u_id = account['u_id']

    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']


    # Error with non existent message_id
    unpin_payload = {
        'token' : token,
        'message_id' : 123415,
    }
    r = requests.post(f"{url}/message/unpin", json=unpin_payload)

    assert r.status_code == 400

    # Message is already unpinned
    send_payload = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id = r.json()['message_id']
    

    pin_payload = {
        'token' : token,
        'message_id' : msg_id,
    }
    r = requests.post(f"{url}/message/pin", json=pin_payload)
    assert r.status_code == 400

############################## MESSAGE_REACT TESTS ##############################

def test_message_react_base_http(url):
    """
    Base test for http message_react ouputting correctly
    """

    r = requests.post(f"{url}/auth/register", json=user1)
    account1 = r.json()
    token1 = account1['token']
    u_id1 = account1['u_id']

    r = requests.post(f"{url}/auth/register", json=user2)
    account2 = r.json()
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invite user 1 into the channel
    invite_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u_id1
    }

    requests.post(f"{url}/channels/create", json=invite_payload)

    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']

    react_id = 1

    react_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/react", json=react_payload)
    assert r.status_code == 200

def test_message_react_inputerror_http(url):
    """
    Test message react works in server with errors
    """
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']
    u_id = account['u_id']


    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invalid message_id
    react_id = 1

    react_payload = {
        'token' : token1,
        'message_id' : 123415,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/react", json=react_payload)
    assert r.status_code == 400


    # Invalid react_id
    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']

    react_id = 123415

    react_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : 123415,
    }
    r = requests.post(f"{url}/message/react", json=react_payload)
    assert r.status_code == 400


    # react twice
    react_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    requests.post(f"{url}/message/react", json=react_payload)

    react_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/react", json=react_payload)
    assert r.status_code == 400
    

############################## MESSAGE_UNREACT TESTS ##############################


def test_message_unreact_base_http(url):
    """
    Base test for http message_unreact ouputting correctly
    """

    r = requests.post(f"{url}/auth/register", json=user1)
    account1 = r.json()
    token1 = account1['token']
    u_id1 = account1['u_id']

    r = requests.post(f"{url}/auth/register", json=user2)
    account2 = r.json()
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    test_channel['token'] = token2
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invite user 1 into the channel
    invite_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'u_id' : u_id1
    }

    requests.post(f"{url}/channels/create", json=invite_payload)

    # Send messages
    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']


    # React
    react_id = 1

    react_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    requests.post(f"{url}/message/react", json=react_payload)

    # Unreact
    react_id = 1

    unreact_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/unreact", json=react_payload)
    assert r.status_code == 200

def test_message_unreact_inputerror_http(url):
    """
    Test message unreact works in server with errors
    """
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']
    u_id = account['u_id']


    # Create channel
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']

    # Invalid message_id
    react_id = 1

    unreact_payload = {
        'token' : token1,
        'message_id' : 123415,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/unreact", json=unreact_payload)
    assert r.status_code == 400


    # Invalid react_id
    send_payload = {
        'token' : token2,
        'channel_id' : channel_id,
        'message' : "Hello",
    }
    r = requests.post(f"{url}/message/send", json=send_payload)
    msg_id1 = r.json()['message_id']

    react_id = 123415

    unreact_payload = {
        'token' : token1,
        'message_id' : 123415,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/runeact", json=unreact_payload)
    assert r.status_code == 400


    # unreact when not reacted
    unreact_payload = {
        'token' : token1,
        'message_id' : msg_id1,
        'react_id' : react_id,
    }
    r = requests.post(f"{url}/message/unreact", json=unreact_payload)
    assert r.status_code == 400
