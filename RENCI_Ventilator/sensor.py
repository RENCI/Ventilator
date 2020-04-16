import random
from RENCI_Ventilator.utils import get_settings
from RENCI_Ventilator.models import Configuration
from RENCI_Ventilator.models import Calibration


# provides access to demo or real sensor data
class SensorHandler:
    # define sensor number constants
    SENSOR_0: int = 0
    SENSOR_1: int = 1

    # list of previous pressure values
    # we fill the array with 0 for the number of samples per second up for a minute
    pressure_history: list = [0] * 4 * 60

    # debug class that simulates the real sensor
    class DebugBmp:
        # init the debug simulator class
        def __init__(self):
            self.pressure: int = 0
            self.temperature: int = 0
            self.altitude: int = 0
            self.sea_level_pressure: int = 0

    # init the SensorHandler class
    def __init__(self, sensor_number: int = 0, sea_level_pressure: float = 1000.8, standard_units: bool = True):
        # get the configuration settings
        config_settings = get_settings(Configuration)
        calib_settings = get_settings(Calibration)

        # save the debug mode
        self.debug_mode: int = bool(config_settings['demomode']['value'])

        # save the sensor type
        self.sensor_type: int = sensor_number

        # counter for fake breathing waveform data
        self.sample_counter: int = 0

        # init the units type flag
        self.standard_units: bool = standard_units

        # get the calibration reading
        self.pressure_correction = calib_settings[f'sensor{sensor_number}']['value']

        # if we are not in debug mode setup the raspberry pi
        if not self.debug_mode:
            import board
            import busio
            import adafruit_bmp3xx

            # type 0 is the i2c bus for sensor 0
            if sensor_number == SensorHandler.SENSOR_0:
                # i2c bus config
                i2c = busio.I2C(board.SCL, board.SDA)
                self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
            # else we are setting up SPI for sensor 1
            else:
                import digitalio

                # spi bus config
                spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
                cs = digitalio.DigitalInOut(board.D5)
                self.bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)
        else:
            # load up the demo bmp emulator
            self.bmp = self.DebugBmp()

        # set the sensor sampling rates and reference pressure
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2
        self.bmp.sea_level_pressure = sea_level_pressure

    @staticmethod
    def diagnostics():
        # TODO: return the result of diagnostics
        return True

    #################
    # declare methods that will get sensor data in selected units
    #################

    # demo pressure waveform data, 1 second per line
    demo_pressure_samples: list = [10, 20, 22, 27,
                                   26, 26, 25, 24,
                                   19, 12, 9, 8,
                                   8, 7, 6, 6,
                                   6, 6, 6, 5,
                                   # 5, 5, 5, 5,
                                   # 5, 5, 5, 5,
                                   5, 5, 1, 0]

    # get pressure
    def get_pressure(self) -> float:
        # if in debug mode return a random number in a reasonable range
        if self.debug_mode:
            # reset to the beginning if needed
            if self.sample_counter >= len(self.demo_pressure_samples):
                self.sample_counter = 0

            # get the next pressure data point with a little variation
            ret_val: float = self.demo_pressure_samples[self.sample_counter] + random.randrange(1, 2, 1)

            # go to the next data point
            self.sample_counter += 1
        else:
            # in standard mode return psi
            if self.standard_units:
                ret_val: float = self.get_psi_pressure() - self.pressure_correction
            # else return hpa
            else:
                ret_val: float = self.get_hpa_pressure()

        # out with the old
        if len(self.pressure_history) >= 240:
            self.pressure_history.pop(0)

        # in with the new
        self.pressure_history.append(ret_val)

        # return to the caller
        return ret_val

    # returns the pressure history
    def get_pressure_history(self) -> list:
        return self.pressure_history

    # get temperature
    def get_temperature(self) -> float:
        # return Fahrenheit
        if self.standard_units:
            return self.get_fahrenheit()
        # return Celsius
        else:
            return self.get_celsius()

    # get altitude
    def get_altitude(self) -> float:
        # return feet
        if self.standard_units:
            return self.get_altitude_feet()
        # return meters
        else:
            return self.get_altitude_meter()

    #################
    # return sensor readings in standard units
    #################

    # get pressure in psi
    def get_psi_pressure(self) -> float:
        # convert the pressure in hpa to psi and return
        return round(((self.bmp.pressure / 10) / 6.89475729), 2)

    # get mmHg in inches
    def get_mmhg_pressure(self) -> float:
        return round(self.bmp.pressure * 0.02952998751, 2)

    # get temp in F
    def get_fahrenheit(self) -> float:
        return round((((9 / 5) * self.bmp.temperature) + 32), 2)

    # get altitude in feet
    def get_altitude_feet(self) -> float:
        return round(self.bmp.altitude * 3.28, 2)

    #################
    # return sensor readings in metric units
    #################
    # get pressure in hPa
    def get_hpa_pressure(self) -> float:
        return round(self.bmp.pressure, 2)

    # return the temperature in celsius
    def get_celsius(self) -> float:
        return round(self.bmp.temperature, 2)

    # return the altitude in meters
    def get_altitude_meter(self) -> float:
        return round(self.bmp.altitude, 2)

    # set sea level pressure
    def set_sea_level_pressure(self, sea_level_pressure):
        self.bmp.sea_level_pressure = sea_level_pressure
