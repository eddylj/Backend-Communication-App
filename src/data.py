"""
Database for all users, channels, tokens and messages, stored in the global variable
'data'
"""

class User:
    """
    User class which holds the necessary identifiers of a user, as well as
    accessor and mutator methods for each attribute.

    Parameters:
        - u_id          (int): Unique identifier for the user.
        - email         (str): Email which the user registered/logs in with.
        - password      (str): SHA256 hash of the user's password.
        - name_first    (str): User's first name.
        - name_last     (str): User's last name.
        - handle_str    (str): User's public handle, which is generating from
                               their name.
        - permission_id (int): User's access level (1 = Admin, 2 = Member)
    """
    def __init__(self, u_id, email, password, name_first, name_last, handle_str,
                 permission_id=None):

        if permission_id is None:
            permission_id = 2

        self.__u_id = u_id
        self.__email = email
        self.__password = password
        self.__name_first = name_first
        self.__name_last = name_last
        self.__handle_str = handle_str
        self.__permission_id = permission_id
        self.__reset_status = False

    def get_uid(self):
        """ Gets the u_id of the user. """
        return self.__u_id

    def get_email(self):
        """ Gets the email of the user. """
        return self.__email
    def set_email(self, new_email):
        """ Changes the user's email. """
        self.__email = new_email

    def get_password(self):
        """ Gets the password hash of the user. """
        return self.__password
    def set_password(self, new_password):
        """ Changes the user's password. """
        self.__password = new_password

    def get_name(self):
        """ Gets the full name of the user. """
        return self.__name_first + " " + self.__name_last
    def set_name(self, new_first_name=None, new_last_name=None):
        """ Changes the user's name. """
        if new_first_name is not None:
            self.__name_first = new_first_name
        if new_last_name is not None:
            self.__name_last = new_last_name

    def get_handle(self):
        """ Gets the handle of the user. """
        return self.__handle_str
    def set_handle(self, new_handle):
        """ Changes the user's handle. """
        self.__handle_str = new_handle

    def get_permissions(self):
        """ Gets the permission of the user. """
        return self.__permission_id
    def set_permissions(self, new_perms):
        """ Changes the user's permissions. """
        self.__permission_id = new_perms

    def get_reset_status(self):
        """ Returns whether or not a password reset was requested. """
        return self.__reset_status
    def set_reset_status(self, is_being_reset):
        """ Changes whether or not the password is being reset. """
        self.__reset_status = is_being_reset

data = {
    # Stores registered users
    'users': [],
    # Stores active channels
    'channels': [],
    # Stores active tokens
    'tokens': [],
    # Stores messages
    'messages': [],
}
