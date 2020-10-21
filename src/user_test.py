import message
import pytest
import user
from error import InputError
from other import clear
from data import data


def profile_valid():
    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']
    email1 = account1['email']
    handle1 = account1['handle']


    user1_details = {
        'u_id': u_id1,
        'email': email1
        'name_first': 'Hayden',
        'name_last': 'Everest',
        'handle': handle
    }

    assert user.user_profile(token1, u_id1) == user1_details

def test_invalid_user():

    '''
    Invalid user accessing different account
    '''

    user1 = ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    account1 = auth.auth_register(*user1)
    token1 = account1['token']
    u_id1 = account1['u_id']

    user2 = ('alsovalid@gmail.com', 'aW5Me@l!', 'Andras', 'Arato')
    account2 = auth.auth_register(*user2)
    token2 = account2['token']
    u_id2 = account2['u_id']

    # Invalid token
    with pytest.raises(InputError):
        user.user_profile(token2, u_id1)

    # Invalid u_id
    with pytest.raises(InputError):
        user.user_profile(token1, u_id2)


