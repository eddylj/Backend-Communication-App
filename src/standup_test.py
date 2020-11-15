""" This module contains test functions for standup.py """
import time
import pytest
import auth
import channel
import standup
from error import InputError, AccessError
from other import clear

############################# STANDUP_START TESTS ##############################

def test_standup_start_valid(test_data):
    """
    Base case for standup_start(), when a user tries to start a standup in a
    channel without an ongoing one.
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id0 = test_data.u_id(0)
    u_id1 = test_data.u_id(1)
    channel_id = test_data.channel(0)

    channel.channel_invite(token0, channel_id, u_id1)

    start_time = round(time.time())
    end_time = standup.standup_start(token0, channel_id, 1)['time_finish']
    assert end_time == start_time + 1
    assert standup.standup_active(token0, channel_id)['is_active']

    standup.standup_send(token0, channel_id, "Is this working?")
    standup.standup_send(token1, channel_id, "Should be")

    assert not channel.channel_messages(token0, channel_id, 0)['messages']

    time.sleep(1.1)
    messages = channel.channel_messages(token0, channel_id, 0)['messages']
    assert messages
    assert messages[0]['u_id'] == u_id0
    assert messages[0]['time_created'] == start_time + 1
    assert messages[0]['message'] == '''haydeneverest: Is this working?
andrasarato: Should be'''

    clear()

def test_standup_start_no_messages(test_data):
    """
    Testing behaviour of standup_start if nothing was send using standup_send
    while the standup was active. Assumed that nothing gets sent into channel if
    nothing was sent during the standup.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token, channel_id, 1)

    time.sleep(1.1)
    assert not channel.channel_messages(token, channel_id, 0)['messages']

    clear()

def test_standup_start_invalid_channel(test_data):
    """
    Testing behaviour when an invalid channel_id is passed into standup_start.
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
    """
    token0 = test_data.token(0)

    with pytest.raises(InputError):
        standup.standup_start(token0, 123, 1)

    # Assumed that you must be in the channel to start a standup.
    channel_id = test_data.channel(1)
    with pytest.raises(AccessError):
        standup.standup_start(token0, channel_id, 1)

    clear()

def test_standup_start_already_active(test_data):
    """
    Testing behaviour when standup_start is called while another standup on the
    same channel is already in progress. Expected to raise an InputError.
    """
    token = test_data.token(0)

    channel_id = test_data.channel(0)
    standup.standup_start(token, channel_id, 1)
    assert standup.standup_active(token, channel_id)['is_active']

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, 1)

    time.sleep(1.1)
    clear()

def test_standup_start_sender_leave_before_end(test_data):
    """
    Testing this scenario:
        1. User 1 starts a standup in a channel with them and another user (2).
        2. User 2 sends a message through standup_send().
        3. User 2 leaves the channel before standup finishes.
    Expected to record User 2's message successfully.
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id0 = test_data.u_id(0)
    u_id1 = test_data.u_id(1)
    channel_id = test_data.channel(0)

    channel.channel_invite(token0, channel_id, u_id1)

    standup.standup_start(token0, channel_id, 1)

    standup.standup_send(token1, channel_id, "Hello and goodbye.")
    channel.channel_leave(token1, channel_id)

    time.sleep(1.1)
    messages = channel.channel_messages(token0, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id0
    assert messages[0]['message'] == "andrasarato: Hello and goodbye."

    clear()

def test_standup_start_caller_leave_before_end(test_data):
    """
    Testing this scenario:
        1. User 1 starts a standup in a channel with them and another user.
        2. User 1 sends a message through standup_send().
        3. User 1 leaves the channel before standup finishes.
    Expected to send the final message under User 1's name anyway.
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id0 = test_data.u_id(0)
    u_id1 = test_data.u_id(1)
    channel_id = test_data.channel(0)

    channel.channel_invite(token0, channel_id, u_id1)

    standup.standup_start(token0, channel_id, 1)

    standup.standup_send(token0, channel_id, "I'm out.")
    assert not channel.channel_messages(token1, channel_id, 0)['messages']
    channel.channel_leave(token0, channel_id)

    time.sleep(1.1)
    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages
    assert messages[0]['u_id'] == u_id0
    assert messages[0]['message'] == "haydeneverest: I'm out."

    clear()

def test_standup_start_caller_logout(test_data):
    """
    Testing behaviour when the user who started the standup logs out before it
    finishes. The final message is expected to send anyway.
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id0 = test_data.u_id(0)
    u_id1 = test_data.u_id(1)
    channel_id = test_data.channel(0)

    channel.channel_invite(token0, channel_id, u_id1)

    standup.standup_start(token0, channel_id, 1)

    standup.standup_send(token0, channel_id, "I'm out.")
    assert not channel.channel_messages(token1, channel_id, 0)['messages']
    auth.auth_logout(token0)

    time.sleep(1.1)
    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages
    assert messages[0]['u_id'] == u_id0
    assert messages[0]['message'] == "haydeneverest: I'm out."

    clear()

def test_standup_start_invalid_length(test_data):
    """
    Testing behaviour for the edge case where the length passed into
    standup_start is less than 1. Expected to raise InputError.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, 0.9)

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, 0)

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, -10)

    clear()

def test_standup_start_long_composite_message(test_data):
    """
    Testing behaviour when the final message to be sent into the channel at the
    end of a standup exceeds 1000 characters in length.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token, channel_id, 1)

    # haydeneverest: Hello there. :) -> 30 character string
    # Repeated 34 times to create a final string of 1020 + 33 (newlines) chars.
    for _ in range(34):
        standup.standup_send(token, channel_id, "Hello there. :)")

    time.sleep(1.1)
    messages = channel.channel_messages(token, channel_id, 0)['messages']
    print(messages[0]['message'])
    assert len(messages[0]['message']) == 1053

    clear()

def test_standup_start_invalid_token(test_data):
    """
    Testing behaviour when an inactive or invalid token is passed into
    standup_start(). Expected to raise an AccessError.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    # Tampered token
    with pytest.raises(AccessError):
        standup.standup_start(token + "tZSI6", channel_id, 1)

    # Inactive token
    auth.auth_logout(token)
    with pytest.raises(AccessError):
        standup.standup_start(token, channel_id, 1)

    clear()

