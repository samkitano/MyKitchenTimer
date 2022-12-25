from rotary import Rotary
from buzzer import BUZZER
import utime as time

from oled.config import WIDTH, HEIGHT, setup_ssd
from oled.writer import Writer
from micropython import const
from machine import Timer

import oled.seven_segment_48 as font_big

# init classes
ssd     = setup_ssd()                        # Setup SSD [scl = 1, sda = 0, i2c = 0]
rotary  = Rotary(2, 3, 4)                    # initialize rotary encoder
buzzer  = BUZZER(15)                         # initialize buzzer
tim     = Timer(-1)                          # initialize rotary switch IRQ timer


# constants (states)
TIMER_RUNNING      = const(0)                # [state] timer is running
TIMER_PAUSED       = const(1)                # [state] timer is paused
TIMER_FINISHED     = const(2)                # [state] time has finished

SET_MINUTES        = const(0)                # [mode] app is setting minutes
SET_SECONDS        = const(1)                # [mode] app is setting seconds
RUN_MODE           = const(2)                # [mode] app is doing the timing
MAX_TIME           = const(5999)             # 99 * 60 + 59 maximum time allowed


# character lengths for x position center calculation. Font seven_segment_48 is NOT monospaced
char_lens = { ':': 3, '0': 9, '1': 3, '2': 9, '3': 8, '4': 9, '5': 9, '6': 9, '7': 8, '8': 9, '9': 9 }


# globals
state              = TIMER_PAUSED            # initial state
mode               = RUN_MODE                # initial mode
default_start_time = 5#8 * 60                  # default is 8 minutes
current_time       = default_start_time      # time in seconds

write_blue   = Writer(ssd, font_big, False)  # init writer for small font
old_time     = 0                             # a holder to watch for time changes
timer_y      = 16                            # default Y position for timer
set_y        = 0                             # default Y position for setup
sw_pressed   = False                         # flag for rotary switch pressed
is_lng_press = False                         # flag for long press


def rotate_display():                        # rotate the screen by 180º
    global timer_y, set_y

    ssd.rotate(2)
    timer_y = 0
    set_y   = 64 - 16


buzzer.shortBeep()                           # hello! we are open for business

rotate_display()                             # in my case, I do need to rotate the screen


def clear_blue():
    ssd.fill_rect(0, timer_y, 128, 64, 0)
    ssd.show()


def endloop():
    """Timer finished. Make some noise."""

    buzzer.doubleBeep()
    end_msg()

    return


def update_time():
    global mode, old_time, current_time

    if old_time == current_time:
        return
    
    old_time = current_time

    ms           = get_str_time()
    str_time     = ms[0] + ":" + ms[1]
    str_time_len = get_time_len(str_time)
    x_pos        = (64 - str_time_len) / 2

    if mode == RUN_MODE:
        ssd.fill(0)
    else:
        clear_blue()
    
    write_blue.set_textpos(ssd, timer_y, int(x_pos))
    write_blue.printstring(str_time)
    ssd.show()


def get_time_len(el_stringo):
    global char_lens
    len = 0

    for c in el_stringo:
        len += char_lens[c]

    return len


def get_str_time():
    global current_time
    
    seconds = current_time % 60
    str_sec = str(seconds)
    
    if seconds < 10:
        str_sec = '0' + str_sec

    minutes = int((current_time - seconds) / 60)
    str_min = str(minutes)
    
    if minutes < 10:
        str_min = '0' + str_min
    
    return str_min, str_sec


def end_msg():
    write_blue.set_textpos(ssd, timer_y, 9)
    write_blue.printstring("00:00")
    ssd.show()
    time.sleep(0.5)
    ssd.fill(0)
    ssd.show()


def clear_yellow():
    ssd.fill_rect(0, set_y, 128, 16, 0)
    ssd.show()


def set_minutes():
    clear_yellow()
    ssd.fill_rect(10, set_y, 46, 16, 1)
    ssd.show()


def set_seconds():
    clear_yellow()
    ssd.fill_rect(70, set_y, 46, 16, 1)
    ssd.show()


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


def manage_mode():
    global mode

    if mode == SET_MINUTES:
        mode = SET_SECONDS
        set_seconds()

    elif mode == SET_SECONDS:
        mode = RUN_MODE
        clear_yellow()

    else:
        mode = SET_MINUTES
        set_minutes()


def manage_cw():
    global mode

    if mode == SET_MINUTES:
        minutes_up()

    elif mode == SET_SECONDS:
        seconds_up()


def manage_ccw():
    global mode

    if mode == SET_MINUTES:
        minutes_down()

    elif mode == SET_SECONDS:
        seconds_down()


def short_press():
    global state, mode, current_time

    if state == TIMER_RUNNING:
        state = TIMER_PAUSED

    elif state == TIMER_PAUSED:
        if mode == SET_MINUTES or mode == SET_SECONDS:
            mode = RUN_MODE
            clear_yellow()
        
        state = TIMER_RUNNING

    elif state == TIMER_FINISHED:
        current_time = default_start_time
        state = TIMER_PAUSED


def long_press():
    global mode, state, is_lng_press

    if state == TIMER_RUNNING:
        return

    is_lng_press = True
    tim.deinit()

    if mode == SET_MINUTES:
        mode = SET_SECONDS
        set_seconds()

    elif mode == SET_SECONDS:
        mode = RUN_MODE
        clear_yellow()

    else:
        mode = SET_MINUTES
        set_minutes()

    time.sleep_ms(300)


def button_callback(t):
    global sw_pressed

    if sw_pressed == True:
        long_press()


def manage_button():
    global sw_pressed

    sw_pressed = True
    tim.init(mode=Timer.ONE_SHOT, period=1000, callback=button_callback)


def rotary_changed(change):
    """
    ISR - Interrupt Service Routine for the rotary encoder

    Parameters
    ----------
    change : int
        the value to process
    """

    global state, mode, sw_pressed, is_lng_press

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


rotary.add_handler(rotary_changed)           # Register ISR


if __name__ == '__main__':
    """Main loop"""

    while True:
        if state == TIMER_RUNNING:
            current_time -= 1
            time.sleep(0.9) # meh, calibrated with my phone. accurate enough for a kitchen timer tho

            if current_time <= 0:
                state = TIMER_FINISHED

            else:
                update_time()

        elif state == TIMER_PAUSED:
            update_time()

        elif state == TIMER_FINISHED:
            endloop()
