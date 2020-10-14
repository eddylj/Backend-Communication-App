import message
import pytest
from error import InputError
from other import clear
from data import data


############################### MESSAGE_SEND TESTS ###############################

def test_message_send_too_long():
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
    
