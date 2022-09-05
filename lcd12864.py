"""" lcd12864 is a FrameBuffer based MicroPython driver for the graphical
     LiquidCrystal LCD12864 display (also known as DFR0091).

Project path: https://github.com/r2d2-arduino/micropython-lcd12864

This project is updated version of
    project: https://github.com/mchobby/esp8266-upy/tree/master/lcdspi-lcd12864

Additions:
    * vertical rotaion;
    * fast graphic render;
    * disabled blinking of display;

Author:
  28 june 2022 - r2d2-arduino
  
LCD -> ESP8266
--------------
GND -> GND
VCC -> 5V
V0
RS  -> D8 GPIO15 CS/SS
R/W -> D7 GPIO13 MOSI
E   -> D5 GPIO14 SCK
DB0
..
DB7
PSB -> GND
NC
RST -> 5V
VOUT
BLA -> 3.3V
BLK -> GND

"""

import framebuf
import time

LCD_X_RES = 128
LCD_Y_RES = 64

LCD_CLS         = 0x01
LCD_HOME        = 0x02
LCD_ADDRINC     = 0x06
LCD_DISPLAYON   = 0x0C
LCD_DISPLAYOFF  = 0x08
LCD_CURSORON    = 0x0E
LCD_CURSORBLINK = 0x0F
LCD_BASIC       = 0x30
LCD_EXTEND      = 0x34
LCD_GFXMODE     = 0x36
LCD_TXTMODE     = 0x34
LCD_STANDBY     = 0x01
LCD_ADDR        = 0x80


class SPI_LCD12864( framebuf.FrameBuffer ):
    def __init__( self, spi, cs, width = LCD_X_RES, height = LCD_Y_RES, rotation = 0 ):
        """ constructor

            :param spi: initialized spi bus (only mosi is used)
            :param cs: slave select pin for the SPI bus
        """
        # Driving the LCD3310
        self.spi = spi
        self.cs = cs

        # Other properties
        self.height = height
        self.width  = width
        self._buf1 = bytearray( 1 ) # 1 byte data
        self._cmdbuf = bytearray(3)
        self._rotation = rotation
        
        #order of bites in buffer depending of screen position
        _bufFormat = framebuf.MONO_HLSB
        if (self._rotation == 1):
            _bufFormat = framebuf.MONO_HMSB
            
        # Initialize the FrameBuffer
        _bufsize = (self.width * self.height)//8
        self._buffer = bytearray( _bufsize ) # 8 pixels per Bytes MONO_VLSB (1bit/pixel, 7th bit the topmost pixel)
        super().__init__(
                        self._buffer,
                        self.width, # pixels width
                        self.height, # pixels height
                        _bufFormat # 1 bit per pixel, 7th bit the leftmost pixel
                )
        # Initilize controler
        self._begin()
        # Clear and Update
        #self.clear()

    def _begin(self):
        """ Initialize the LCD controler """
        try:
            self.cs.value( 1 )
        
            self._write_cmd( LCD_BASIC ) # basic instruction set
            self._write_cmd( LCD_CLS ) #clear
            time.sleep_us(50) #wait for clearing
            
            self._write_cmd( LCD_ADDRINC )
            self._write_cmd( LCD_DISPLAYON ) # display on
           
        finally:
            self.cs.value( 0 )
        time.sleep_us(50) # Don't start too fast

    def clear( self ):
        self.fill( 0 ) # Clear FrameBuffer
        try:
            self.cs.value( 1 )
            self._write_cmd( LCD_BASIC )
            self._write_cmd( LCD_CLS ) #clear
            time.sleep_us(50)
        finally:
            self.cs.value( 0 ) 
        
    def _write_cmd( self, cmd ):
        self._cmdbuf[0] = 0xF8
        self._cmdbuf[1] = cmd & 0xF0
        self._cmdbuf[2] = (cmd & 0x0F) << 4        
        self.spi.write( self._cmdbuf )
        
    def _write_dat( self, dat ):
        self._cmdbuf[0] = 0xFA
        self._cmdbuf[1] = dat & 0xF0
        self._cmdbuf[2] = (dat & 0x0F) << 4        
        self.spi.write( self._cmdbuf )

    def update( self, y1 = 0, y2 = 64): # Send FrameBuffer to lcd  
        #Set text mode
        try:
            self.cs.value( 1 )
            self._write_cmd(LCD_EXTEND)
            self._write_cmd(LCD_GFXMODE)
        finally:
            self.cs.value( 0 )
        
        for ygroup in range(y1, y2):
            x = LCD_ADDR
            y = ygroup + LCD_ADDR
                
            if ygroup>31:
                x += 8
                y -= 32
                
            try:
                self.cs.value( 1 )
                #Set addres position
                self._write_cmd(LCD_ADDR | y)
                self._write_cmd(LCD_ADDR | x)
                
                #Send buffer to display
                for i in range(16):
                    if (self._rotation == 1):
                        bufi = 1023 - (ygroup * 16) - i
                    else:
                        bufi = (ygroup * 16) + i
                    self._write_dat(self._buffer[bufi])
            finally:
                self.cs.value( 0 )      
