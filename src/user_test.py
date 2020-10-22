'''
Tests for all functions in user.py
'''
import pytest
import user
import auth
from error import InputError
from other import clear
from data import data

############################### USER_PROFILE TESTS ###############################


def test_profile_valid():
    '''
    Test for checking for valid profile
    '''
    clear()
    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']
    email1 = data['users'][u_id1]['email']
    handle1 = data['users'][u_id1]['handle']


    user1_details = {
        'u_id' : u_id1,
        'email' : email1,
        'name_first' : 'Hayden',
        'name_last' : 'Everest',
        'handle_str' : handle1
    }

    assert user.user_profile(token1, u_id1) == {'user': user1_details}

def test_invalid_user():
    '''
    Test for invalid user trying to remove a message
    '''
    clear()
    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    token2 = '124124'
    u_id2 = 1001

    # Invalid token
    with pytest.raises(InputError):
        user.user_profile(token2, u_id1)

    # Invalid u_id
    with pytest.raises(InputError):
        user.user_profile(token1, u_id2)


############################### USER_PROFILE_SETNAME TESTS ###############################

# BASE CASE - Valid name change
def test_user_profile_setname_valid():
    '''
    Test for valid update in user profile name
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']
    user.user_profile_setname(token1, 'John', 'Albert')
    assert data['users'][u_id1]['name_first'] == 'John'
    assert data['users'][u_id1]['name_last'] == 'Albert'

# INVALID NAME
def test_user_profile_setname_invalid_name():
    '''
    Test for invalid update in user profile name
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # No names entered
    with pytest.raises(InputError):
        user.user_profile_setname(token1, '', '')

    # First name > 50 characters
    with pytest.raises(InputError):
        user.user_profile_setname(token1,
                                  'Jooooooooooooooooo\
                            oooooooooooooooooo\
                            oooooooooooooooooo\
                            ooooooooooooooooohn', 'Albert')
    # Last name > 50 characters
    with pytest.raises(InputError):
        user.user_profile_setname(token1, 'John',
                                  'Alllllllllllllllll\
                            llllllllllllllllll\
                            llllllllllllllllll\
                            lllllllllllllllbert')

############################### USER_PROFILE_SETEMAIL TESTS ###############################

# BASE TEST - Valid email change
def test_user_profile_setemail_valid():
    '''
    Test for valid update in user's email
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user.user_profile_setemail(token1, 'info@nip.gl')

    assert data['users'][u_id1]['email'] == 'info@nip.gl'

# INVALID EMAIL
def test_user_profile_setemail_invalid_email():
    '''
    Test for invalid update in user's email
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    with pytest.raises(InputError):
        user.user_profile_setemail(token1, 'invalidemail.com')

# EMAIL ALREADY IN USE
def test_user_profile_setemail_email_taken():
    '''
    Test for when email is already taken
    '''
    clear()

    # Creates 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register(*user1)

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    with pytest.raises(InputError):
        user.user_profile_setemail(token2, 'validemail@gmail.com')

############################### USER_PROFILE_SETHANDLE TESTS ###############################

# BASE TEST - Valid handle change
def test_user_profile_sethandle_valid():
    '''
    Test for checking valid update in user handle
    '''
    clear()

    #Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    valid_handle = 'NIPFORLIFE'

    user.user_profile_sethandle(token1, valid_handle)

    assert data['users'][u_id1]['handle'] == valid_handle

# INVALID HANDLE NAME (< 3 or > 20 characters)
def test_user_profile_sethandle_invalid_handle():
    '''
    Test for checking invalid update in user handle
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    invalid_handle1 = 'hi'
    invalid_handle2 = 'hihihihihihiihiihihihi'

    with pytest.raises(InputError):
        user.user_profile_sethandle(token1, invalid_handle1)

    with pytest.raises(InputError):
        user.user_profile_sethandle(token1, invalid_handle2)

# HANDLE ALREADY IN USE
def test_user_profile_sethandle_handle_taken():
    '''
    Test for checking user handle being taken already
    '''
    clear()

    # Creates 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    valid_handle = 'NIPFORLIFE'
    user.user_profile_sethandle(token1, valid_handle)

    with pytest.raises(InputError):
        user.user_profile_sethandle(token2, valid_handle)
