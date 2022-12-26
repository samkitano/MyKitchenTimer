from oled.writer import Writer
from oled.config import *

from rotary import Rotary
from buzzer import BUZZER
from screen import Screen

from micropython import const
from utime       import sleep_ms
from machine     import Timer, ADC

import oled.seven_segment_48 as font

# init classes
ssd     = setup_ssd()                        # Setup SSD [scl = 1, sda = 0, i2c = 0]
rotary  = Rotary(2, 3, 4)                    # initialize rotary encoder
buzzer  = BUZZER(15)                         # initialize buzzer
tim     = Timer(-1)                          # initialize rotary switch IRQ timer
Vsys    = ADC(29)                            # initialize ADC for Vsys reading
Vin     = ADC(26)                            # init ADC for Vin (battery) measurement
writer  = Writer(ssd, font, False)           # init writer NOT verbose
screen  = Screen(ssd, writer, rotate = True) # set rotate to False if you don't need to rotate screen


# states
TIMER_RUNNING  = const(0)                    # [state] timer is running
TIMER_PAUSED   = const(1)                    # [state] timer is paused
TIMER_FINISHED = const(2)                    # [state] time has finished

SET_MINUTES    = const(0)                    # [mode] app is setting minutes
SET_SECONDS    = const(1)                    # [mode] app is setting seconds
RUN_MODE       = const(2)                    # [mode] app is doing the timing


# globals
state          = TIMER_PAUSED                # initial state
mode           = RUN_MODE                    # initial mode
current_time   = DEFAULT_TIMER               # time in seconds
old_time       = 0                           # a holder to watch for time changes
sw_pressed     = False                       # flag for rotary switch pressed
is_lng_press   = False                       # flag for long press
bat_chrg       = 0                           # battery charge (percentage)


buzzer.shortBeep()                           # hello! we are open for business


def endloop():
    """Timer finished. Make some noise."""

    buzzer.doubleBeep()
    screen.end_msg()


def update_time():
    """Update the time on screen"""

    global old_time, current_time

    if old_time == current_time:
        return

    old_time = current_time

    if mode == RUN_MODE:
        screen.clear_all()
    else:
        screen.clear_main()

    screen.print_timer(current_time)


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

    if current_time < 1:
        current_time = 1


def minutes_up():
    """Increment minutes"""

    global current_time

    current_time += 60

    if current_time == MAX_TIME:
        current_time = MAX_TIME


def minutes_down():
    """Decrement minutes"""

    global current_time

    current_time -= 60

    if current_time < 0:
        current_time = 1


def manage_mode():
    """Manage App Mode"""

    global mode

    if mode == SET_MINUTES:
        mode = SET_SECONDS
        screen.set_seconds()

    elif mode == SET_SECONDS:
        mode = RUN_MODE
        screen.clear_underline()

    else:
        mode = SET_MINUTES
        screen.set_minutes()


def manage_cw():
    """Action: Rotary was turned clockwise"""

    if mode == SET_MINUTES:
        minutes_up()

    elif mode == SET_SECONDS:
        seconds_up()


def manage_ccw():
    """Action: Rotary was turned counter-clockwise"""

    if mode == SET_MINUTES:
        minutes_down()

    elif mode == SET_SECONDS:
        seconds_down()


def short_press():
    """Action: Rotary button was shortly pressed"""

    global state, mode, current_time

    if state == TIMER_RUNNING:
        state = TIMER_PAUSED

    elif state == TIMER_PAUSED:
        if mode == SET_MINUTES or mode == SET_SECONDS:
            mode = RUN_MODE
            screen.clear_underline()

        state = TIMER_RUNNING

    elif state == TIMER_FINISHED:
        current_time = DEFAULT_TIMER
        state = TIMER_PAUSED


def long_press():
    """Action: Rotary button was long pressed"""

    global mode, is_lng_press

    if state == TIMER_RUNNING:
        return

    is_lng_press = True

    tim.deinit()

    if mode == SET_MINUTES:
        mode = SET_SECONDS
        screen.set_seconds()

    elif mode == SET_SECONDS:
        mode = RUN_MODE
        screen.clear_underline()

    else:
        mode = SET_MINUTES
        screen.set_minutes()

    sleep_ms(300)


def button_callback(t):
    """ISR for rotary switch timer"""

    if sw_pressed == True:
        long_press()


def manage_button():
    """Manage a Rotary switch press"""

    global sw_pressed

    sw_pressed = True

    tim.init(mode = Timer.ONE_SHOT, period = 1000, callback = button_callback)


def rotary_changed(change):
    """
    ISR - Interrupt Service Routine for the rotary encoder

    Parameters
    ----------
    change : int
        the value to process
    """

    global sw_pressed, is_lng_press

    if change == Rotary.ROT_CW:
        manage_cw()

    elif change == Rotary.ROT_CCW:
        manage_ccw()

    elif change == Rotary.SW_PRESS:
        manage_button()

    elif change == Rotary.SW_RELEASE:
        if is_lng_press == True:
            is_lng_press = False
        else:
            tim.deinit()
            is_lng_press = False
            short_press()

        sw_pressed = False


def read_voltage():
    """
    Read supplied voltage
    """

    return Vsys.read_u16() * CONV_FACTOR


def check_pwr():
    """
    Check income pwr supply
    """

    adc0  = Vin.read_u16()  * CONV_FACTOR
    adc29 = Vsys.read_u16() * CONV_FACTOR

    if adc29 > 4.7:
        usb  = True
        vlts = adc29
        chrg = 0
    else:
        usb  = False
        vlts = adc0
        chrg = int(((adc0 - BATTERY_MIN)) / (BATTERY_MAX - BATTERY_MIN) * 100)

    screen.print_voltage(str("{:.1f}".format(vlts)), usb, chrg)

    if vlts < BATTERY_MIN:
        screen.clear_all()
        ssd.text("Charge Battery!", 0, 0)
        ssd.show()

        while True:
            pass


rotary.add_handler(rotary_changed)           # Register Rotary encoder ISR


if __name__ == '__main__':
    """Main loop"""

    while True:
        check_pwr()

        if state == TIMER_RUNNING:
            current_time -= 1
            # meh! calibrated with my phone. accurate enough for a kitchen timer tho
            sleep_ms(934)

            if current_time <= 0:
                state = TIMER_FINISHED

            else:
                update_time()

        elif state == TIMER_PAUSED:
            update_time()

        elif state == TIMER_FINISHED:
            endloop()
