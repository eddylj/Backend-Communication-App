'''
Tests for all functions in user.py
'''
<<<<<<< HEAD
import pytest
import server
import json
=======
>>>>>>> master
import requests
from echo_http_test import url

user = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}


############################ CHANNELS_CREATE TESTS #############################
# Base Case
def test_channels_create_success_http(url):
    '''
    Base test for channels_create
    '''
    # register
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    # create channel
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

<<<<<<< HEAD
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()
=======
    requests.post(f"{url}/channels/create", json=channel_payload)
>>>>>>> master

    # list channels
    req = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    listed = req.json()

    assert len(listed['channels']) == 1

    # create channel2
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

<<<<<<< HEAD
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel2 = req.json()
=======
    requests.post(f"{url}/channels/create", json=channel_payload)
>>>>>>> master

    # list channels
    req = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    listed = req.json()

    assert len(listed['channels']) == 2

# Channel name > 20 characters
def test_channels_create_fail_http(url):
    '''
    Test channels_create fails with a name too long
    '''
    # register
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    # Invalid name (too long)
    channel_payload = {
        'token' : account['token'],
        'name' : 'Channel 1234567890abcdef',
        'is_public' : True
    }

    response = requests.post(f"{url}/channels/create", json=channel_payload)
    assert response.status_code == 400



############################ CHANNELS_LISTALL TESTS ############################

def test_channels_listall_base_http(url):
    '''
    Base test for channels_listall
    '''

    # register
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    # create channel1
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()

    # create channel2
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel2 = req.json()

    # create channel3
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 3',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel3 = req.json()

    # Assertion
    channel_list = [
        {
            'channel_id': channel1['channel_id'],
            'name': 'Channel 1',
        },
        {
            'channel_id': channel2['channel_id'],
            'name': 'Channel 2',
        },
        {
            'channel_id': channel3['channel_id'],
            'name': 'Channel 3',
        }
    ]

    req = requests.get(f"{url}/channels/listall", params={'token' : account['token']})
    lists = req.json()

    assert lists == {'channels': channel_list}

############################# CHANNELS_LIST TESTS ##############################

def test_channels_list_base_http(url):
    '''
    Base test for channels_list
    '''

    user2 = {
    'email': 'alsovalidemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Goat',
    'name_last': 'James',
    }

    # register
    req = requests.post(f"{url}/auth/register", json=user)
    account1 = req.json()

    # register
    req = requests.post(f"{url}/auth/register", json=user2)
    account2 = req.json()

    empty_channels_list = []


    # Assert no channels listed right now
    req = requests.get(f"{url}/channels/listall", params={'token' : account1['token']})
    lists = req.json()

    assert lists == {'channels': empty_channels_list}

    req = requests.get(f"{url}/channels/listall", params={'token' : account2['token']})
    lists = req.json()

    assert lists == {'channels': empty_channels_list}


    # Create a channel1 with user1
    channel_payload ={
        'token' : account1['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()


    channel_list = [
        {
            'channel_id': channel1['channel_id'],
            'name': 'Channel 1',
        }
    ]

    # Assert only user 1 can see the channel
    req = requests.get(f"{url}/channels/list", params={'token' : account1['token']})
    lists = req.json()

    assert lists == {'channels': channel_list}

    req = requests.get(f"{url}/channels/list", params={'token' : account2['token']})
    lists = req.json()

    assert lists == {'channels': empty_channels_list}


    # Invite user 2
    user_payload = {
        'token' : account1['token'],
        'channel_id' : channel1['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/invite", json=user_payload)


    # Assert both users can see the channel
    req = requests.get(f"{url}/channels/list", params={'token' : account1['token']})
    lists = req.json()

    assert lists == {'channels': channel_list}

    req = requests.get(f"{url}/channels/list", params={'token' : account2['token']})
    lists = req.json()

    assert lists == {'channels': channel_list}


# Calling channels functions with invalid tokens
def test_channels_invalid_token_http(url):
    '''
    Test channels_invalid fails with an invalid token
    '''

    # register
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()


    # Create a channel1 with user1
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

<<<<<<< HEAD
    req = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = req.json()

=======
    requests.post(f"{url}/channels/create", json=channel_payload)
>>>>>>> master

    # Deactivate token by logging out
    requests.post(f"{url}/auth/logout", json={'token': account['token']})

    # Cannot use when token is invalid
    channel_payload = {
        'token' : account['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    response = requests.post(f"{url}/channels/create", json=channel_payload)
    assert response.status_code == 400

    response = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    assert response.status_code == 400

    response = requests.get(f"{url}/channels/listall", params={'token' : account['token']})
    assert response.status_code == 400
