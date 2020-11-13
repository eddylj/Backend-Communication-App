"""
Login, logout and register functions
"""
import threading
from time import time
import hashlib
import smtplib
import ssl
import jwt
from data import data, User
from error import InputError
from other import is_valid, SECRET

def auth_login(email, password):
    """
    Given a registered user's email and password and generates a valid token for
    the user to remain authenticated.

    Parameters:
        email (str)     : User's email
        password (str)  : User's password

    Returns:
        {u_id (int), token (str)}:
            A dictionary containing the user's u_id and a token if the email and
            password can be authenticated against the flockr database.

    Raises:
        InputError:
            When:
                - Email entered is not a valid email.
                - Email entered does not belong to a user.
                - Password is not correct.
    """
    try:
        user = data['users']['by_email'][email]
    except KeyError:
        raise InputError

    if not validate_pw(user, password):
        raise InputError
    u_id = user.get_uid()

    try:
        token = data['tokens'][u_id]
    except KeyError:
        payload = {'u_id': u_id, 'session': time()}
        token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
        data['tokens'][u_id] = token

    return{
        'u_id': u_id,
        'token': token
    }

def validate_pw(user, password):
    """
    Hashes the provided password with SHA256 and compares the result with the
    password hash stored in the specified user's data.

    Parameters:
        user (dict)     : User's stored data.
        password (str)  : Password being checked against data.

    Returns:
        (bool): Whether or not the entered password's hash matches the stored
                hash.
    """
    password = hashlib.sha256(password.encode())
    return password.hexdigest() == user.get_password().hexdigest()

def auth_logout(token):
    """
    Given an active token, invalidates the token to log the user out. If a valid
    token is given, and the user is successfully logged out, it returns true,
    otherwise false.

    Parameters:
        token (str) : User's authorisation hash.

    Returns:
        {is_success (bool)}:
            Whether or not token does correspond to an active token.
    """
    try:
        u_id = jwt.decode(token, SECRET, algorithms='HS256')['u_id']
    except jwt.exceptions.DecodeError:
        return {'is_success': False}

    try:
        del data['tokens'][u_id]
        return {'is_success': True}
    except KeyError:
        return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password, store a new
    account for them in the flockr database. A handle is generated that is the
    concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters.
    If the handle is already taken, an integer (number of people with the same
    name) is added at the end of the handle. The integer will replace end
    characters if needed to stay within the 20 character limit.

    Parameters:
        email (str)     : User's email
        password (str)  : User's password
        name_first (str): User's first name
        name_last (str) : User's last name

    Returns:
        {u_id (int), token (str)}:
            A dictionary containing the user's new u_id and a token if the
            parameters are valid.

    Raises:
        InputError:
            When:
                - Email entered is not a valid email.
                - Email entered already belongs to a user.
                - Password entered is less than 6 characters long.
                - name_first not is between 1 and 50 characters inclusively
                  in length
                - name_last is not between 1 and 50 characters inclusively
                  in length
    """
    u_id = len(data['users']['by_uid'])

    if not is_valid(email):
        raise InputError

    if email in data['users']['by_email']:
        raise InputError

    number = 0
    for _, user in data['users']['by_uid'].items():
        if user.get_name() == f"{name_first} {name_last}":
            number += 1

    is_valid_password(password)
    password = hashlib.sha256(password.encode())

    if not 1 <= len(name_first) <= 50:
        raise InputError

    if not 1 <= len(name_last) <= 50:
        raise InputError

    new_user = User(
        u_id, email, password, name_first, name_last,
        handle_str=(name_first + name_last)[:20].lower()
    )

    # Permission_id for owner (automatically for u_id 0)
    if u_id == 0:
        new_user.set_permissions(1)

    if number != 0:
        new_user.set_handle(new_handle(new_user.get_handle(), number))

    data['users']['by_uid'][u_id] = new_user
    data['users']['by_email'][email] = new_user

    payload = {'u_id': u_id, 'session': time()}
    token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
    data['tokens'][u_id] = token

    return {
        'u_id': u_id,
        'token': token,
    }

def start_email_server():
    """
    Starts a SMTP_SSL session in order to send an email.
    """
    port = 0
    context = ssl.create_default_context()
    return smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)

# Method to send an email to a user adapted from:
# https://realpython.com/python-send-email/#starting-a-secure-smtp-connection
def auth_passwordreset_request(email):
    """
    Given an email, checks against the existing users to see if one registered
    with that email exists. If they do, send a unique reset code to that email,
    otherwise raise InputError. The reset code is a jwt string which expires
    after 10 minutes.

    Parameters:
        email (str): User's email

    Returns:
        {}: An empty dictionary if the code was sent successfully.

    Raises:
        InputError: If no user is registered with the provided email.
    """
    try:
        user = data['users']['by_email'][email]
    except KeyError:
        raise InputError

    authenticator = "flockrauth@gmail.com"
    password = "7P9adNdsvdVYgRu"
    with start_email_server() as server:
        server.login(authenticator, password)
        payload = {
            'u_id': user.get_uid(),
            'exp': time() + 600
        }
        code = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
        message = ("Subject: Flockr password reset\n\n"
                   "Your password reset code is: " + code + "\n"
                   "This code expires in 10 minutes.")

        server.sendmail(authenticator, email, message)
        user.set_reset_status(True)
        # Might not work, needs testing
        def end_reset(user):
            user.set_reset_status(False)
        threading.Timer(600, end_reset, [user])
        server.quit()

    return {}

# Consider adding either:
#   - Logout after password reset
#   - Can only request if logged out
def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a reset code, replace the password stored in the database with the
    new password if the reset code can be verified.

    Parameters:
        reset_code (str)    : Code which was sent to the user's email through
                              auth_passwordreset_request().
        new_password (str)  : New password to replace old.

    Returns:
        {}: An empty dictionary if the user's password was reset successfully.

    Raises:
        InputError:
            When:
                - The reset code doesn't match the one sent out.
                - The reset code expired already.
                - The new password is exactly the same as the old.
                - If the user somehow passed a valid token, but didn't request
                  a password reset.
    """
    try:
        u_id = jwt.decode(reset_code, SECRET, algorithms='HS256')['u_id']
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise InputError

    user = data['users']['by_uid'][u_id]
    if not user.get_reset_status():
        raise InputError

    is_valid_password(new_password)
    new_password = hashlib.sha256(new_password.encode())
    if user.get_password().hexdigest() == new_password.hexdigest():
        raise InputError
    user.set_password(new_password)
    user.set_reset_status(False)

    return {}

def is_valid_password(password):
    """
    Checks if a password is valid (6 or more characters in length). Raises
    InputError if not.
    """
    if len(password) < 6:
        raise InputError
    return True

def new_handle(handle, num):
    """
    Given an existing handle and an integer, generates a new handle by appending
    num to the end of handle. Num will replace end characters if needed to stay
    within the 20 character limit.

    Parameters:
        handle (str): Handle string
        num (int)   : Integer to be appended to handle

    Returns:
        (str): The newly generated handle.
    """
    offset = len(str(num))
    if len(handle) <= (20 - offset):
        return handle + str(num)

    # Workaround method to replace a substring inside a string from:
    # https://stackoverflow.com/questions/49701989/python-replace-character-range-in-a-string-with-new-string/49702020
    return str(num).join([handle[:20 - offset], handle[20:]])
