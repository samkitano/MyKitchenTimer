import micropython
from machine import Pin

class Rotary:
    """
    A handy class for dealing with Rotary Encoders,
    particularly the very cheap and popular KY-040 / HW-040

    Inspired on a script by: gurgleapps - https://github.com/gurgleapps/rotary-encoder

    Attributes
    --------------
    ROT_CW : int
        state for clockwise rotation
    ROT_CCW : int
        state for counter-clockwise rotation
    SW_PRESS : int
        state for switch pressed
    SW_RELEASE : int
        state for switch released

    Methods
    --------------
    rotary_change(pin)
        Rotation handler
    switch_detect(pin)
        Switch handler
    add_handler(handler)
        Register Handler
    call_handlers(type)
        Trigger handlers
    """

    ROT_CW      = 1
    ROT_CCW     = 2
    SW_PRESS    = 4
    SW_RELEASE  = 8

    def __init__(self, dt, clk, sw):
        """
        Instantiate class; Register IRQ handlers

        Parameters
        ----------
        dt : int
            data pin
        clk : int
            clock pin
        sw : int
            switch pin
        """

        self.dt_pin  = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.clk_pin = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.sw_pin  = Pin(sw, Pin.IN, Pin.PULL_UP)

        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()

        self.dt_pin.irq(handler  = self.rotary_change, trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.clk_pin.irq(handler = self.rotary_change, trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.sw_pin.irq(handler  = self.switch_detect, trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING )

        self.handlers = []
        self.last_button_status = self.sw_pin.value()


    def rotary_change(self, pin):
        """Handler to deal with a rotary action

        Parameters
        ----------
        pin : int
            trigger for the interrupt request

            Options:
                Pin.IRQ_FALLING
                Pin.IRQ_RISING
                Pin.IRQ_LOW_LEVEL
                Pin.IRQ_HIGH_LEVEL
        """

        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()

        if new_status == self.last_status:
            return

        transition = (self.last_status << 2) | new_status

        if transition == 0b1110:
            micropython.schedule(self.call_handlers, Rotary.ROT_CW)
        elif transition == 0b1101:
            micropython.schedule(self.call_handlers, Rotary.ROT_CCW)

        self.last_status = new_status


    def switch_detect(self, pin):
        """Handler to deal with a switch action

        Parameters
        ----------
        pin : int
            trigger for the interrupt request

            Options:
                Pin.IRQ_FALLING
                Pin.IRQ_RISING
                Pin.IRQ_LOW_LEVEL
                Pin.IRQ_HIGH_LEVEL
        """

        if self.last_button_status == self.sw_pin.value():
            return

        self.last_button_status = self.sw_pin.value()

        if self.sw_pin.value():
            micropython.schedule(self.call_handlers, Rotary.SW_RELEASE)
        else:
            micropython.schedule(self.call_handlers, Rotary.SW_PRESS)


    def add_handler(self, handler):
        """Add a handler

        Parameters
        ----------
        handler : function
            the callback function
        """

        self.handlers.append(handler)


    def call_handlers(self, type):
        """Call the assigned handlers

        Parameters
        ----------
        type : int
            the handler index
        """

        for handler in self.handlers:
            handler(type)
