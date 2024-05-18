"""
Project path: https://github.com/r2d2-arduino/micropython-lcd12864

Author:
  28 june 2022 - r2d2-arduino
  
Author(s): Derkach Arthur

LCD	| PICO	| Notes
-----------------------
GND	| GND	|
VCC	| VSYS	| 5V
RS	| GP9	| SPI CS
R/W	| GP11	| SPI mosi
E	| GP10	| SPI sck
PSB	| GND	|
RST	| VBUS	| 5V
BLA	| 3V3	| or 5V
BLK	| GND	|

"""
import machine
from machine import SPI, Pin
from lcd12864 import SPI_LCD12864
import time

spi = SPI(1, baudrate=1_000_000, polarity=1, phase=1) #for pico: sck (E) - GP10, mosi (R/W) - GP11
cs = Pin( 9, Pin.OUT, value=0 )# cs (RS) - GP9
lcd = SPI_LCD12864( spi=spi, cs=cs, rotation=1 )

lcd.fill(0)

lcd.text('Hello World!', 0, 0, 1)
lcd.update()

