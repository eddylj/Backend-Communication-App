import channel 
import pytest

def test_channel_invite_base():
    invite = {'token': '', 'channel_id': '', 'u_id': ''}
    channel_inv = {'token': '', 'channel_id': '', 'u_id': ''}
    assert channel.channel_invite(*invite) == channel.channel_invite(*channel_inv)

def test_channel_invite_valid():
    invite = {'token': '123456', "channel_id": '1', 'u_id': '1'}
    channel_inv = {'token': '12345', 'channel_id': '1', 'u_id': '1'}
    assert channel.channel_invite(*channel_inv) == channel.channel_invite(*invite)

# assuming that the channel id aand u_id is a number

def test_channel_invite_invalid():
    invite = {'token': '123456', "channel_id": '1', 'u_id': '1'}
    channel_inv = {'token': '12341', 'channel_id': 'asv', 'u_id': 'nasd'}
    assert channel.channel_invite(*invite) == channel.channel_invite(*channel_inv)

   
# auth user is not already in channel 

def test_channel_invite_access_error():
 
    pass