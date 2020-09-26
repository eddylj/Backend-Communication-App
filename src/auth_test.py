import auth
import pytest
from error import InputError

def test_auth_login_invalid_email():
    invalid_email = ('invalidemail.com', '123abc!@#')
    with pytest.raises(InputError)
        auth.auth_login(invalid_email)