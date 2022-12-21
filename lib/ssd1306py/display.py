"""ASCII fonts for SSD1306

Inspired on the original work by jdhxyy - 2021
<jdh821@163.com> https://github.com/jdhxyy/ssd1306py-micropython

This script provides the tooling required for working with the
ssd1306 oled display.
"""

import os
import sys
import machine

import ssd1306py.ssd1306 as ssd1306
import ssd1306py.ascii as ascii


_oled   = None
_i2c    = None
_width  = 0
_height = 0
_fonts  = {}


def init_i2c(scl, sda, width, height, i2c = 0):
    """Initialize the i2c interface for ssd1306.

    Parameters
    ----------
     scl : int
        oled clock pin
    sda : int
        oled data pin
    width : int
        oled screen width in pixels
    height : int
        oled screen height in pixels
    i2c : int
        i2c port
    """

    global _oled, _width, _height

    _i2c    = machine.I2C(i2c, scl = machine.Pin(scl), sda = machine.Pin(sda))
    _width  = width
    _height = height
    _oled   = ssd1306.SSD1306_I2C(_width, _height, _i2c)


def clear():
    """ Clear display """

    global _oled

    _oled.fill(0)


def show():
    """ Refresh display """

    global _oled

    _oled.show()


def pixel(x, y):
    """
    Draw a pixel

    Parameters
    ----------
    x : int
        x position
    y : int
        y position
    """

    global _oled

    _oled.pixel(x, y, 1)


def getWidth():
    """
    Get the oled width

    Returns
    ----------
    int
        the display width in pixels
    """

    global _width

    return _width


def getHeight():
    """
    Get the oled height

    Returns
    ----------
    int
        the display height in pixels
    """

    global _height

    return _height


def detectFonts():
    """Register existing font files
    Remember:
        - font file names must be formatted like 'font-[font name]-[font size].txt'
        - font files must be in the 'ssd1306py' directory

    Fonts will be registered to <_fonts> as a dictionary:
    {font_name: [font_sizes],}
    """

    global _fonts

    root  = sys.path[2]
    path  = root + '/ssd1306py/'
    files = os.listdir(path)
    name  = ''
    size  = 0

    for file in files:
        spl = file.split('.')
        ext = spl[1]

        if ext == 'txt':
            _f = spl[0]
            spl2 = _f.split('-')

            if spl2[0] == 'font':
                name = spl2[1]
                if not name in _fonts:
                    _fonts[name] = []
                size = int(spl2[2])
                _fonts[name].append(size)


def text(msg, x, y, size = 8, font = 'ascii'):
    """Display the message

    Parameters
    ----------
    msg : str
        the message to display
    x : int
        the X position
    y : int
        the Y position
    size : int, optional
        the font size.
        Default is 8
        Options: 8, 16, 24, 32
    font : str, optional
        the font name
        Default is 'ascii'
    """

    global _oled, _fonts

    if font not in _fonts:
        # I'm lazy
        print("Assumed 'ascii': No Such Font -> ", font)
        font = 'ascii'

    #if size != 16 and size != 24 and size != 32:
    if size not in _fonts[font]:
        # assume size 8. Told you: I'm lazy, can't bother to rise exceptions
        # also, I'd hate to break the program because of fantasy absent font files
        print("Assumed 8: No Such Size -> ", size)
        _oled.text(msg, x, y)
        return

    ascii.display(_oled, msg, x, y, size, font)
