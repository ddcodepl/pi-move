#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import Water


def callback(PIN):
    if GPIO.input(PIN):
        print "Plant is dry!"

    else:
        print "Plant is wet!"


PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

GPIO.add_event_detect(PIN, GPIO.BOTH, bouncetime=300)

while True:
    callback(PIN)
    time.sleep(2)
