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

############################# MESSAGE_SEND TESTS ###############################

def test_message_send_valid():
    """
    Base case for message_send(), as well as an additional test to see if
    messages persist if a user leaves the channel after sending one.
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
    # Processing time could potentially affect pytest results
    time1 = int(time.time())
    m_id1 = message.message_send(token1, channel_id, "Hello")['message_id']

    time2 = int(time.time())
    m_id2 = message.message_send(token2, channel_id, "Goodbye")['message_id']

    expected = {
        'messages': [
            {
                'message_id': m_id1,
                'u_id': u_id1,
                'message': "Hello",
                'time_created': time1
            },
            {
                'message_id': m_id2,
                'u_id': u_id2,
                'message': "Goodbye",
                'time_created': time2
            }
        ],
        'start': 0,
        'end': -1
    }

    assert channel.channel_messages(token1, channel_id, 0) == expected

    # User2 leaves the channel
    channel.channel_leave(token2, channel_id)
    assert channel.channel_messages(token1, channel_id, 0) == expected

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

############################ CHANNELS_LISTALL TESTS ############################



############################# CHANNELS_LIST TESTS ##############################

clear()
