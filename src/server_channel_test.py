<<<<<<< HEAD
'''
Tests for all functions in user.py
'''
import pytest
import server
import json
=======
"""
Tests for all functions in user.py
"""
>>>>>>> master
import requests
from echo_http_test import url

user = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}

############################# CHANNEL_INVITE TESTS #############################

# BASE CASE
def test_channel_invite_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_invite
    '''
=======
    """
    Base test for channel_invite
    """
>>>>>>> master

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    # create channel
    channel_payload = {
        'token' : account1['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()

<<<<<<< HEAD

=======
>>>>>>> master
    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }

    user2_details = {
        'u_id': account2['u_id'],
        'name_first': 'Goat',
        'name_last': 'James',
    }

    passed = {
        'name': 'Channel 1',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details]
    }

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel1['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

<<<<<<< HEAD

=======
>>>>>>> master
    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel1['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed


# # INVALID CHANNEL_ID
def test_channel_invite_channel_invalid_http(url):
<<<<<<< HEAD
    '''
    Test channel_invite fails if the channel is invalid
    '''
=======
    """
    Test channel_invite fails if the channel is invalid
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 1231512

    payload = {
        'token' : account['token'],
        'channel_id' : channel_id,
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/invite", json=payload)
    assert response.status_code == 400

# INVITING YOURSELF
def test_channel_invite_self_invite_http(url):
<<<<<<< HEAD
    '''
    Test channel_invite fails if you invite yourself
    '''
=======
    """
    Test channel_invite fails if you invite yourself
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    # create channel
    channel_payload = {
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()

    # invite yourself
    invite_payload = {
        'token' : account['token'],
        'channel_id' : channel1['channel_id'],
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/invite", json=invite_payload)
    assert response.status_code == 400

# INVITING WHILE NOT BEING A MEMBER
def test_channel_invite_non_member_http(url):
<<<<<<< HEAD
    '''
    Test channel_invite fails when you aren't a member of the channel being invite to
    '''
=======
    """
    Test channel_invite fails when you aren't a member of the channel being invite to
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    user3 = {
        'email': 'anothervalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Howard',
        'name_last': 'Dwight',
    }

    # Register user3
    req = requests.post(f"{url}/auth/register", json=user3)
    account3 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : False
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    # invite yourself
    invite_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account3['u_id']
    }

    response = requests.post(f"{url}/channel/invite", json=invite_payload)
    assert response.status_code == 400

# INVITING A PERSON THAT'S ALREADY A MEMBER
def test_channel_invite_already_member_http(url):
<<<<<<< HEAD
    '''
    Test channel_invite fails when you invite an existing member
    '''
=======
    """
    Test channel_invite fails when you invite an existing member
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

<<<<<<< HEAD
    join_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

=======
>>>>>>> master
    # invite yourself
    invite_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    response = requests.post(f"{url}/channel/invite", json=invite_payload)
    assert response.status_code == 200


############################ CHANNEL_MESSAGES TESTS ############################

# BASE CASE - Valid channel with no messages
def test_channel_messages_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_messages
    '''
=======
    """
    Base test for channel_messages
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_payload = {
        'token' : account['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()


    passed = {'messages': [], 'start': 0, 'end': -1}

    messages_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id'],
        'start' : 0
    }

    req = requests.get(f"{url}/channel/messages", params=messages_payload)
    messages = req.json()

    assert messages == passed

# INVALID CHANNEL
def test_channel_messages_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_messages fails when using an invalid channel
    '''
=======
    """
    Test channel_messages fails when using an invalid channel
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 123

    messages_payload = {
        'token' : account['token'],
        'channel_id' : channel_id,
        'start' : 0
    }

    response = requests.get(f"{url}/channel/messages", params=messages_payload)
    assert response.status_code == 400

# INVALID START PARAMETER
def test_channel_messages_invalid_start_http(url):
<<<<<<< HEAD
    '''
    Test channel_messages fails when having an invalid start
    '''
=======
    """
    Test channel_messages fails when having an invalid start
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_payload = {
        'token' : account['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()


    messages_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id'],
        'start' : 50
    }

    response = requests.get(f"{url}/channel/messages", params=messages_payload)
    assert response.status_code == 400

    messages_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id'],
        'start' : -1
    }

    response = requests.get(f"{url}/channel/messages", params=messages_payload)
    assert response.status_code == 400


# INACCESSBILE CHANNEL
def test_channel_messages_no_access_http(url):
<<<<<<< HEAD
    '''
    Test channel_messages fails when channel is not public
    '''
=======
    """
    Test channel_messages fails when channel is not public
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()


    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : False
    }
    # Create channel
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    passed = {'messages': [], 'start': 0, 'end': -1}

    # pass
    messages_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'start' : 0
    }

    req = requests.get(f"{url}/channel/messages", params=messages_payload)
    messages = req.json()

    assert messages == passed

    # fail
    messages_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'start' : 0
    }

    response = requests.get(f"{url}/channel/messages", params=messages_payload)
    assert response.status_code == 400


############################# CHANNEL_LEAVE TESTS ##############################

