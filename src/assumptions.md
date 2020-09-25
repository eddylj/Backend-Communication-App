# Assumptions

## Auth
### auth_register()
*whats the difference between handle and u_id lol? where is handle even created*
- If a u_id is already taken (multiple people with same name), a number is added at the end to differentiate individual accounts.
    - **TO BE CONSIDERED**: if a number pushes the u_id over the 20 char limit.

## Channel
### channel_details()
- Name = name of the channel, not members
### channel_messages()
- Negative start parameters are treated as invalid.
### channel_leave()
- Leave = user voluntarily leaving a channel, not a target user being removed by an "owner".
- Creator of a channel can leave that channel, however the channel remains.

## Channels
### channels_create()
- Creator of a channel automatically joins that channel.
