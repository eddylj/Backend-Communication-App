'''
Functions used to return and change information regarding user's data
'''
import requests
from PIL import Image
from data import data
from error import InputError, AccessError
from other import get_active, is_valid, validate_token

def user_profile(token, u_id):
    '''
    Return information on the user (u_id, email, first name, last name, handle)
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Invalid user
    if not is_user(u_id):
        raise InputError

    user = data['users'][u_id]

    return_user = {
        'u_id' : user['u_id'],
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle_str'],
    }

    return {'user': return_user}

def user_profile_setname(token, name_first, name_last):
    '''
    Change first or last name of the user if valid
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # name_first invalid length
    if not 1 <= len(name_first) <= 50:
        raise InputError

    # name_last invalid length
    if not 1 <= len(name_last) <= 50:
        raise InputError

    if (data['users'][caller_id]['name_first'] == name_first and
        data['users'][caller_id]['name_last'] == name_last):
        raise InputError

    data['users'][caller_id]['name_first'] = name_first
    data['users'][caller_id]['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    '''
    Change email of the user
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Check if valid email
    if not is_valid(email):
        raise InputError

    # Not used by another account
    for user in data['users']:
        if user['email'] == email:
            raise InputError

    data['users'][caller_id]['email'] = email

    return {}

def user_profile_sethandle(token, handle_str):
    '''
    Change handle of the user
    '''

    caller_id = get_active(token)
    if caller_id is None:
        raise AccessError

    # Invalid length
    if not 3 <= len(handle_str) <= 20:
        raise InputError

    # Check for uppercase letters.
    if not handle_str.islower():
        raise InputError

    # Not used by another account
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise InputError

    data['users'][caller_id]['handle_str'] = handle_str

    return {}

@validate_token
def user_profile_uploadphoto(user_id, img_url, x_start, y_start, x_end, y_end):
    filename = save_image(user_id, img_url)
    print(filename)
    crop_image(filename, x_start, y_start, x_end, y_end)
    return {}

def save_image(user_id, img_url):
    filename = f"src/static/{user_id}.jpg"
    image = requests.get(img_url)
    file = open(filename, "wb")
    file.write(image.content)
    file.close()
    return filename

def crop_image(filename, x_start, y_start, x_end, y_end):
    image = Image.open(filename)
    cropped = image.crop((x_start, y_start, x_end, y_end))
    cropped.save(filename)

def is_user(u_id):
    '''
    Check for valid user ID
    '''
    return -1 < u_id < len(data['users'])
