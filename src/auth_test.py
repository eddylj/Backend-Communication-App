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