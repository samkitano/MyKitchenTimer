"""ASCII fonts for SSD1306

Inspired on the original work by jdhxyy - 2021
<jdh821@163.com> https://github.com/jdhxyy/ssd1306py-micropython

This script allows the user to print ASCII characters in
different font sizes to an SSD1306 OLED display, rather
than the default size 8

Font sizes are limited to whatever font files are in
the ssd1306py directory. By default: 16, 24 and 32

In order to be detected, the Font file name MUST be formatted as follows:
'font-[font_name]-[font_size].txt'

for example: 'font-ascii-24'

Font files MUST be UTF-8 encoded with no BOM
"""

import sys

file        = None
has_2_lines = False
font_name   = 'ascii'

def get_ch(ch, size):
    """Get correspondent ascii character data, based on font size

    Parameters
    ----------
    size : int
        font size

    Returns
    --------------
        list
            the binary data for the ascii char
    """

    global file, has_2_lines, font_name

    data      = []
    offsets   = {16: 85, 24: 247, 32: 327}
    root      = sys.path[2]
    path      = root + '/ssd1306py/font-'
    file_path = path + font_name + '-' + str(size) + '.txt'
    file      = open(file_path, 'r')

    file.seek(ord(ch) * offsets[size])

    line_1 = file.readline()

    if has_2_lines:
        line_2 = file.readline()

    get_data(data, line_1, size)

    if has_2_lines:
        get_data(data, line_2, size)

    return data


def get_data(data, line, limit):
    """Gets the data for a given file line,
    and appends it to data list

    Parameters
    ----------
    data : list
        the list we will append the data onto
    line : string
        the line grabbed from the file
    limit : int
        the limit for iteration (the byte size)
    """

    counter = 0

    for bytes in line.split(','):
        data.append(int(bytes))
        counter += 1

        if counter == limit:
            break


def display(oled, msg, x, y, size, font = 'ascii'):
    """Display a given message

    Parameters
    ----------
    oled : module
        an instance of the display class
    msg : str
        the message to display
    x : int
        the X position
    y : int
        the Y position
    size : int
        the font size
    font : str
        the font name
    """

    global has_2_lines, font_name, file

    font_name   = font
    offset      = 0
    has_2_lines = size > 16

    for n in msg:
        byte_data = get_ch(n, size)

        for row in range(0, size):
            a = bin(byte_data[row]).replace('0b', '')

            while len(a) < 8:
                a = '0' + a

            if has_2_lines:
                b = bin(byte_data[row + size]).replace('0b', '')

                while len(b) < 8:
                    b = '0' + b

            for col in range(0, 8):
                oled.pixel(x + offset + col, row + y, int(a[col]))

                if has_2_lines:
                    oled.pixel(x + offset + col + 8, row + y, int(b[col]))

        if has_2_lines:
            offset += 16
        else:
            offset += 8

    file.close()
