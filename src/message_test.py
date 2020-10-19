import pytest
import message
import auth
import channel 
import channels
from error import InputError, AccessError
from other import clear
from data import data

def test_message_edit_valid():
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']


    # Create channel
    name = 'Channel'
    channel_id = channels.channels_create(token1, name, True)['channel_id']
    message_valid = "what it do"
    message_edited = "do it what"

    # Sends a valid message
    message_id1 = message.message_send(token1, channel_id, message_valid)
    message.message_edit(token1, message_id1, message_edited)
    assert data['channels'][channel_id]['messages'][0] == message_edited

# Edited message is too long
def test_message_edit_invalid_length():
    clear()

    # Creates a user
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

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
    message_id1 = message.message_send(token1, channel_id, message_valid)

    with pytest.raises(InputError):
        message.message_edit(token1, channel_id, message_error)

# if the user trying to edit is not the owner of the channel or the user
# that sent the message
def test_message_edit_unauthorised_user():
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
    channel.channel_invite(token1, channel_id, u_id2)
    message_valid = "what it do"
    message_edited = "do it what"
    message_id1 = message.message_send(token1, channel_id, message_valid)

    with pytest.raises(AccessError):
        message.message_edit(token2, message_id1, message_edited)
