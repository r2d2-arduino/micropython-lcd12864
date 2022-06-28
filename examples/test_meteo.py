"""
Project path: https://github.com/r2d2-arduino/micropython-lcd12864

Author:
  28 june 2022 - r2d2-arduino

"""
from machine import SPI, Pin
from lcd12864 import SPI_LCD12864
from writer import Writer

# Font
import font14 as bigFont
import time

machine.freq(80000000)

spi = SPI(1, baudrate=2000000, polarity=1, phase=1)
cs = Pin( 15, Pin.OUT, value=0 )

lcd = SPI_LCD12864( spi=spi, cs=cs, rotation=1 )

wriBig = Writer(lcd, bigFont, verbose=False)

def drawScreen():
    #lcd.clear()
    
    lcd.line(0, 30, 127, 30, 1)
    lcd.line(64, 0, 64, 63, 1)
    
    #Labels  
    lcd.text( "temp *c", 0, 22, 1 )
    lcd.text( "hum %", 68, 22, 1 )  
    lcd.text( "pres mm", 0, 32, 1 )
    lcd.text( "co2 pmm", 68, 32, 1 ) 
    
    #center
    lcd.fill_rect(64, 31, 1, 1, 1)
    
    draw_icon( lcd, 50, 5, HEART_ICON )
    draw_icon( lcd, 50, 45, HEART_ICON )
    
    draw_icon( lcd, 110, 5, HEART_ICON )
    draw_icon( lcd, 110, 45, HEART_ICON )
    
    lcd.update()
    
def updateScreen(tmp, hum, pres, co2):
    #Temp    
    Writer.set_textpos(lcd, 0, 0)
    wriBig.printstring(str(round(float(tmp),1)))
    
    #Hum
    Writer.set_textpos(lcd, 0, 68)
    wriBig.printstring(str(round(float(hum))))
    
    #Press
    Writer.set_textpos(lcd, 41, 0)
    wriBig.printstring(str(round(float(pres))))
    
    #CO2
    Writer.set_textpos(lcd, 41, 68)
    wriBig.printstring(str(round(float(co2))))
    
    #center
    lcd.fill_rect(64, 30, 1, 1, 0)        
        
    start = time.ticks_ms()
    
    #lcd.update(y1=0, y2=24)
    #lcd.update(y1=40, y2=64)

    lcd.update()
    
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(delta/1000)

HEART_ICON = [
  [0,0,0,0,0,0,0,0,0,0,0],
  [0,0,1,1,1,0,1,1,1,0,0],
  [0,1,1,0,1,1,1,1,1,1,0],
  [0,1,0,1,1,1,1,1,1,1,0],
  [0,1,1,1,1,1,1,1,1,1,0],
  [0,0,1,1,1,1,1,1,1,0,0],
  [0,0,0,1,1,1,1,1,0,0,0],
  [0,0,0,0,1,1,1,0,0,0,0],
  [0,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0] ]

def draw_icon( lcd, from_x, from_y, icon ):
    for y, row in enumerate( icon ):
        for x, color in enumerate( row ):
            if color==None:
                continue
            lcd.pixel( from_x+x,
                       from_y+y,
                       color )

drawScreen()
updateScreen(27.5, 39, 749, 399)
#time.sleep(1)
#updateScreen(28.1, 41, 751, 412)
#time.sleep(1)
#updateScreen(28.3, 45, 757, 431)
