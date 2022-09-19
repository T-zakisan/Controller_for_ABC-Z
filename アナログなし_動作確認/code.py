'''
2022年9月19日(月)
※等幅フォントを利用してください！
■■■ ABC-Z専用の入力キーボード for PS用コントローラ(アナログなし動作確認) ■■■
  本番用プログラムのボタンとマイコン端子の調整時の対応端子番号を表示するためのプログラム
  [使い方]
  1. 付属のテキストファイル(CodeTable.txt)を開く
  2. カーソルを1行目の最後尾に移動
  3. 行先頭表記のコントロールのボタンを押す
      ※全ての行を埋めること
  4. 保存して終了する
  
  例)
-- メモ帳の出力結果 ---------------------------------------------------------------------------------------------------------------------------
 上,  5
 左,  3
 下,  8
 右,  2
 △,  4
 〇,  9
 ☓,  1
 L1,  0
 L2,  10
 R1,  6
 R2,  7

'''

# パラメータ #####################################################################
MYDELAY = 0.1       #遅延時間[秒]　※特に問題なければ触る必要なし！
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio(Digital)
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ

kbd = Keyboard(usb_hid.devices)       #キーボード


''' 任意キーを押して放すヤツ '''
def myPush( key1, key2="" ):
  kbd.press( key1 )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key1 )      #押したら戻す

  if key2 != "" :
    kbd.press( key2 )        #ボタンを押す
    time.sleep( 1*MYDELAY ) #適当な表示待ち
    kbd.release( key2 )      #押したら戻す

  kbd.press( Keycode.DOWN_ARROW )
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( Keycode.DOWN_ARROW )




''' SW用GPIO(Digital)の初期設定(プルアップ) '''
''' ボタンの割り当て '''
#  ii in Loop :  0         1         2         3         4         5         6         7         8         9         10
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
      elif ii==10 : myPush( Keycode.ONE,  Keycode.ZERO  )
    
