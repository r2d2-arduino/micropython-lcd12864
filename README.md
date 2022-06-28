# micropython-lcd12864 (st7920)

![Image](./photo/lcd12864.jpg)

**LCD12864 connect**

|LCD12864|ESP8266|
| ------ | ------ |
|GND|GND|
|VCC|+5V|
|V0|-|
|RS|GPIO15(D8)|
|R/W|GPIO13(D7)|
|E|GPIO14(D5)|
|DB0|-|
|..|-|
|DB7|-|
|PSB|GND|
|NC|-|
|RST|+5V|
|VOUT|-|
|BLA|+5v|
|BLK|GND|

Code example:

```python
from machine import SPI, Pin
from lcd12864 import SPI_LCD12864

spi = machine.SPI(1, baudrate=100000, polarity=1, phase=1)
cs = Pin( 15, Pin.OUT, value=0 )

lcd = SPI_LCD12864( spi=spi, cs=cs )
lcd.text( "MicroPython !", 10, 25, 1 )
lcd.rect(0,0,128,64,1)
lcd.rect(3,3,128-6,64-6,1)
lcd.update()
```
