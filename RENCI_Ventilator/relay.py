import RPi.GPIO as GPIO
from time import sleep
from .utils import get_settings
from .models import Configuration


# provides access to demo or real relay data
class RelayHandler:
    # define relay number constants to the physical GPIO pin on the RPi
    RELAY_1: int = 32
    RELAY_2: int = 36
    RELAY_3: int = 38
    RELAY_4: int = 40

    def __init__(self):
        # get the configuration settings
        config_settings = get_settings(Configuration)

        # save the debug mode
        self.debug_mode: int = bool(int(config_settings['demomode']['value']))

        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)

        # set up the GPIO channels
        GPIO.setup(RelayHandler.RELAY_1, GPIO.OUT)
        GPIO.setup(RelayHandler.RELAY_2, GPIO.OUT)
        GPIO.setup(RelayHandler.RELAY_3, GPIO.OUT)
        GPIO.setup(RelayHandler.RELAY_4, GPIO.OUT)

    @staticmethod
    def toggle_relay(relay_num: int, duration: int):
        GPIO.output(relay_num, GPIO.HIGH)
        print(f'RELAY {relay_num}: OFF')

        GPIO.output(relay_num, GPIO.LOW)
        print(f'RELAY {relay_num}: ON')

        sleep(duration)

        GPIO.output(relay_num, GPIO.HIGH)
        print(f'RELAY {relay_num}: OFF')

    def diags(self):
        while 1:
            self.toggle_relay(RelayHandler.RELAY_1, 2)
            self.toggle_relay(RelayHandler.RELAY_2, 2)
            self.toggle_relay(RelayHandler.RELAY_3, 2)
            self.toggle_relay(RelayHandler.RELAY_4, 2)
