"""
ssd1306_setup.py
Device initialisation
Original script(V0.3 12th Aug 2018): Copyright (c) 2016 Peter Hinch MIT License (MIT)
https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html
"""


from oled.ssd1306 import SSD1306_I2C
from micropython import const
from machine import I2C, Pin

WIDTH  = const(128)    # display width
HEIGHT = const(64)     # display height

def setup_ssd(scl = 1, sda = 0, i2c = 0):
    """
    Init device for i2c communication protocol

    Parameters
    ----------
    scl : int, optional
        Clock pin. Default 1
    sda : int, optional
        Data pin. Default 0
    i2c : int, optional
        i2c Port. Default 0

    Wiring - RPi Pico (I2C)
    ----------
    3v3 : Vin
    Gnd : Gnd
    0 : scl
    1 : sda
    """

    _i2c = I2C(i2c, scl = Pin(scl), sda = Pin(sda))

    ssd = SSD1306_I2C(WIDTH, HEIGHT, _i2c)

    return ssd
