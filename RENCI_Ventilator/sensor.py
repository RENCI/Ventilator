import time


# provides access to the sensor data
class SensorHandler:
    # debug class that simulates the real sensor
    class DebugBmp:
        # init the debug simulator class
        def __init__(self):
            import random
            self.pressure = random.randrange(975, 1002, 1)
            self.temperature = random.randrange(20, 30, 1)
            self.altitude = random.randrange(220, 230, 1)

    # init the SensorHandler class
    def __init__(self, debug_mode: bool = False, type: int = 0, sea_level_pressure: float = 1000.8, standard_units: bool = True):
        # if we are not in debug mode setup the raspberry pi
        if not debug_mode:
            import board
            import busio
            import adafruit_bmp3xx

            if type == 0:
                # i2c init
                i2c = busio.I2C(board.SCL, board.SDA)
                self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
            else:
                import digitalio

                spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
                cs = digitalio.DigitalInOut(board.D5)
                self.bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)
        else:
            self.bmp = self.DebugBmp()

        # set the sensor sampling rates
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2

        # init the other params
        self.bmp.sea_level_pressure = sea_level_pressure
        self.standard_units = standard_units

    # TODO: return the result of diagnostics
    @staticmethod
    def diagnotics():
        return True

    #################
    # declare methods that will get sensor data in selected units
    #################
    # get pressure
    def get_pressure(self):
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
    sh = SensorHandler(True)

    # forever
    while True:
        # get the temperature
        temperature = sh.get_temperature()

        # get the altitude
        altitude = sh.get_altitude()

        # get the ambient pressure in psi
        psi = sh.get_pressure()

        print(f'Pressure: {psi}  Temperature: {temperature}  Altitude (M): {altitude}')

        # do it again in a second
        time.sleep(2)
