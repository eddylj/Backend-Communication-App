"""
This module contains tests for standup routes in server.py.
"""
import requests
from echo_http_test import url


############################# STANDUP_START TESTS ##############################

def test_standup_start_base_http(url, http_test_data):
    """
    Base test making sure standup in http outputs correctly
    """
    start_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'length' : 1,
    }
    r = requests.post(f"{url}/standup/start", json=start_payload)
    assert r.status_code == 200

def test_standup_start_fail_http(url, http_test_data):
    """
    Make sure that it fails when supposed to
    """

    # Invalid channel_id
    start_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : 123415,
        'length' : 1,
    }
    r = requests.post(f"{url}/standup/start", json=start_payload)
    assert r.status_code == 400

    # Active standup already
    start_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'length' : 10,
    }
    requests.post(f"{url}/standup/start", json=start_payload)


    start_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'length' : 1,
    }
    r = requests.post(f"{url}/standup/start", json=start_payload)
    assert r.status_code == 400


############################# STANDUP_ACTIVE TESTS #############################

def test_standup_active_base_http(url, http_test_data):
    """
    Make sure server outputting the correct output when running this
    """
    active_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
    }
    r = requests.get(f"{url}/standup/active", params=active_payload)
    assert r.status_code == 200

def test_standup_active_fail_http(url, http_test_data):
    """
    Make sure server outputting error when error
    """
    # Invalid channel_id
    active_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : 123145
    }
    r = requests.get(f"{url}/standup/active", params=active_payload)
    assert r.status_code == 400


############################## STANDUP_SEND TESTS ##############################

def test_standup_send_base_http(url, http_test_data):
    """
    Standup_send, server is outputting the correct output
    """

    # Activate standup
    start_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'length' : 10,
    }
    requests.post(f"{url}/standup/start", json=start_payload)


    # Standup send
    send_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'message' : "what it do",
    }
    r =requests.post(f"{url}/standup/send", json=send_payload)
    assert r.status_code == 200

def test_standup_send_fail_http(url, http_test_data):
    """
    Standup_send server sends correct error message
    """

    # Standup send
    send_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(0),
        'message' : "what it do",
    }
    r = requests.post(f"{url}/standup/send", json=send_payload)
    assert r.status_code == 400

    # User not part of channel
    send_payload = {
        'token' : http_test_data.token(0),
        'channel_id' : http_test_data.channel(1),
        'message' : "ok bruh",
    }
    r = requests.post(f"{url}/standup/send", json=send_payload)
    assert r.status_code == 400
