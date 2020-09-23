import auth
import pytest
from error import InputError

# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# BASE TEST
def test_auth_register_simple():
    assert auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest') == {
        'u_id': 1,
        'token': '12345',
    } # Should pass. 

# INVALID EMAIL
def test_auth_register_invalid_email():
    assert auth.auth_register('invalidemail.com', '123abc!@#', 'Hayden', 'Everest') == {
        'u_id': 1,
        'token': '12345',
    } # Should fail. 

    # Exception method
    '''
    with pytest.raises(InputError):
        auth.auth_register('invalidemail.com', '123abc!@#', 'Hayden', 'Everest')
    '''

# EMAIL ALREADY IN USE
def test_auth_register_taken():
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth.auth_register('validemail@gmail.com', '123abc!@#', 'Everest', 'Hayden') == {
        'u_id': 1,
        'token': '12345',
    } # Should fail. 

    # Exception method
    '''
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'Everest', 'Hayden')
    '''

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    assert auth.auth_register('validemail@gmail.com', '12345', 'Hayden', 'Everest') == {
        'u_id': 1,
        'token': '12345',
    } # Should fail. 

    # EMPTY PASSWORD
    assert auth.auth_register('validemail@gmail.com', '', 'Hayden', 'Everest') == {
        'u_id': 1,
        'token': '12345',
    } # Should fail. 

    # Exception method
    '''
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '12345', 'Hayden', 'Everest')
        auth.auth_register('validemail@gmail.com', '', 'Hayden', 'Everest')
    '''

# INVALID NAME
def test_auth_register_invalid_name():
    # EMPTY NAME
    assert auth.auth_register('validemail@gmail.com', '123abc!@#', '', '') == {
        'u_id': 1,
        'token': '12345',
    } # Should fail. 

    # Names > 50 characters

    # Exception method
    '''
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', '', '')
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'Haaaaaaaaaaaaaaaaa\
                                                                 aaaaaaaaaaaaaaaaaa\
                                                                 aaaaaaaaaaaaaaaaaa\
                                                                 aaaaaaaaaaaaaayden', 'Everest')
    '''

def test_auth_logout_success(): 
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}
