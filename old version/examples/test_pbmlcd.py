# Test the PBM reading on the SPI_LCD12864 LCD graphical screen 128x64
#
# bpm & img libraries: https://github.com/mchobby/esp8266-upy/tree/master/FILEFORMAT/imglib
# lcd12864 library: https://github.com/mchobby/esp8266-upy/tree/master/lcdspi-lcd12864/lib
# mpy.pbm : image bitmap of older MicroPython logo
#
# LCD12864 hardware: https://shop.mchobby.be/fr/gravity-boson/1878-afficheur-lcd-128x64-spi-3-fils-3232100018785-dfrobot.html
#

from machine import SPI, Pin
from lcd12864 import SPI_LCD12864
from img import open_image

# PYBStick: S19=mosi, S23=sck, S26=/ss
cs = Pin( 15, Pin.OUT, value=0 )
spi = machine.SPI(1, baudrate=100000, polarity=1, phase=1)

# Pico: GP7=mosi, GP6=sck, GP5=/ss
#cs = Pin( 5, Pin.OUT, value=0 )
#spi = SPI( 0 )
#spi.init( polarity=0, phase=1 )

# PYBOARD: Y8=mosi, Y6=sck, Y5=/ss
#cs = Pin( 'Y5', Pin.OUT, value=0 )
#spi = SPI( 2 )
#spi.init( polarity=0, phase=1 )

lcd = SPI_LCD12864( spi=spi, cs=cs )
# texte à X=10, Y=25, couleur=1 (trait)
#lcd.text( "MicroPython !", 10, 25, 1 )
#lcd.update()

def color_transform( rgb ):
	# transform the clipreader (rgb) color to the target FrameBuffer color (2 colors)
	return 0 if rgb==(0,0,0) else 1

reader = open_image( 'mpy.pbm' )
reader.clip(0,0,lcd.width,lcd.height)
# Copy the clipped aread TO a target FrameBuffer (lcd) at is starting
# position 0,0 for the given clipping width,height .
reader.copy_to(lcd, 0,0, color_transform )
lcd.update()
