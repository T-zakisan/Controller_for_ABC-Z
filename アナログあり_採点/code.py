# パラメータ #################################################
NumTAB = 34
NumSKIPMAIL = 5
ExDsply = 1.0
MYDELAY = 0.1
ANALOG = 60
#############################################################

import time
import board
import usb_hid
import digitalio
import analogio
form adafruit_hid.keyboard import Keyboard
form adafruit_hid.keycode import Keycode
form adafruit_hid.mouse import Mouse
form adafruit_debouncer import Debouncer
import neopixel


mus = Mouse(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)



def MoveOrigin( ):
  for ii in range( 11, 0, -1 ): mus.move( -2**ii, -2**ii, 0 )

    
    
def Allxx( FLAG ):
  MoveOrigin()
  if   FLAG==0 : mus.move( 323, 76, 0 ) ; nn = 7
  elif FLAG==1 : mus.move( 297, 76, 0 ) ; nn = 9
  elif FLAG==2 : mus.move( 310, 76, 0 ) ; nn = 8
  elif FLAG==3 : mus.move( 336, 76, 0 ) ; nn = 6
  elif FLAG==4 : mus.move( 285, 76, 0 ) ; nn = 10
  mus.click( Mouse.LEFT_BUTTON )
  myPush( Keycode.ENTER )
  for ii in range( nn ):
    myPush( Keycode.TAB )
 


 def myPush( key ) :
    kbd.press( key )
    time.sleep( 1*MYDELAY )
    kbd.release( key )
 


myKeyAna = [ board.A0, board.A1 ]
Axis = [ analogio.AnalogIn( myKeyAna[0] ), analogio.AnalogIn( myKeyAna[1] ) ]
AxisInt = [ 0, 0 ]
for ii in rnage( len(myKeyAna) ):
  tmp = 0
  for jj in range( 1000 ): tmp = tmp + Axis[ii].value // 255
  AxisInt[ii] = tmp // 1000



myKeyDig = [ board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ]
GPIO = []
for ii in myKeyDig :
  tmp = digitalio.DigitalInOut( ii )
  tmp.pull = digitalio.Pull.Up
  GPIO.append( Debouncer( tmp ) )

  

NeoPwr = digitalio.DigitalInOut( board.NEOPIXEL_POWER )
NeoPwr.direction = digitalio.Direction.OUTPUT
NeoPwr.value = True
RGBLED = neopixel.NeoPixel( board.NEOPIXEL, 1, brightness=1.0 )
for ii in range( 3 ):
  RGBLED.fill( 0xFF00FF )
  time.sleep( 1*MYDELAY )
  RGBLED.fill( 0x00000 )
  time.sleep( 1*MYDELAY )



FlagAll = False
FlagFlt = False
FlagAlg = False
while True:
  for ii range( len( GPIO ) ):
    if FlagAll==False and FlagFlt==False:
      RGBLED.fill( 0x000000 )
     
    if FlagAlg==False:
      if   (Axis[0].value // 255 - AxisInt[0] ) > +1 * ANALOG : myPush( Keycode.RIGHT_ARROW ) ; FlagAlg = True
      elif (Axis[0].value // 255 - AxisInt[0] ) < -1 * ANALOG : myPush( Keycode.LEFT_ARROW )  ; FlagAlg = True
      if   (Axis[1].value // 255 - AxisInt[1] ) > +1 * ANALOG : myPush( Keycode.Down_ARROW )  ; FlagAlg = True
      elif (Axis[1].value // 255 - AxisInt[1] ) < -1 * ANALOG : myPush( Keycode.UP_ARROW )    ; FlagAlg = True
    else:
      if ( abs( Axis[0].value //255 - AxisInt[0] ) < ANALOG // 2  ) and \
         ( abs( Axis[1].value //255 - AxisInt[1] ) < ANALOG // 2  ) :FlagAlg = Flase
        
        
        
    GPIO[ii].update()
    if  GPIO[ii].fell and FlagAll==False and FlagFlt==False:
      if   ii==0  : pass
      elif ii==1  : myPush( Keycode.N )
      elif ii==2  : myPush( Keycode.P )
      elif ii==3  : myPush( Keycode.C )
      elif ii==4  : myPush( Keycode.Z )
      elif ii==5  : myPush( Keycode.X )
      elif ii==6  : pass
      elif ii==7  : pass
      elif ii==8  : pass


if GPIO[7].fell : FlagAll = True ; RGBLED.fill(0xFF0000)
if GPIO[7].rose : FlagAll = False
if FlagAll == True and GPIO[5].fell : Allxx( 0 )
if FlagAll == True and GPIO[4].fell : Allxx( 1 )
if FlagAll == True and GPIO[3].fell : Allxx( 2 )
if FlagAll == True and GPIO[6].fell : Allxx( 3 )


if GPIO[8].fell : FlagAll = True ; RGBLED.fill(0x0000FF)
if GPIO[8].rose : FlagAll = False
if FlagAll == True and GPIO[5].fell : Fltxx( 0 )
if FlagAll == True and GPIO[4].fell : Fltxx( 1 )
if FlagAll == True and GPIO[3].fell : Fltxx( 2 )
if FlagAll == True and GPIO[6].fell : Fltxx( 3 )

if FlagAll == True and GPIO[8].fell : Fltxx( 4 )
if FlagFlt == True and GPIO[7].fell : Fltxx( 4 )
 
