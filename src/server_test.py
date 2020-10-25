'''
Tests for all functions in user.py
'''
import pytest
import server
import json
import requests
from echo_http_test import url

user = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}

############################### AUTH_LOGIN TESTS ###############################

# BASE TEST - VALID EMAIL
def test_auth_login_user_email_http(url):
    '''
    Base test for auth_login
    '''
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

    requests.post(f"{url}/auth/logout", json={'token': account['token']})

    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
    r = requests.post(f"{url}/auth/login", json=login_payload)
    login = r.json()

    assert login['u_id'] == account['u_id']

# INVALID EMAIL
def test_auth_login_invalid_email_http(url):
    '''
    Test auth_login fails using an invalid email
    '''
    invalid_email = {
        'email': 'invalidemail.com',
        'password': '123abc!@#'
    }
    response = requests.post(f"{url}/auth/login", json=invalid_email)
    assert response.status_code == 400

# NON USER EMAIL
def test_auth_login_non_user_email_http(url):
    '''
    Test auth_login fails using using an email belonging to noone
    '''
    requests.post(f"{url}/auth/register", json=user)

    non_user_email = {
        'email': 'nonuseremail@gmail.com',
        'password': '123abc!@#'
    }
    response = requests.post(f"{url}/auth/login", json=non_user_email)
    assert response.status_code == 400

# WRONG PASSWORD
def test_auth_login_wrong_password_http(url):
    '''
    Test auth_login fails using the wrong password
    '''
    requests.post(f"{url}/auth/register", json=user)

    wrong_password = {
        'email': user['email'],
        'password': user['password'] + 'salt'
    }
    response = requests.post(f"{url}/auth/login", json=wrong_password)
    assert response.status_code == 400

############################## AUTH_REGISTER TESTS #############################

# BASE TEST - Valid user registration
def test_auth_register_valid_http(url):
    '''
    Base test for auth_register
    '''
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
    requests.post(f"{url}/auth/login", json=login_payload)
    response = requests.post(f"{url}/auth/logout", json={'token': token})
    assert response.status_code == 200

# INVALID EMAIL
def test_auth_register_invalid_email_http(url):
    '''
    Test auth_register fails using an invalid email
    '''
    invalid_email = dict(user)
    invalid_email['email'] = 'invalidemail.com'
    response = requests.post(f"{url}/auth/register", json=invalid_email)
    assert response.status_code == 400

# EMAIL ALREADY IN USE
def test_auth_register_email_taken_http(url):
    '''
    Test auth_register fails when an email has been registered with before
    '''
    requests.post(f"{url}/auth/register", json=user)
    email_taken = dict(user)
    email_taken['name_first'] = 'Andras'
    email_taken['name_last'] = 'Arato'

    response = requests.post(f"{url}/auth/register", json=email_taken)
    assert response.status_code == 400

# INVALID PASSWORD
def test_auth_register_invalid_pw_http(url):
    '''
    Test auth_register fails with an invalid password
    '''
    bad_pw = dict(user)

    # Password too short (5 characters)
    bad_pw['password'] = '12345'
    response = requests.post(f"{url}/auth/register", json=bad_pw)
    assert response.status_code == 400

    # Empty password
    bad_pw['password'] = ''
    response = requests.post(f"{url}/auth/register", json=bad_pw)
    assert response.status_code == 400

# INVALID NAME
def test_auth_register_invalid_name_http(url):
    '''
    Tst auth_register fails with an invalid name
    '''
    bad_name = dict(user)

    # Empty name parameters
    # No names entered
    bad_name['name_first'] = ""
    bad_name['name_last'] = ""
    response = requests.post(f"{url}/auth/register", json=bad_name)
    assert response.status_code == 400
    # Only first name entered
    bad_name['name_first'] = "Hayden"
    response = requests.post(f"{url}/auth/register", json=bad_name)
    assert response.status_code == 400
    # Only last name entered
    bad_name['name_first'] = ""
    bad_name['name_last'] = "Everest"
    response = requests.post(f"{url}/auth/register", json=bad_name)
    assert response.status_code == 400

    # First name > 50 characters (51 characters)
    bad_name['name_first'] = "Haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaayden"
    response = requests.post(f"{url}/auth/register", json=bad_name)
    assert response.status_code == 400

    # Last name > 50 characters (51 characters)
    bad_name['name_first'] = "Hayden"
    bad_name['name_last'] = "Eveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerest"
    response = requests.post(f"{url}/auth/register", json=bad_name)
    assert response.status_code == 400


