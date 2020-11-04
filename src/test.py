import requests
from echo_http_test import url

user = {
    'email': 'validemail@gmail.com',
    'password': '123abc!@#',
    'name_first': 'Hayden',
    'name_last': 'Everest',
}
test_channel = {
    'token': '',
    'name': 'Test Channel',
    'is_public': True
}

def test_user1_can_post_msg(url):
    # usr1 = test_data.usr1
    r = requests.post(f"{url}/auth/register", json=user)
    account = r.json()
    token = account['token']

    # ch1 = test_data.ch1
    test_channel['token'] = token
    r = requests.post(f"{url}/channels/create", json=test_channel)
    channel = r.json()

    # msg1 = test_data.msg1

    # js = { 'token': usr1.token, 'channel_id': ch1.channel_id, 'message': msg1.message }
    js = { 'token': token, 'channel_id': channel['channel_id'], 'message': "Hello" }

    # msg1.timestamp = int(time.time())
    # res = requests.post(URL1 + 'message/send', json=js)
    print(url)
    res = requests.post(url + 'message/send', json=js)
    ret = res.json()

    assert res.status_code == 200
