# Assumptions

## Auth
###
- If a handle is already taken (multiple people with same name), a number is added at the end to differentiate individual accounts. TO BE CONSIDERED: if a number pushes the handle over the 20 char limit

## Channel
### channel_messages()
- Negative start parameters are treated as invalid 

## Channels
### channels_create()
- Creator of a channel automatically joins that channel
