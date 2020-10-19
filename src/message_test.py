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
#from other import create_account


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

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)

    message_valid = "what it do"


    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)


    # Both users should be able to send messages
    message_id1 = message.message_send(token1, channel_id, message_valid)
    assert message_id1['message_id'] == 1

    message_id2 = message.message_send(token2, channel_id, message_valid)
    assert message_id2['message_id'] == 2



def test_message_send_error_tests():
    '''
    Tests to test the errors from different case using message_send
    '''
    token2 = account2['token']

    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)

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
    message.message_remove(token1, message_id)

    assert data['channels'][channel_id]['messages'] == []


def test_message_remove_invalid_message_id():
    clear()

    # Create user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']
    channel_id2 = channels.channels_create(token1, 'another channel', True)['channel_id']
    
    # Random Message ID
    message_id = 1231415

    with pytest.raises(InputError):
        message.message_remove(token1, message_id)

    # Removing Message Twice
    message_id2 = message.message_send(token1, channel_id, 'what it do')['message_id']
    message.message_remove(token1, message_id2)
    message.message_remove(token1, message_id2)

    with pytest.raises(InputError):
        message.message_remove(token1, message_id2)

    # Removing Message from different channel
    message_id3 = message.message_send(token1, channel_id, 'mechy5')['message_id']
    message_id4 = message.message_send(token1, channel_id2, 'lavar ball')['message_id']
    message.message_remove(token1, message_id4)
    
    with pytest.raises(InputError):
        message.message_remove(token1, message_id4)

# test for when a user who is not authorised is trying to remove a message
def test_message_remove_not_authorised_member():
     clear()

    # Create 2 users
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']  
    
    # Message
    channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']
    message_id = message.message_send(token1, channel_id, 'what it do')['message_id']
    message.message_remove(token2, message_id)

    with pytest.raises(AccessError):
        message.message_remove(token2, message_id)

# def test_message_remove_not_owner():
#     clear()

#       # Create 2 users
#     user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#     account1 = auth.auth_register(*user1)
#     token1 = account1['token']
#     u_id1 = account1['u_id']

#     user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
#     account2 = auth.auth_register(*user2)
#     token2 = account2['token']
#     u_id2 = account2['u_id']

#     user3 = ('alsoalsovalid@gmail.com', '1234abc!@#', 'Mark', 'Head')
#     account3 = auth.auth_register(*user3)
#     token3 = account3['token']
#     u_id3 = account3['u_id']
    
#     channel_id = channels.channels_create(token1, 'test channel', True)['channel_id']

#     messages = data['channels'][channel_id]['messages']
#     message_id = message.message_send(token2, channel_id, messages)
#     message_removed = message.message_remove(token3, message_id)

#     with pytest.raises(AccessError):
#         message.message_remove(token3, message_id)