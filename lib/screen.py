from utime import sleep_ms

class Screen:
    """
    A handy class to manipulate the screen messages

    Methods
    --------------
    update_time(raw_seconds)
        Updates the displayed timer
    updateInterval(raw_seconds)
        Updates the timer interval
    flashyMessage(msg, duration_ms)
        Displays a flashing message
    calculateXpos(msg)
        Calculets a centered X position for a message
    """

    def __init__(self, oled):
        """
        Initialize class

        Parameters
        ----------
        oled : module
            Instance of display class
        """

        self.display = oled
        self.set_y_pos = 0
        self.time_y_pos = 25


    def update_time(self, raw_seconds):
        """
        Updates the time on the display

        Parameters
        ----------
        raw_seconds : int
            The raw time to display in seconds
        """

        output = self.stringifyTime(raw_seconds)
        x_pos = self.calculateXpos(output)

        self.display.text(output, x_pos, self.time_y_pos, 32)
        self.display.show()

        return

    def set_seconds(self):
        """
        Indicates setting seconds
        """

        self.display.clear()
        self.display.text("          VVV", 0, 0, 16)
        self.display.show()


    def set_minutes(self):
        """
        Indicates setting minutes
        """

        self.display.clear()
        self.display.text("    VVV      ", 0, 0, 16)
        self.display.show()

    def unset_all(self):
        """
        Remove setting indications
        """

        self.display.clear()


    def stringifyTime(self, raw_seconds):
        """
        Formats a time string as mm:ss

        Parameters
        ----------
        raw_seconds : int
            The total seconds to convert

        Returns
        ----------
            str
                the formatted time
        """

        seconds = raw_seconds % 60

        if seconds < 10:
            str_seconds = '0' + str(seconds)
        else:
            str_seconds = str(seconds)

        minutes = int((raw_seconds - seconds) / 60)

        if minutes < 10:
            str_minutes = '0' + str(minutes)
        else:
            str_minutes = str(minutes)

        return str_minutes + ':' + str_seconds


    def flashyMessage(self, msg, duration_ms):
        """
        Displays a flashing message

        Parameters
        ----------
        msg : str
            The message to display
        duration : int
            The flash durations in milliseconds
        """

        x_pos = self.calculateXpos(msg)

        self.display.clear()
        self.display.text(msg, x_pos, self.time_y_pos, 32)
        self.display.show()
        sleep_ms(duration_ms)
        self.display.clear()
        self.display.show()

        return


    def calculateXpos(self, msg):
        """
        Calculates the X position for centering a given message
        It assumes characters are 32px heigh by 16px wide

        Parameters
        ----------
        msg : str
            The message to calculate from

        Returns
        ----------
            int
                the position in pixels
        """

        len_msg = len(msg) * 16

        return int((self.display.getWidth() / 2) - (len_msg / 2))
