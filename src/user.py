'''
Functions used to return and change information regarding user's data
'''
import requests
from PIL import Image
from data import data
from error import InputError
from other import is_valid, validate_token

@validate_token
def user_profile(_, u_id, url=None):
    '''
    Return information on the user (u_id, email, first name, last name, handle)
    '''
    user = data['users'].get_user(u_id=u_id)

    return {'user': user.output(url=url)}

@validate_token
def user_profile_setname(caller_id, name_first, name_last):
    '''
    Change first or last name of the user if valid
    '''
    if not (1 <= len(name_first) <= 50 and 1 <= len(name_last) <= 50):
        raise InputError

    user = data['users'].get_user(u_id=caller_id)
    if user.get_name() == f"{name_first} {name_last}":
        raise InputError
    user.set_name(new_first_name=name_first, new_last_name=name_last)
    return {}

@validate_token
def user_profile_setemail(caller_id, email):
    '''
    Change email of the user
    '''
    # Check if valid email
    if not is_valid(email):
        raise InputError

    # Not used by another account
    if data['users'].is_user(email=email):
        raise InputError

    user = data['users'].get_user(u_id=caller_id)
    user.set_email(email)

    return {}

@validate_token
def user_profile_sethandle(caller_id, handle_str):
    '''
    Change handle of the user
    '''
    # Invalid length
    if not 3 <= len(handle_str) <= 20:
        raise InputError

    # Check for uppercase letters.
    if not handle_str.islower():
        raise InputError

    # Not used by another account
    for user in data['users'].list_all_details():
        if user['handle_str'] == handle_str:
            raise InputError

    user = data['users'].get_user(u_id=caller_id)
    user.set_handle(handle_str)

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
    if image.status_code != 200:
        raise InputError

    file = open(filename, "wb")
    file.write(image.content)
    file.close()
    return filename

def crop_image(filename, x_start, y_start, x_end, y_end):
    image = Image.open(filename)
    try:
        cropped = image.crop((x_start, y_start, x_end, y_end))
    except IndexError:
        raise InputError
    cropped.save(filename)
