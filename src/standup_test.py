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
    """
    Base case for standup_start(), when a user tries to start a standup in a
    channel without an ongoing one.
    """
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
    assert standup.standup_active(token1, channel_id)['is_active']

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
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
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
    assert standup.standup_active(token, channel_id)['is_active']

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

def test_standup_start_nonpositive_length():
    """
    Testing behaviour for the edge case where the length passed into
    standup_start is non-positive.
    """
    clear()

    users = register([user1])
    token = users[0]['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, 0)

    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, -10)

# To be added to message_send tests, testing whether or not it can be called
# during a standup. Reference implementation doesn't allow it.

############################# STANDUP_ACTIVE TESTS #############################

def test_standup_active_valid():
    """ Base case for standup_active(), with both active and inactive cases. """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    assert not standup.standup_active(token1, channel_id)['is_active']
    assert standup.standup_active(token1, channel_id)['time_finish'] is None
    start_time = round(time.time())
    standup.standup_start(token1, channel_id, 3)
    status = standup.standup_active(token1, channel_id)
    assert status['is_active']
    assert status['time_finish'] == start_time + 3

    time.sleep(3)

    assert not standup.standup_active['is_active']

def test_standup_active_invalid_channel():
    """
    Testing behaviour when an invalid channel_id is passed into standup_active.
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    standup.standup_start(token1, channel_id, 3)

    with pytest.raises(AccessError):
        standup.standup_active(token2, channel_id)

    with pytest.raises(InputError):
        standup.standup_active(token1, channel_id + 10)

    time.sleep(3) # <- Unsure if this is necessary

############################## STANDUP_SEND TESTS ##############################

def test_standup_send_valid():
    """
    Base case for standup_send(), when a user tries to send a message during
    an active standup.
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']
    u_id2 = users[1]['u_id']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    channel.channel_invite(token1, channel_id, u_id2)

    standup.standup_start(token1, channel_id, 3)

    standup.standup_send(token1, channel_id, "Is this working?")
    standup.standup_send(token2, channel_id, "Should be")

    time.sleep(3)
    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages[0]['message'] == """haydeneverest: Is this working?
    andrasarato: Should be"""

def test_standup_send_join_ongoing():
    """
    Testing behaviour when a user joins an ongoing standup and tries to send a
    message through standup_send().
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']
    u_id1 = users[0]['u_id']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    standup.standup_start(token1, channel_id, 5)

    time.sleep(1)

    channel.channel_join(token2, channel_id)
    standup.standup_send(token2, channel_id, "Hello there")

    time.sleep(4)

    messages = channel.channel_messages(token1, channel_id, 0)['messages']
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['message'] == "andrasarato: Hello there"

def test_standup_send_invalid_channel():
    """
    Testing behaviour when an invalid channel_id is passed into standup_send.
    A channel_id is invalid when:
        - No corresponding channel exists. -> InputError
        - Caller is not in the corresponding channel. -> AccessError
    """
    clear()

    users = register([user1, user2])
    token1 = users[0]['token']
    token2 = users[1]['token']

    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    standup.standup_start(token1, channel_id, 3)

    with pytest.raises(AccessError):
        standup.standup_send(token2, channel_id, "Let me in!")

    with pytest.raises(InputError):
        standup.standup_send(token1, channel_id + 10, "LET ME INNNNN!!!")

    time.sleep(3) # <- Unsure if this is necessary

def test_standup_send_invalid_message():
    """
    Testing behaviour when an invalid message is passed into standup_send.
    A message is invalid when it's not between 1-1000 characters in length.
    """
    clear()

    users = register([user1])
    token = users[0]['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']
    standup.standup_start(token, channel_id, 3)

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

    time.sleep(3) # <- Unsure if this is necessary

def test_standup_send_inactive_standup():
    """
    Testing behaviour when someone tries to call standup_send() when there isn't
    an ongoing standup. Tries both scenarios where:
        1. There hasn't been any standups held in this channel yet.
        2. There has been standups held in this channel.
    """
    clear()

    users = register([user1])
    token = users[0]['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, "Hello")

    standup.standup_start(token, channel_id, 1)

    time.sleep(1)

    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, "Goodbye")
