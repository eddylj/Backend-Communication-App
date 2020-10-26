'''
Tests to test the login, logout and register functions in channel.py
'''
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
from other import clear, SECRET

user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')

############################# CHANNEL_INVITE TESTS #############################

# BASE CASE
def test_channel_invite_valid():
    '''
    Base test for channel_invite
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    print(SECRET)
    print(token1)
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    print(token2)
    u_id2 = account2['u_id']

    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }

    user2_details = {
        'u_id': u_id2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }

    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details]
    }

    channel.channel_join(token2, channel_id)

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL_ID
def test_channel_invite_channel_invalid():
    '''
    Test channel_invite fails if the channel is invalid
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    u_id2 = account2['u_id']

    channel_id = 1231512

    with pytest.raises(InputError):
        channel.channel_invite(token1, channel_id, u_id2)

# INVALID U_ID
def test_channel_invite_user_invalid():
    '''
    Test if channel_invite fails if the u_id is invalid
    '''
    clear()
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = channels.channels_create(token, 'test channel', True)['channel_id']

    with pytest.raises(InputError):
        channel.channel_invite(token, channel_id, u_id + 1)

    with pytest.raises(InputError):
        channel.channel_invite(token, channel_id, u_id * -1)

# INVITING YOURSELF
def test_channel_invite_self_invite():
    '''
    Test channel_invite fails if you invite yourself
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']

    with pytest.raises(InputError):
        channel.channel_invite(token1, channel_id, u_id1)

# INVITING WHILE NOT BEING A MEMBER
def test_channel_invite_non_member():
    '''
    Test channel_invite fails when you aren't a member of the channel being invite to
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    account3 = auth.auth_register(*user3)
    u_id3 = account3['u_id']

    channel_id = channels.channels_create(token1, 'test channel', False)['channel_id']

    with pytest.raises(AccessError):
        channel.channel_invite(token2, channel_id, u_id3)

# INVITING A PERSON THAT'S ALREADY A MEMBER
def test_channel_invite_already_member():
    '''
    Test channel_invite fails when you invite an existing member
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']
    channel.channel_join(token2, channel_id)
    with pytest.raises(InputError):
        channel.channel_invite(token1, channel_id, u_id2)

############################ CHANNEL_MESSAGES TESTS ############################

# BASE CASE - Valid channel with no messages
def test_channel_messages_valid():
    '''
    Base test for channel_messages
    '''
    clear()
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token, channel_id, 0) == passed
    clear()

# INVALID CHANNEL
def test_channel_messages_invalid_channel():
    '''
    Test channel_messages fails when using an invalid channel
    '''
    clear()
    token = auth.auth_register(*user)['token']

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, 0)
    clear()

# INVALID START PARAMETER
def test_channel_messages_invalid_start():
    '''
    Test channel_messages fails when having an invalid start
    '''
    clear()
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    # Start > total # of messages in channel
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, 50)

    # Start < 0
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, -1)

# INACCESSBILE CHANNEL
def test_channel_messages_no_access():
    '''
    Test channel_messages fails when channel is not public
    '''
    clear()
    token1 = auth.auth_register(*user1)['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')

    token2 = auth.auth_register(*user2)['token']

    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token1, channel_id, 0) == passed
    with pytest.raises(AccessError):
        channel.channel_messages(token2, channel_id, 0)

def test_channel_messages_pagination():
    """
    Test case when start + 50 is less than total number of messages in channel.
    Non-negative end expected in that case.
    """
    clear()
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', False)
    channel_id = new_channel['channel_id']

    for _ in range(80):
        message.message_send(token, channel_id, "HELLO *ELLO HELLO")

    channel_messages = channel.channel_messages(token, channel_id, 20)
    assert len(channel_messages['messages']) == 50
    assert channel_messages['start'] == 20
    assert channel_messages['end'] == 70

############################# CHANNEL_LEAVE TESTS ##############################

# BASE CASE
def test_channel_leave_valid():
    '''
    Base test for channel_leave
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    account3 = auth.auth_register(*user3)
    token3 = account3['token']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    channel.channel_join(token2, channel_id)
    channel.channel_join(token3, channel_id)

    # Adds user2 to owners to check if they remain after they leave the channel.
    channel.channel_addowner(token1, channel_id, u_id2)
    channel.channel_leave(token2, channel_id)
    # User3 remains a normal member
    channel.channel_leave(token3, channel_id)

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details]
    }

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL
def test_channel_leave_invalid_channel():
    '''
    Test channel_leave fails when invalid channel
    '''
    clear()
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel['channel_id'] + 1 # Does this work?
    with pytest.raises(InputError):
        channel.channel_leave(token, channel_id)

