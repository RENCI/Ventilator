import time
import random

# provides access to the sensor data
class SensorHandler:
    # define instance type constants
    SENSOR_PRESSURE = 0
    SENSOR_RESPIRATION = 1

    # debug class that simulates the real sensor
    class DebugBmp:
        # init the debug simulator class
        def __init__(self):
            import random
            self.pressure = 0
            self.temperature = 0
            self.altitude = 0

    # init the SensorHandler class
    def __init__(self, debug_mode: bool = False, sensor_type: int = 0, sea_level_pressure: float = 1000.8, standard_units: bool = True):
        # save the debug mode
        self.debug_mode = debug_mode

        # save the sensor type
        self.sensor_type = sensor_type

        # counter for fake breathing waveform data
        self.sample_counter = 0

        # if we are not in debug mode setup the raspberry pi
        if not debug_mode:
            import board
            import busio
            import adafruit_bmp3xx

            # type 0 is the i2c bus for sensor 0
            if sensor_type == 0:
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

        # set the sensor sampling rates
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2

        # init the other params
        self.bmp.sea_level_pressure = sea_level_pressure
        self.standard_units = standard_units

    # TODO: return the result of diagnostics
    @staticmethod
    def diagnostics():
        return True

    #################
    # declare methods that will get sensor data in selected units
    #################

    # demo pressure waveform data, each line is 1 second at a 25% UI duty cycle
    demo_pressure_samples = [10, 20, 22, 25,
                             25, 26, 25, 21,
                             20, 15, 13, 10,
                             9, 8, 7, 8,
                             7, 6, 6, 6,
                             6, 5, 5, 5,
                             5, 5, 4, 5,
                             4, 5, 0, -1]

    # the UI is set to sample every 500ms. so divide by two to get the number of seconds
    # so the respiration/min cycle rate is (60 / (the number of samples / second))
    demo_cycle_duration = int(60/(len(demo_pressure_samples)/4))

    # get pressure
    def get_pressure(self):
        # if in debug mode return a random number in a reasonable range
        if self.debug_mode:
            # do the x-axis points
            if self.sensor_type == SensorHandler.SENSOR_PRESSURE:
                # reset to the beginning if needed
                if self.sample_counter >= len(self.demo_pressure_samples):
                    self.sample_counter = 0

                # get the next pressure data point with a little variation
                ret_val = self.demo_pressure_samples[self.sample_counter] + random.randrange(1, 2, 1)

                # go to the next data point
                self.sample_counter = self.sample_counter + 1
            # else return the respiration rate
            else:
                # make the respiration rate a little variable for effect
                ret_val = random.randrange(self.demo_cycle_duration-1, self.demo_cycle_duration+1, 1)

            return ret_val
        else:
            # in standard mode return psi
            if self.standard_units:
                return self.get_psi_pressure()
            # else return hpa
            else:
                return self.get_hpa_pressure()

    # get temperature
    def get_temperature(self):
        # return Fahrenheit
        if self.standard_units:
            return self.get_fahrenheit()
        # return Celsius
        else:
            return self.get_celsius()

    # get altitude
    def get_altitude(self):
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
    def get_psi_pressure(self):
        # convert the pressure in hpa to psi and return
        return round(((self.bmp.pressure / 10) / 6.89475729), 2)

    # get mmHg in inches
    def get_mmhg_pressure(self):
        return round(self.bmp.pressure * 0.02952998751, 2)

    # get temp in F
    def get_fahrenheit(self):
        return round((((9/5) * self.bmp.temperature) + 32), 2)

    # get altitude in feet
    def get_altitude_feet(self):
        return round(self.bmp.altitude * 3.28, 2)

    #################
    # return sensor readings in metric units
    #################
    # get pressure in hPa
    def get_hpa_pressure(self):
        return round(self.bmp.pressure, 2)

    # return the temperature in celsius
    def get_celsius(self):
        return round(self.bmp.temperature, 2)

    # return the altitude in meeters
    def get_altitude_meter(self):
        return round(self.bmp.altitude, 2)

    # set sea level pressure
    def set_sea_level_pressure(self, sea_level_pressure):
        self.bmp.sea_level_pressure = sea_level_pressure


# debug testing
if __name__ == '__main__':
    # fire up the class to read the sensor
    sh0 = SensorHandler(debug_mode=False, sensor_type=0)
    sh1 = SensorHandler(debug_mode=False, sensor_type=1)

    print("Sensor 0")
    print(f'Current mode: {sh0.debug_mode}, Sensor: {sh0.sensor_type}')
    print(f'standard units: {sh0.standard_units}, Sea level pressure: {sh0.bmp.sea_level_pressure}')

    print("Sensor 1")
    print(f'Current mode: {sh1.debug_mode}, Sensor: {sh1.sensor_type}')
    print(f'standard units: {sh1.standard_units}, Sea level pressure: {sh1.bmp.sea_level_pressure}')

    # forever
    while True:
        try:
            # get the temperature
            #temperature0 = sh0.get_temperature()
            #altitude0 = sh0.get_altitude()
            psi0 = sh0.get_pressure()

            #temperature1 = sh1.get_temperature()
            #altitude1 = sh1.get_altitude()
            psi1 = sh1.get_pressure()

            print(f'\nSensor 0 - Pressure: {psi0}') #  Temperature: {temperature0}  Altitude (M): {altitude0}
            print(f'Sensor 1 - Pressure: {psi1}') #  Temperature: {temperature1}  Altitude (M): {altitude1}
        except Exception as e:
            print(f'Exception: {e}')

        # do it again in a second
        time.sleep(1)
