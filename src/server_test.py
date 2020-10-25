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

# BASE TEST - VALID EMAIL
def test_auth_login_user_email_http(url):
    '''
    Base test for auth_login
    '''
    r = requests.post(f"{url}/auth/register", json=user)
    register = r.json()

    requests.post(f"{url}/auth/logout", json={'token': register['token']})

    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
    r = requests.post(f"{url}/auth/login", json=login_payload)
    login = r.json()

    assert login['u_id'] == register['u_id']

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