# TRYING TO LEAVE A CHANNEL WHICH USER IS NOT IN
def test_channel_leave_not_member():
    '''
    Test channel_leave fails when a user is not in it already
    '''
    clear()
    token1 = auth.auth_register(*user1)['token']

    token2 = auth.auth_register(*user2)['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel['channel_id']

    with pytest.raises(AccessError):
        channel.channel_leave(token2, channel_id)

############################ CHANNEL_DETAILS TESTS #############################

# BASE CASE
def test_channel_details_valid():
    '''
    Base test for channel_details
    '''
    clear()
    # Register two users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    u_id2 = account2['u_id']

    # Create a channel with user1
    new_channel = channels.channels_create(token1, "Test Channel", True)
    channel_id = new_channel['channel_id']

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': u_id2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'Test Channel',
        'owner_members': [user1_details],
        'all_members': [user1_details],
    }
    # user1 owner, user1 member
    assert channel.channel_details(token1, channel_id) == passed

    channel.channel_invite(token1, channel_id, u_id2)

    passed = {
        'name': 'Test Channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details],
    }

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL
def test_channel_details_invalid_channel():
    '''
    Test channel_details fails when invalid channel
    '''
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = 1231

    with pytest.raises(InputError):
        channel.channel_details(token, channel_id)

# USER NOT A MEMBER
def test_channel_details_not_member():
    '''
    Test channel_details fails when the user is not a member of the channel
    '''
    clear()

    token1 = auth.auth_register(*user1)['token']

    token2 = auth.auth_register(*user2)['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel['channel_id']

    with pytest.raises(AccessError):
        channel.channel_details(token2, channel_id)

############################# CHANNEL_JOIN TESTS ###############################

# BASE CASE
def test_channel_join_valid():
    '''
    Base test for channel_join
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': u_id2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL
def test_channel_join_invalid_channel():
    '''
    Test channel_join fails when and invalid channel is used
    '''
    clear()
    token = auth.auth_register(*user)['token']

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_join(token, channel_id)

# PRIVATE CHANNEL
def test_channel_join_private_channel():
    '''
    Test channel_join fails when the channel is private
    '''
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')

    with pytest.raises(AccessError):
        channel.channel_join(token2, channel_id)

# JOINING A CHANNEL USER IS ALREADY IN
def test_channel_join_already_member():
    '''
    Test channel_join fails when user is already a member
    '''
    clear()
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    with pytest.raises(InputError):
        channel.channel_join(token, channel_id)

########################### CHANNEL_ADDOWNER TESTS #############################

# BASE CASE
def test_channel_addowner_valid():
    '''
    Base test for channel_addowner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token1, channel_id, u_id2)

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': u_id2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details, user2_details],
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed

 # INVALID CHANNEL
def test_channel_addowner_invalid_channel():
    '''
    Test channel_addowner fails when invalid channel
    '''
    clear()

    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = 123

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

# WHEN USER IS ALREADY AN OWNER OF THE CHANNEL
def test_channel_addowner_already_owner():
    '''
    Test channel_addowner fails when user is already an owner
    '''
    clear()

    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel['channel_id']

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

