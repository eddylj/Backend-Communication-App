'''
Tests for all functions in message.py
'''
import pytest
import message
import auth
import channel
import channels
from error import InputError, AccessError
from other import clear
from data import data

############################### MESSAGE_SEND TESTS ###############################
def test_message_send_base():
    '''
    Base tests to test out valid workings of message_send
    '''
    clear()

    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']

    message_valid = "what it do"


    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)


    # Both users should be able to send messages
    message_id1 = message.message_send(token1, channel_id, message_valid)
    assert message_id1['message_id'] == 0

    message_id2 = message.message_send(token2, channel_id, message_valid)
    assert message_id2['message_id'] == 1

    # Both messages stored correctly in database
    assert data['messages'][0] == {
        'message_id' : 0,
        'u_id': u_id1,
        'message' : "what it do",
        'time_created' : 0,
        'channel_id' : channel_id,
    }

    assert data['messages'][1] == {
        'message_id' : 1,
        'u_id': u_id2,
        'message' : "what it do",
        'time_created' : 0,
        'channel_id' : channel_id,
    }

def test_message_send_error_tests():
    '''
    Tests to test the errors from different case using message_send
    '''
    clear()

    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']

    message_valid = "what it do"

    message_error = "what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do what it do what it do what it do what it do \
            what it do what it do what it do what it do "

    # Message is too long
    with pytest.raises(InputError):
        message.message_send(token1, channel_id, message_error)

    # User not part of channel
    with pytest.raises(AccessError):
        message.message_send(token2, channel_id, message_valid)

    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']
    message_id = message.message_send(token1, channel_id, 'what it do')['message_id']

    assert data['messages'][message_id] == {
        'message_id' : message_id,
        'u_id' : int(token1),
        'message' : 'what it do',
        'time_created' : 0,
        'channel_id' : channel_id,
    }

############################### MESSAGE_REMOVE TESTS ###############################
def test_message_remove_invalid_message_id():
    '''
    Tests removing a message with an invalid message id
    '''
    clear()

    # Create user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']

    # Random Message ID
    message_id = 1231415

    with pytest.raises(InputError):
        message.message_remove(token1, message_id)

    # Removing Message Twice
    message_id2 = message.message_send(token1, channel_id, 'what it do')['message_id']
    message.message_remove(token1, message_id2)

    with pytest.raises(InputError):
        message.message_remove(token1, message_id2)

def test_message_remove_not_authorised_member():
    '''
    Test for when a user who is not authorised is trying to remove a message
    '''
    clear()

    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Message
    channel_id1 = channels.channels_create(token1, 'test channel', True)['channel_id']

    message_id1 = message.message_send(token1, channel_id1, 'what it do')['message_id']


    with pytest.raises(AccessError):
        message.message_remove(token2, message_id1)


    # Doesn't matter if you are member of channel
    channel.channel_invite(token1, channel_id1, u_id2)

    with pytest.raises(AccessError):
        message.message_remove(token2, message_id1)


    # Works if you are the owner of channel
    channel.channel_addowner(token1, channel_id1, u_id2)

    message.message_remove(token2, message_id1)
    assert data['messages'][message_id1] == {}

    # Works if you are the owner of flockr (i.e. user1)
    channel_id2 = channels.channels_create(token2, 'second channel', True)['channel_id']
    message_id2 = message.message_send(token2, channel_id2, 'what it do')['message_id']

    message.message_remove(token1, message_id2)
    assert data['messages'][message_id2] == {}

############################### MESSAGE_EDIT TESTS ###############################
def test_message_edit_valid():
    '''
    Base valid case - an authorised user edits a message
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']
    message_valid = "what it do"
    message_edited = "do it what"

    # Sends a valid message
    message_id1 = message.message_send(token1, channel_id, message_valid)['message_id']
    message.message_edit(token1, message_id1, message_edited)
    assert data['messages'][message_id1]['message'] == message_edited

    # Tests for if the edit is an empty string
    message_empty = ""
    message.message_edit(token1, message_id1, message_empty)
    assert data['messages'][message_id1] == {}

def test_message_edit_invalid_length():
    '''
    Tests for if the edited message is over 1000 characters
    '''
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']
    message_valid = "what it do"

    message_error = "what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do "

    message_id1 = message.message_send(token1, channel_id, message_valid)['message_id']

    with pytest.raises(InputError):
        message.message_edit(token1, message_id1, message_error)

def test_message_edit_unauthorised_user():
    '''
    If the user trying to edit is not the owner of the channel or the user
    that sent the message, raise 'AccessError'
    '''
    clear()
    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)
    message_valid = "what it do"
    message_edited = "do it what"
    message_id1 = message.message_send(token1, channel_id, message_valid)['message_id']

    with pytest.raises(AccessError):
        message.message_edit(token2, message_id1, message_edited)
