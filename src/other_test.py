""" This module contains tests for the miscellaneous functions in other.py """
import pytest
import auth
import channel
import channels
import message
import other
from error import InputError, AccessError
from data import data

user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')

################################# CLEAR() TEST #################################

def test_clear():
    """
    Unit test to see if data gets cleared after various function calls.
    """
    other.clear()
    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    # Send messages
    message.message_send(token1, channel_id, "Hello")
    message.message_send(token2, channel_id, "Goodbye")

    other.clear()
    assert data == {
        'users': [],
        'channels': [],
        'tokens': [],
        'messages' : [],
    }

############################## GET_ACTIVE() TEST ###############################

def test_get_active():
    """
    Unit test to see if get_active returns the correct u_id given a token.
    """
    other.clear()
    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    assert other.get_active(token1) == u_id1
    assert other.get_active(token2) == u_id2

############################### IS_VALID() TEST ################################

def test_is_valid():
    """
    Unit test to see if is_valid() correctly checks if an email is valid or not.
    """
    other.clear()
    assert other.is_valid("validemail@gmail.com")
    assert other.is_valid("987654321@gmail.com")
    assert other.is_valid("VALIDEMAIL@gmail.com") is None
    assert other.is_valid("invalidemailgmail.com") is None
    assert other.is_valid("invalid@gmail") is None

############################### USERS_ALL() TESTS ##############################

def test_users_all_valid():
    """
    Base case for users_all().
    """
    other.clear()

    # Create three users
    account1 = auth.auth_register(*user1)
    token = account1['token']
    u_id1 = account1['u_id']

    u_id2 = auth.auth_register(*user2)['u_id']
    u_id3 = auth.auth_register(*user3)['u_id']

    # User 1 calls users_all()
    users = other.users_all(token)['users']
    assert users == [
        {
            'u_id': u_id1,
            'email': 'validemail@gmail.com',
            'name_first': 'Hayden',
            'name_last': 'Everest',
            'handle_str': 'haydeneverest'
        },
        {
            'u_id': u_id2,
            'email': 'alsovalid@gmail.com',
            'name_first': 'Andras',
            'name_last': 'Arato',
            'handle_str': 'andrasarato'
        },
        {
            'u_id': u_id3,
            'email': 'alsoalsovalid@gmail.com',
            'name_first': 'Mark',
            'name_last': 'Head',
            'handle_str': 'markhead'
        }
    ]

def test_users_all_invalid_token():
    """
    Test for invalid token passed into users_all().
    """
    other.clear()

    token = auth.auth_register(*user1)['token']

    # Invalidate token by logging out
    auth.auth_logout(token)

    with pytest.raises(AccessError):
        other.users_all(token)

##################### ADMIN_USERPERMISSION_CHANGE() TESTS ######################

def test_userpermission_change_valid():
    """
    Base case for admin_userpermission_change()
    """
    other.clear()

    # Create two users
    token1 = auth.auth_register(*user1)['token']

    u_id2 = auth.auth_register(*user2)['u_id']

    # User 1 (Flockr owner) changes user 2's permissions to owner level.
    other.admin_userpermission_change(token1, u_id2, 1)

    # User 1 then creates a channel and invites user 2 in.
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)

    # Checks if user 2 is automatically an owner
    owners = channel.channel_details(token1, channel_id)['owner_members']
    is_owner = False
    for owner in owners:
        if owner['u_id'] == u_id2:
            is_owner = True

    assert is_owner

def test_userpermission_change_not_owner():
    """
    Test for normal members calling admin_userpermission_change().
    """
    other.clear()

    u_id1 = auth.auth_register(*user1)['u_id']

    token2 = auth.auth_register(*user2)['token']

    with pytest.raises(AccessError):
        other.admin_userpermission_change(token2, u_id1, -1)

def test_userpermission_change_invalid_uid():
    """
    Test for invalid u_id passed into admin_userpermission_change().
    """
    other.clear()

    account = auth.auth_register(*user1)
    token = account['token']
    u_id = account['u_id']

    with pytest.raises(InputError):
        other.admin_userpermission_change(token, u_id + 1, 1)

def test_userpermission_change_invalid_permission():
    """
    Test for invalid permission_id passed into admin_userpermission_change().
    """
    other.clear()

    token = auth.auth_register(*user1)['token']

    u_id2 = auth.auth_register(*user2)['u_id']

    with pytest.raises(InputError):
        other.admin_userpermission_change(token, u_id2, -1)

    with pytest.raises(InputError):
        other.admin_userpermission_change(token, u_id2, 3)

    with pytest.raises(InputError):
        other.admin_userpermission_change(token, u_id2, 1111)

def test_userpermission_change_invalid_token():
    """
    Test for invalid token passed into admin_userpermission_change().
    """
    other.clear()

    token = auth.auth_register(*user1)['token']
    account2 = auth.auth_register(*user2)
    u_id2 = account2['u_id']

    # Invalidate token by logging out
    auth.auth_logout(token)

    with pytest.raises(AccessError):
        other.admin_userpermission_change(token, u_id2, 1)

################################ SEARCH() TESTS ###############################

def test_search_valid():
    """ Base case for search(). """
    other.clear()
    token = auth.auth_register(*user1)['token']

    channel_id = channels.channels_create(token, "Test1", True)['channel_id']
    channel.channel_leave(token, channel_id)
    channel_id = channels.channels_create(token, "Test2", True)['channel_id']
    message.message_send(token, channel_id, "Hello!")
    message.message_send(token, channel_id, "HELLO?")
    message.message_send(token, channel_id, "Yellow.")
    message.message_send(token, channel_id, "ELLO!")
    message.message_send(token, channel_id, "ello?")
    message.message_send(token, channel_id, "I am deceased.")

    assert len(other.search(token, "ello")['messages']) == 5
    assert len(other.search(token, "ThisShouldNotBeFound")['messages']) == 0

def test_search_invalid_token():
    """
    Test for invalid token passed into search().
    """
    other.clear()

    token = auth.auth_register(*user1)['token']

    channel_id = channels.channels_create(token, "Test", True)['channel_id']
    message.message_send(token, channel_id, "Hello!")

    # Invalidate token by logging out
    auth.auth_logout(token)

    with pytest.raises(AccessError):
        other.search(token, "ello")
