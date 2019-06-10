#!/usr/bin/python
import telegram
import subprocess
import RPi.GPIO as GPIO
import time
import pymongo
import config
import os
from Spotify import switch_device_and_play_music

SENSOR_PIN = config.device.move_sensor_port

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# DB Config
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["movement_tracker"]

# Telegram Config
telegram = telegram.Bot(config.telegram_token)
chat_id = config.telegram_chat_id

# Actions list
# # 1 - Move detected
# # 2 - Move detected and photo taken
# # 3 - Movement detected and Spotify activated
# # 4 - Movement detected, photo taken and Spotify activated

# Turn off after X seconds

# define our clear function
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def save_record(location=config.device.id, action=1):
    logs = db.logs
    data = {
        "location_id": location,
        "action_id": action,
        "time": int(time.time())
    }
    insert = logs.insert_one(data)


def move_cb(channel):
    actionID = 1

    if config.device.has_speaker == 1:
        switch_device_and_play_music()
        actionID = 3

    save_record(config.device.id, actionID)

    if telegram.send_message(chat_id=chat_id, text="Movement detected in attic"):
        print('message sent')


def photo_cb(channel):
    actionID = 2

    if config.device.has_speaker == 1:
        switch_device_and_play_music()
        actionID = 4

    subprocess.call('./photo.sh', shell=True)
    clear()

    if telegram.send_photo(chat_id=chat_id, photo=open('./snap.jpg', 'rb')) :
        print('photo sent')

    if telegram.send_message(chat_id=chat_id, text="Movement detected in the "+config.device.location.name):
        print('message sent')

    save_record(config.device.id, actionID)


time.sleep(2)

try:

    if config.device.has_camera == 0:
        print("Init without camera")
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=move_cb)
    else:
        print("Init with camera")
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=photo_cb)

    while 1:
        time.sleep(1)

except KeyboardInterrupt:
    print "Finish..."
GPIO.cleanup()
