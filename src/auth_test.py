import auth

def test_auth_logout_success():
	assert auth.auth_logout(None) == False

def test_auth_logout_fail():
	assert auth.auth_logout("online") == True