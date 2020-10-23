# Assumptions

## Auth
### auth_login()
- A user can login while already being logged in. Auth_login just returns the current active token in that case.
### auth_logout()
- Auth_logout returns {'is_success': False} if invalid token is passed. Conflicting statements in project specs:
    - 6.2: "If a valid token is given, and the user is successfully logged out, it returns true, otherwise false."
    - 6.3: "For all functions except auth_register and auth_login, an AccessError is thrown when the token passed in is not a valid token"
### auth_register()
- If a handle is already taken (multiple people with same name), a number is added at the end to differentiate individual accounts.
    - If the number puts the handle over the 20 character limit, the number would replace characters at the end of the handle string instead.

## Channel
### channel_invite()
- InputError if you try to invite someone that's already in the channel, including yourself.
### channel_details()
- Members are ordered by joining date.
### channel_messages()
- Negative start parameters are treated as invalid.
### channel_leave()
- Last member of a channel can leave, however the channel still remains with the same channel_id.
### channel_join()
- Attempting to join a channel you're already part of raises InputError.
- Flockr owner (global permissions) can join private channels.
### channel_removeowner()
- The flockr owner can remove the last owner in a channel. 

## Channels
### channels_create()
- Creator of a channel automatically joins that channel.
