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

############################## MESSAGE_UNPIN TESTS ##############################

def test_message_react_valid():
    '''
    Base Test for message_react. Owner reacting to a message and checking with channel_messages()
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

    # Owner of Channel reacting
    message.message_react(token2, msg_id1, 1)

    # Invitee reacting
    message.message_react(token1, msg_id2, 1)

    expected = [
        {
            'message_id' : msg_id2,
            'u_id': u_id2,
            'message' : "goodnight",
            'time_created': timestamp2,
            'reacts' : [1],
            'is_pinned': False, 
        },   
        {
            'message_id': msg_id1,
            'u_id' : u_id2,
            'message' : "Hello",
            'time_created' : timestamp1,
            'reacts' : [1],
            'is_pinned': False, 
        },
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages' : expected,
        'start' : 0,
        'end' : -1
    }

def test_message_react_invalid_message_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Input error when message_id is not valid
    with pytest.raises(InputError):
        message.message_react(token1, 123415, 1)
    

def test_message_react_invalid_react_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    # Input error when react_id is not valid -> isn't this test flawed because 12345 could potentially be a valid react_id later on
    with pytest.raises(InputError):
        message.message_react(token1, msg_id1, 12345)

    
def test_message_react_already_reacted():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    # User reacting once
    message.message_react(token1, msg_id1, 1)

    # User reacting twice
    with pytest.raises(InputError):
        message.message_react(token1, msg_id1, 1)


############################## MESSAGE_UNPIN TESTS ##############################

def test_message_unreact_valid():
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
    channel.channel_invite(token2, channel_id, u_id1)

    # Send messages
    timestamp1 = int(time.time())
    msg_id1 = message.message_send(token2, channel_id, "Hello")['message_id']

    timestamp2 = int(time.time())
    msg_id2 = message.message_send(token2, channel_id, "what it do")['message_id']

    message.message_react(token1, msg_id1, 1)
    message.message_react(token2, msg_id2, 1)

    before_unreacted = [
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "what it do",
            'time_created': timestamp2,
            'reacts' : [1],
            'is_pinned': False, 
        },
        {
            'message_id': msg_id1,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp1,
            'reacts' : [1],
            'is_pinned': False, 
        },
    ]

    # Check that the messages were pinned before unpinning
    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': before_unpinned,
        'start': 0,
        'end': -1
    }

    # Flockr Owner unpinning
    message.message_unreact(token1, msg_id2, 1)

    # Channel Owner unpinning
    message.message_unreact(token2, msg_id1, 1)

    expected = [
        {
            'message_id': msg_id2,
            'u_id': u_id2,
            'message': "what it do",
            'time_created': timestamp2,
            'reacts' : [],
            'is_pinned': False, 
        },
        {
            'message_id': msg_id1,
            'u_id': u_id2,
            'message': "Hello",
            'time_created': timestamp1,
            'reacts' : [],
            'is_pinned': False, 
        }
    ]

    assert channel.channel_messages(token1, channel_id, 0) == {
        'messages': expected,
        'start': 0,
        'end': -1
    }


def test_message_unreact_invalid_message_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']

    # Input error when message_id is not valid
    with pytest.raises(InputError):
        message.message_unreact(token1, 123415, 1)


def test_message_unreact_invalid_react_id():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    
    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    
    # Create message
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    with pytest.raises(InputError):
        message.message_unpin(token1, msg_id1, 12345)


def test_message_unreact_already_unreacted():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    
    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    
    # Create messages
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']
    msg_id2 = message.message_send(token1, channel_id, "cool story")['message_id']
   
    # Unreacting the same message twice
    message.message_react(token1, msg_id1, 1)
    message.message_unreact(token1, msg_id1, 1)

    with pytest.raises(InputError):
        message.message_unreact(token1, msg_id1, 1)


def test_message_unreact_never_reacted():
    clear()

    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    
    # Create channel
    channel_id = channels.channels_create(token1, "Testing", True)['channel_id']
    
    # Create message
    msg_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    # Unreacting a message that was never reacted
    with pytest.raises(InputError):
        message.message_unpin(token1, msg_id2, 1)
