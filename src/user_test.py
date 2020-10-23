""" This module contains test functions for user.py """
import pytest
import auth
import user
from error import InputError#, AccessError
from other import clear

user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

# Consider changing user registration to fixtures

############################# USER_PROFILE TESTS ###############################

def test_user_profile_valid():
    """ Base case for user_profile(). """
    clear()
    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    expected = {
        'u_id': u_id,
        'email': 'validemail@gmail.com',
        'name_first': 'Hayden',
        'name_last': 'Everest',
        'handle_str': 'haydeneverest'
    }

    assert user.user_profile(token, u_id) == {expected}

def test_user_profile_invalid_id():
    """
    Test case for user_profile(), where u_id does not correspond to a registered
    user.
    """
    clear()
    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    with pytest.raises(InputError):
        user.user_profile(token, u_id + 1)

########################## USER_PROFILE_SETNAME TESTS ##########################


########################## USER_PROFILE_SETEMAIL TESTS #########################

######################### USER_PROFILE_SETHANDLE TESTS #########################


# To be added: invalid token tests

clear()
