"""
This module contains tests for user routes in server.py.
"""
import requests

user1 = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}
user2 = {
    'email': 'alsovalid@gmail.com',
    'password': 'aW5Me@l!',
    'name_first': 'Andras',
    'name_last': 'Arato',
}

############################# USER_PROFILE TESTS ###############################

def test_user_profile_valid_http(url, http_test_data):
    """ Base case for user_profile(). """
    payload = {
        'token': http_test_data.token(0),
        'u_id': http_test_data.u_id(0)
    }
    r = requests.get(f"{url}/user/profile", params=payload)
    assert r.status_code == 200

def test_user_profile_invalid_id_http(url):
    """
    Test case for user_profile(), where u_id does not correspond to a registered
    user.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    u_id = account['u_id']

    payload = {
        'token': account['token'],
        'u_id': u_id + 1
    }
    response = requests.get(f"{url}/user/profile", params=payload)
    assert response.status_code == 400

########################## USER_PROFILE_SETNAME TESTS ##########################

def test_user_setname_valid_http(url, http_test_data):
    """ Base case for user_profile_setname() """
    token = http_test_data.token(0)
    # Changing name to Andras Arato
    setname_payload = {
        'token': token,
        'name_first': "Andras",
        'name_last': "Arato"
    }
    r = requests.put(f"{url}/user/profile/setname", json=setname_payload)
    assert r.status_code == 200

def test_user_setname_invalid_http(url):
    """
    Invalid name cases for user_profile_setname(). Names have to been in ASCII
    characters and between 1-50 characters inclusively in length.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()

    # 70-character long names
    long_first_name = (
        "Haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaayden"
    )
    long_last_name = (
        "Eveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerest"
    )

    payload = {
        'token': account['token'],
        'name_first': long_first_name,
        'name_last': long_last_name
    }
    response = requests.put(f"{url}/user/profile/setname", json=payload)
    assert response.status_code == 400

    # Empty strings passed into setname. 0 length < required 1.
    payload['name_first'] = ""
    payload['name_last'] = ""
    response = requests.put(f"{url}/user/profile/setname", json=payload)
    assert response.status_code == 400

def test_user_setname_repeated_http(url):
    """
    Test case for user_profile_setname(), where the passed name is the same as
    the existing name. Expected to raise an input error.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()

    payload = {
        'token': account['token'],
        'name_first': "Hayden",
        'name_last': "Everest"
    }
    response = requests.put(f"{url}/user/profile/setname", json=payload)
    assert response.status_code == 400

########################## USER_PROFILE_SETEMAIL TESTS #########################

def test_user_setemail_valid_http(url, http_test_data):
    """ Base case for user_profile_setemail(). """
    # Changing email
    email_payload = {
        'token': http_test_data.token(0),
        'email': "another@gmail.com"
    }
    r = requests.put(f"{url}/user/profile/setemail", json=email_payload)
    assert r.status_code == 200

def test_user_setemail_invalid_http(url):
    """
    Test case for user_profile_setemail(), where the email passed doesn't
    conform to the predetermined format rules.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token = account['token']

    # Attempting to change email to an invalid one.
    email_payload = {
        'token': token,
        'email': "invalidemail.com"
    }
    response = requests.put(f"{url}/user/profile/setemail", json=email_payload)
    assert response.status_code == 400

def test_user_setemail_email_taken_http(url):
    """
    Test case for user_profile_setemail(), where a user tries to change their
    email to one already used by another registered user.
    """
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    requests.post(f"{url}/auth/register", json=user2)

    email_payload = {
        'token': account['token'],
        'email': "alsovalid@gmail.com"
    }
    response = requests.put(f"{url}/user/profile/setemail", json=email_payload)
    assert response.status_code == 400

def test_user_setemail_repeated_http(url):
    """
    Test case for user_profile_setemail(), where the passed email is the same as
    the existing email. Expected to raise an input error.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()

    email_payload = {
        'token': account['token'],
        'email': "validemail@gmail.com"
    }
    response = requests.put(f"{url}/user/profile/setemail", json=email_payload)
    assert response.status_code == 400

######################### USER_PROFILE_SETHANDLE TESTS #########################

def test_user_sethandle_valid_http(url, http_test_data):
    """ Base case for user_profile_sethandle() """
    handle_payload = {
        'token': http_test_data.token(0),
        'handle_str': "everesthayden"
    }
    r = requests.put(f"{url}/user/profile/sethandle", json=handle_payload)
    assert r.status_code == 200

def test_user_sethandle_invalid_http(url):
    """
    Test cases for invalid handles passed to user_profile_sethandle. Invalid
    handles include handles which are not:
        - Between 3-20 characters inclusively in length.
        - Contains upper-case letters.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token = account['token']

    # Empty handle string
    payload = {
        'token': token,
        'handle_str': ""
    }
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

    # 2-character handle string
    payload['handle_str'] = "he"
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

    # 21-character handle string
    payload['handle_str'] = "haaaaaaaaaydeneverest"
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

    # Valid length, but contains upper-case characters.
    payload['handle_str'] = "EverestHayden"
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

def test_user_sethandle_handle_taken_http(url):
    """
    Test case for user_profile_sethandle(), where a user tries to change their
    handle to one already used by another registered user.
    """
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    requests.post(f"{url}/auth/register", json=user2)

    payload = {
        'token': account['token'],
        'handle_str': "andrasarato"
    }
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

def test_user_sethandle_repeated_http(url):
    """
    Test case for user_profile_sethandle(), where the passed handle is the same
    as the existing handle. Expected to raise an input error.
    """
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()

    payload = {
        'token': account['token'],
        'handle_str': "haydeneverest"
    }
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

# Checking invalid token
def test_user_invalid_token_http(url):
    '''
    Test for if token is invalid throughout all user functions
    '''
    # Register a user
    r = requests.post(f"{url}/auth/register", json=user1)
    account = r.json()
    token = account['token']

    # Deactivate token by logging out
    requests.post(f"{url}/auth/logout", json={'token': token})

    # Cannot use when token is invalid
    payload = {
        'token': token,
        'u_id': account['u_id']
    }
    response = requests.get(f"{url}/user/profile", params=payload)
    assert response.status_code == 400

    del payload['u_id']
    payload['email'] = "anothervalidemail@gmail.com"
    response = requests.put(f"{url}/user/profile/setemail", json=payload)
    assert response.status_code == 400

    del payload['email']
    payload['handle_str'] = "andrasarato19"
    response = requests.put(f"{url}/user/profile/sethandle", json=payload)
    assert response.status_code == 400

    del payload['handle_str']
    payload['name_first'] = "Andras"
    payload['name_last'] = "Arato"
    response = requests.put(f"{url}/user/profile/setname", json=payload)
    assert response.status_code == 400
