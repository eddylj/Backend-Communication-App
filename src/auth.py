from data import data
from error import InputError
import re 
from other import activate_token

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'

def auth_login(email, password):
    index = 0
    for user in data['users']:
        index += 1
        if user['email'] == email and user['password'] == password:
            activate_token(email)
            return {
                'u_id': index,
                'token': email,
            }
    raise InputError

def auth_logout(token):
    for index in range(len(data['tokens'])):
        if data['tokens'][index] == token:
            data['tokens'].pop(index)
            return {'is_success': True}
    return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    new_user = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
    }

    # Check if email is valid
    if not is_valid(email):
        raise InputError

    # Check if email is taken
    for user in data['users']:
        if user['email'] == email:
            raise InputError
    
    # Check if password is valid
    if len(new_user['password']) < 6:
        raise InputError

    # Check if first name is valid
    if not 1 <= len(new_user['name_first']) <= 50:
        raise InputError

    # Check if last name is valid
    if not 1 <= len(new_user['name_last']) <= 50:
        raise InputError
    
    data['users'].append(new_user)
    activate_token(email)

    return {
        'u_id': len(data['users']),
        'token': email,
    }


# Code provided in project specs, from:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Checks if email is valid
def is_valid(email):  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):
        return True
          
    else:  
        return False
