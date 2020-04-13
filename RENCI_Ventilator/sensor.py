import time

# set the operational mode
DEBUG = True

# provides access to the sensor data
class SensorHandler:
    standard_units = True

    class debug_bmp:
        sea_level_pressure = 0
        pressure = 0
        temperature = 0
        altitude = 0
        bmp = None

        # init the class variables
        def __init__(self):
            import random
            self.pressure = random.randrange(975, 1002, 1)
            self.temperature = random.randrange(20, 30, 1)
            self.altitude = random.randrange(220, 230, 1)

    def __init__(self, sea_level_pressure, standard_units: bool = True):
        # if we are not in debug mode setup the raspberry pi
        if not DEBUG:
            import board
            import busio
            import adafruit_bmp3xx

            # I2C setup
            i2c = busio.I2C(board.SCL, board.SDA)
            self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

            # set the sampling rates
            self.bmp.pressure_oversampling = 8
            self.bmp.temperature_oversampling = 2
        else:
            self.bmp = self.debug_bmp()

        # init the other params
        self.bmp.sea_level_pressure = sea_level_pressure
        self.standard_units = standard_units

    def get_pressure(self):
        if self.standard_units:
            return self.get_psi_pressure()
        else:
            return self.get_hpa_pressure()

    def get_temperature(self):
        if self.standard_units:
            return self.get_fahrenheit()
        else:
            return self.get_celsius()

    def get_altitude(self):
        if self.standard_units:
            return self.get_altitude_feet()
        else:
            return self.get_altitude_meter()

    #################
    # return standard units
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
    # return metric units
    #################

    # get pressure in hPa
    def get_hpa_pressure(self):
        return round(self.bmp.pressure, 2)

    def get_celsius(self):
        return round(self.bmp.temperature, 2)

    def get_altitude_meter(self):
        return round(self.bmp.altitude, 2)

    # set sea level pressure
    def set_sea_level_pressure(self, sea_level_pressure):
        self.bmp.sea_level_pressure = sea_level_pressure

if __name__ == '__main__':
    sh = SensorHandler(1001.8)

    while (1):
        temperature = sh.get_temperature()
        altitude = sh.get_altitude()
        psi = sh.get_pressure()

        print(f'Pressure: {psi}  Temperature: {temperature}  Altitude (M): {altitude}')
        time.sleep(1)
