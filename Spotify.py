import os
import json
import spotipy
import requests
import spotipy.util as util
from simplejson import JSONDecodeError

username = '< YOUR_SPOTIFY_LOGIN >'
scope = 'user-read-playback-state user-modify-playback-state'
client_id = '< YOUR_CLIENT_ID>'
client_secret = '< YOUR_CLIENT_SECRET>'
redirect_uri = 'http://localhost:8888/callback'

try:
    token = util.prompt_for_user_token(
        username, scope, client_id, client_secret, redirect_uri)
except (AttributeError, JSONDecodeError):
    os.remove('.cache-'+username)
    token = util.prompt_for_user_token(
        username, scope, client_id, client_secret, redirect_uri)

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer "+token,
    'Content-Type': "application/json",
}


def find_device_id_by_name(name='raspotify'):
    url = 'https://api.spotify.com/v1/me/player/devices'
    r = requests.get(url, headers=headers)
    data = r.json()
    for device in data['devices']:
        if name == device['name']:
            deviceID = device['id']
            break

    if deviceID:
        print name + " id is: " + deviceID
        return deviceID
    else:
        print "Couldn't find device with this name"


def switch_device_and_play_music():
    deviceID = find_device_id_by_name('raspotify')
    url = 'https://api.spotify.com/v1/me/player'
    data = '{"device_ids":["'+deviceID+'"]}'
    r = requests.put(url, data=data, headers=headers)

    if r.text:
        print r.text
    else:
        print 'Device changed'
