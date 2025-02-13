from machine import Pin, SPI
from lcd12864_spi import LCD12864_SPI
from time import sleep_ms

spi = SPI( 1, baudrate = 1_000_000, polarity = 1, phase = 1 )
lcd = LCD12864_SPI( spi = spi, cs_pin = 15, rotation = 1 )

lcd.fill(0)

radius = 4

x_border = lcd.width - 1
y_border = lcd.height - 1

prev_x = radius
prev_y = radius

x = radius
y = radius

x_speed = 2
y_speed = 2

while True:    
    lcd.ellipse(prev_x, prev_y, radius, radius, 0, True) # clear previos
    lcd.ellipse(x, y, radius, radius, 1, True)
    prev_x = x
    prev_y = y
    
    x += x_speed
    y += y_speed
    
    if x + radius > x_border or x - radius < 0:
        x_speed = -x_speed
        
    if y + radius > y_border or y - radius < 0:
        y_speed = -y_speed    
    
    lcd.show() 


    

