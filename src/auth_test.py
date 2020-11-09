"""
Tests to test the login, logout and register functions in auth.py
"""
import pytest
import auth
from error import InputError
from other import clear
from user import user_profile

user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')

############################### AUTH_LOGIN TESTS ###############################

# BASE TEST - VALID EMAIL
def test_auth_login_user_email():
    """
    Base test for auth_login
    """
    clear()
    token1 = auth.auth_register(*user)['token']
    auth.auth_logout(token1)

    email, password, *_ = user
    token2 = auth.auth_login(email, password)['token']

    assert token1 != token2

# INVALID EMAIL
def test_auth_login_invalid_email():
    """
    Test auth_login fails using an invalid email
    """
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*invalid_email)

# NON USER EMAIL
def test_auth_login_non_user_email():
    """
    Test auth_login fails using using an email belonging to noone
    """
    clear()
    auth.auth_register(*user)

    non_user_email = ('nonuseremail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*non_user_email)

# WRONG PASSWORD
def test_auth_login_wrong_password():
    """
    Test auth_login fails using the wrong password
    """
    clear()
    auth.auth_register(*user)

    wrong_password = ('validemail@gmail.com', '12345abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*wrong_password)

def test_auth_login_repeated():
    """
    Test case when a user tries to log in when already logged in.
    """
    clear()
    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    auth.auth_register(*user2)

    token1 = auth.auth_register(*user)['token']

    email, password, *_ = user
    token2 = auth.auth_login(email, password)['token']

    assert token1 == token2


############################## AUTH_REGISTER TESTS #############################

# BASE TEST - Valid user registration
def test_auth_register_valid():
    """
    Base test for auth_register
    """
    clear()
    account = auth.auth_register(*user)
    token = account['token']
    assert auth.auth_logout(token) == {'is_success': True}
    email, password, *_ = user
    auth.auth_login(email, password)

# INVALID EMAIL
def test_auth_register_invalid_email():
    """
    Test auth_register fails using an invalid email
    """
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register(*invalid_email)

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    """
    Test auth_register fails when an email has been registered with before
    """
    clear()
    user1 = ('asdf@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('asdf@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    """
    Test auth_register fails with an invalid password
    """
    clear()
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*empty_pw)
    with pytest.raises(InputError):
        auth.auth_register(*short_pw)

# INVALID NAME
def test_auth_register_invalid_name():
    """
    Tst auth_register fails with an invalid name
    """
    clear()
    email, password, *_ = user

    # Empty name parameters
    # No names entered
    with pytest.raises(InputError):
        auth.auth_register(email, password, '', '')
    # Only first name entered
    with pytest.raises(InputError):
        auth.auth_register(email, password, 'Hayden', '')
    # Only last name entered
    with pytest.raises(InputError):
        auth.auth_register(email, password, '', 'Everest')

    # First name > 50 characters
    with pytest.raises(InputError):
        auth.auth_register(email, password,
                           'Haaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaayden', 'Everest')

    # Last name > 50 characters
    with pytest.raises(InputError):
        auth.auth_register(email, password, 'Hayden',
                           'Eveeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeerest')

def test_auth_register_handles():
    """
    White-box test to test handle generation. Checks that users' with the same
    name get different handles, and that handles abide by the rules:
        - Between 3-20 characters in length
        - No uppercase.
    """
    clear()

    # 19 character full name so when the 10th user gets registered, the handle
    # could potentially go over 20 characters in length.
    email, password, *_ = user
    name_first = "Hayden"
    name_last = "Eveeeeeeerest"
    for i in range(11):
        new_email = str(i) + email
        account = auth.auth_register(new_email, password, name_first, name_last)
        if i == 10:
            last_user = account
        elif i > 0:
            profile = user_profile(account['token'], account['u_id'])['user']
            expected = (name_first + name_last + str(i)).lower()
            assert profile['handle_str'] == expected

    profile = user_profile(last_user['token'], last_user['u_id'])['user']
    assert profile['handle_str'] == "haydeneveeeeeeeres10"

############################## AUTH_LOGOUT TESTS ###############################

# BASE CASE
def test_auth_logout_success():
    """
    Base test for auth_logout
    """
    clear()
    # Register user
    token = auth.auth_register(*user)['token']

    logout_success = {'is_success' : True}
    # Logout after logging in
    assert auth.auth_logout(token) == logout_success

# LOGGING OUT WITHOUT LOGGING IN
def test_auth_logout_fail():
    """
    Test that logout fails when not logged in
    """
    clear()
    # Register a user
    token = auth.auth_register(*user)['token']

    logout_success = {'is_success' : True}
    logout_fail = {'is_success' : False}

    # Try logging out right after registering
    assert auth.auth_logout(token) == logout_success

    # Try logging out, without being logged in
    assert auth.auth_logout(token) == logout_fail

    # Login with user, getting a new active token
    token = auth.auth_login('validemail@gmail.com', '123abc!@#')['token']

    # Try logging out right after logging in
    assert auth.auth_logout(token) == logout_success


####################### AUTH_PASSWORDRESET_REQUEST TESTS #######################

def test_auth_passwordreset_request():
    """
    Test for auth_passwordreset_request with invalid email
    """

    clear()

    # Create a user
    auth.auth_register(*user)

    with pytest.raises(InputError):
        auth.auth_passwordreset_request('alsovalidemail@gmail.com')


######################## AUTH_PASSWORDRESET_RESET TESTS ########################
def test_auth_passwordreset_reset_base():
    """
    Base test for auth_passwordreset_reset
    """

    clear()

    # Create a user
    auth.auth_register(*user)

    reset_code = "abcdef"
    new_password = "asdf1234qwer"

    # Request a password reset
    auth.auth_passwordreset_request('validemail@gmail.com')

    # Reset
    auth.auth_passwordreset_reset(reset_code, new_password)


    # passed = {
    #     'u_id' : 0,
    #     'token' : 
    # }
    # Not sure about if JWT for the token is possible
    assert auth.auth_login('validemail@gmail.com', 'asdf1234qwer')['u_id'] == 0

def test_auth_passwordreset_reset_invalid_code():
    """
    Test auth_passwordreset_reset fails with an invalid code
    """

    clear()

    # Create a user
    auth.auth_register(*user)

    reset_code = "bcdefa"
    new_password = "asdf1234qwer"

    # Request a password reset
    auth.auth_passwordreset_request('validemail@gmail.com')

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset(reset_code, new_password)

def test_auth_passwordreset_reset_invalid_pw():
    """
    Test auth_passwordreset_reset fails with an invalid password
    """

    clear()

    # Create a user
    auth.auth_register(*user)

    reset_code = "abcdef"
    new_password = "asdf1234qwer"

    # Request a password reset
    auth.auth_passwordreset_request('validemail@gmail.com')

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset(reset_code, new_password)
