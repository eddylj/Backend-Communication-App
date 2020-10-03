# Assumptions

## Auth
### auth_register()
- If a u_id is already taken (multiple people with same name), a number is added at the end to differentiate individual accounts.

## Channel
### channel_details()
- Name = name of the channel, not members.
- Members are ordered by joining date.
### channel_messages()
- Negative start parameters are treated as invalid.
### channel_leave()
- Leave = user voluntarily leaving a channel, not a target user being removed by an "owner".
- Creator of a channel can leave that channel, however the channel remains.
### channel_join()
- Attempting to join a channel you're already part of raises InputError.

## Channels
### channels_create()
- Creator of a channel automatically joins that channel.

# KEEP IN MIND, U_ID 1 IS A GLOBAL OWNER