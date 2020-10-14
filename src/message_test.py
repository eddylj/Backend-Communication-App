import message
import auth, channel, channels
import pytest
from error import InputError
from other import clear
from data import data
from other import create_account


############################### MESSAGE_SEND TESTS ###############################

def test_message_send_error_tests():
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
    channel_id = channels.channels_create(token, name, True)

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

    channel.channel_invite(token1, channel_id, u_id2)

    message_id1 = message.message_send(token1, channel_id, message_valid)
    assert message_id1['message_id'] == 1

    message_id2 = message.message_send(token2, channel_id, message_valid)
    assert message_id2['message_id'] == 2



    