# BASE CASE
def test_channel_leave_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_leave
    '''
=======
    """
    Base test for channel_leave
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()


    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }
    # Create channel
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    user2_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=user2_payload)
    requests.post(f"{url}/channel/leave", json=user2_payload)

    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details]
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed

# INVALID CHANNEL
def test_channel_leave_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_leave fails when invalid channel
    '''
=======
    """
    Test channel_leave fails when invalid channel
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_payload = {
        'token' : account['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    # Create channel
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    leave_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id'] + 1
    }

    response = requests.post(f"{url}/channel/leave", json=leave_payload)
    assert response.status_code == 400

    # new_channel = channels.channels_create(token, 'test channel', True)
    # channel_id = new_channel['channel_id'] + 1 # Does this work?
    # with pytest.raises(InputError):
    #     channel.channel_leave(token, channel_id)

# TRYING TO LEAVE A CHANNEL WHICH USER IS NOT IN
def test_channel_leave_not_member_http(url):
<<<<<<< HEAD
    '''
    Test channel_leave fails when a user is not in it already
    '''
=======
    """
    Test channel_leave fails when a user is not in it already
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : False
    }

    # Create channel
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    leave_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    response = requests.post(f"{url}/channel/leave", json=leave_payload)
    assert response.status_code == 400


############################ CHANNEL_DETAILS TESTS #############################

# BASE CASE
def test_channel_details_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_details
    '''
=======
    """
    Base test for channel_details
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'Test Channel',
        'is_public' : True
    }

    # Create channel
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()


    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': account2['u_id'],
        'name_first': 'Goat',
        'name_last': 'James',
    }

    passed = {
        'name': 'Test Channel',
        'owner_members': [user1_details],
        'all_members': [user1_details],
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed

    # invite user2
    invite_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/invite", json=invite_payload)

    passed = {
        'name': 'Test Channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details],
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed

# INVALID CHANNEL
def test_channel_details_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_details fails when invalid channel
    '''
=======
    """
    Test channel_details fails when invalid channel
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    channel_id = 1231

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel_id
    }

    response = requests.get(f"{url}/channel/details", params=details_payload)
    assert response.status_code == 400

# USER NOT A MEMBER
def test_channel_details_not_member_http(url):
<<<<<<< HEAD
    '''
    Test channel_details fails when the user is not a member of the channel
    '''
=======
    """
    Test channel_details fails when the user is not a member of the channel
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : False
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    details_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    response = requests.get(f"{url}/channel/details", params=details_payload)
    assert response.status_code == 400

############################# CHANNEL_JOIN TESTS ###############################

# BASE CASE
def test_channel_join_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_join
    '''
=======
    """
    Base test for channel_join
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)


    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': account2['u_id'],
        'name_first': 'Goat',
        'name_last': 'James',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details]
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed

# INVALID CHANNEL
def test_channel_join_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_join fails when and invalid channel is used
    '''
=======
    """
    Test channel_join fails when and invalid channel is used
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 123

    join_payload = {
        'token' : account['token'],
        'channel_id' : channel_id
    }

    response = requests.post(f"{url}/channel/join", json=join_payload)
    assert response.status_code == 400

# PRIVATE CHANNEL
def test_channel_join_private_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_join fails when the channel is private
    '''
=======
    """
    Test channel_join fails when the channel is private
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()


    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    response = requests.post(f"{url}/channel/join", json=join_payload)
    assert response.status_code == 200

# JOINING A CHANNEL USER IS ALREADY IN
def test_channel_join_already_member_http(url):
<<<<<<< HEAD
    '''
    Test channel_join fails when user is already a member
    '''
=======
    """
    Test channel_join fails when user is already a member
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_payload = {
        'token' : account['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id']
    }

    response = requests.post(f"{url}/channel/join", json=join_payload)
    assert response.status_code == 400

########################### CHANNEL_ADDOWNER TESTS #############################

# BASE CASE
def test_channel_addowner_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_addowner
    '''
=======
    """
    Base test for channel_addowner
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    addowner_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/addowner", json=addowner_payload)

    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': account2['u_id'],
        'name_first': 'Goat',
        'name_last': 'James',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details, user2_details],
        'all_members': [user1_details, user2_details]
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed


