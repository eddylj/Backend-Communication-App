import message
import pytest
from error import InputError
from other import clear
from data import data
from other import create_account


############################### MESSAGE_SEND TESTS ###############################

def test_message_send_too_long(create_account):
    message = "what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do what it do what it do what it do \
                what it do what it do what it do "
    
    