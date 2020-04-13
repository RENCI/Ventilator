import time

# set the operational mode
DEBUG = True

# debug class to simulate the hardware
class debug_bmp:
    sea_level_pressure = 0
    pressure = 0
    temperature = 0
    altitude = 0

    # init the class variables
    def __init__(self):
        import random
        self.sea_level_pressure
        self.pressure = random.randrange(975, 1002, 1)
        self.temperature = random.randrange(20, 30, 1)
        self.altitude = random.randrange(220, 230, 1)

# if we are not in debug mode setup the raspberry pi
if DEBUG == False:
    import board
    import busio
    import adafruit_bmp3xx

    # I2C setup
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    bmp.pressure_oversampling = 8
    bmp.temperature_oversampling = 2

# test loop
while True:
    # check the operational mode
    if DEBUG == True:
        bmp = debug_bmp()

    bmp.sea_level_pressure = 1001.8

    mmhg = round(bmp.pressure * 0.02952998751, 2)
    F = round((((9/5) * bmp.temperature) + 32) ,2)
    feet = round(bmp.altitude * 3.28, 2)
    psi = round(((bmp.pressure / 10) / 6.89475729), 2)

    hpa = round(bmp.pressure, 2)
    C = round(bmp.temperature, 2)
    altitude = round(bmp.altitude, 2)

    print(f'\nPressure (hPa): {hpa}  Temperature (C): {C}  Altitude (M): {altitude}')
    print(f'Pressure (mmhg): {mmhg}  Pressure (psi): {psi}  Temperature (F): {F}  Altitude (feet): {feet}')
    time.sleep(1)
