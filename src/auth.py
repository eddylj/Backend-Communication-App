from data import data
from error import InputError, AccessError
import re 
from other import get_active

# Formula for determining invalid/valid email
regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'

# Function to generate a valid token given a user's email and password
def auth_login(email, password):
    # looping through user database
    for (index, user) in enumerate(data['users']):
        # checking if login details are correct
        if user['email'] == email and user['password'] == password:
            if get_active(index) == None: # checking for a valid token
                data['tokens'].append(index) # updating user's token
            return {
                'u_id': index,
                'token': index,
            }
    raise InputError
# Function to invalidate user's token when logging out
def auth_logout(token):
    # looping through token database
    for (index, active_token) in enumerate(data['tokens']):
        if token == active_token:
            data['tokens'].pop(index) # remove the given token
            return {'is_success': True} # logout is successful
    return {'is_success': False} # non-active token 

# Function to create an account for the new user and return a new token
def auth_register(email, password, name_first, name_last):
    u_id = len(data['users'])
    new_user = {
        'u_id': u_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': (name_first + name_last)[:20]
    }
    # Check if email is valid
    if not is_valid(email):
        raise InputError

    # Check if email is taken. Also checks for people with the same name to
    # create unique handles.
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
    data['tokens'].append(u_id)

    return {
        'u_id': u_id,
        'token': u_id,
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

# Creating a handle
def new_handle(handle, num):
    offset = len(str(num))
    if len(handle) <= (20 - offset):
        return handle + str(num)
    else:
        # Workaround method to replace a substring inside a string from:
        # https://stackoverflow.com/questions/49701989/python-replace-character-range-in-a-string-with-new-string/49702020
        return str(num).join([handle[:20 - offset], handle[20:]])
