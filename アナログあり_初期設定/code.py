'''
2022年8月23日
■■■ ABC-Z専用の入力キーボード for PS用コントローラ(アナログあり動作確認) ■■■
  メモ帳を開き、コントローラの各ボタンを押したときに何が入力されたか確認するためのモノ
  本番用プログラムのボタンとマイコン端子の調整時の参考資料にも使える
'''

# パラメータ #####################################################################
MYDELAY = 0.0       #遅延時間[秒]　※特に問題なければ触る必要なし！
ANALOG = 60         #アナログ入力の動作しきい値(大:大きく倒して反応  小:僅かな傾きで反応　※0 <= ThrAna <= 127)
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio(Digital)
import analogio   #set gpio(Anallog)
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ

mus = Mouse(usb_hid.devices)          #マウス
kbd = Keyboard(usb_hid.devices)       #キーボード
lyo = KeyboardLayoutUS(kbd)



''' 任意キーを押して放すヤツ '''
def myPush( key1, key2="" ):
  kbd.press( key1 )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key1 )      #押したら戻す
  if key2 != "" :
    kbd.press( key2 )        #ボタンを押す
    time.sleep( 0*MYDELAY ) #適当な表示待ち
    kbd.release( key2 )      #押したら戻す
  kbd.press( Keycode.DOWN_ARROW )
  time.sleep( 0*MYDELAY ) #適当な表示待ち
  kbd.release( Keycode.DOWN_ARROW )



''' Analog入力の初期値 '''
Axis = [ analogio.AnalogIn( board.A0 ), analogio.AnalogIn( board.A1 ) ]
AxisInt = [ 0, 0 ]
for ii in range( len( Axis ) ) :
  tmp = 0
  for jj in range( 1000 ): tmp = tmp + Axis[ii].value // 255 #アナログ信号を1/255で取得
  AxisInt[ii] = tmp // 1000  #初期値の読み込み(1000回平均値)



''' SW用GPIO(Digital)の初期設定(プルアップ) '''
''' ボタンの割り当て '''
#   ii in Loop : 0         1         2         3         4         5         6         7         8
#  Output Char : a         b         c         d         e         f         g         h         i
KeyDig = [ board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ]
GPIO =  []  #空リスト(≒配列)定義
for ii in KeyDig : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
  GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)



''' Main Loop '''
FlagAlg = False  #アナログ入力の有無
while True: #無限ループ

  # アナログ入力の確認
  if FlagAlg==False:
    if   (Axis[0].value // 255 - AxisInt[0] ) > +1 * ANALOG : myPush( Keycode.ZERO ) ; FlagAlg = True
    elif (Axis[0].value // 255 - AxisInt[0] ) < -1 * ANALOG : myPush( Keycode.ZERO ) ; FlagAlg = True
    if   (Axis[1].value // 255 - AxisInt[1] ) > +1 * ANALOG : myPush( Keycode.ONE )  ; FlagAlg = True
    elif (Axis[1].value // 255 - AxisInt[1] ) < -1 * ANALOG : myPush( Keycode.ONE )  ; FlagAlg = True
  else:
    if ( abs( Axis[0].value //255 - AxisInt[0] ) < ANALOG // 2  ) and \
        ( abs( Axis[1].value //255 - AxisInt[1] ) < ANALOG // 2  ) :FlagAlg = False


  #デジタル(ボタン)の確認
  for ii in range( len( GPIO ) ): #ボタンの数で繰り返し
    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell :#スイッチが押されていたら
      if   ii==0  : myPush( Keycode.TWO )
      elif ii==1  : myPush( Keycode.THREE )
      elif ii==2  : myPush( Keycode.FOUR )
      elif ii==3  : myPush( Keycode.FIVE )
      elif ii==4  : myPush( Keycode.SIX )
      elif ii==5  : myPush( Keycode.SEVEN )
      elif ii==6  : myPush( Keycode.EIGHT )
      elif ii==7  : myPush( Keycode.NINE )
      elif ii==8  : myPush( Keycode.ONE, Keycode.ZERO )
      
