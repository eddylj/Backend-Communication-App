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

    # Create a channel
    name = 'Channel 1'
    channel_id = channels.channels_create(token, name, True) 
    assert data['channels'] == [
        {
            'channel_id' : channel_id['channel_id'], 
            'name' : name, 
            'owners' : [0], 
            'members' : [0],
            'is_public' : True,
            'messages' : [],
        }
    ]


# Will fail, because name is longer than 20 characters
def test_channels_create_fail():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Invalid name (too long)
    name = 'Channel 1234567890abcdef'
    with pytest.raises(InputError):
        channels.channels_create(token, name, True)

    # User logged out
    auth.auth_logout(token)

    name = 'Channel'
    with pytest.raises(AccessError):
        channels.channels_create(token, name, True)

# CHANNELS_LISTALL TEST
def test_channels_listall_base():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Create channels
    name1 = 'Channel 1'
    id1 = channels.channels_create(token, name1, True)

    name2 = 'Channel 2'
    id2 = channels.channels_create(token, name2, True)

    name3 = 'Channel 3'
    id3 = channels.channels_create(token, name3, True)

    channel_list = [
        {
            'channel_id' : id1['channel_id'],
            'name' : name1,
        },
        {
            'channel_id' : id2['channel_id'],
            'name' : name2,
        },
        {
            'channel_id' : id3['channel_id'],
            'name' : name3,
        }
    ]
    
    assert channels.channels_listall(token) == { 'channels' : channel_list}


# CHANNELS_LIST TEST

def test_channels_list_base():
    clear()

    # Create users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    u_id1 = 0
    token1 = auth.auth_register(*user1)['token']

    user2 = ('goodemail@gmail.com', '123abc!@#', 'LeBron', 'James')
    u_id2 = 1
    token2 = auth.auth_register(*user2)['token']

    empty_channels_list = [
    ]

    # Assert no channels listed right now
    assert channels.channels_list(token1) == { 'channels' : empty_channels_list}
    assert channels.channels_list(token2) == { 'channels' : empty_channels_list}

    # Create a channel with user1
    channel_id = channels.channels_create(token1, 'Test Channel', True)

    channel_list = [
        {
            'channel_id' : channel_id['channel_id'],
            'name' : 'Test Channel',
        }
    ]

    # Assert only user 1 can see the channel
    assert channels.channels_list(token1) == { 'channels' : channel_list}
    assert channels.channels_list(token2) == { 'channels' : empty_channels_list}
    
    # Invite user 2
    channel.channel_invite(token1, channel_id['channel_id'], u_id2)

    # Assert both users can see the channel
    assert channels.channels_list(token1) == { 'channels' : channel_list}
    assert channels.channels_list(token2) == { 'channels' : channel_list}


# Breaks if the user is inactive (logged out)

def test_channels_list_listall_inactive():
    clear()

    # Create a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Create a channel
    name = 'Channel 1'
    channel_id = channels.channels_create(token, name, True) 
    assert data['channels'] == [
        {
            'channel_id' : channel_id['channel_id'], 
            'name' : name, 
            'owners' : [0], 
            'members' : [0],
            'is_public' : True,
            'messages' : [],
        }
    ]

    # If user becomes inactive
    auth.auth_logout(token)

    # Cannot use channels_list nor channels_listall
    with pytest.raises(AccessError):
        channels.channels_list(token)

    with pytest.raises(AccessError):
        channels.channels_listall(token)