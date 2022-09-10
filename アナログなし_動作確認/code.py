'''
2022年8月20日
※等幅フォントを利用してください！
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログなし動作確認) ■■■
  本番用プログラムのボタンとマイコン端子の調整時の対応端子番号を表示するためのプログラム
  [使い方]
  1. 付属のExcelファイルを開き、A2（A列2行目）にカーソルを移す
  2. 1行目記載の記号通りのコントロールのボタンを押す(10はXが出力される)
  3. 本番用プログラムの" myKey = ( " の行の各 " board.D* " の*を2.の数字に書き換える

  　例)
-- メモ帳の出力結果 ---------------------------------------------------------------------------------------------------------------------------
 Ａ | Ｂ | Ｃ | Ｄ | Ｅ | Ｆ | Ｇ | Ｈ | Ｉ | Ｊ | Ｋ |
 上 | 左 | 下 | 右 | △ | 〇 | ☓ | L1 | L2 | R1 | R2 | 
 5 |  3 |  8 |  2 |  4 |  9 |  1 |  0 |  x |  6 |  7

-- 本番用プログラムより抜粋 ---------------------------------------------------------------------------------------------------------------------------
    # ボタンの割り当て
    #  ii in Loop : 0         1         2         3         4         5         6         7         8         9         10
    #         ABC : △        〇        ×        次        All       Filter    戻        上        右        左        下
    #         BTN : △        〇        ×        R1        R2        L2        L1        上        右        左        下    SkipMail
    #myKey = ( board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ) ←変更前
     myKey = ( board.D4, board.D9, board.D1, board.D6, board.D7, board.D10, board.D0, board.D5, board.D2, board.D3, board.D8 ) ←変更後

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
  kbd.press( Keycode.TAB )
  kbd.release( Keycode.TAB )



''' SW用GPIO(Digital)の初期設定(プルアップ) '''
''' ボタンの割り当て '''
#  ii in Loop :  0         1         2         3         4         5         6         7         8         9         10
# Output Char :  0         1         2         3         4         5         6         7         8         9         X
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
      if   ii==0  : myPush( Keycode.ZERO )
      elif ii==1  : myPush( Keycode.ONE )
      elif ii==2  : myPush( Keycode.TWO )
      elif ii==3  : myPush( Keycode.THREE )
      elif ii==4  : myPush( Keycode.FOUR )
      elif ii==5  : myPush( Keycode.FIVE )
      elif ii==6  : myPush( Keycode.SIX )
      elif ii==7  : myPush( Keycode.SEVEN )
      elif ii==8  : myPush( Keycode.EIGHT )
      elif ii==9  : myPush( Keycode.NINE )
      elif ii==10 : myPush( Keycode.X )
