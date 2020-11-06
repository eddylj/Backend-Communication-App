""" This module contains test functions for message.py """
import time
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
from other import clear

user = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

# Consider changing user registration to fixtures

############################# MESSAGE_SEND TESTS ###############################

def test_message_send_valid():
    """
    Base case for message_send().
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    timestamp2 = int(time.time())
    msg_id2 = message.message_send(token2, channel_id, "Goodbye")['message_id']

    expected = [
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "Goodbye",
            'time_created': timestamp2
        },
        {
            'message_id': msg_id1,
            'u_id': u_id1,
            'message': "Hello",
            'time_created': timestamp1
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_send_too_long():
    """
    Test case for message_send(), where the passed message exceeds the 1000
    character limit.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

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
        message.message_send(token, channel_id, long_message)

def test_message_send_not_member():
    """
    Test case for message_send(), where the caller is trying to send a message
    to a channel they're not part of.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel using user1
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    with pytest.raises(AccessError):
        message.message_send(token2, channel_id, "Hello")

############################# MESSAGE_REMOVE TESTS #############################

def test_message_remove_valid():
    """
    Base case for message_remove(). Ensures that correct message was deleted.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    msg_id1 = message.message_send(token, channel_id, "Hello")['message_id']
    msg_id2 = message.message_send(token, channel_id, "Goodbye")['message_id']

    message.message_remove(token, msg_id1)

    # Check that message with msg_id2 still remains.
    messages = channel.channel_messages(token, channel_id, 0)['messages']
    assert len(messages) == 1
    assert messages[0]['message_id'] == msg_id2

