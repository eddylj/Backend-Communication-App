# Assumptions

## Auth
### auth_login()
- A user can "login" while already being logged in. Auth_login just returns the current active token in that case.
### auth_logout()
- Auth_logout returns {'is_success': False} if invalid token is passed. Conflicting statements in project specs:
    - 6.2: "If a valid token is given, and the user is successfully logged out, it returns true, otherwise false."
    - 6.3: "For all functions except auth_register and auth_login, an AccessError is thrown when the token passed in is not a valid token"
### auth_register()
- If a handle is already taken (multiple people with same name), a number is added at the end to differentiate individual accounts.
    - If the number puts the handle over the 20 character limit, the number would replace characters at the end of the handle string instead.
### auth_passwordreset_request()
- If an email is given which does not refer to a registered account, then raise InputError
- Reset codes will expire after 10 minutes.
### auth_passwordreset_request()
- If the new password is the same as the existing one, raise InputError.

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
- If removeowner() is called on a normal member/non-owner, InputError is raised.

## Channels
### channels_create()
- Creator of a channel automatically joins that channel.

## Message
- message_id is unique across all channels
### message_send()
- The Flockr owner cannot send messages into a channel without being in it.
- Message cannot be empty. Raise InputError in that case.
### message_remove()
- Users can't remove message from another channel. 
- Flockr owner cannot remove messages without being in the channel.
- Users can't remove a message after leaving the channel where the message was sent. Raise AccessError if attempted.
### message_edit()
- Cannot edit message to be longer than 1000 characters
- Flockr owner cannot edit messages without being in the channel.
- Edit updates the timestamp of the message
- Edit raises InputError if passed message is the same as the existing message.
- Edit does not change the original sender's ID if edited by a different user.
### message_pin()
- the owner of the flockr can also pin messages despite not being the owner of the channel, however, they must be in the channel
- only owners in the channel can pin
### message_unpin()
- the owner of the flockr can also unpin messages despite not being the owner of the channel, however, they must be in the channel
- only owners in the channel can unpin
### message_react()
- The user reacting has to be in the channel where the message was sent. raise AccessError otherwise.
- If no message with the passed message_id exists, raise InputError.
^I think this makes more sense^
### message_unreact()
- The user unreacting has to be in the channel where the message was sent. raise AccessError otherwise.
- If no message with the passed message_id exists, raise InputError.
^I think this makes more sense^
- If the user hasn't reacted with an ID of react_id, raise InputError

## User
### user_profile_setname()
- If the new name passed into setname() is exactly the same as the existing name, InputError is raised.
### user_profile_setemail()
- If the new email is the same as the existing email stored in the user's data, InputError is raised.
### user_profile_sethandle()
- If the new handle is the same as the existing handle stored in the user's data, InputError is raised.
- The new handle must comply by the original handle rules, raise InputError otherwise.
    - Between 3-20 characters in length.
    - No uppercase characters.

## Other
### search()
- Searches for messages which contain the query_str, not limited to an exact match.
- Case insensitive.
## Server
### /message
- Some black-box HTTP message tests which need to call /channel/messages for comparison cannot be done because of the latency affecting the accuracy of the timestamp.

## Standup
- Caller must be in the specified channel to use standup functions. If the caller isn't in the channel, AccessError gets raised.
### standup_start()
- Length inputs less than 1 are treated as InputErrors. Float inputs greater than 1 are rounded down to it's floor (largest integer not greater than it).
- If the caller/user that started the standup leaves or logs out before it finishes, the final composite message still gets sent under their name.
- If nothing was sent during the standup through standup_send, no message gets sent into the channel at the end.
- On the other hand, if the composite message is longer than 1000 characters, it still gets sent at the conclusion of the standup.
- The message sent at the end of standup is treated as a regular message that ignores the length limit. It can still be editted.
### standup_send()
- If a sender of a message leaves the channel before the standup finishes, their message still gets sent.
- A user can join a channel mid-standup and send messages into it.