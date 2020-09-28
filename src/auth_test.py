import auth
import pytest
from error import InputError
from other import clear
from data import data

# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# AUTH_REGISTER TESTS

# BASE TEST - Valid user registration
def test_auth_register_valid():
    passed = {'u_id': 1, 'token': '12345'}
    user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth.auth_register(*user) == passed
    
    print(data['users']) 
    clear()
    print(data['users']) 
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
    clear()
    print(data['users'])

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    user1 = ('asdf@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = ('asdf@gmail.com', '123abc!@#', 'Andras', 'Arato')
    auth.auth_register(*user1)
    with pytest.raises(InputError):
        auth.auth_register(*user2)
    clear()
    print(data['users'])

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*short_pw)
        auth.auth_register(*empty_pw)
    clear()
    print(data['users'])

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
    clear()

def test_auth_logout_success(): 
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}