#!/usr/bin/env python
import time
from time import localtime, strftime
import signal
import socket
import bme680
from w1thermsensor import W1ThermSensor
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


running = True


def signal_handler(signal, frame):
    global running
    running = False


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def init_PiOLED():
    # Raspberry Pi pin configuration: on the PiOLED this pin isnt used
    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    return disp, width, height, image, draw, top, bottom, x, font


def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)

    # These oversampling settings can be tweaked to
    # change the balance between accuracy and noise in
    # the data.
    sensorAmbient = bme680.BME680()
    sensorAmbient.set_humidity_oversample(bme680.OS_2X)
    sensorAmbient.set_pressure_oversample(bme680.OS_4X)
    sensorAmbient.set_temperature_oversample(bme680.OS_8X)
    sensorAmbient.set_filter(bme680.FILTER_SIZE_3)

    sensorFridge = W1ThermSensor()

    disp, width, height, image, draw, top, bottom, x, font = init_PiOLED()

    while running:
        TIME = strftime('%Y-%m-%d %H:%M:%S', localtime())
        ip = get_ip()
        host = socket.gethostname()
        HOST = 'IP: ' + ip + ' ' + host

        AMBIENT = ''
        if sensorAmbient.get_sensor_data():
            AMBIENT = u'Ambient: {:.1f}\u00b0C {:.1f}%'.format(sensorAmbient.data.temperature,
                                                        sensorAmbient.data.humidity)
        FRIDGE = ''
        tempC = sensorFridge.get_temperature()
        if tempC is not None:
            FRIDGE = u'Fridge: {:.1f}\u00b0C'.format(tempC)

        # print(TIME)
        # print(HOST)
        # print(AMBIENT)
        # print(FRIDGE)
        # print('')

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Write two lines of text.
        draw.text((x, top + 0), TIME, font=font, fill=255)
        draw.text((x, top + 8), HOST, font=font, fill=255)
        draw.text((x, top + 16), AMBIENT, font=font, fill=255)
        draw.text((x, top + 25), FRIDGE, font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(1)

    # clear display before exit
    disp.clear()
    disp.display()


if __name__ == '__main__':
    main()
