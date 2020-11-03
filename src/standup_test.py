""" This module contains test functions for standup.py """
import time
import pytest
import auth
import channel
import channels
import standup
from error import InputError, AccessError
from other import clear

user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

############################# STANDUP_START TESTS ##############################

def register(user_list):
    """
    Helper function to register users. Returns a list of dictionaries in the
    format: {
        'token': "",
        'u_id': ""
    }
    """
    output = []
    for user in user_list:
        output.append(auth.auth_register(*user))
    return output

def test_standup_start_valid():
    """ Base case for standup_start. """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']
    u_id1 = users[0]['u_id']
    u_id2 = users[1]['u_id']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)

    start_time = round(time.time())
    end_time = standup.standup_start(token1, channel_id, 3)['time_finish']
    assert end_time == start_time + 3
    assert standup.standup_active(token1, channel_id)['is_active'] == True

    standup.standup_send(token1, channel_id, "Is this working?")
    standup.standup_send(token2, channel_id, "Should be")

    time.sleep(3)
    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['time_created'] == start_time + 3
    assert messages[0]['message'] == """haydeneverest: Is this working?
    andrasarato: Should be"""

def test_standup_start_no_messages():
    """
    Testing behaviour of standup_start if nothing was send using standup_send
    while the standup was active.
    """
    # Assumed that nothing gets sent into channel if nothing was sent during
    # standup.
    clear()

    users = register([user1])
    token = users[0]['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    standup.standup_start(token, channel_id, 3)

    time.sleep(3)
    assert len(channel.channel_messages(token, channel_id, 0)['messages']) == 0

def test_standup_start_invalid_channel():
    """
    Testing behaviour when an invalid channel_id is passed into standup_start.
    A channel_id
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']

    with pytest.raises(InputError):
        standup.standup_start(token1, 123, 3)

    # Assumed that you must be in the channel to start a standup.
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']
    with pytest.raises(AccessError):
        standup.standup_start(token1, channel_id, 3)

    time.sleep(3) # <- Unsure if this is necessary

def test_standup_start_already_active():
    """
    Testing behaviour when standup_start is called while another standup on the
    same channel is already in progress.
    """
    clear()

    users = register([user1])
    token = users[0]['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    standup.standup_start(token, channel_id, 3)
    assert standup.standup_active(token, channel_id)['is_active'] == True

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, 3)

    time.sleep(3) # <- Unsure if this is necessary

def test_standup_start_sender_leave_before_end():
    """
    Testing this scenario:
        1. User 1 starts a standup in a channel with them and another user (2).
        2. User 2 sends a message through standup_send().
        3. User 2 leaves the channel before standup finishes.
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']
    u_id1 = users[0]['u_id']
    u_id2 = users[1]['u_id']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)

    standup.standup_start(token1, channel_id, 3)

    standup.standup_send(token2, channel_id, "Hello and goodbye.")
    channel.channel_leave(token2, channel_id)

    time.sleep(3)
    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['message'] == "andrasarato: Hello and goodbye."

def test_standup_start_caller_leave_before_end():
    """
    Testing this scenario:
        1. User 1 starts a standup in a channel with them and another user.
        2. User 1 sends a message through standup_send().
        3. User 1 leaves the channel before standup finishes.
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']
    u_id1 = users[0]['u_id']
    u_id2 = users[1]['u_id']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)

    standup.standup_start(token1, channel_id, 3)

    standup.standup_send(token1, channel_id, "I'm out.")
    channel.channel_leave(token1, channel_id)

    time.sleep(3)
    messages = channel.channel_messages(token2, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['message'] == "haydeneverest: I'm out."

# To be added to message_send tests, testing whether or not it can be called
# during a standup. Reference implementation doesn't allow it.

