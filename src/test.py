import auth
import pytest
from error import InputError
from other import clear
from data import data

# ASSERT VALUES TO BE CHANGED ACCORDINGLY

# AUTH_REGISTER TESTS

# INVALID PASSWORD
def test_auth_register_invalid_pw():
    short_pw = ('validemail@gmail.com', '12345', 'Hayden', 'Everest')
    empty_pw = ('validemail@gmail.com', '', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        auth.auth_register(*short_pw)
        auth.auth_register(*empty_pw)
    print(data['users'])
    clear()
    print(data['users'])

# INVALID NAME
def test_auth_register_invalid_name():
    email = 'validemail@gmail.com'
    password = '123abc!@#'
    with pytest.raises(InputError):
        # No names entered
        auth.auth_register(email, password, '', '')

        # First name > 50 characters
        auth.auth_register(email, password,
                           'Haaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaaaaaa\
                            aaaaaaaaaaaaaayden', 'Everest')
                            
        # Last name > 50 characters
        auth.auth_register(email, password, 'Hayden',
                           'Eveeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeeeeee\
                            eeeeeeeeeeeeeerest')
    print(data['users'])
    clear()
    print(data['users'])

test_auth_register_invalid_name()
test_auth_register_invalid_pw()