import pytest
import auth
import channels
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
    token0 = users[0]['token']
    token1 = users[1]['token']
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
    output = []
    for user in user_list:
        output.append(auth.auth_register(*user))
    return output
