from time import sleep
from .utils import get_settings
from .models import Configuration


# provides access to demo or real relay data
class RelayHandler:
    # debug class that simulates the real relays
    class DebugRelay:
        HIGH = 0
        LOW = 1
        OUT = 2
        BOARD = 3

        @staticmethod
        def setmode(val: int):
            return None

        @staticmethod
        def setup(val1: int, val2: int):
            return None

        @ staticmethod
        def output(val: int, val2: int):
            return None

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

        if not self.debug_mode:
            import RPi.GPIO as GPIO
            self.relay_handle = GPIO
        else:
            self.relay_handle = self.DebugRelay()

        # to use Raspberry Pi board pin numbers
        self.relay_handle.setmode(self.relay_handle.BOARD)

        # set up the GPIO channels
        self.relay_handle.setup(RelayHandler.RELAY_1, self.relay_handle.OUT)
        self.relay_handle.setup(RelayHandler.RELAY_2, self.relay_handle.OUT)
        self.relay_handle.setup(RelayHandler.RELAY_3, self.relay_handle.OUT)
        self.relay_handle.setup(RelayHandler.RELAY_4, self.relay_handle.OUT)

    def toggle_relay(self, relay_num: int, duration: int):

        self.relay_handle.output(relay_num, self.relay_handle.HIGH)
        print(f'RELAY {relay_num}: OFF')

        self.relay_handle.output(relay_num, self.relay_handle.LOW)
        print(f'RELAY {relay_num}: ON')

        sleep(duration)

        self.relay_handle.output(relay_num, self.relay_handle.HIGH)
        print(f'RELAY {relay_num}: OFF')

    def get_diagnostics(self):
        for x in range(0, 3):
            self.toggle_relay(RelayHandler.RELAY_1, 2)
            self.toggle_relay(RelayHandler.RELAY_2, 2)
            self.toggle_relay(RelayHandler.RELAY_3, 2)
            self.toggle_relay(RelayHandler.RELAY_4, 2)
