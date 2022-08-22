'''
2022年8月20日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログあり動作確認) ■■■
  メモ帳を開き、コントローラの各ボタンを押したときに何が入力されたか確認するためのモノ
  本番用プログラムのボタンとマイコン端子の調整時の参考資料にも使える
'''

# パラメータ #####################################################################
MYDELAY = 0.1       #遅延時間[秒]　※特に問題なければ触る必要なし！
ThrAna = 80         #アナログ入力の動作しきい値(大:大きく倒して反応  小:僅かな傾きで反応　※0 <= ThrAna <= 127)
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
# import neopixel   #フルカラーLED

mus = Mouse(usb_hid.devices)          #マウス
kbd = Keyboard(usb_hid.devices)       #キーボード
lyo = KeyboardLayoutUS(kbd)

''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' Analog入力の初期値 '''
AxisInt = [2] #x, yの2つ
KeyAna = [ board.A0, board.A1 ]  #割り当てている端子
#初期値の読み込み(1000回平均値)
for ii in range(1000) :
  for jj in range( len(KeyAna) ) : AxisInt[jj] = analogio.AnalogIn( KeyAna[jj] )/1000



''' SW用GPIO(Digital)の初期設定(プルアップ) '''
''' ボタンの割り当て '''
#  ii in Loop : 0         1         2         3         4         5         6         7
# Output Char : a         b         c         d         e         f         g         h
KeyDig = [ board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9 ]
GPIO =  []  #空リスト(≒配列)定義
for ii in KeyDig : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)



''' Main Loop '''
flag=False  #アナログ入力の有無
while True: #無限ループ

  #アナログ入力の確認
  for ii in range( len(KeyAna) ):
    myAnalog = analogio.AnalogIn( KeyAna[ii] ) - AxisInt[jj]
    if ii==0 and flag==False :
      if myAnalog >= ThrAna :
        lyo.write('Right\n') 
        flag=True; break
      elif myAnalog <= -ThrAna :
        lyo.write('Left\n')
        flag=True; break
    elif ii==1 and flag==False:
      if myAnalog >= ThrAna :
        lyo.write('Up\n')
        flag=True; break
      elif myAnalog <= -ThrAna :
        lyo.write('Down\n')
        flag=True; break
    else :
      flag=False; break


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
      
