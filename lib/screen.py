from oled.config import WIDTH, BAR_WIDTH, BAR_THICKNESS
from utime import sleep_ms

class Screen:
    """
    A handy class to unclutter main from display stuff
    """

    # most used characters lengths in pixels
    char_lens = {
        ':': 3,
        '0': 9,
        '1': 3,
        '2': 9,
        '3': 8,
        '4': 9,
        '5': 9,
        '6': 9,
        '7': 8,
        '8': 9,
        '9': 9
    }


    def __init__(self, ssd, writer, rotate = False):
        """
        Init class

        Parameters
        ----------
        ssd : module
            instance of ssd class
        writer : module
            instance of writer class
        rotate : bool
            If true, screen will be rotated by 180º
        """

        self.ssd          = ssd
        self.writer       = writer
        self.timer_y      = 16               # default Y position for timer
        self.set_y        = 0                # default Y position for setup
        self.pwr_scr_line = 0                # ssd Y pos power supply indicator

        if rotate == True:
            self.rotate()


    def rotate(self):
        """
        Rotate the screen by 180º
        """

        self.ssd.rotate(2)

        self.timer_y      = 0
        self.set_y        = (WIDTH // 2) - 16
        self.pwr_scr_line = 56


    def clear_main(self):
        """
        Clear display main (blue) area
        """

        self.ssd.fill_rect(0, self.timer_y, WIDTH, self.set_y, 0)
        self.ssd.show()


    def clear_all(self):
        """
        Clear the whole display
        """

        self.ssd.fill(0)


    def clear_underline(self):
        """
        Clear auxiliary (yellow) area
        """

        self.ssd.fill_rect(0, self.set_y, WIDTH, BAR_THICKNESS, 0)
        self.ssd.show()


    def print_timer(self, el_timo):
        """
        Print the actual timer

        Parameters
        ----------
        el_timo : int
            the time to print in seconds
        """

        ms           = self.__get_str_time(el_timo)
        str_time     = ms[0] + ":" + ms[1]
        str_time_len = self.__get_time_len(str_time)
        x_pos        = (64 - str_time_len) / 2

        self.writer.set_textpos(self.ssd, self.timer_y, int(x_pos))
        self.writer.printstring(str_time)
        self.ssd.show()


    def set_minutes(self):
        """
        Draw a bar under(if rotated)/above minutes in aux display area
        """

        self.clear_underline()
        self.ssd.fill_rect(14, self.set_y, BAR_WIDTH, BAR_THICKNESS, 1)
        self.ssd.show()


    def set_seconds(self):
        """
        Draw a bar under(if rotated)/above seconds in aux display area
        """

        self.clear_underline()
        self.ssd.fill_rect(74, self.set_y, BAR_WIDTH, BAR_THICKNESS, 1)
        self.ssd.show()


    def print_voltage(self, v, is_usb = False, percentile = 0):
        """
        Print power supply info

        Parameters
        ----------
        v : str
            the volts, 1 decimal place (formatted as string)
        is_usb : bool
            flag: value comes from usb pwr
        percentile : str
            Battery charge percent
        """

        if is_usb:
            txt = "USB: " + v + "V"
        else:
            txt = "BAT: " + v + "V"

            if percentile > 0:
                if percentile > 100:
                    percentile = 100
                txt += " (" + str("{:d}".format(percentile)) + "%)"

        self.__clear_aux()
        self.ssd.text(txt, 0, self.pwr_scr_line)
        self.ssd.show()


    def end_msg(self):
        """
        Print a flashy message when timer is done
        """

        self.writer.set_textpos(self.ssd, self.timer_y, 9)
        self.writer.printstring("00:00")
        self.ssd.show()

        sleep_ms(500)

        self.clear_all()
        self.ssd.show()


    def __clear_aux(self):
        """Clear Auxiliary (yellow) area"""

        self.ssd.fill_rect(0, self.set_y + BAR_THICKNESS, WIDTH, 16 - BAR_THICKNESS, 0)


    def __get_str_time(self, el_timo):
        """
        Convert the time in seconds to a fancy string

        Parameters
        ----------
        el_timo : int
            the time to convert
        """

        seconds = el_timo % 60
        str_sec = str(seconds)

        if seconds < 10:
            str_sec = '0' + str_sec

        minutes = int((el_timo - seconds) / 60)
        str_min = str(minutes)

        if minutes < 10:
            str_min = '0' + str_min

        return str_min, str_sec


    def __get_time_len(self, el_timo_stringo):
        """
        Calculate the length in pixels of a given string

        Parameters
        ----------
        el_timo_stringo : str
            the string to analyse
        """

        len = 0

        for c in el_timo_stringo:
            len += Screen.char_lens[c]

        return len
