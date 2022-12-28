"""
config.py
Device configuration
"""

from lib.oled.ssd1306 import SSD1306_I2C
from lib.io.rotary    import Rotary
from lib.sound.buzzer import BUZZER
from lib.oled.writer  import Writer

from micropython      import const
from machine          import I2C, Pin, Timer, ADC

import lib.oled.seven_segment_48 as font


# Settings
WIDTH         = const(128)                   # display width
HEIGHT        = const(64)                    # display height
DEFAULT_TIMER = const(8 * 60)                # default timer is 8 minutes
MAX_TIME      = const(5999)                  # 99 * 60 + 59 maximum time allowed
CONV_FACTOR   = (3.3 / (65535)) * 3          # ADC voltage conversion factor
BATTERY_MAX   = const(4.20)                  # volts
BATTERY_MIN   = const(3.3)                   # volts
BAR_WIDTH     = const(48)                    # setup underline width
BAR_THICKNESS = const(4)                     # setup underline thickness


# States - PLEASE DO NOT CHANGE
TIMER_RUNNING  = const(0)                    # [state] timer is running
TIMER_PAUSED   = const(1)                    # [state] timer is paused
TIMER_FINISHED = const(2)                    # [state] time has finished

SET_MINUTES    = const(0)                    # [mode] app is setting minutes
SET_SECONDS    = const(1)                    # [mode] app is setting seconds
RUN_MODE       = const(2)                    # [mode] app is doing the timing


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

ssd = setup_ssd()
rotary  = Rotary(2, 3, 4)                    # initialize rotary encoder
buzzer  = BUZZER(15)                         # initialize buzzer
tim     = Timer(-1)                          # initialize rotary switch IRQ timer
Vsys    = ADC(29)                            # initialize ADC for Vsys reading
Vin     = ADC(26)                            # init ADC for Vin (battery) measurement
writer  = Writer(ssd, font, False)           # init writer NOT verbose