# WHEN AUTHORISED USER IS NOT AN OWNER AND ADDOWNERS THEMSELF
def test_channel_addowner_auth_self():
    '''
    Test channel_addowner fails when adding oneself
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)

    with pytest.raises(AccessError):
        channel.channel_addowner(token2, channel_id, u_id2)

# WHEN AUTHORISED USER IS NOT AN OWNER AND ADDOWNERS ANOTHER USER
def test_channel_addowner_auth_not_owner():
    '''
    Test channel_addowner fails when the a non-owner tries to addowner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    account3 = auth.auth_register(*user3)
    token3 = account3['token']
    u_id3 = account3['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_join(token3, channel_id)

    with pytest.raises(AccessError):
        channel.channel_addowner(token2, channel_id, u_id3)


########################## CHANNEL_REMOVEOWNER TESTS ###########################

# BASE CASE
def test_channel_removeowner_valid():
    '''
    Base test for channel_removeowner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token1, channel_id, u_id2)
    channel.channel_removeowner(token2, channel_id, u_id1)

    user1_details = {
        'u_id': u_id1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': u_id2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user2_details],
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL
def test_channel_removeowner_invalid_channel():
    '''
    Test channel_removeowner fails when invalid channel
    '''
    clear()

    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = 123

    with pytest.raises(InputError):
        channel.channel_removeowner(token, channel_id, u_id)

# WHEN AUTHORISED USER IS NOT AN OWNER
def test_channel_removeowner_not_owner():
    '''
    Test channel_removeowner fails when not an owner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    account3 = auth.auth_register(*user3)
    token3 = account3['token']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token1, channel_id, u_id2)
    channel.channel_join(token3, channel_id)

    with pytest.raises(AccessError):
        channel.channel_removeowner(token3, channel_id, u_id2)

# REMOVING THEMSELVES AS OWNER
def test_channel_removeowner_auth_self():
    '''
    Test channel_removeowner fails when removing themselves as owner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token1, channel_id, u_id2)

    with pytest.raises(InputError):
        channel.channel_removeowner(token2, channel_id, u_id2)

# REMOVING LAST OWNER AS GLOBAL OWNER
def test_channel_removeowner_last_owner():
    '''
    Test channel_removeowner fails when global owner
    '''
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token2, 'test channel', True)
    channel_id = new_channel['channel_id']

    channel.channel_join(token1, channel_id)

    channel.channel_removeowner(token1, channel_id, u_id2)
    assert len(channel.channel_details(token2, channel_id)['owner_members']) == 0

def test_channel_removeowner_nonowner():
    """
    Attempting to remove a non-owner/normal member.
    """
    clear()
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']

    channel.channel_join(token2, channel_id)

    with pytest.raises(InputError):
        channel.channel_removeowner(token1, channel_id, u_id2)

# Checking invalid token
def test_channel_invalid_token():
    '''
    Test for if token is invalid throughout all functions
    '''
    clear()

    # Create 2 users
    token1 = auth.auth_register(*user1)['token']

    account2 = auth.auth_register(*user2)
    u_id2 = account2['u_id']

    channel_id = channels.channels_create(token1, "Test Channel", True)['channel_id']

    # Deactivate token by logging out
    auth.auth_logout(token1)

    # Cannot use when token is invalid
    with pytest.raises(AccessError):
        channel.channel_invite(token1, channel_id, u_id2)

    with pytest.raises(AccessError):
        channel.channel_details(token1, channel_id)

    with pytest.raises(AccessError):
        channel.channel_messages(token1, channel_id, 0)

    with pytest.raises(AccessError):
        channel.channel_leave(token1, channel_id)

    with pytest.raises(AccessError):
        channel.channel_join(token1, channel_id)

    with pytest.raises(AccessError):
        channel.channel_addowner(token1, channel_id, u_id2)

    with pytest.raises(AccessError):
        channel.channel_removeowner(token1, channel_id, u_id2)

clear()
