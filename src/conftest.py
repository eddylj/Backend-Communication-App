"""
Conftest file which holds a pytest fixture which registers two users and creates
a channel for each of them.
"""
import requests
import pytest
import auth
import channels
from other import clear

user0 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
user1 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')

class Data:
    """
    Barebones data object which holds the data returned by register, as well
    as the IDs of channels created in the fixture. For simplicity, there are
    only two users, User 0 and User 1, who have tokens (0 and 1 respectively)
    as well as a channel each (likewise, 0 and 1 respectively).
    """
    def __init__(self, users, chans):
        self.__users = users
        self.__channels = chans

    def token(self, user_number):
        """ Gets the token of the nth user. """
        return self.__users[user_number]['token']

    def channel(self, user_number):
        """ Gets the channel created by the nth user. """
        return self.__channels[user_number]

    def u_id(self, user_number):
        """ Gets the u_id of the nth user. """
        return self.__users[user_number]['u_id']

@pytest.fixture
def test_data():
    """
    Pytest fixture which registers two users and creates a channel for each of
    them. The resulting data is then passed to the test functions as a Data
    object.
    """
    clear()

    users = register([user0, user1])
    token0 = users[0]['token']
    token1 = users[1]['token']
    chans = []
    chans.append(channels.channels_create(token0, "Chan1", True)['channel_id'])
    chans.append(channels.channels_create(token1, "Chan2", True)['channel_id'])

    return Data(users, chans)

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    '''
    Fixture for creating a server
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture
def http_test_data(url):
    user0 = {
        'email': 'validemail@gmail.com',
        'password': '123abc!@#',
        'name_first': 'Hayden',
        'name_last': 'Everest',
    }
    user1 = {
        'email': 'alsovalid@gmail.com',
        'password': 'aW5Me@l!',
        'name_first': 'Andras',
        'name_last': 'Arato',
    }
    test_channel = {
        'token': '',
        'name': 'Test Channel',
        'is_public': True
    }

    users = []
    # Create 2 users
    r = requests.post(f"{url}/auth/register", json=user0)
    account0 = r.json()
    users.append(account0)

    r = requests.post(f"{url}/auth/register", json=user1)
    account1 = r.json()
    users.append(account1)

    chans = []
    # Create channel
    print(account0)
    test_channel['token'] = account0['token']
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']
    chans.append(channel_id)

    test_channel['token'] = account1['token']
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel_id = r.json()['channel_id']
    chans.append(channel_id)

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
