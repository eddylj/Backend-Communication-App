""" This module contains test functions for user.py """
import pytest
import auth
import user
from error import InputError, AccessError
from other import clear

user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

############################# USER_PROFILE TESTS ###############################

def test_user_profile_valid(test_data):
    """ Base case for user_profile(). """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    assert user.user_profile(token, u_id)['user'] == {
        'u_id': u_id,
        'email': "validemail@gmail.com",
        'name_first': "Hayden",
        'name_last': "Everest",
        'handle_str': "haydeneverest",
        'profile_img_url': None
    }

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

    # White-box test for negative u_ids
    with pytest.raises(InputError):
        user.user_profile(token, -1)

########################## USER_PROFILE_SETNAME TESTS ##########################

def test_user_setname_valid(test_data):
    """ Base case for user_profile_setname() """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    # Changing name to Andras Arato
    user.user_profile_setname(token, "Andras", "Arato")

    profile = user.user_profile(token, u_id)['user']
    assert profile['name_first'] == "Andras"
    assert profile['name_last'] == "Arato"

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
    the existing name. Expected to raise an input error.
    """
    clear()

    token = auth.auth_register(*user1)['token']

    with pytest.raises(InputError):
        user.user_profile_setname(token, "Hayden", "Everest")

########################## USER_PROFILE_SETEMAIL TESTS #########################

def test_user_setemail_valid(test_data):
    """ Base case for user_profile_setemail(). """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    user.user_profile_setemail(token, "anothr@gmail.com")

    assert user.user_profile(token, u_id)['user']['email'] == "anothr@gmail.com"

def test_user_setemail_invalid(test_data):
    """
    Test case for user_profile_setemail(), where the email passed doesn't
    conform to the predetermined format rules.
    """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "invalidemail.com")

    profile = user.user_profile(token, u_id)['user']
    assert profile['email'] == "validemail@gmail.com"

def test_user_setemail_email_taken(test_data):
    """
    Test case for user_profile_setemail(), where a user tries to change their
    email to one already used by another registered user.
    """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "alsovalid@gmail.com")

    profile = user.user_profile(token, u_id)['user']
    assert profile['email'] == "validemail@gmail.com"

def test_user_setemail_repeated():
    """
    Test case for user_profile_setemail(), where the passed email is the same as
    the existing email. Expected to raise an input error.
    """
    clear()

    token = auth.auth_register(*user1)['token']

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "validemail@gmail.com")

######################### USER_PROFILE_SETHANDLE TESTS #########################

def test_user_sethandle_valid(test_data):
    """ Base case for user_profile_sethandle() """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    user.user_profile_sethandle(token, "everesthayden")

    profile = user.user_profile(token, u_id)['user']
    assert profile['handle_str'] == "everesthayden"

def test_user_sethandle_invalid(test_data):
    """
    Test cases for invalid handles passed to user_profile_sethandle. Invalid
    handles include handles which are not:
        - Between 3-20 characters inclusively in length.
        - Contains upper-case letters.
    """
    token = test_data.token(0)
    u_id = test_data.u_id(0)

    # Empty handle string
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "")

    # 2-character handle string
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "he")

    # 21-character handle string
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "haaaaaaaaaydeneverest")

    # Valid length, but contains upper-case characters.
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "EverestHayden")

    profile = user.user_profile(token, u_id)['user']
    assert profile['handle_str'] == "haydeneverest"

def test_user_sethandle_handle_taken():
    """
    Test case for user_profile_sethandle(), where a user tries to change their
    handle to one already used by another registered user.
    """
    clear()

    token = auth.auth_register(*user1)['token']
    auth.auth_register(*user2)

    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "andrasarato")

def test_user_sethandle_repeated():
    """
    Test case for user_profile_sethandle(), where the passed handle is the same
    as the existing handle. Expected to raise an input error.
    """
    clear()

    token = auth.auth_register(*user1)['token']

    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "haydeneverest")

# Checking invalid token
def test_user_invalid_token():
    """
    Test for invalid tokens throughout all user functions
    """
    clear()

    # Register a user
    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    # Deactivate token by logging out
    auth.auth_logout(token)

    # Cannot use when token is invalid
    with pytest.raises(AccessError):
        user.user_profile(token, u_id)

    with pytest.raises(AccessError):
        user.user_profile_setname(token, "Andras", "Arato")

    with pytest.raises(AccessError):
        user.user_profile_setemail(token, "anothervalidemail@gmail.com")

    with pytest.raises(AccessError):
        user.user_profile_sethandle(token, "andrasarato19")

clear()
