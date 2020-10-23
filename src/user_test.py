""" This module contains test functions for user.py """
import pytest
import auth
import user
from error import InputError#, AccessError <- used for invalid token tests
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

def test_user_setname_valid():
    """ Base case for user_profile_setname() """
    clear()

    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    # Changing name to Andras Arato
    user.user_profile_setname(token, "Andras", "Arato")

    expected = {
        'u_id': u_id,
        'email': 'validemail@gmail.com',
        'name_first': 'Andras',
        'name_last': 'Arato',
        'handle_str': 'haydeneverest'
    }

    assert user.user_profile(token, u_id) == {expected}

def test_user_setname_invalid():
    """
    Invalid name cases for user_profile_setname(). Names have to been in ASCII
    characters and between 1-50 characters inclusively in length.
    """
    clear()

    account = auth.auth_register(*user1)
    token = account['token']

    # 70-character long names
    long_first_name = (
        "Haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaayden"
    )
    long_last_name = (
        "Eveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerest"
    )

    with pytest.raises(InputError):
        user.user_profile_setname(token, long_first_name, "Everest")

    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", long_last_name)

    # Empty strings passed into setname. 0 length < required 1.
    with pytest.raises(InputError):
        user.user_profile_setname(token, "", "")

def test_user_setname_repeated():
    """
    Test case for user_profile_setname(), where the passed name is the same as
    the existing name.
    """
    # Assumed to just work; nothing changes but no errors raised.
    clear()

    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    user.user_profile_setname(token, "Hayden", "Everest")

    expected = {
        'u_id': u_id,
        'email': 'validemail@gmail.com',
        'name_first': 'Hayden',
        'name_last': 'Everest',
        'handle_str': 'haydeneverest'
    }

    assert user.user_profile(token, u_id) == {expected}

########################## USER_PROFILE_SETEMAIL TESTS #########################

######################### USER_PROFILE_SETHANDLE TESTS #########################


# To be added: invalid token tests

clear()
