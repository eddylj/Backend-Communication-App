import auth
import pytest
from error import InputError

<<<<<<< HEAD
# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# AUTH_REGISTER TESTS

# BASE TEST - Valid user registration
def test_auth_register_valid():
    passed = {'u_id': 'haydeneverest', 'token': 'validemail@gmail.com'}
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth.auth_register(*user) == passed

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
    invalid_email = ('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register(*invalid_email)

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('validemail@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*short_pw)
        auth.auth_register(*empty_pw)

# INVALID NAME
def test_auth_register_invalid_name():
    email = 'validemail@gmail.com'
    password = '123abc!@#'
    with pytest.raises(InputError):
        # No names entered
        auth.auth_register(email, password, '', '')

        # First name > 50 characters
        auth.auth_register(email, password,
                           'Haaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaayden', 'Everest')
                            
        # Last name > 50 characters
        auth.auth_register(email, password, 'Hayden',
                           'Eveeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeerest')

def test_auth_logout_success(): 
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}


def test_auth_login_invalid_email():
    invalid_email = ('invalidemail.com', '123abc!@#')
    with pytest.raises(InputError)
        auth.auth_login(invalid_email)