# Will need to check for handle generation, which requires user_profile (not in
# iteration 1)

############################## AUTH_LOGOUT TESTS ###############################

# BASE CASE
def test_auth_logout_success_http(url):
    '''
    Base test for auth_logout
    '''
    # Register user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

    r = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = r.json()
    assert status['is_success'] is True

# LOGGING OUT WITHOUT LOGGING IN
def test_auth_logout_fail_http(url):
    '''
    Test that logout fails when not logged in
    '''
    # Register a user
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

    # Try logging out right after registering
    r = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = r.json()
    assert status['is_success'] is True

    # Try logging out, without being logged in
    r = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = r.json()
    assert status['is_success'] is False

    # Login with user, getting a new active token
    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
    r = requests.post(f"{url}/auth/login", json=login_payload)
    account = r.json()

    # Try logging out right after logging in
    r = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = r.json()
    assert status['is_success'] is True




### CHANNEL FUNCTIONS





### CHANNELS FUNCTIONS

############################ CHANNELS_CREATE TESTS #############################
# Base Case
def test_channels_create_success_http(url):
    '''
    Base test for channels_create
    '''
    # register
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

    # create channel
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = r.json()

    # list channels
    r = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    listed = r.json()

    assert len(listed['channels']) == 1

    # create channel2
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel2 = r.json()

    # list channels
    r = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    listed = r.json()

    assert len(listed['channels']) == 2

# Channel name > 20 characters
def test_channels_create_fail_http(url):
    '''
    Test channels_create fails with a name too long
    '''
    # register
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

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
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()

    # create channel1
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = r.json()

    # create channel2
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 2',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel2 = r.json()

    # create channel3
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 3',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel3 = r.json()

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

    r = requests.get(f"{url}/channels/listall", params={'token' : account['token']})
    lists = r.json()

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
    r = requests.post(f"{url}/auth/register", json=user)
    account1 = r.json()

    # register
    r = requests.post(f"{url}/auth/register", json=user2)
    account2 = r.json()

    empty_channels_list = []


    # Assert no channels listed right now
    r = requests.get(f"{url}/channels/listall", params={'token' : account1['token']})
    lists = r.json()

    assert lists == {'channels': empty_channels_list}

    r = requests.get(f"{url}/channels/listall", params={'token' : account2['token']})
    lists = r.json()

    assert lists == {'channels': empty_channels_list}


    # Create a channel1 with user1
    channel_payload ={
        'token' : account1['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = r.json()


    channel_list = [
        {
            'channel_id': channel1['channel_id'],
            'name': 'Channel 1',
        }
    ]

    # Assert only user 1 can see the channel
    r = requests.get(f"{url}/channels/list", params={'token' : account1['token']})
    lists = r.json()

    assert lists == {'channels': channel_list}

    r = requests.get(f"{url}/channels/list", params={'token' : account2['token']})
    lists = r.json()

    assert lists == {'channels': empty_channels_list}


    # Invite user 2
    user_payload = {
        'token' : account1['token'],
        'channel_id' : channel1['channel_id'],
        'u_id' : account2['u_id']
    }

    requests.post(f"{url}/channel/invite", json=user_payload)


    # Assert both users can see the channel
    r = requests.get(f"{url}/channels/list", params={'token' : account1['token']})
    lists = r.json()

    assert lists == {'channels': channel_list}

    r = requests.get(f"{url}/channels/list", params={'token' : account2['token']})
    lists = r.json()

    assert lists == {'channels': channel_list}


# Calling channels functions with invalid tokens
def test_channels_invalid_token_http(url):
    '''
    Test channels_invalid fails with an invalid token
    '''

    # register
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()


    # Create a channel1 with user1
    channel_payload ={
        'token' : account['token'],
        'name' : 'Channel 1',
        'is_public' : True
    }

    r = requests.post(f"{url}/channels/create", json=channel_payload)
    channel1 = r.json()


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

    respone = requests.get(f"{url}/channels/list", params={'token' : account['token']})
    assert response.status_code == 400

    respone = requests.get(f"{url}/channels/listall", params={'token' : account['token']})
    assert response.status_code == 400
