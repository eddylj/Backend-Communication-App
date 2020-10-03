
import auth, channel, channels
import pytest
from error import InputError, AccessError
from other import clear

# CHANNEL_INVITE TESTS

def test_channel_invite_valid():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
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

# assuming that the channel id aand u_id is a number


def test_channel_invite_channel_invalid():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    channel_id = 1231512

    with pytest.raises(InputError):
        channel.channel_invite(token1, channel_id, u_id1)

def test_channel_invite_self_invite():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']
   
    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']

    with pytest.raises(InputError):
        channel.channel_invite(token1, channel_id, u_id1)


# auth user is not already in channel 

def test_channel_invite_access_error():
    clear()
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')
    account3 = auth.auth_register(*user3)
    u_id3 = account3['u_id']

    channel_id = channels.channels_create(token1, 'test channel', False)['channel_id']

    with pytest.raises(AccessError):
        channel.channel_invite(token2, channel_id, u_id3)
     

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

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')
    
    with pytest.raises(AccessError):
        channel.channel_join(token2, channel_id)
    
# JOINING A CHANNEL USER IS ALREADY IN
def test_channel_join_already_member():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')
    with pytest.raises(InputError):
        channel.channel_join(token, channel_id)
    
# CHANNEL_ADDOWNER TESTS

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

# WHEN AUTHORISED USER IS NOT AN OWNER AND ADDOWNERS THEMSELF
def test_channel_addowner_auth_self():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
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
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    
    user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')
    account3 = auth.auth_register(*user3)
    token3 = account3['token']
    u_id3 = account3['u_id']

    new_channel = channels.channels_create(token1, 'test channel', True)
    channel_id = new_channel['channel_id']
    channel.channel_join(token2, channel_id)
    channel.channel_join(token3, channel_id)
    
    with pytest.raises(AccessError):
        channel.channel_addowner(token2, channel_id, u_id3)


# CHANNEL_REMOVEOWNER TESTS

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
    clear()

    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = 123

    with pytest.raises(InputError):
        channel.channel_removeowner(token, channel_id, u_id)
        
# WHEN AUTHORISED USER IS NOT AN OWNER REMOVE ANOTHER OWNER
def test_channel_removeowner_not_owner():
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']
    
    user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')
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
    clear()
    
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
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
    clear()

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    new_channel = channels.channels_create(token2, 'test channel', True)
    channel_id = new_channel['channel_id']

    channel.channel_join(token1, channel_id)

    with pytest.raises(InputError):
        channel.channel_removeowner(token1, channel_id, u_id2)