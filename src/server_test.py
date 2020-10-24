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

