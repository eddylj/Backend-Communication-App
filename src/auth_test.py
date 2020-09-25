from auth import *

def test_auth_logout_success():
#	assert auth.auth_logout(None) == False

	assert auth.auth_logout(None) == {'is_success': True,}

def test_auth_logout_fail():
	assert auth.auth_logout("online") == {'is_success': True,}


def test_auth_reg_login_logout():
    {u_id, token} = auth_register("mechy5@gmail.com", "lolol", "Eddy", "Zhang")
    assert auth_login("mechy5@gmail.com", "lolol") == {u_id, token}
    assert auth_logout(token) == {True} # is_success == True

