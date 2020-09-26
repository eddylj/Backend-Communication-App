import channels
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
    
    assert channels_listall(token) == channel_list

    

