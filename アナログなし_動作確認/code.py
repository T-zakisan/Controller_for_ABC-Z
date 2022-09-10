'''
2022年8月20日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログなし動作確認) ■■■
  メモ帳を開き、コントローラの各ボタンを押したときに何が入力されたか確認するためのモノ
  本番用プログラムのボタンとマイコン端子の調整時の参考資料にも使える
'''

# パラメータ #####################################################################
MYDELAY = 0.1       #遅延時間[秒]　※特に問題なければ触る必要なし！
#ThrAna = 80         #アナログ入力の動作しきい値(大:大きく倒して反応  小:僅かな傾きで反応　※0 <= ThrAna <= 127)
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio(Digital)
import analogio   #set gpio(Anallog)
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ
# import neopixel   #フルカラーLED

mus = Mouse(usb_hid.devices)          #マウス
kbd = Keyboard(usb_hid.devices)       #キーボード
#lyo = KeyboardLayoutUS(kbd)

''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' SW用GPIO(Digital)の初期設定(プルアップ) '''
''' ボタンの割り当て '''
#  ii in Loop :  0         1         2         3         4         5         6         7         8         9         10
# Output Char :  a         b         c         d         e         f         g         h         i         j         k
KeyDig = [ board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ]
GPIO =  []  #空リスト(≒配列)定義
for ii in KeyDig : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
  GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)



''' Main Loop '''
while True: #無限ループ

  #デジタル(ボタン)の確認
  for ii in range( len( GPIO ) ): #ボタンの数で繰り返し
    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell :#スイッチが押されていたら
      if   ii==0  : myPush( Keycode.A )
      elif ii==1  : myPush( Keycode.B )
      elif ii==2  : myPush( Keycode.C )
      elif ii==3  : myPush( Keycode.D )
      elif ii==4  : myPush( Keycode.E )
      elif ii==5  : myPush( Keycode.F )
      elif ii==6  : myPush( Keycode.G )
      elif ii==7  : myPush( Keycode.H )
      elif ii==8  : myPush( Keycode.I )
      elif ii==9  : myPush( Keycode.J )
      elif ii==10 : myPush( Keycode.K )
