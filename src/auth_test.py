import auth
import pytest
from error import InputError
from other import clear
from data import data

#AUTH_LOGIN TESTS

# BASE TEST - VALID EMAIL
def test_auth_login_user_email():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    passed = {'u_id': u_id, 'token': token}
    valid_login = ('validemail@gmail.com', '123abc!@#')
    assert auth.auth_login(*valid_login) == passed

# INVALID EMAIL
def test_auth_login_invalid_email():
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*invalid_email)

# NON USER EMAIL
def test_auth_login_non_user_email():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    non_user_email = ('nonuseremail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*non_user_email)

# WRONG PASSWORD
def test_auth_login_wrong_password():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    wrong_password = ('validemail@gmail.com', '12345abc!@#')
    with pytest.raises(InputError):
        auth.auth_login(*wrong_password)

# AUTH_REGISTER TESTS

# BASE TEST - Valid user registration
def test_auth_register_valid():
    clear()
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account = auth.auth_register(*user)
    token = account['token']
    email, password, *_ = user
    auth.auth_login(email, password)
    assert auth.auth_logout(token) == {'is_success': True}
    
# INVALID EMAIL
def test_auth_register_invalid_email():
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register(*invalid_email)
    clear()

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    clear()
    user1 = ('asdf@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('asdf@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)
    clear()

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    clear()
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*empty_pw)
    with pytest.raises(InputError):
        auth.auth_register(*short_pw)

# INVALID NAME
def test_auth_register_invalid_name():
    clear()
    email = 'validemail@gmail.com'
    password = '123abc!@#'

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
    clear()

# Will need to check for handle generation, which requires user_profile (not in
# iteration 1)

# AUTH_LOGOUT TESTS

# BASE CASE
def test_auth_logout_success(): 
    clear()
    # Register user1
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    token = auth.auth_register(*user)['token']

    # Login
    auth.auth_login('validemail@gmail.com', '123abc!@#')

    logout_success = {'is_success' : True}
    # Logout after logging in
    assert auth.auth_logout(token) == logout_success
    
# LOGGING OUT WITHOUT LOGGING IN
def test_auth_logout_fail():
    clear()
    # Register a user
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
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