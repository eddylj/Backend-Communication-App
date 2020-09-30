from data import data
from error import InputError
import re 
from other import is_active

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'

def auth_login(email, password):
    for (index, user) in enumerate(data['users']):
        if user['email'] == email and user['password'] == password:
            if not is_active(email):
                data['tokens'].append(email)
            return {
                'u_id': index + 1,
                'token': email,
            }
    raise InputError

def auth_logout(token):
    for (index, active_token) in enumerate(data['tokens']):
        if token == active_token:
            data['tokens'].pop(index)
            return {'is_success': True}
    return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    new_user = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': (name_first + name_last)[:20]
    }
    # Check if email is valid
    if not is_valid(email):
        raise InputError

    '''
    Check if email is taken. Also checks for people with the same name to
    create unique handles.
    '''
    number = 0
    for user in data['users']:
        if user['email'] == email:
            raise InputError
        if (user['name_first'] == new_user['name_first'] and
            user['name_last'] == new_user['name_last']):
            number += 1

    # Generates a new handle if there are repeated names
    if number != 0:
        new_user['handle'] = new_handle(new_user['handle'], number)

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
    if not is_active(email):
        data['tokens'].append(email)

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

def new_handle(handle, num):
    offset = len(str(num))
    if len(handle) <= (20 - offset):
        return handle + str(num)
    else:
        return str(num).join([handle[:20 - offset], handle[20:]])
