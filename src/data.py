"""
Database for all users, channels, tokens and messages, stored in the global variable
'data'
"""
# class Channel:
#     def __init__(self, channel_id, name, owners, )

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
        all_users = data['users'].list_all(by_email=True)
        del all_users[self.__email]
        self.__email = new_email
        all_users[new_email] = self

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

    def output(self):
        return {
            'u_id': self.__u_id,
            'email': self.__email,
            'name_first': self.__name_first,
            'name_last': self.__name_last,
            'handle_str': self.__handle_str,
            'profile_img_url': None
        }

class Users:
    """
    Users object which contains dictionaries of user, keyed by ID and email, and
    accessor and mutator functions to see current users and add new ones.
    """
    def __init__(self):
        self.__users_by_id = {}
        self.__users_by_email = {}

    def get_user(self, u_id=None, email=None):
        """
        Given a unique identifier (ID or email), returns a reference to that
        user.
        """
        if u_id is not None:
            return self.__users_by_id[u_id]
        elif email is not None:
            return self.__users_by_email[email]

    def add_user(self, user):
        """ Adds a user object to both dictionaries. """
        self.__users_by_id[user.get_uid()] = user
        self.__users_by_email[user.get_email()] = user

    def list_all(self, by_email=None):
        """
        Lists all users. Returns the dictionary with u_id as keys by default,
        but can return the dictionary with email keys if by_email is given.
        """
        if by_email is not None:
            return self.__users_by_email
        return self.__users_by_id

    def num_users(self):
        """ Returns the current number of registered users. """
        return len(self.__users_by_id)

    def clear(self):
        """ Clears the data stored in this Users object. """
        self.__users_by_id.clear()
        self.__users_by_email.clear()

data = {
    # Stores registered users by u_id and email
    'users': Users(),
    # Stores active channels
    'channels': [],
    # Stores active tokens by u_id
    'tokens': {},
    # Stores messages
    'messages': [],
}
