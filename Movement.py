#!/usr/bin/python
import os
import time
import config
import subprocess
import RPi.GPIO as GPIO
from DBLogger import Logger


# # Sensor Settings
SENSOR_PIN = config.movement_sensor_pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def move_cb(channel):
    log.save_record('5d1d3efa46c0175c60aaafa4', '')
    if config.device['send_notifications']:
        if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Movement detected in " + config.location):
            log.save_record('5d1d3f4f46c0175c60aaafab', '')
            print('message sent')


def photo_cb(channel):
    date = time.time()
    subprocess.call('./photo.sh '+date, shell=True)
    log.save_record('5d1d3f0a46c0175c60aaafa5', date+'.jpg')

    if config.device['send_notifications']:
        if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Movement detected in " + config.location):
            log.save_record('5d1d3f4f46c0175c60aaafab', '')
            print('message sent')

        if config.telegram.send_photo(chat_id=config.telegram_chat_id, photo=open('./ai_model/test/snap.jpg', 'rb')):
            print('photo sent')


time.sleep(2)


def init():
    log = Logger(config.device['location']['_id'])

    try:

        if config.device['has_camera']:
            print("Init with camera")
            GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=photo_cb)
        else:
            print("Init without camera")
            GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=move_cb)

        config.telegram.send_message(
            chat_id=config.telegram_chat_id, text=config.device['name'] + " turned on in " + config.location)

        log.save_record('5d23232072fa8f1bab88cf88', '')

        while 1:
            time.sleep(1)

    except KeyboardInterrupt:
        print "Finish..."
        GPIO.cleanup()
