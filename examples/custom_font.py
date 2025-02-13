from machine import Pin, SPI
from lcd12864_spi import LCD12864_SPI
import LibreBodoni20 as MY_FONT
from time import sleep
# Set pins here
spi = SPI( 1, baudrate = 1_000_000, polarity = 1, phase = 1 )
lcd = LCD12864_SPI( spi = spi, cs_pin = 15, rst_pin = 4, rotation = 1 )

lcd.fill(0)
lcd.set_font(MY_FONT)
lcd.set_text_wrap()
lcd.text("Default 8x8 font", 0, 0)
lcd.draw_text("Custom font:  LibreBodoni  size 20", 0, 10)

lcd.show()