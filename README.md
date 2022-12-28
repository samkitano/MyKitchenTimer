# My Kitchen Timer

A DIY kitchen timer with a Raspberry Pi Pico H to help you stop burning your rice and noodles.


## BOM

| Qtty | Item | Pic |
|------|------|-----|
| 1 | Raspberry Pi Pico H | ![Raspberry Pi Pico](/img/pi-pico.jpg?raw=true "Raspberry Pi Pico")
| 1 | OLED display SSD1306 (128 x 64) | ![SSD1306](/img/oled.jpg?raw=true "SSD1306")
| 1 | Rotary encoder KY-040 | ![KY-040](/img/rotary.jpg?raw=true "KY-040")
| 1 | Piezoelectric buzzer 5V | ![Piezo](/img/piezo.jpg?raw=true "Piezo")
| 1    | 18650 battery holder | ![18650 Battery Holder](/img/18650-single-battery-holder.jpg?raw=true "18650 Battery Holder")
| 1    | TP4056 charge module |  ![TP4056](/img/18650_chrg_module.jpg?raw=true "TP4056")
| 1    | 1KΩ resistor | ![1K](/img/1k.jpg?raw=true "1K ohm")
| 1    | 2KΩ resistor | ![2K](/img/2k.jpg?raw=true "2K ohm")
| 1    | 18650 battery | ![18650](/img/18650.jpg?raw=true "18650")
| 1  | Switch - any model | ![switch](/img/switch.jpg?raw=true "switch")

## WIRING

OLED  | PICO
------|------
scl  | gp 1
sda  | gp 0
vcc  | 3v3
gnd  | gnd


Y-040 | PICO
------|------
clk  | gp 2
dt  | gp 3
sw  | gp 4
\+  | 3v3
gnd  | gnd


Piezo  | PICO
------|------
\+  | gp 15
\-  | gnd


Battery | *
------|------
\+  | To Switch "a"
\-  | gnd


Switch | *
------|------
"a"  | Battery +
"b"  | Vsys (Pico)


1K Resistor | PICO
------|------
any leg  | Vsys
other leg  | gp 26


2K Resistor | PICO
------|------
any leg  | gp 26
other leg  | gnd



## USAGE

Timer is set to 8 minutes by default. My kind of pasta. Don't judge!

To change the default time, edit line 17 in file `config.py` to a desired value. Suppose you want 120 seconds (2 min):

```python
# in minutes
DEFAULT_TIMER = const(2 * 60)
# in seconds
DEFAULT_TIMER = const(120)
```

### Start/Pause
Short Press Rotary to start

Short press to Pause

Short Press to Resume

### Set
Long press (1 sec +) Rotary to set minutes

Long press (1 sec +) Rotary again to set seconds

Short press to restart

### End
Depending on the Piezo thing, the time-out alarm can be loud AF as PWM's duty cycle is set next to the limit. More loud = more fun. Don't judge.

Short press Rotary to stop the noise.

**For educational purposes only**: *do not leave the device hidden somewhere at random friend's/mother-in-law's place.* Not cool. For that purpose one should implement a PIR sensor. You know... to temporarily shut the thing up if they get too close?


## LICENSES
This software is licensed under the [MIT license](https://opensource.org/licenses/MIT)

The included font (7 Segment Display Font) is NOT licensed for commercial use. For that purpose you should [GET A LICENSE](https://creativemarket.com/KraftiLab/2702060-7-Segment-Display-Font?utm_source=Link&utm_medium=CM+Social+Share&utm_campaign=Product+Social+Share&utm_content=7+Segment+Display+Font+~+Display+Fonts+~+Creative+Market&ts=201806)

## DISCLAIMER
Although thoroughly tested, this software and hardware installation guides are provided in good faith and to the best of both my habilities and knowledge. Under no circumstances am I responsible for any damages, malfunctions or injuries in a replication attempt. Do it at your own risk.

Always read the documentation pertaining to electronic hardware. RTFM!
