# External module imp
import RPi.GPIO as GPIO
import datetime
import config
import time


GPIO.setmode(GPIO.BCM)


def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def pump_on(pump_pin=17, delay=2):
    init_output(pump_pin)
    config.telegram.send_message(
        chat_id=config.telegram_chat_id, text="Plant was dry")
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pump_pin, GPIO.HIGH)


pump_on()
