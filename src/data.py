"""
Database for all users, channels, tokens and messages, stored in the global variable
'data'
"""
import bisect
from error import InputError
class User:
    """
    User class which holds the necessary identifiers of a user, as well as
    accessor and mutator methods for each attribute.

    Attributes:
        - u_id          (int)       : Unique identifier for the user.
        - email         (str)       : Email which the user registered/logs in
                                      with.
        - password      (str)       : SHA256 hash of the user's password.
        - name_first    (str)       : User's first name.
        - name_last     (str)       : User's last name.
        - handle_str    (str)       : User's public handle, which is generating
                                      from their name.
        - channels      (Channels)  : List of all channels the user is part of.
        - permission_id (int)       : User's access level (1=Admin, 2=Member)
        - reset_status  (bool)      : Whether or not the user requested a
                                      password reset in the last 10 minutes.
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
        self.__channels = Channels()
        self.__reset_status = False

    def get_id(self):
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

    def get_channels(self):
        """ Gets all channels the user is a member of. """
        return self.__channels

    def get_reset_status(self):
        """ Returns whether or not a password reset was requested. """
        return self.__reset_status
    def set_reset_status(self, is_being_reset):
        """ Changes whether or not the password is being reset. """
        self.__reset_status = is_being_reset

    def output(self, url=None):
        """
        Filters sensitive data from the current User object and returns the rest
        in a dictionary. An additional profile_img_url (where the User's display
        picture is stored) is also returned.
        """
        path = f"{url}/static/{self.__u_id}.jpg" if url is not None else None
        return {
            'u_id': self.__u_id,
            'email': self.__email,
            'name_first': self.__name_first,
            'name_last': self.__name_last,
            'handle_str': self.__handle_str,
            'profile_img_url': path
        }

class Users:
    """
    Users object which contains dictionaries of user, keyed by ID and email, and
    accessor and mutator methods to see current users and add/remove new ones.
    """
    def __init__(self):
        self.__users_by_id = {}
        self.__users_by_email = {}

    def get_user(self, u_id=None, email=None):
        """
        Given a unique identifier (ID or email), returns a reference to that
        user.
        """
        try:
            if u_id is not None:
                return self.__users_by_id[u_id]
            elif email is not None:
                return self.__users_by_email[email]
            raise Exception("Must provide a parameter to Users.get_user()")
        except KeyError:
            raise InputError

    def is_user(self, u_id=None, email=None):
        """
        Checks that a user with either a given u_id or email, exists in this
        Users object.
        """
        try:
            if u_id is not None:
                _ = self.__users_by_id[u_id]
                return True
            if email is not None:
                _ = self.__users_by_email[email]
                return True
            raise Exception("Must provide a parameter to Users.is_user()")
        except KeyError:
            return False

    def add_user(self, user):
        """ Adds a user object to the database. """
        self.__users_by_id[user.get_id()] = user
        self.__users_by_email[user.get_email()] = user

    def remove_user(self, u_id=None, email=None):
        """
        Given a unique identifier (ID or email), removes that user from the
        database.
        """
        if u_id is not None:
            user = self.get_user(u_id=u_id)
        elif email is not None:
            user = self.get_user(email=email)
        else:
            raise Exception("Must provide a parameter to Users.remove_user()")

        del self.__users_by_id[user.get_id()]
        del self.__users_by_email[user.get_email()]

    def list_all(self, by_email=None):
        """
        Lists all users. Returns the dictionary with u_id as keys by default,
        but can return the dictionary with email keys if by_email is given.
        """
        if by_email is not None:
            return self.__users_by_email
        return self.__users_by_id

    def list_all_details(self, url=None):
        """
        Returns a list of dictionaries containing in-depth details of all users.
        """
        result = []
        for _, user in self.__users_by_id.items():
            result.append(user.output(url=url))
        return result

    def num_users(self):
        """ Returns the current number of registered users. """
        return len(self.__users_by_id)

    def clear(self):
        """ Clears the data stored in this Users object. """
        self.__users_by_id.clear()
        self.__users_by_email.clear()

class Channel:
    """
    Channel class which stores its own identifying attributes, as well as a
    record of users and messages in it.

    Attributes:
        - channel_id    (int)   : Unique identifier for the channel.
        - name          (str)   : Name of the channel.
        - owners        (Users) : Users class of users with owner permissions in
                                  the channel.
        - members       (Users) : Users class of all users in the channel.
        - is_public     (bool)  : Whether or not the channel is public.
        - messages      (List)  : List of all messages sent in the channel.
    """
    def __init__(self, creator, channel_id, name, is_public):
        self.__channel_id = channel_id
        self.__name = name
        self.__owners = Users()
        self.__members = Users()
        self.__is_public = is_public
        self.__messages = Messages()

        self.join(creator)
        self.__owners.add_user(creator)

    def get_id(self):
        """ Returns the ID of the channel. """
        return self.__channel_id

    def get_name(self):
        """ Returns the name of the channel. """
        return self.__name

    def get_members(self):
        """ Returns the Users object holding all users in the channel. """
        return self.__members
    def is_member(self, u_id):
        """
        Checks whether or not a user with u_id is a member of this channel.
        """
        return self.__members.is_user(u_id=u_id)

    def get_owners(self):
        """ Returns the Users object holding all owners in the channel. """
        return self.__owners
    def is_owner(self, u_id):
        """
        Checks whether or not a user with u_id is an owner of this channel.
        """
        return self.__owners.is_user(u_id=u_id)

    def join(self, user):
        """
        Adds a user to members, and owners if necessary. Also updates the
        channels the user is part of in their own class.
        """
        self.__members.add_user(user)
        if user.get_permissions() == 1:
            self.__owners.add_user(user)
        user.get_channels().add_channel(self)
    def leave(self, u_id):
        """
        Removes a user from members, and owners if necessary. Also updates the
        channels the user is part of in their own class.
        """
        if self.is_owner(u_id):
            self.__owners.remove_user(u_id=u_id)
        self.__members.remove_user(u_id=u_id)
        user = data['users'].get_user(u_id=u_id)
        user.get_channels().remove_channel(self)

    def is_public(self):
        """
        Returns whether or not the channel is public.
        """
        return self.__is_public

    def get_messages(self):
        """
        Returns the list of messages stored in this channel.
        """
        return self.__messages

class Channels:
    """
    Channels object which contains dictionaries of channel objects keyed by ID,
    as well as methods to add and remove them. Other useful properties such as
    number of existing channels are also included.
    """
    def __init__(self):
        self.__channels = {}

    def get_channel(self, channel_id):
        """
        Tries to access a channel given it's channel_id. If the channel isn't
        stored in the Channels object or channel_id is invalid, InputError is
        raised.
        """
        try:
            return self.__channels[channel_id]
        except KeyError:
            raise InputError

    def add_channel(self, channel):
        """
        Adds a channel to the internal dictionary, with it's channel_id as the
        key.
        """
        self.__channels[channel.get_id()] = channel
    def remove_channel(self, channel):
        """ Removes a channel from the internal dictionary. """
        try:
            del self.__channels[channel.get_id()]
        except KeyError:
            raise InputError

    def list_all(self):
        """
        Returns a list of dictionaries containing two keys:
            - channel_id (int): The unique identifier of the channel.
            - name       (str): The name of the channel at creation.
        for all the channels stored.
        """
        output = []
        for _, channel in self.__channels.items():
            output.append({
                'channel_id': channel.get_id(),
                'name': channel.get_name()
            })
        return output

    def num_channels(self):
        """ Returns the number of existing channels """
        return len(self.__channels)

    def clear(self):
        """ Clears all the data stored in the Channels object. """
        self.__channels.clear()

class Message:
    def __init__(self, message_id, channel, sender_id, message, timestamp):
        self.__message_id = message_id
        self.__channel = channel
        self.__u_id = sender_id
        self.__message = message
        self.__time_created = timestamp
        self.__reacts = {}
        self.__is_pinned = False

    def get_id(self):
        return self.__message_id

    def get_channel(self):
        return self.__channel

    def is_sender(self, u_id):
        return self.__u_id == u_id

    def get_message(self):
        return self.__message
    def set_message(self, new_message):
        self.__message = new_message

    def get_timestamp(self):
        return self.__time_created
    def set_time(self, timestamp):
        self.__time_created = timestamp

    def get_reacts(self, react_id):
        return self.__reacts[react_id]
    def add_react(self, user_id, react_id):
        if react_id not in self.__reacts:
            self.__reacts[react_id] = {
                'react_id': react_id,
                'u_ids': [],
                'is_the_user_reacted': False
            }
        bisect.insort(self.__reacts[react_id]['u_ids'], user_id)
        if user_id == self.__u_id:
            self.__reacts[react_id]['is_the_user_reacted'] = True
    def already_reacted(self, user_id, react_id):
        def b_search(start, end, user_id):
            if start >= end:
                return None
            mid = (start + end) // 2
            u_id = self.__reacts[react_id]['u_ids'][mid]

            if u_id == user_id:
                return mid

            if u_id < user_id:
                return b_search(start, mid - 1, user_id)
            return b_search(mid + 1, end, user_id)

        try:
            return b_search(0, len(self.__reacts[react_id]['u_ids']), user_id)
        except KeyError:
            raise InputError

    def remove_react(self, user_id, react_id):
        index = self.already_reacted(user_id, react_id)
        if index is None:
            raise InputError
        if len(self.__reacts[react_id]['u_ids']) == 1:
            del self.__reacts[react_id]
            return
        self.__reacts[react_id]['u_ids'].pop(index)
        if user_id == self.__u_id:
            self.__reacts[react_id]['is_the_user_reacted'] = False

    def is_pinned(self):
        return self.__is_pinned

    def compare(self, message):
        return self.__message == message

    def output(self):
        return {
            'message_id': self.__message_id,
            'u_id': self.__u_id,
            'message': self.__message,
            'time_created': self.__time_created,
            'reacts': list(self.__reacts.values()),
            'is_pinned': self.__is_pinned,
        }

class Messages:
    def __init__(self):
        self.__messages_list = []
        self.__messages_dict = {}

    def is_message(self, message_id):
        return (
            -1 < message_id < self.num_messages() and
            self.__messages_dict[message_id] is not None
        )

    def get_message(self, message_id):
        try:
            message = self.__messages_dict[message_id]
            if message is not None:
                return message
            raise InputError
        except KeyError:
            raise InputError

    def add_message(self, new_message, message_id):
        if new_message is not None:
            self.__messages_list.insert(0, new_message)
        self.__messages_dict[message_id] = new_message

    def remove_message(self, message_id):
        def b_search(start, end, message_id):
            if start >= end:
                return None
            mid = (start + end) // 2
            msg_id = self.__messages_list[mid].get_id()

            if msg_id == message_id:
                return mid

            if msg_id < message_id:
                return b_search(start, mid - 1, message_id)
            return b_search(mid + 1, end, message_id)

        index = b_search(0, len(self.__messages_list), message_id)
        if index is None:
            raise InputError
        self.__messages_list.pop(index)
        self.__messages_dict[message_id] = None

    def get_details(self, start, end):
        if end < 0:
            end = len(self.__messages_list)
        return [self.__messages_list[i].output() for i in range(start, end)]

    def num_messages(self, sent=None):
        if sent is not None:
            return len(self.__messages_list)
        return len(self.__messages_dict)

    def clear(self):
        self.__messages_list.clear()
        self.__messages_dict.clear()

data = {
    # Stores registered users by u_id and email
    'users': Users(),
    # Stores active channels
    'channels': Channels(),
    # Stores active tokens by u_id
    'tokens': {},
    # Stores messages
    'messages': Messages(),
}
