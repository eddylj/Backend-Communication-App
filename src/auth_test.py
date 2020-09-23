import auth
import pytest
from error import InputError

# WORKING 
def test_auth_register_simple():
    assert auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest') == {
        'u_id': 1,
        'token': '12345',
    } # TO BE CHANGED ACCORDINGLY

def test_auth_register_invalid():
    #assert auth.auth_register('')

def test_auth_logout_success():
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}