def test_message_remove_nonexistent():
    """
    Test case for message_remove(), where the message corresponding to the ID
    passed into message_remove() does not exist. e.g. Never been sent or already
    deleted.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    # No messages sent yet
    with pytest.raises(InputError):
        message.message_remove(token, 12345)

    # Sending a message, then removing it
    msg_id = message.message_send(token, channel_id, "Hello")['message_id']
    message.message_remove(token, msg_id)

    with pytest.raises(InputError):
        message.message_remove(token, msg_id)

def test_message_remove_not_owner():
    """
    Test case for message_remove(), where the caller isn't the user who sent the
    message, or an owner of the channel/Flockr.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    timestamp = int(time.time())
    msg_id = message.message_send(token1, channel_id, "Hello")['message_id']

    with pytest.raises(AccessError):
        message.message_remove(token2, msg_id)

    expected = [
        {
            'message_id': msg_id,
            'u_id': u_id1,
            'message': "Hello",
            'time_created': timestamp
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_remove_as_owner():
    """
    Testing if an owner of the flockr or channel can freely remove messages.
    """
    clear()

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

    # User 2 sends a message, then user 1 removes it.
    msg_id = message.message_send(token2, channel_id, "Goodbye")['message_id']
    message.message_remove(token1, msg_id)

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_remove_not_member():
    """
    Edge case for message_remove(), where the caller isn't even in the channel
    where the message is sent. This includes the Flockr owner.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    msg_id = message.message_send(token2, channel_id, "Goodbye")['message_id']

    # User 1 tries to delete user 2's message
    with pytest.raises(AccessError):
        message.message_remove(token1, msg_id)

    # User 2 leaves the channel then tries to delete their message.
    channel.channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message.message_remove(token2, msg_id)

############################## MESSAGE_EDIT TESTS ##############################

def test_message_edit_valid():
    """
    Base case for message_edit(). Editing a message normally and checking
    against channel_messages().
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']
    u_id = account['u_id']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    timestamp = int(time.time())
    msg_id = message.message_send(token, channel_id, "Hello")['message_id']

    expected = [
        {
            'message_id': msg_id,
            'u_id': u_id,
            'message': "Hello",
            'time_created': timestamp
        }
    ]

    assert channel.channel_messages(token, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

    timestamp = int(time.time())
    message.message_edit(token, msg_id, "Goodbye")

    expected[0]['message'] = "Goodbye"
    expected[0]['time_created'] = timestamp
    assert channel.channel_messages(token, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_edit_empty():
    """
    Test case for message_edit(), where the passed string is empty. Should
    delete the message as per specification.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    msg_id = message.message_send(token, channel_id, "Hello")['message_id']

    message.message_edit(token, msg_id, "")

    assert channel.channel_messages(token, channel_id, 0) == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_message_edit_not_owner():
    """
    Test case for message_edit(), where the caller isn't the user who sent the
    message, or an owner of the channel/Flockr.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    timestamp = int(time.time())
    msg_id = message.message_send(token1, channel_id, "Hello")['message_id']

    expected = [
        {
            'message_id': msg_id,
            'u_id': u_id1,
            'message': "Hello",
            'time_created': timestamp
        }
    ]

    with pytest.raises(AccessError):
        message.message_edit(token2, msg_id, "Goodbye")

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_edit_as_owner():
    """
    Testing if an owner of the flockr or channel can freely edit messages.
    """
    clear()

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

    # User 2 sends a message, then user 1 edits it.
    msg_id = message.message_send(token2, channel_id, "Goodbye")['message_id']
    timestamp = int(time.time())
    message.message_edit(token1, msg_id, "Hello")

    expected = [
        {
            'message_id': msg_id,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_edit_not_member():
    """
    Edge case for message_edit(), where the caller isn't even in the channel
    where the message is sent. This includes the Flockr owner.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    msg_id = message.message_send(token2, channel_id, "Goodbye")['message_id']

    with pytest.raises(AccessError):
        message.message_edit(token1, msg_id, "Hello")

    # User 2 leaves the channel then tries to edit their message.
    channel.channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message.message_edit(token2, msg_id, "Hello")

def test_message_edit_removed():
    """
    Test case for message_edit(), where the target message to be edited has
    already been removed.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    msg_id = message.message_send(token, channel_id, "Hello")['message_id']

    message.message_remove(token, msg_id)
    with pytest.raises(InputError):
        message.message_edit(token, msg_id, "Goodbye")

def test_message_edit_too_long():
    """
    Test case for message_edit(), where the passed message exceeds the 1000
    character limit.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']
    msg_id = message.message_send(token, channel_id, "Hello")['message_id']

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
        message.message_edit(token, msg_id, long_message)

def test_message_edit_identical():
    """
    Test case where message passed into message_edit is the same as the existing
    message stored in data.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

    msg_id = message.message_send(token, channel_id, "Hello")['message_id']
    message.message_send(token, channel_id, "What?")
    message.message_send(token, channel_id, "Goodbye")

    with pytest.raises(InputError):
        message.message_edit(token, msg_id, "Hello")

# Checking invalid token
def test_message_invalid_token():
    """
    Test for invalid tokens throughout all message functions
    """
    clear()

    # Register a user and create a channel with one message in it.
    token = auth.auth_register(*user1)['token']

    channel_id = channels.channels_create(token, "Test", True)['channel_id']
    msg_id = message.message_send(token, channel_id, "Hello")['message_id']

    # Deactivate token by logging out
    auth.auth_logout(token)

    # Cannot use when token is invalid
    with pytest.raises(AccessError):
        message.message_send(token, channel_id, "Hello")

    with pytest.raises(AccessError):
        message.message_remove(token, msg_id)

    with pytest.raises(AccessError):
        message.message_edit(token, msg_id, "Goodbye")

clear()

############################## MESSAGE_PIN TESTS ##############################

def test_message_pin_valid():
    '''
    Base Test for message_pin. Owner pinning a message and checking with channel_messages()
    '''
    clear()

     # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    # Invite user 1 into the channel
    channel.channel_invite(token2, channel_id, u_id1)

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token2, channel_id, "Hello")['message_id']
    timestamp2 = int(time.time())
    msg_id2 = message.message_send(token2, channel_id, "goodnight")['message_id']

    # Owner of Channel pinning
    message.message_pin(token2, msg_id1)

    # Owner of FLockr pinning
    message.message_pin(token1, msg_id2)

    

    expected = [
        {
            'message_id': msg_id1,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp1
            'is_pinned': True
        },
        {
            'message_id': msg_id2,
            'u_id': u_id1,
            'message': "goodnight",
            'time_created': timestamp2
            'is_pinned': True
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }


def test_message_pin_invalid_message_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Input error when message_id is not valid
    with pytest.raises(InputError):
        message.message_pin(token1, 123415)
    
    # Message is already pinned
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']
    message.message_pin(token1, msg_id1)

    with pytest.raises(InputError):
        message.message_pin(token1, msg_id1)

def test_message_pin_not_member():
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    msg_id = message.message_send(token2, channel_id, "KOOLL")['message_id']

    # Even if flockr owner, cannot pin unless in channel
    with pytest.raises(AccessError):
        message.message_pin(token1, msg_id)

    #If the owner who wants to pin the message leaves
    channel.channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message.message_pin(token2, msg_id)

def test_message_pin_not_owner():
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    msg_id = message.message_send(token2, channel_id, "that one")['message_id']
    
    # Not the owner of the channel
    with pytest.raises(AccessError):
        message.message_pin(token2, msg_id)

############################## MESSAGE_UNPIN TESTS ##############################

def test_message_unpin_valid():
    '''
    Base Test for message_unpin. Owner pinning a message and checking with channel_messages()
    '''
    clear()

     # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    # Invite user 1 into the channel
    channel.channel_invite(token1, channel_id, u_id1)

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token2, channel_id, "Hello")['message_id']

    timestamp2 = int(time.time())
    msg_id2 = message.message_send(token2, channel_id, "what it do")['message_id']

    message.message_pin(token1, msg_id1)
    message.message_pin(token2, msg_id2)

    before_unpinned = [
        {
            'message_id': msg_id1,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp1
            'is_pinned': True
        },
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "What it do",
            'time_created': timestamp2
            'is_pinned': True
        }
    ]

    # Check that the messages were pinned before unpinning
    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': before_unpinned,
        'start': 0,
        'end': -1
    }

    # Flockr Owner unpinning
    message.message_unpin(token1, msg_id2)

    # Channel Owner unpinning
    message.message_unpin(token2, msg_id1)

    expected = [
        {
            'message_id': msg_id1,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp1
            'is_pinned': False
        },
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "What it do",
            'time_created': timestamp2
            'is_pinned': False
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_unpin_invalid_message_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Input error when message_id is not valid
    with pytest.raises(InputError):
        message.message_unpin(token1, 123415)
    
    #Message is already unpinned
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']
    msg_id2 = message.message_send(token1, channel_id, "cool story")['message_id']
   
    # Unpinning the same message twice
    message.message_pin(token1, msg_id1)
    message.message_unpin(token1, msg_id1)

    with pytest.raises(InputError):
        message.message_unpin(token1, msg_id1)

    # Unpinning a message that was never pinned
    with pytest.raises(InputError):
        message.message_unpin(token1, msg_id2)

def test_message_unpin_not_member():
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel
    channel_id = channels.channels_create(token2, "Testing", True)['channel_id']

    msg_id = message.message_send(token2, channel_id, "KOOLL")['message_id']
    message.message_pin(token2, msg_id)

    with pytest.raises(AccessError):
        message.message_unpin(token1, msg_id)

    #If the owner who wants to pin the message leaves
    channel.channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message.message_unpin(token2, msg_id)

def test_message_unpin_not_owner():
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)

    msg_id = message.message_send(token2, channel_id, "that one")['message_id']
    message.message_pin(token1, msg_id)

    # Not the owner of the channel
    with pytest.raises(AccessError):
        message.message_unpin(token2, msg_id)




############################## MESSAGE_SENDLATER TESTS ##############################

def test_message_sendlater_valid():
    """
    Base case for message_sendlater().
    """
    clear()

    # Creates two users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Invite user 2 into the channel
    channel.channel_invite(token1, channel_id, u_id2)
    
    # Sends two messages in the future
    future_time1 = round(time.time() + 1)
    msg_id1 = message.message_sendlater(token1, channel_id, "I'm famous", future_time1) ['message_id']

    future_time2 = round(time.time() + 2)
    msg_id2 = message.message_sendlater(token2, channel_id, "Plz", future_time2) ['message_id']

    time.sleep(5)

    expected = [
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "Plz",
            'time_created': future_time2,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': msg_id1,
            'u_id': u_id1,
            'message': "I'm famous",
            'time_created': future_time1
            'reacts': [],
            'is_pinned': False
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }

def test_message_sendlater_invalid_channel():
    """
    Test case for message_sendlater() where the message is sent to a channel id that is invalid.
    """
    
    clear()

    # Create a user
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    # An invalid channel id
    channel_id = 123213

    # A valid time 1min in the future
    future_time = round(time.time() + 10)

    with pytest.raises(InputError):
        message.message_send(token1, channel_id, "Hallo guys", future_time)

def test_message_sendlater_too_long():
    """
    Test case for message_sendlater(), where the passed message exceeds the 1000
    character limit.
    """
    clear()

    account = auth.auth_register(*user)
    token = account['token']

    channel_id = channels.channels_create(token, "Testing", True)['channel_id']

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
    # A valid time 1min in the future
    future_time = round(time.time() + 10)

    with pytest.raises(InputError):
        message.message_sendlater(token, channel_id, long_message, future_time)

def test_message_sendlater_invalid_time():
    """
    Test case for message_sendlater() where the specified time to send the message
    is in the past.
    """

    # Create a user
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # An invalid time 1min in the past
    past_time = round(time.time() - 10)

    with pytest.raises(InputError):
        message.message_sendlater(token1, channel_id, "rawr", past_time)

def test_message_sendlater_not_member():
    """
    Test case for message_sendlater(), where the caller is trying to send a message
    to a channel they're not part of.
    """
    clear()

    # Create 2 users
    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    account2 = auth.auth_register(*user2)
    token2 = account2['token']

    # Create channel using user1
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # A valid time 1min in the future
    future_time = round(time.time() + 10)

    with pytest.raises(AccessError):
        message.message_sendlater(token2, channel_id, "Hello", future_time)
