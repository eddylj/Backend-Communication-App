'''
Tests to test the login, logout and register functions in auth.py
'''
import pytest
import auth
from error import InputError
from other import clear
from data import data

user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')

############################### AUTH_LOGIN TESTS ###############################

# BASE TEST - VALID EMAIL
def test_auth_login_user_email():
    '''
    Base test for auth_login
    '''
    clear()
    token = auth.auth_register(*user)['token']
    auth.auth_logout(token)

    email, password, *_ = user
    auth.auth_login(email, password)

# INVALID EMAIL
def test_auth_login_invalid_email():
    '''
    Test auth_login fails using an invalid email
    '''
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*invalid_email)

# NON USER EMAIL
def test_auth_login_non_user_email():
    '''
    Test auth_login fails using using an email belonging to noone
    '''
    clear()
    auth.auth_register(*user)

    non_user_email = ('nonuseremail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*non_user_email)

# WRONG PASSWORD
def test_auth_login_wrong_password():
    '''
    Test auth_login fails using the wrong password
    '''
    clear()
    auth.auth_register(*user)

    wrong_password = ('validemail@gmail.com', '12345abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*wrong_password)

############################## AUTH_REGISTER TESTS #############################

# BASE TEST - Valid user registration
def test_auth_register_valid():
    '''
    Base test for auth_register
    '''
    clear()
    account = auth.auth_register(*user)
    token = account['token']
    email, password, *_ = user
    auth.auth_login(email, password)
    assert auth.auth_logout(token) == {'is_success': True}

# INVALID EMAIL
def test_auth_register_invalid_email():
    '''
    Test auth_register fails using an invalid email
    '''
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register(*invalid_email)

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    '''
    Test auth_register fails when an email has been registered with before
    '''
    clear()
    user1 = ('asdf@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('asdf@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    '''
    Test auth_register fails with an invalid password
    '''
    clear()
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*empty_pw)
    with pytest.raises(InputError):
        auth.auth_register(*short_pw)

# INVALID NAME
def test_auth_register_invalid_name():
    '''
    Tst auth_register fails with an invalid name
    '''
    clear()
    email, password, *_ = user

    # No names entered
    with pytest.raises(InputError):
        auth.auth_register(email, password, '', '')
    print(data)
    # First name > 50 characters
    with pytest.raises(InputError):
        auth.auth_register(email, password,
                           'Haaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaayden', 'Everest')
    print(data)
    # Last name > 50 characters
    with pytest.raises(InputError):
        auth.auth_register(email, password, 'Hayden',
                           'Eveeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeerest')

# Will need to check for handle generation, which requires user_profile (not in
# iteration 1)

############################## AUTH_LOGOUT TESTS ###############################

# BASE CASE
def test_auth_logout_success():
    '''
    Base test for auth_logout
    '''
    clear()
    # Register user
    token = auth.auth_register(*user)['token']

    # Login
    auth.auth_login('validemail@gmail.com', '123abc!@#')

    logout_success = {'is_success' : True}
    # Logout after logging in
    assert auth.auth_logout(token) == logout_success

# LOGGING OUT WITHOUT LOGGING IN
def test_auth_logout_fail():
    '''
    Test that logout fails when not logged in
    '''
    clear()
    # Register a user
    token = auth.auth_register(*user)['token']

    logout_success = {'is_success' : True}
    logout_fail = {'is_success' : False}

    # Try logging out right after registering
    assert auth.auth_logout(token) == logout_success

    # Try logging out, without being logged in
    assert auth.auth_logout(token) == logout_fail

    # Login with user
    auth.auth_login('validemail@gmail.com', '123abc!@#')

    # Try logging out right after logging in
    assert auth.auth_logout(token) == logout_success

clear()
