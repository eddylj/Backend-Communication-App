import auth, channel, channels
import pytest
from error import InputError, AccessError
from other import clear

# CHANNEL_MESSAGES TESTS

# BASE TEST - Valid channel with no messages
def test_channel_messages_valid():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']
    
    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token, channel_id, 0) == passed
    clear()
    
# INVALID CHANNEL
def test_channel_messages_invalid_channel():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, 0)
    clear()

# INVALID START PARAMETER
def test_channel_messages_invalid_start():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    with pytest.raises(InputError):
        # Start > total # of messages in channel
        channel.channel_messages(token, channel_id, 50)
        
        # Start < 0
        channel.channel_messages(token, channel_id, -1)
    clear()

# INACCESSBILE CHANNEL
def test_channel_messages_no_access():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    token2 = auth.auth_register(*user2)['token']
    
    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token1, channel_id, 0) == passed
    with pytest.raises(AccessError):
        channel.channel_messages(token2, channel_id, 0)
    clear()

# Can't implement other cases without messages_send(), which isn't in iter1?

# VALID CHANNEL WITH MESSAGES
# START > NON-ZERO NUMBER OF MESSAGES IN CHANNEL
# CHECKING IF RETURNED START/END IS CORRECT
# CHECKING RETURNED MESSAGES ATTRIBUTES

# CHANNEL_LEAVE TESTS

# BASE TEST
def test_channel_leave_valid():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    token2 = auth.auth_register(*user2)['token']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    channel.channel_join(token2, channel_id)
    channel.channel_leave(token2, channel_id)

    user1_details = {
        'u_id': '1',
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details],
        'all_members': [user1_details]
    }

    assert channel.channel_details(token1, channel_id) == passed
    clear()

# INVALID CHANNEL
def test_channel_leave_invalid_channel():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id') + 1 # Does this work?
    with pytest.raises(InputError):
        channel.channel_leave(token, channel_id)

# TRYING TO LEAVE A CHANNEL WHICH USER IS NOT IN
def test_channel_leave_not_member():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    token2 = auth.auth_register(*user2)['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')
    
    with pytest.raises(AccessError):
        channel.channel_leave(token2, channel_id)
    


# CHANNEL_DETAILS TEST
def test_channel_details():

    # Register two users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user1)
    token1 = user1[0]

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    auth.auth_register(*user2)
    token2 = user2[0] 

    # Create a channel with user1
    channel_id = channels.channels_create(token1, "Test Channel", True)

    user1_details = {
        'u_id': 1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': 2,
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

    channel.channel_invite(token1, channel_id, user2_details['u_id'])

    passed = {
        'name': 'Test Channel',
        'owner_members': [user1_details],
        'all_members': [user1_details, user2_details],
    }

    assert channel.channel_details(token1, channel_id) == passed

    clear()


# CHANNEL_JOIN TESTS

# BASE TEST
def test_channel_join_valid():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    token2 = auth.auth_register(*user2)['token']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    channel.channel_join(token2, channel_id)

    user1_details = {
        'u_id': 1,
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': 2,
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details], #, user2_details], only one owner?
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed

# INVALID CHANNEL
def test_channel_join_invalid_channel():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_join(token, channel_id)

# PRIVATE CHANNEL
def test_channel_join_private_channel():
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account = auth.auth_register(*user2)
    token2 = account['token']
    u_id2 = account['u_id']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')
    
    with pytest.raises(AccessError):
        channel.channel_join(token2, channel_id)
    
    channel.channel_addowner(token1, channel_id, u_id2)
    channel.channel_join(token2, channel_id)

    user1_details = {
        'u_id': '1',
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user2_details = {
        'u_id': '2',
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    passed = {
        'name': 'test channel',
        'owner_members': [user1_details, user2_details],
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed
    
    clear()