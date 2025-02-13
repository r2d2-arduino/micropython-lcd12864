from machine import SPI
from lcd12864_spi import LCD12864_SPI
from time import sleep
# Set pins here
spi = SPI( 1, baudrate = 1_000_000, polarity = 1, phase = 1 )
lcd = LCD12864_SPI( spi = spi, cs_pin = 15, rotation = 1 )

SCREEN_WIDTH  = lcd.width
SCREEN_HEIGHT = lcd.height

lcd.fill(0) # clear

lcd.pixel(0, 63, 1)

lcd.ellipse(16, 20, 16, 16, 1, True)
lcd.ellipse(42, 46, 16, 16, 1)

lcd.rect(60, 4, 30, 30, 1, True)
lcd.rect(94, 32, 30, 30, 1)


for y in range(SCREEN_HEIGHT // 4):
    lcd.line(0, 0, SCREEN_WIDTH, y * 4 , 1)

lcd.show()
