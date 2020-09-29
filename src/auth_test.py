import auth
import pytest
from error import InputError
from other import clear
from data import data

# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# AUTH_REGISTER TESTS

# BASE TEST - Valid user registration
def test_auth_register_valid():
    '''
    Because we can't guarantee other people's implementation is going to use the
    same u_id and token system as us (not a black box test), I don't think we 
    can explicitly assert auth_register against an expected value. 
    
    Proposed workaround is to assume that auth_logout and auth_login is 
    guaranteed to work, so the return value of auth_login should match up with 
    auth_register (checking if u_id & token is valid) and auth_logout should 
    succeed (checking if token is valid).

    Two glaring problems:
        1. IDK if we *can* assume that auth_login/logout works in auth_test,
           even though we're testing register here.
        2. Token would probably change in later iterations, so generated tokens
           for register and login would probably be different.
    '''
    clear()
    # passed = {'u_id': 1, 'token': 'validemail@gmail.com'}
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # assert auth.auth_register(*user) == passed
    account = auth.auth_register(*user)
    token = account['token']
    email, password, *_ = user
    assert auth.auth_login(email, password) == account
    assert auth.auth_logout(token) == {'is_success': True}

    '''
    Style?
    assert auth.auth_register('validemail@gmail.com',
                              '123abc!@#',
                              'Hayden',
                              'Everest') == passed

    OR 

    email = 'validemail@gmail.com'
    password = '123abc!@#'
    first_name = 'Hayden'
    last_name = 'Everest'
    assert auth.auth_register(email, password, first_name, last_name) == passed
    '''

# INVALID EMAIL
def test_auth_register_invalid_email():
    clear()
    invalid_email = ('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register(*invalid_email)

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    clear()
    user1 = ('asdf@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('asdf@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)

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
    print(data)

    clear()

def test_auth_logout_success(): 
    clear()
    assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
    clear()
    assert auth.auth_logout("online") == {'is_success': True,}
    