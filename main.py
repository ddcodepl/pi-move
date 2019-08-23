#!/usr/bin/python
import config
import Movement
import Temperature


def init():
    print('Device initiated')

    if config.device['has_movement_sensor']:
        print('Movement sensor initiated')
        Movement.init()

    if config.device['has_thermometer']:
        print('Termomether initiated')
        Temperature.init()


init()
