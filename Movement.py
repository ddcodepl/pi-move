#!/usr/bin/python
import os
import time
import config
import subprocess
import RPi.GPIO as GPIO
import FaceLogger
from DBLogger import Logger


# # Sensor Settings
SENSOR_PIN = config.movement_sensor_pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

log = Logger(config.device['location']['_id'])
log_face = FaceLogger


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
            print('Message sent')


def photo_cb(channel):
    date = time.time()

    subprocess.call(
        ['fswebcam -r 1920x1080 --no-banner ./ai_model/test/snap.jpg'], shell=True)
    subprocess.call(
        ['cp ./ai_model/test/snap.jpg ./photos/'+str(date) + '.jpg'], shell=True)

    log.save_record('5d1d3f0a46c0175c60aaafa5', str(date)+'.jpg')

    log_face.init()

    if config.device['send_notifications']:
        if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Movement detected in " + config.location):
            log.save_record('5d1d3f4f46c0175c60aaafab', '')
            print('Message sent')

        if config.telegram.send_photo(chat_id=config.telegram_chat_id, photo=open('./ai_model/test/snap.jpg', 'rb')):
            print('Photo sent')


def init():
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
