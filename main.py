import config
import Movement
import Temperature


def init():
    print('Init device')

    if config.device['has_movement_sensor']:
        print('Movement sensor init')
        Movement.init()

    if config.device['has_thermometer']:
        print('Termomether init')
        Temperature.init()


init()
