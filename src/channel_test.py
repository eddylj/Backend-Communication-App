import auth, channel, channels
import pytest
from error import InputError, AccessError

# CHANNEL_MESSAGES TESTS

# BASE TEST - Valid channel with no messages
def test_channel_messages_valid():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = user[0] # May change to auth_register().get
    
    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token, channel_id, 0) == passed
    
# INVALID CHANNEL
def test_channel_messages_invalid_channel():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = user[0] # May change to auth_register().get

    channel_id = 123
    with pytest.raises(InputError):
        channel.channel_messages(token, channel_id, 0)

# INVALID START PARAMETER
def test_channel_messages_invalid_start():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = user[0] # May change to auth_register().get

    new_channel = channels.channels_create(token, 'test channel', True)
    channel_id = new_channel.get('channel_id')

    with pytest.raises(InputError):
        # Start > total # of messages in channel
        channel.channel_messages(token, channel_id, 50)
        
        # Start < 0
        channel.channel_messages(token, channel_id, -1)

# INACCESSBILE CHANNEL
def test_channel_messages_no_access():
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user1)
    token1 = user1[0] # May change to auth_register().get

    new_channel = channels.channels_create(token1, 'test channel', False)
    channel_id = new_channel.get('channel_id')

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Heydan', 'Everest')
    auth.auth_register(*user2)
    token2 = user2[0] # May change to auth_register().get
    
    passed = {'messages': [], 'start': 0, 'end': -1}
    assert channel.channel_messages(token1, channel_id, 0) == passed
    with pytest.raises(AccessError):
        channel.channel_messages(token2, channel_id, 0)

# Can't implement other cases without messages_send(), which isn't in iter1?

# VALID CHANNEL WITH MESSAGES
# START > NON-ZERO NUMBER OF MESSAGES IN CHANNEL
# CHECKING IF RETURNED START/END IS CORRECT
# CHECKING RETURNED MESSAGES ATTRIBUTES