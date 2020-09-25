import auth
import pytest
from error import InputError

# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# BASE TEST
def test_auth_register_valid():
    valid_user = {'u_id': 1, 'token': '12345'}
    assert auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest') == valid_user

    '''
    Style?
    assert auth.auth_register('validemail@gmail.com',
                              '123abc!@#',
                              'Hayden',
                              'Everest') == valid_user
    '''

# INVALID EMAIL
def test_auth_register_invalid_email():
    with pytest.raises(InputError):
        auth.auth_register('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')

# EMAIL ALREADY IN USE
def test_auth_register_email_taken():
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#',
                           'Everest', 'Hayden')

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    with pytest.raises(InputError):
        # Too short
        auth.auth_register('validemail@gmail.com', '12345', 'Hayden', 'Everest')

        # Empty
        auth.auth_register('validemail@gmail.com', '', 'Hayden', 'Everest')

# INVALID NAME
def test_auth_register_invalid_name():
    with pytest.raises(InputError):
        # No names entered
        auth.auth_register('validemail@gmail.com', '123abc!@#', '', '')

        # First name > 50 characters
        auth.auth_register('validemail@gmail.com', '123abc!@#',
                           'Haaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaayden', 'Everest')
                            
        # Last name > 50 characters
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden',
                           'Eveeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeerest')

def test_auth_logout_success(): 
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}
