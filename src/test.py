import auth, channel, channels
import pytest
from data import data
from error import InputError, AccessError
from other import clear

# CHANNELS_CREATE TESTS

# Base Case

user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
auth.auth_register(*user)
token = user[0]
name = 'Channel 1'
channel_id = channels.channels_create(token, name, True) 
assert data['channels'] == [
    {
        'id' : channel_id['id'], 
        'name' : name, 
        'owners' : ['validemail@gmail.com'], 
        'members' : ['validemail@gmail.com'],
    }
]


# Will fail, because name is longer than 20 characters
user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
auth.auth_register(*user)
token = user[0]
name = 'Channel 1234567890abcdef'
with pytest.raises(InputError):
    channels.channels_create(token, name, True)
clear()

# CHANNELS_LISTALL TEST\
user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
auth.auth_register(*user)
token = user[0]

name1 = 'Channel 1'
id1 = channels.channels_create(token, name1, True)

name2 = 'Channel 2'
id2 = channels.channels_create(token, name2, True)

name3 = 'Channel 3'
id3 = channels.channels_create(token, name3, True)

channel_list = [
    {
        'id' : id1['id'],
        'name' : name1,
        'owners' : ['validemail@gmail.com'],
        'members' : ['validemail@gmail.com'],
    },
    {
        'id' : id2['id'],
        'name' : name2,
        'owners' : ['validemail@gmail.com'],
        'members' : ['validemail@gmail.com'],
    },
    {
        'id' : id3['id'],
        'name' : name3,
        'owners' : ['validemail@gmail.com'],
        'members' : ['validemail@gmail.com'],
    }
]

assert channels.channels_listall(token) == channel_list

clear()