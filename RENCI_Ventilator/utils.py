import random
from RENCI_Ventilator.sensor import SensorHandler

# TODO: actually create the diagnostics
def run_diagnostic() -> int:
    return 1

sh = SensorHandler(False)

# TODO: get the data from the sensor
def get_pressure_data() -> int:
    # return the pressure
    return sh.get_pressure()


# TODO: get the data from the sensor
def get_respiration_data() -> int:
    return random.randrange(10, 15, 1)
