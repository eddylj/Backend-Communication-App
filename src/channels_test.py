import auth, channel, channels
import pytest
from error import InputError, AccessError

# Base Case
def channels_create_success():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = user[0]
    name = "Channel 1"
    channel_id = channels.channels_create(token, name, True) 
    assert channels[0] == {"id" : channel_id, "name" : name,}

# Will fail, because name is longer than 20 characters
def channels_create_fail():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = user[0]
    name = "Channel 1234567890abcdef"
    with pytest.raises(InputError):
        channels.channels_create(token, name, True)

# Base Case for channels_listall
def channels_listall_base():
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = users[0]

    name1 = "Channel 1"
    id1 = channels.channels_create(token, name1, True)

    name2 = "Channel 2"
    id2 = channels.channels_create(token, name2, True)

    name3 = "Channel 3"
    id3 = channels.channels_create(token, name3, True)

    channel_list = [
        {
            "id" = id1,
            "name" = name1,
        },
        {
            "id" = id2,
            "name" = name2,
        },
        {
            "id" = id3,
            "name" = name3,
        }
    ]
    
    assert channels.channels_listall(token) == channel_list

def channels_list_base():
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    {u_id1, token1} = auth.auth_register(*user1)
    

    user2 = ('goodemail@gmail.com', '123abc!@#', 'LeBron', 'James')
    {u_id2, token2} = auth.auth_register(*user2)

    empty_channels_list = [
        {
        }
    ]

    # Assert no channels listed right now
    assert channels.channels_list(token1) == empty_channels_list
    assert channels.channels_list(token2) == empty_channels_list

    # Create a channel with user1
    channel_id = channels.channels_create(token1, "Test Channel", True)

    channel_list = [
        {
            "id" = channel_id
            "name" = "Test Channel"
        }
    ]

    # Assert only user 1 can see the channel
    assert channels.channels_list(token2) == channel_list
    assert channels.channels_list(token2) == empty_channels_list
    
    # Invite user 2
    channel.channel_invite(token1, channel_id, u_id2)

    # Assert both users can see the channel
    assert channels.channels_list(token2) == channel_list
    assert channels.channels_list(token2) == channel_list