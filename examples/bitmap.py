from machine import SPI
from lcd12864_spi import LCD12864_SPI
from bitmaps import sun, suncloud, rain, rainlight, snowman
from time import sleep

spi = SPI( 1, baudrate = 4_000_000, polarity = 1, phase = 1 )
lcd = LCD12864_SPI( spi = spi, cs_pin = 15, rotation = 1 )
  
bitmaps = [sun, suncloud, rain, rainlight, snowman]
size = 16
for i in range(len(bitmaps)):
    lcd.fill(0) # clear
    bitmap = bitmaps[i]
    for x in range(8):
        for y in range(4):
            lcd.draw_bitmap(bitmap, x * size, y * size, 1)
    lcd.show()
    sleep(1)
    