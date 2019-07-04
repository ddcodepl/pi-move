#!/usr/bin/python
import os
import time
import config
import subprocess
import RPi.GPIO as GPIO

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
    if config.device['send_notifications']:
        if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Movement detected in " + config.location):
            print('message sent')


def photo_cb(channel):
    subprocess.call('./photo.sh', shell=True)

    if config.device['send_notifications']:
        if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Movement detected in " + config.location):
            print('message sent')

        if config.telegram.send_photo(chat_id=config.telegram_chat_id, photo=open('./snap.jpg', 'rb')):
            print('photo sent')


time.sleep(2)


def main():
    try:
        if config.device['has_camera']:
            print("Init with camera")
            GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=photo_cb)
        else:
            print("Init without camera")
            GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=move_cb)

        config.telegram.send_message(
            chat_id=telegram_chat_id, text=device['name'] + " turned on in " + location)

    while 1:
        time.sleep(1)

    except KeyboardInterrupt:
        print "Finish..."
        GPIO.cleanup()
