#!/usr/bin/python
import sys
import config
import Adafruit_DHT
from DBLogger import Logger


def init():
    prevTemp = 0
    log = Logger(config.device['location']['_id'])

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 23)

        if (int(temperature) - int(prevTemp) >= 2 or (int(prevTemp) - int(temperature)) >= 2):
            if config.device['send_notifications']:
                if config.telegram.send_message(chat_id=config.telegram_chat_id, text="Temperature changed in "+config.location+" to "+str(temperature)):
                    log.save_record('5d23ca7a41f8c8072753eac6',
                                    int(temperature))
                    print('message sent')

            print('Temperature canged more by 2 degrees!')
            prevTemp = int(temperature)

        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(
            float(temperature), float(humidity))
