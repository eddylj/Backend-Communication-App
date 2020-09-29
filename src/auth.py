from data import data
from error import InputError

def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    new_user = {
        'email' : email,
        'password' : password,
        'first_name' : name_first,
        'last_name' : name_last,
    }

    # Check if email is valid
    if not is_valid(email):
        raise InputError

    # Check if email is taken
    for user in data['users']:
        if user['email'] == email:
            raise InputError
    
    data['users'].append(new_user)

    return {
        'u_id': len(data['users']),
        'token': '12345',
    }


# from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Checks if email is valid

# Python program to validate an Email 
  
# import re module 
  
# re module provides support 
# for regular expressions 
import re 
  
# Make a regular expression 
# for validating an Email 
regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
      
# Define a function for 
# for validating an Email 
def is_valid(email):  
  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True
          
    else:  
        return False