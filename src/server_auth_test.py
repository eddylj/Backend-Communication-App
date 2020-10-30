"""
This module contains tests for auth routes in server.py.
"""
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
    """
    Base test for auth_login
<<<<<<< HEAD:src/server_auth_test.py
    '''
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()
=======
    """
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
>>>>>>> master:src/server_auth_test.py

    requests.post(f"{url}/auth/logout", json={'token': account['token']})

    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
<<<<<<< HEAD:src/server_auth_test.py
    req = requests.post(f"{url}/auth/login", json=login_payload)
    login = req.json()

=======
    r = requests.post(f"{url}/auth/login", json=login_payload)
    login = r.json()
>>>>>>> master:src/server_auth_test.py
    assert login['u_id'] == account['u_id']

# INVALID EMAIL
def test_auth_login_invalid_email_http(url):
    """
    Test auth_login fails using an invalid email
    """
    invalid_email = {
        'email': 'invalidemail.com',
        'password': '123abc!@#'
    }
    response = requests.post(f"{url}/auth/login", json=invalid_email)
    assert response.status_code == 400

# NON USER EMAIL
def test_auth_login_non_user_email_http(url):
    """
    Test auth_login fails using using an email belonging to noone
    """
    requests.post(f"{url}/auth/register", json=user)

    non_user_email = {
        'email': 'nonuseremail@gmail.com',
        'password': '123abc!@#'
    }
    response = requests.post(f"{url}/auth/login", json=non_user_email)
    assert response.status_code == 400

# WRONG PASSWORD
def test_auth_login_wrong_password_http(url):
    """
    Test auth_login fails using the wrong password
    """
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
    """
    Base test for auth_register
<<<<<<< HEAD:src/server_auth_test.py
    '''
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()
=======
    """
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
>>>>>>> master:src/server_auth_test.py
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
    """
    Test auth_register fails using an invalid email
    """
    invalid_email = dict(user)
    invalid_email['email'] = 'invalidemail.com'
    response = requests.post(f"{url}/auth/register", json=invalid_email)
    assert response.status_code == 400

# EMAIL ALREADY IN USE
def test_auth_register_email_taken_http(url):
    """
    Test auth_register fails when an email has been registered with before
    """
    requests.post(f"{url}/auth/register", json=user)
    email_taken = dict(user)
    email_taken['name_first'] = 'Andras'
    email_taken['name_last'] = 'Arato'

    response = requests.post(f"{url}/auth/register", json=email_taken)
    assert response.status_code == 400

# INVALID PASSWORD
def test_auth_register_invalid_pw_http(url):
    """
    Test auth_register fails with an invalid password
    """
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
    """
    Tst auth_register fails with an invalid name
    """
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

############################## AUTH_LOGOUT TESTS ###############################

# BASE CASE
def test_auth_logout_success_http(url):
    """
    Base test for auth_logout
    """
    # Register user
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    req = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = req.json()
    assert status['is_success'] is True

# LOGGING OUT WITHOUT LOGGING IN
def test_auth_logout_fail_http(url):
    """
    Test that logout fails when not logged in
    """
    # Register a user
    req = requests.post(f"{url}/auth/register", json=user)
    account = req.json()

    # Try logging out right after registering
    req = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = req.json()
    assert status['is_success'] is True

    # Try logging out, without being logged in
    req = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = req.json()
    assert status['is_success'] is False

    # Login with user, getting a new active token
    login_payload = {
        'email': user['email'],
        'password': user['password']
    }
    req = requests.post(f"{url}/auth/login", json=login_payload)
    account = req.json()

    # Try logging out right after logging in
    req = requests.post(f"{url}/auth/logout", json={'token': account['token']})
    status = req.json()
    assert status['is_success'] is True