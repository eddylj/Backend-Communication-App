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

    # Start > total # of messages in channel
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, 50)

    # Start < 0
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, -1)

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
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    channel.channel_join(token2, channel_id)
    channel.channel_leave(token2, channel_id)

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
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel['channel_id'] + 1 # Does this work?
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
    channel_id = new_channel['channel_id']
    
    with pytest.raises(AccessError):
        channel.channel_leave(token2, channel_id)
    


# CHANNEL_DETAILS TEST
def test_channel_details():
    clear()
    # Register two users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    u_id2 = account2['u_id']

    # Create a channel with user1
    channel_id = channels.channels_create(token1, "Test Channel", True)

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

# CHANNEL_JOIN TESTS

# BASE TEST
def test_channel_join_valid():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
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
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_join(token, channel_id)

# PRIVATE CHANNEL
def test_channel_join_private_channel():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')
    
    with pytest.raises(AccessError):
        channel.channel_join(token2, channel_id)
    
    channel.channel_addowner(token1, channel_id, u_id2)
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
        'owner_members': [user1_details, user2_details],
        'all_members': [user1_details, user2_details]
    }

    assert channel.channel_details(token1, channel_id) == passed
    
# ADDOWNER TESTS

# BASE TEST
def test_channel_addowner_valid():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token2, channel_id, u_id2)

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
    clear()

    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = 123

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

# WHEN USER IS ALREADY AN OWNER OF THE CHANNEL
def test_channel_addowner_already_owner():
    clear()

    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel['channel_id']

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

# WHEN AUTHORISED USER IS NOT AN OWNER
def test_channel_addowner_auth_not_owner():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    
    with pytest.raises(AccessError):
        channel.channel_addowner(token2, channel_id, u_id2)


# REMOVEOWNER TESTS

# BASE CASE
def test_channel_removeowner_valid():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_addowner(token2, channel_id, u_id2)
    channel.channel_removeowner(token1, channel_id, u_id1)

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
    clear()

    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = 123

    with pytest.raises(InputError):
        channel.channel_removeowner(token, channel_id, u_id)

# WHEN USER IS NOT AN OWNER
def test_channel_removeowner_not_owner():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)

    with pytest.raises(InputError):
        channel.channel_removeowner(token2, channel_id, u_id2)

# WHEN AUTHORISED USER IS NOT AN OWNER
def test_channel_removeowner_auth_not_owner():
    clear()
    
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    
    with pytest.raises(AccessError):
        channel.channel_removeowner(token2, channel_id, u_id2)