# INVALID CHANNEL
def test_channel_addowner_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_addowner fails when invalid channel
    '''
=======
    """
    Test channel_addowner fails when invalid channel
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 123

    addowner_payload = {
        'token' : account['token'],
        'channel_id' : channel_id,
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=addowner_payload)
    assert response.status_code == 400

# WHEN USER IS ALREADY AN OWNER OF THE CHANNEL
def test_channel_addowner_already_owner_http(url):
<<<<<<< HEAD
    '''
    Test channel_addowner fails when user is already an owner
    '''
=======
    """
    Test channel_addowner fails when user is already an owner
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_payload = {
        'token' : account['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    addowner_payload = {
        'token' : account['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=addowner_payload)
    assert response.status_code == 400


# WHEN AUTHORISED USER IS NOT AN OWNER AND ADDOWNERS THEMSELF
def test_channel_addowner_auth_self_http(url):
<<<<<<< HEAD
    '''
    Test channel_addowner fails when adding oneself
    '''
=======
    """
    Test channel_addowner fails when adding oneself
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    addowner_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=addowner_payload)
    assert response.status_code == 400

# WHEN AUTHORISED USER IS NOT AN OWNER AND ADDOWNERS ANOTHER USER
def test_channel_addowner_auth_not_owner_http(url):
<<<<<<< HEAD
    '''
    Test channel_addowner fails when the a non-owner tries to addowner
    '''
=======
    """
    Test channel_addowner fails when the a non-owner tries to addowner
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    user3 = {
        'email': 'anothervalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Howard',
        'name_last': 'Dwight',
    }

    # Register user3
    req = requests.post(f"{url}/auth/register", json=user3)
    account3 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    join_payload = {
        'token' : account3['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)


    addowner_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account3['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=addowner_payload)
    assert response.status_code == 400

########################## CHANNEL_REMOVEOWNER TESTS ###########################

# BASE CASE
def test_channel_removeowner_valid_http(url):
<<<<<<< HEAD
    '''
    Base test for channel_removeowner
    '''
=======
    """
    Base test for channel_removeowner
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    addowner_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/addowner", json=addowner_payload)

    removeowner_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account1['u_id']
    }

    requests.post(f"{url}/channel/removeowner", json=removeowner_payload)

    user1_details = {
        'u_id': account1['u_id'],
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': account2['u_id'],
        'name_first': 'Goat',
        'name_last': 'James',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user2_details],
        'all_members': [user1_details, user2_details]
    }

    details_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert details == passed

# INVALID CHANNEL
def test_channel_removeowner_invalid_channel_http(url):
<<<<<<< HEAD
    '''
    Test channel_removeowner fails when invalid channel
    '''
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 123

    removeowner_payload = {
        'token' : account['token'],
        'channel_id' : channel_id,
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/removeowner", json=removeowner_payload)
    assert response.status_code == 400

# INVALID CHANNEL
def test_channel_removeowner_invalid_channel_http(url):
    '''
    Test channel_removeowner fails when invalid channel
    '''

=======
    """
    Test channel_removeowner fails when invalid channel
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    channel_id = 123

    removeowner_payload = {
        'token' : account['token'],
        'channel_id' : channel_id,
        'u_id' : account['u_id']
    }

    response = requests.post(f"{url}/channel/removeowner", json=removeowner_payload)
    assert response.status_code == 400

# WHEN AUTHORISED USER IS NOT AN OWNER REMOVE ANOTHER OWNER
def test_channel_removeowner_not_owner_http(url):
<<<<<<< HEAD
    '''
    Test channel_removeowner fails when not an owner
    '''
=======
    """
    Test channel_removeowner fails when not an owner
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    user3 = {
        'email': 'alsoalsovalidemail@gmail.com',
        'password': '23Goat!@#',
        'name_first': 'Calf',
        'name_last': 'James',
    }

    # Register user3
    req = requests.post(f"{url}/auth/register", json=user3)
    account3 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    addowner_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }
    requests.post(f"{url}/channel/addowner", json=addowner_payload)

    join_payload = {
        'token' : account3['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    removeowner_payload = {
        'token' : account3['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=removeowner_payload)
    assert response.status_code == 400

# REMOVING THEMSELVES AS OWNER
def test_channel_removeowner_auth_self_http(url):
<<<<<<< HEAD
    '''
    Test channel_removeowner fails when removing themselves as owner
    '''
=======
    """
    Test channel_removeowner fails when removing themselves as owner
    """
>>>>>>> master
    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account1['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    addowner_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }
    requests.post(f"{url}/channel/addowner", json=addowner_payload)

    removeowner_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    response = requests.post(f"{url}/channel/addowner", json=removeowner_payload)
    assert response.status_code == 400

# REMOVING LAST OWNER AS GLOBAL OWNER
def test_channel_removeowner_last_owner_http(url):
<<<<<<< HEAD
    '''
    Test channel_removeowner fails when global owner
    '''
=======
    """
    Test channel_removeowner fails when global owner
    """
>>>>>>> master

    # Register user1
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    user2 = {
        'email': 'alsovalidemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Goat',
        'name_last': 'James',
    }

    # Register user2
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    channel_payload = {
        'token' : account2['token'],
        'name' : 'test channel',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel = req.json()

    join_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }

    requests.post(f"{url}/channel/join", json=join_payload)

    removeowner_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/removeowner", json=removeowner_payload)
    # assert len(channel.channel_details(token2, channel_id)['owner_members']) == 0

    details_payload = {
        'token' : account2['token'],
        'channel_id' : channel['channel_id']
    }
<<<<<<< HEAD

=======
    leave_payload = {
        'token' : account1['token'],
        'channel_id' : channel['channel_id']
    }
    requests.post(f"{url}/channel/leave", json=leave_payload)
>>>>>>> master
    req = requests.get(f"{url}/channel/details", params=details_payload)
    details = req.json()

    assert len(details['owner_members']) == 0

