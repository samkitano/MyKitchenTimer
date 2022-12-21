from machine import Pin, ADC
from rotary import Rotary
from buzzer import BUZZER
from screen import Screen
import ssd1306py as display
import time

# oled resolution
oled_x  = 128                                # SSD1306 horizontal resolution
oled_y  = 64                                 # SSD1306 vertical resolution
#adc_2   = machine.ADC(2)                     # ADC channel 2 for input

display.init_i2c(1, 0, oled_x, oled_y)       # initialize oled
display.detectFonts()                        # detect available fonts

rotary = Rotary(2, 3, 4)                     # initialize rotary encoder
screen = Screen(display)                     # instantiate screen class
buzzer = BUZZER(15)                          # initialize buzzer


buzzer.shortBeep()                           # hello! we are open for business


# constants (states)
TIMER_RUNNING  = 0
TIMER_PAUSED   = 1
TIMER_FINISHED = 2

SET_MINUTES    = 0
SET_SECONDS    = 1
RUN_MODE       = 2
MAX_TIME       = 99 * 60 + 59                # maximum time allowed

# globals
state              = TIMER_PAUSED
mode               = RUN_MODE
default_start_time = 8 * 60                  # default is 8 minutes
current_time       = default_start_time      # time in seconds


def endloop():
    """Timer finished. Make some noise."""

    buzzer.doubleBeep()
    screen.flashyMessage("00:00", 300)

    return


def seconds_up():
    """Up. One second at a time"""

    global current_time

    current_time += 1

    if current_time == MAX_TIME:
        current_time = MAX_TIME


def seconds_down():
    """Down. One second at a time"""

    global current_time

    current_time -= 1
    
    if current_time < 0:
        current_time = 1


def minutes_up():
    """Increment minutes"""

    global current_time

    current_time = current_time + 60
    
    if current_time == MAX_TIME:
        current_time = MAX_TIME


def minutes_down():
    """Decrement minutes"""
    global current_time

    current_time = current_time - 60
    
    if current_time < 0:
        current_time = 1


def rotary_changed(change):
    """
    ISR - Interrupt Service Routine for the rotary encoder

    Parameters
    ----------
    change : int
        the value to process
    """

    global state, mode, current_time

    if change == Rotary.ROT_CW:
        if mode == SET_MINUTES:
            minutes_up()
        
        elif mode == SET_SECONDS:
            seconds_up()
    
    elif change == Rotary.ROT_CCW:
        if mode == SET_MINUTES:
            minutes_down()
        
        elif mode == SET_SECONDS:
            seconds_down()
    
    elif change == Rotary.SHORT_PRESS:
        if state == TIMER_RUNNING:
            state = TIMER_PAUSED
        
        elif state == TIMER_PAUSED:
            if mode == SET_MINUTES or mode == SET_SECONDS:
                mode = RUN_MODE
                screen.unset_all()
            state = TIMER_RUNNING
        
        elif state == TIMER_FINISHED:
            current_time = default_start_time
            state = TIMER_PAUSED
    
    elif change == Rotary.LONG_PRESS:
        if state == TIMER_RUNNING:
            return
        
        if mode == SET_MINUTES:
            mode = SET_SECONDS
            screen.set_seconds()
        
        elif mode == SET_SECONDS:
            mode = RUN_MODE
            screen.unset_all()
        
        else:
            mode = SET_MINUTES
            screen. set_minutes()


rotary.add_handler(rotary_changed)           # Register ISR


if __name__ == '__main__':
    while True:
        if state == TIMER_RUNNING:
            current_time = current_time - 1
            time.sleep(0.1875) # meh, calibrated with my phone. accurate enough for a kitchen timer

            if current_time <= 0:
                state = TIMER_FINISHED

            else:
                screen.update_time(current_time)

        elif state == TIMER_PAUSED:
            screen.update_time(current_time)

        elif state == TIMER_FINISHED:
            endloop()