# To be added to message_send tests, testing whether or not it can be called
# during a standup. Reference implementation doesn't allow it.

############################# STANDUP_ACTIVE TESTS #############################

def test_standup_active_valid(test_data):
    """ Base case for standup_active(), with both active and inactive cases. """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    assert not standup.standup_active(token, channel_id)['is_active']
    assert standup.standup_active(token, channel_id)['time_finish'] is None

    start_time = round(time.time())
    standup.standup_start(token, channel_id, 1)
    status = standup.standup_active(token, channel_id)
    assert status['is_active']
    assert status['time_finish'] == start_time + 1

    time.sleep(1.1)

    assert not standup.standup_active(token, channel_id)['is_active']

    clear()

def test_standup_active_invalid_channel(test_data):
    """
    Testing behaviour when an invalid channel_id is passed into standup_active.
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    channel_id = test_data.channel(0)

    standup.standup_start(token0, channel_id, 1)

    with pytest.raises(AccessError):
        standup.standup_active(token1, channel_id)

    with pytest.raises(InputError):
        standup.standup_active(token0, channel_id + 100)

    time.sleep(1.1)
    clear()

def test_standup_active_invalid_token(test_data):
    """
    Testing behaviour when an inactive or invalid token is passed into
    standup_active(). Expected to raise an AccessError.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token, channel_id, 1)

    # Tampered token
    with pytest.raises(AccessError):
        standup.standup_active("UzI1N" + token, channel_id)

    # Inactive token
    auth.auth_logout(token)
    with pytest.raises(AccessError):
        standup.standup_active(token, channel_id)

    time.sleep(1.1)
    clear()

############################## STANDUP_SEND TESTS ##############################

def test_standup_send_valid(test_data):
    """
    Base case for standup_send(), when a user tries to send a message during
    an active standup.
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id1 = test_data.u_id(1)
    channel_id = test_data.channel(0)

    channel.channel_invite(token0, channel_id, u_id1)

    standup.standup_start(token0, channel_id, 1)

    standup.standup_send(token0, channel_id, "Is this working?")
    standup.standup_send(token1, channel_id, "Should be")
    assert not channel.channel_messages(token0, channel_id, 0)['messages']

    time.sleep(1.1)
    messages = channel.channel_messages(token0, channel_id, 0)['messages']
    assert messages
    assert messages[0]['message'] == """haydeneverest: Is this working?
andrasarato: Should be"""

    clear()

def test_standup_send_join_ongoing(test_data):
    """
    Testing behaviour when a user joins a channel during an ongoing standup and
    tries to send a message through standup_send().
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    u_id0 = test_data.u_id(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token0, channel_id, 2)

    time.sleep(0.5)

    channel.channel_join(token1, channel_id)
    standup.standup_send(token1, channel_id, "Hello there")
    assert not channel.channel_messages(token0, channel_id, 0)['messages']

    time.sleep(1.6)

    messages = channel.channel_messages(token0, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id0
    assert messages[0]['message'] == "andrasarato: Hello there"

    clear()

def test_standup_send_invalid_channel(test_data):
    """
    Testing behaviour when an invalid channel_id is passed into standup_send.
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
    """
    token0 = test_data.token(0)
    token1 = test_data.token(1)
    channel_id = test_data.channel(0)

    standup.standup_start(token0, channel_id, 1)

    with pytest.raises(AccessError):
        standup.standup_send(token1, channel_id, "Let me in!")

    with pytest.raises(InputError):
        standup.standup_send(token0, channel_id + 10, "LET ME INNNNN!!!")

    clear()

def test_standup_send_invalid_message(test_data):
    """
    Testing behaviour when an invalid message is passed into standup_send.
    A message is invalid when it's not between 1-1000 characters in length.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token, channel_id, 1)

    # Empty string
    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, "")

    # 1008-character string
    long_message = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean "
        "commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus "
        "et magnis dis parturient montes, nascetur ridiculus mus. Donec quam "
        "felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla "
        "consequat massa quis enim. Donec pede justo, fringilla vel, aliquet "
        "nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, "
        "venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. "
        "Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. "
        "Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, "
        "consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, "
        "viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus "
        "varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies "
        "nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. "
        "Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem "
        "quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam."
    )
    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, long_message)

    clear()

def test_standup_send_inactive_standup(test_data):
    """
    Testing behaviour when someone tries to call standup_send() when there isn't
    an ongoing standup. Tries both scenarios where:
        1. There hasn't been any standups held in this channel yet.
        2. There has been standups held in this channel.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, "Hello")

    standup.standup_start(token, channel_id, 1)

    time.sleep(1.1)

    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, "Goodbye")

    clear()

def test_standup_send_invalid_token(test_data):
    """
    Testing behaviour when an inactive or invalid token is passed into
    standup_send(). Expected to raise an AccessError.
    """
    token = test_data.token(0)
    channel_id = test_data.channel(0)

    standup.standup_start(token, channel_id, 1)

    # Tampered token
    with pytest.raises(AccessError):
        standup.standup_send("UzI1N" + token, channel_id, "Hello")

    # Inactive token
    auth.auth_logout(token)
    with pytest.raises(AccessError):
        standup.standup_send(token, channel_id, "Hello")

    time.sleep(1.1)
    clear()
