import time
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
from other import clear

user0 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user1 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

class Data:
    def __init__(self, users, chans):
        self.users = users
        self.channels = chans

    def token(self, user):
        return self.users[user]['token']

    def u_id(self, user):
        return self.users[user]['u_id']

# Pytest fixture to always register 2 users and create 2 channels.
@pytest.fixture
def test_data():
    clear()

    users = register([user0, user1])
    token0 = users['user0']['token']
    token1 = users['user1']['token']
    chans = []
    chans.append(channels.channels_create(token0, "Chan1", True)['channel_id'])
    chans.append(channels.channels_create(token1, "Chan2", True)['channel_id'])

    return Data(users, chans)

def register(user_list):
    """
    Helper function to register users. Returns a list of dictionaries in the
    format: {
        'token': "",
        'u_id': ""
    }
    """
    output = {}
    for user in user_list:
        output["user" + str(len(output))] = auth.auth_register(*user)
    return output

def test_message_send_later_valid(test_data):
    """
    Base case for message_send_later().
    """
    # Invite user 2 into the channel
    token0 = test_data.token("user0")
    token1 = test_data.token("user1")
    u_id0 = test_data.u_id("user0")
    u_id1 = test_data.u_id("user1")
    channel_id = test_data.channels[0]
    channel.channel_invite(token0, channel_id, u_id1)

    # Sends two messages in the future
    future_time1 = round(time.time()) + 1
    message.message_send_later(token0, channel_id, "I'm famous", future_time1)

    future_time2 = round(time.time()) + 2
    message.message_send_later(token1, channel_id, "Plz", future_time2)

    assert not channel.channel_messages(token0, channel_id, 0)['messages']
    time.sleep(3)

    messages = channel.channel_messages(token0, channel_id, 0)['messages']
    assert len(messages) == 2
    assert messages[1]['u_id'] == u_id0
    assert messages[0]['u_id'] == u_id1
    assert messages[1]['time_created'] == future_time1
    assert messages[0]['time_created'] == future_time2
    assert messages[1]['message'] == "I'm famous"
    assert messages[0]['message'] == "Plz"
