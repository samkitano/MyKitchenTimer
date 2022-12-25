# My Kitchen Timer

A DIY kitchen timer with a Raspberry Pi Pico H to help you stop burning your rice and noodles.


## BOM
--------------

| Qtty | Item | Pic |
|------|------|-----|
| 1 | Raspberry Pi Pico H | ![Raspberry Pi Pico](/img/pi-pico.jpg?raw=true "Raspberry Pi Pico")
| 1 | OLED display SSD1306 (128 x 64) | ![SSD1306](/img/oled.jpg?raw=true "SSD1306")
| 1 | Rotary encoder KY-040 | ![KY-040](/img/rotary.jpg?raw=true "KY-040")
| 1 | Piezoelectric buzzer 5V | ![Piezo](/img/piezo.jpg?raw=true "Piezo")
| 1 | AA triple battery holder | ![Battery Holder](/img/holder.jpg?raw=true "Battery Holder")
| 3 | AA Battery (4.5V)* | ![Battery](/img/aa.jpg?raw=true "Battery")

\* probably to be upgraded to chargeable 18650 in the future. Or not.

Alternatively, the device can be powered with an off-the-shelf 5V power bank directly to the pico's micro-usb port.

Switch and box: I will probably never. Still handier than pulling off a phone timer.

## WIRING
--------------

OLED  | PICO
------|------
scl  | gp 1
sda  | gp 0
vcc  | 3v3
gnd  | gnd
--------------

Y-040 | PICO
------|------
clk  | gp 2
dt  | gp 3
sw  | gp 4
\+  | 3v3
gnd  | gnd
--------------

Piezo  | PICO
------|------
\+  | gp 15
\-  | gnd
--------------

Battery| PICO
------|------
\+  | Vsys
\-  | gnd
--------------


## USAGE
--------------
Timer is set to 8 minutes by default. My kind of pasta. Don't judge!

To change the default time, edit line 37 in file `main.py` to a desired value in minutes or seconds x 60. Suppose you want 60 seconds:

```python
# in minutes
default_start_time = 1 * 60
#in seconds
default_start_time = 60
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
