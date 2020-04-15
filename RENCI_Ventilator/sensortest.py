from .sensor import SensorHandler

# debug testing
if __name__ == '__main__':
    # fire up the class to read the sensor
    sh0 = SensorHandler(sensor_number=0)
    sh1 = SensorHandler(sensor_number=1)

    print("Sensor 0")
    print(f'Current mode: {sh0.debug_mode}, Sensor: {sh0.sensor_type}')
    print(f'standard units: {sh0.standard_units}, Sea level pressure: {sh0.bmp.sea_level_pressure}')

    print("Sensor 1")
    print(f'Current mode: {sh1.debug_mode}, Sensor: {sh1.sensor_type}')
    print(f'standard units: {sh1.standard_units}, Sea level pressure: {sh1.bmp.sea_level_pressure}')

    count = 1

    # forever
    while True:
        try:
            print(f'\nTest number: {count}')

            # get the temperature
            temperature0 = sh0.get_temperature()
            altitude0 = sh0.get_altitude()
            psi0 = sh0.get_pressure()

            temperature1 = sh1.get_temperature()
            altitude1 = sh1.get_altitude()
            psi1 = sh1.get_pressure()

            if psi0 < 14 or psi0 > 15:
                print(f'Abnormal pressure reading for sensor 0: {psi0}')
            else:
                print(f'Sensor 0 - Pressure: {psi0}  Temperature: {temperature0}  Altitude (M): {altitude0}')

            if psi1 < 14 or psi1 > 15:
                print(f'Abnormal pressure reading for sensor 1: {psi1}')
            else:
                print(f'Sensor 1 - Pressure: {psi1}  Temperature: {temperature1}  Altitude (M): {altitude1}')

            count = count + 1
        except Exception as e:
            print(f'Exception: {e}')

        # do it again in a second
        time.sleep(1)