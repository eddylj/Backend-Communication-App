'''
Tests for all functions in user.py
'''
import pytest
import server
import json
import requests
from echo_http_test import url

BASE_URL = 'http://127.0.0.1:9557'

def test_auth_base(url):
    '''
    Base test for auth functions
    '''

    # Create user1
    dataIn = {
        'email' : 'validemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'Howard',
        'name_last' : 'Dwight',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user1 = r.json()

    assert user1['u_id'] == 0
    assert user1['token'] == '0'

    # Create user2
    dataIn = {
        'email' : 'alsovalidemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'West',
        'name_last' : 'Delonte',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user2 = r.json()

    assert user2['u_id'] == 1
    assert user2['token'] == '1'

    # Logout user1 (successful)

    dataIn = {
        'token' : user1['token']
    }

    r = requests.post(f"{BASE_URL}/auth/logout", json=dataIn)
    payload = r.json()

    assert payload['is_success'] == True

    # Logout user1 again (fail)

    r = requests.post(f"{BASE_URL}/auth/logout", json=dataIn)
    payload = r.json()

    assert payload['is_success'] == False

    # Logout user2

    dataIn = {
        'token' : user2['token']
    }

    r = requests.post(f"{BASE_URL}/auth/logout", json=dataIn)
    payload = r.json()

    assert payload['is_success'] == True

    # Login user1

    dataIn = {
        'email' : 'validemail@gmail.com',
        'password' : 'asdfqwer1234',
    }

    r = requests.post(f"{BASE_URL}/auth/login", json=dataIn)
    payload = r.json()

    assert payload['u_id'] == 0
    assert payload['token'] == '0'

    # Logout user1
    dataIn = {
        'token' : user1['token']
    }

    r = requests.post(f"{BASE_URL}/auth/logout", json=dataIn)
    payload = r.json()

    assert payload['is_success'] == True

def test_channels_base(url):
    '''
    Base test for channel functions
    '''
    
    # Create user1
    dataIn = {
        'email' : 'validemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'Howard',
        'name_last' : 'Dwight',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user1 = r.json()

    assert user1['u_id'] == 0
    assert user1['token'] == '0'

    # Create user2
    dataIn = {
        'email' : 'alsovalidemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'West',
        'name_last' : 'Delonte',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user2 = r.json()

    assert user2['u_id'] == 1
    assert user2['token'] == '1'


    # Create a channel with user1

    dataIn = {
        'token' : user1['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    r = requests.post(f"{BASE_URL}/channels/create", json=dataIn)
    channel_id1 = r.json()['channel_id']

    assert channel_id1 == 0

    # Create a channel with user2

    dataIn = {
        'token' : user2['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    r = requests.post(f"{BASE_URL}/channels/create", json=dataIn)
    channel_id2 = r.json()['channel_id']

    assert channel_id2 == 1

    # List user2 channels

    # dataIn = {
    #     'token' : user2['token']
    # }

    r = requests.get(f"{BASE_URL}/channels/list?token={user2['token']}")
    payload = r.json()
    assert payload == {
        'channels' : [
            {
                'channel_id' : 1,
                'name' : 'Channel 2'
            }
        ]
    }

    # Listall channels

    dataIn = {
        'token' : user2['token']
    }

    r = requests.get(f"{BASE_URL}/channels/listall?token={user2['token']}")
    payload = r.json()
    assert payload == {
        'channels' : [
            {
                'channel_id' : 0,
                'name' : 'Channel 1'
            },
            {
                'channel_id' : 1,
                'name' : 'Channel 2'
            }
        ]
    }

def test_channel_base(url):
    '''
    Base test for channel functions
    '''

    # Create user1
    dataIn = {
        'email' : 'validemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'Howard',
        'name_last' : 'Dwight',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user1 = r.json()

    assert user1['u_id'] == 0
    assert user1['token'] == '0'

    # Create user2
    dataIn = {
        'email' : 'alsovalidemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'West',
        'name_last' : 'Delonte',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user2 = r.json()

    assert user2['u_id'] == 1
    assert user2['token'] == '1'

    # Create channel 1 with user1 

    dataIn = {
        'token' : user1['token'],
        'name' : 'Channel 1',
        'is_public' : False
    }

    r = requests.post(f"{BASE_URL}/channels/create", json=dataIn)
    channel_id1 = r.json()['channel_id']

    assert channel_id1 == 0

    # Create channel 2 with user2

    dataIn = {
        'token' : user2['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    r = requests.post(f"{BASE_URL}/channels/create", json=dataIn)
    channel_id2 = r.json()['channel_id']

    assert channel_id2 == 1

    # List details of channel1 with user1 

    # dataIn = {
    #     'token' : user1['token'],
    #     'channel_id' : channel_id1
    # }

    r = requests.get(f"{BASE_URL}/channel/details?token={user1['token']}&channel_id={channel_id1}")
    payload = r.json()
    assert payload == {
        'name' : 'Channel 1',
        'owner_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
        'all_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
    }

    # Invite user2 into channel1

    dataIn = {
        'token' : user1['token'],
        'channel_id' : channel_id1,
        'u_id' : user2['u_id']
    }

    requests.post(f"{BASE_URL}/channel/invite", json=dataIn)

    # List details of channel1 with user2

    # dataIn = {
    #     'token' : user1['token'],
    #     'channel_id' : channel_id1
    # }

    r = requests.get(f"{BASE_URL}/channel/details?token={user1['token']}&channel_id={channel_id1}")
    payload = r.json()
    assert payload == {
        'name' : 'Channel 1',
        'owner_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
        'all_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            },
            {
                'u_id' : 1,
                'name_first' : 'West',
                'name_last' : 'Delonte'
            }
        ],
    }

    # Leave channel1 with user2

    dataIn = {
        'token' : user2['token'],
        'channel_id' : channel_id1,
    }

    requests.post(f"{BASE_URL}/channel/leave", json=dataIn)

    # Join channel1 with user2 (fail)

    # dataIn = {
    #     'token' : user2['token'],
    #     'channel_id' : channel_id1,
    # }

    # with pytest.raises(InputError):
    #     requests.post(f"{BASE_URL}/channel/leave", json=dataIn).json()

    # Join channel2 with user1

    dataIn = {
        'token' : user1['token'],
        'channel_id' : channel_id2,
    }

    requests.post(f"{BASE_URL}/channel/join", json=dataIn)

    # Addowner user2 into channel1

    dataIn = {
        'token' : user1['token'],
        'channel_id' : channel_id1,
        'u_id' : user2['u_id']
    }

    requests.post(f"{BASE_URL}/channel/addowner", json=dataIn)    

    # List details with user1 channel1

    # dataIn = {
    #     'token' : user1['token'],
    #     'channel_id' : channel_id1
    # }

    r = requests.get(f"{BASE_URL}/channel/details?token={user1['token']}&channel_id={channel_id1}")
    payload = r.json()
    assert payload == {
        'name' : 'Channel 1',
        'owner_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            },
            {
                'u_id' : 1,
                'name_first' : 'West',
                'name_last' : 'Delonte'
            }
        ],
        'all_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
    }    

    # Removeowner user2 from channel1

    dataIn = {
        'token' : user1['token'],
        'channel_id' : channel_id1,
        'u_id' : user2['u_id']
    }

    requests.post(f"{BASE_URL}/channel/removeowner", json=dataIn)  

    # List details with user1 channel

    # dataIn = {
    #     'token' : user1['token'],
    #     'channel_id' : channel_id1
    # }

    r = requests.get(f"{BASE_URL}/channel/details?token={user1['token']}&channel_id={channel_id1}")
    payload = r.json()
    assert payload == {
        'name' : 'Channel 1',
        'owner_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
        'all_members' : [
            {
                'u_id' : 0,
                'name_first' : 'Howard',
                'name_last' : 'Dwight'
            }
        ],
    }        


def test_user_base(url):
    
    '''
    Base test for user functions
    '''

    # Create user1
    dataIn = {
        'email' : 'validemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'Howard',
        'name_last' : 'Dwight',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user1 = r.json()

    assert user1['u_id'] == 0
    assert user1['token'] == '0'

    # Create user2
    dataIn = {
        'email' : 'alsovalidemail@gmail.com',
        'password' : 'asdfqwer1234',
        'name_first' : 'West',
        'name_last' : 'Delonte',
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=dataIn)
    user2 = r.json()

    assert user2['u_id'] == 1
    assert user2['token'] == '1'


    # Get profile of user1

    dataIn = {
        'token' : user1['token'],
        'u_id' : u_id1['u_id']
    }

    r = request.get(f"{BASE_URL}/user/profile", json=dataIn)
    payload = r.json()
    assert payload == {
        'u_id' : 0,
        'email' : 'validemail@gmail.com',
        'name_first' : 'Howard',
        'name_last' : 'Dwight',
        'handle_str' : user1['handle'], # not sure bout this handle        
    }

    # change name for user1 in profile

    dataIn = {
        'token' : user1['token'],
        'name_first' : "Dawon",
        'name_last' : "Other"
    }

    r = request.put(f"{BASE_URL}/user/profile", json=dataIn)
    
    # change email for user1 in profile
    dataIn = {
         'token' : user1['token'],
         'email' : "randomemail@gmail.com"
    }

    r = request.put(f"{BASE_URL}/user/profile", json=dataIn)
    
    # change handle 
    dataIn = {
         'token' : user1['token'],
         'handle_str' : "Lavar Ball"
    }

    r = request.put(f"{BASE_URL}/user/profile", json=dataIn)

    # show the profile of user1 after change
    dataIn = {
        'token' : user1['token'],
        'u_id' : u_id1['u_id']
    }

    r = request.get(f"{BASE_URL}/user/profile", json=dataIn)
    payload = r.json()
    assert payload == {
        'u_id' : 0,
        'email' : 'randomemail@gmail.com',
        'name_first' : 'Dawon',
        'name_last' : 'Other',
        'handle_str' : 'Lavar Ball', # not sure bout this handle        
    }

    # list out all the users

    dataIn = {
        'token' : user1['token']
    }

    r = request.get(f"{BASE_URL}/user/profile", json=dataIn)
    payload = r.json()
    assert payload == {
        'users' : [
            { 
                'u_id' : 0,
                'email' : 'randomemail@gmail.com',
                'name_first' : 'Dawon',
                'name_last' : 'Other',
                'handle_str' : 'Lavar Ball'
            },
            {
                'u_id' : 1,
                'email' : 'alsovalidemail@gmail.com',
                'name_first' : 'West',
                'name_last' : 'Delonte',
                'handle_str' : user2['handle']


            }
        ]
    }




    

    


    

