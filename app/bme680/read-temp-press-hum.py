#!/usr/bin/env python
import bme680

sensor = bme680.BME680()

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

if sensor.get_sensor_data():
	output = "{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
	print(output)
else:
	exit(1)
