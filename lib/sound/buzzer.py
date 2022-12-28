from machine import Pin, PWM
from utime import sleep_ms


class BUZZER:
    """
    A handy class to make some sound out of a piezo

    Methods
    -----------
    shortBeep()
    doubleBeep()
    errorBeep()
    halfSecondBeep()
    """

    duty_cycle  = 50000
    normal_freq = 3000
    error_freq  = 500

    def __init__(self, buzzer_pin = 15):
        """
        Initialize the buzzer

        Parameters
        ----------
        buzzer_pin : int, optional
            buzzer pin. Default is pin 15
        """

        self.buzz = PWM(Pin(buzzer_pin))


    def shortBeep(self):
        """Sound a short beep"""

        self.buzz.freq(BUZZER.normal_freq)
        self.buzz.duty_u16(BUZZER.duty_cycle)
        sleep_ms(200)
        self.buzz.duty_u16(0)


    def doubleBeep(self):
        """Sound a double beep"""

        self.shortBeep()
        sleep_ms(15)
        self.shortBeep()


    def errorBeep(self):
        """Sound an error beep"""

        self.buzz.freq(BUZZER.error_freq)
        self.buzz.duty_u16(BUZZER.duty_cycle)
        sleep_ms(700)
        self.buzz.duty_u16(0)


    def halfSecondBeep(self):
        """Sound a half second beep"""

        self.buzz.freq(BUZZER.normal_freq)
        self.buzz.duty_u16(BUZZER.duty_cycle)
        sleep_ms(500)
        self.buzz.duty_u16(0)
