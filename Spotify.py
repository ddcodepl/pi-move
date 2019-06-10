#!/usr/bin/python
import os
import json
import time
import config
import spotipy
import requests
import subprocess
import spotipy.util as util
from simplejson import JSONDecodeError

# Requirements
# # Run as root

try:
    token = util.prompt_for_user_token(
        config.spotify_username, config.spotify_scope, config.spotify_client_id, config.spotify_client_secret, config.spotify_redirect_uri)
except (AttributeError, JSONDecodeError):
    os.remove('.cache-'+username)
    token = util.prompt_for_user_token(
        config.spotify_username, config.spotify_scope, config.spotify_client_id, config.spotify_client_secret, config.spotify_redirect_uri)

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer "+token,
    'Content-Type': "application/json",
}

deviceName = 'raspotify'


def get_current_device():
    url = 'https://api.spotify.com/v1/me/player/devices'
    r = requests.get(url, headers=headers)
    data = r.json()
    for device in data['devices']:
        if device['is_active'] == True:
            return device['name']


def find_device_id_by_name(name='raspotify'):
    subprocess.Popen(['sudo', 'systemctl', 'restart', 'raspotify'])
    time.sleep(1)
    url = 'https://api.spotify.com/v1/me/player/devices'
    r = requests.get(url, headers=headers)
    data = r.json()
    print data
    deviceID = ' '
    for device in data['devices']:
        if name == device['name']:
            deviceID = device['id']
            return deviceID

    if deviceID:
        print name + " id is: " + deviceID
        return deviceID
    else:
        print "Couldn't find device with this name"


def switch_device_and_play_music():
    # Need root
    currentDevice = get_current_device()

    if currentDevice == deviceName:
        print 'This device is already active'
        return False
    else:
        deviceID = find_device_id_by_name(deviceName)
        url = 'https://api.spotify.com/v1/me/player'
        data = '{"device_ids":["'+deviceID+'"]}'
        r = requests.put(url, data=data, headers=headers)

        time.sleep(1)

        if r.text:
            print r.text
        else:
            print 'Device changed'
            return True