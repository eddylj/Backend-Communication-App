import auth, channel, channels
import pytest
from data import data
from error import InputError, AccessError
from other import clear

# CHANNELS_CREATE TESTS

# Base Case
def test_channels_create_success():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Create channels
    channels.channels_create(token, 'Channel 1', True)
    assert len(channels.channels_list(token)['channels']) == 1
    channels.channels_create(token, 'Channel 2', True)
    assert len(channels.channels_list(token)['channels']) == 2

# Channel name > 20 characters
def test_channels_create_fail():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Invalid name (too long)
    name = 'Channel 1234567890abcdef'
    with pytest.raises(InputError):
        channels.channels_create(token, name, True)

# CHANNELS_LISTALL TEST
def test_channels_listall_base():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Create channels
    name1 = 'Channel 1'
    channel_id1 = channels.channels_create(token, name1, True)

    name2 = 'Channel 2'
    channel_id2 = channels.channels_create(token, name2, True)

    name3 = 'Channel 3'
    channel_id3 = channels.channels_create(token, name3, True)

    channel_list = [
        {
            'channel_id': channel_id1['channel_id'],
            'name': name1,
        },
        {
            'channel_id': channel_id2['channel_id'],
            'name': name2,
        },
        {
            'channel_id': channel_id3['channel_id'],
            'name': name3,
        }
    ]
    
    assert channels.channels_listall(token) == {'channels': channel_list}


# CHANNELS_LIST TEST

def test_channels_list_base():
    clear()

    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token1 = auth.auth_register(*user1)['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    empty_channels_list = [
    ]

    # Assert no channels listed right now
    assert channels.channels_list(token1) == {'channels': empty_channels_list}
    assert channels.channels_list(token2) == {'channels': empty_channels_list}

    # Create a channel with user1
    channel_id = channels.channels_create(token1, 'Test Channel', True)

    channel_list = [
        {
            'channel_id': channel_id['channel_id'],
            'name': 'Test Channel',
        }
    ]

    # Assert only user 1 can see the channel
    assert channels.channels_list(token1) == {'channels': channel_list}
    assert channels.channels_list(token2) == {'channels': empty_channels_list}
    
    # Invite user 2
    channel.channel_invite(token1, channel_id['channel_id'], u_id2)

    # Assert both users can see the channel
    assert channels.channels_list(token1) == {'channels': channel_list}
    assert channels.channels_list(token2) == {'channels': channel_list}

# Calling channels functions with invalid tokens
def test_channels_invalid_token():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Create a channel
    channels.channels_create(token, 'Channel 1', True) 

    # Deactivate token by logging out
    auth.auth_logout(token)

    # Cannot use when token is invalid
    with pytest.raises(AccessError):
        channels.channels_create(token, "Channel 2", True)

    with pytest.raises(AccessError):
        channels.channels_list(token)

    with pytest.raises(AccessError):
        channels.channels_listall(token)