import time
import framebuf

# register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)


class SSD1306:
    """
    MicroPython SSD1306 OLED driver by Adafruit
    Modified by: jdh99 <jdh821@163.com> - 2021
    Modified by: Sam Kitano - 2022

    Methods
    ----------
    init_display()
        Initializes the display
    powerOff()
        Shuts the display down
    contrast(contrast)
        Sets the display contrast
    invert(invert)
        Inverts the screen
    show()
        Renders the buffer
    fill(col)
        Fills the screen with the specified color
    pixel(x, y, col)
        Draws a pixel
    scroll(dx, dy)
        Scrolls a region
    text(msg, x, y, col)
        Draws a text
    """

    def __init__(self, width, height, external_vcc):
        """
        Parameters
        ----------
        width : int
            the width of the oled display in pixels
        height : int
            the height of the oled display in pixels
        external_vcc : bool
            the external power flag
        """

        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8

        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()


    def init_display(self):
        """
        Initializes the Oled display
        """
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()


    def poweroff(self):
        """
        Shut the display down
        """

        self.write_cmd(SET_DISP | 0x00)


    def contrast(self, contrast):
        """
        Set the display's contrast

        Parameters
        ----------
        contrast : int
            the contrast to set (0 to 255)
        """

        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)


    def invert(self, invert):
        """
        Inverts the display

        Parameters
        ----------
        invert : bool
            inversion flag
        """

        self.write_cmd(SET_NORM_INV | (invert & 1))


    def show(self):
        """
        Render the stuff in the buffer to the display
        """

        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()


    def fill(self, col):
        """
        Fill the entire FrameBuffer with the specified color

        Parameters
        ----------
        col : int
            the color (0 for black, 1 for white)
        """

        self.framebuf.fill(col)


    def pixel(self, x, y, col):
        """
        If color [col] is not given, get the color value of the specified pixel.
        If color [col] is given, set the specified pixel to the given color.

        Parameters
        ----------
        x : int
            X position in pixels
        y : int
            Y position in pixels
        col : int
            the color (0 for black, 1 for white)
        """

        self.framebuf.pixel(x, y, col)


    def scroll(self, dx, dy):
        """
        Shift the contents of the FrameBuffer by the given vector.
        This may leave a footprint of the previous colors in the FrameBuffer.

        Parameters
        ----------
        dx : int
            X step
        dy : int
            Y step
        """

        self.framebuf.scroll(dx, dy)


    def text(self, msg, x, y, col = 1):
        """
        Write text to the FrameBuffer using the the coordinates as the upper-left corner of the text.
        The color of the text can be defined by the optional argument but is otherwise a default value of 1.
        All characters have dimensions of 8x8 pixels and there is currently no way to change the font.

        Parameters
        ----------
        msg : str
            The string to display
        x : int
            X Position in pixels
        y : int
            Y position in pixels
        col : int, optional
            the pixel color
            Default is 1 (white)
        """

        self.framebuf.text(msg, x, y, col)


class SSD1306_I2C(SSD1306):
    """
    MicroPython SSD1306 OLED I2C driver by Adafruit
    Modified by: jdh99 <jdh821@163.com> - 2021
    Modified by: Sam Kitano - 2022

    Methods
    ----------
    write_cmd(cmd)
        Writes a command to the display
    write_framebuf()
        Writes data onto the buffer
    power_on()
        Powers ON the display
    """

    def __init__(self, width, height, i2c, addr = 0x3c, external_vcc = False):
        """
        Initializes the Oled display for i2c communication
        """

        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)


    def write_cmd(self, cmd):
        """
        Write a command to the display

        Parameters
        ----------
        cmd : hex
            The command to execute
        """

        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)


    def write_framebuf(self):
        """
        Write to the buffer
        """

        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)


    def poweron(self):
        """
        Power the display ON
        """

        pass
