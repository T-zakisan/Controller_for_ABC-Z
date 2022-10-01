'''
2022年10月01日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログなし動作確認) ■■■
  プレステのコントローラを採点ソフトABC用にチューニング
  〇、△、☓、次の問題、前の問題、十字キーだけでなく、一括やフィルタにも対応
■動作と対応ボタン
[シングル]
    ボタン   |     機能     
------------------------------
  上下左右   |   そのまま
   〇×△    |   そのまま
     L1      |   戻
     R1      |   次
   Select    |   機能なし
   Start     |   機能なし
[コンビネーション] ※L2/R2を先に押す！
        |     L2     |     R2     |
-----------------------------------
   〇   |   一括〇   |   〇のみ   |
   ×   |   一括×   |   ×のみ   |
   △   |   一括△   |   △のみ   |
   上   |   一括未   |   未のみ   |←未実装！必要に応じて追加してみてください！
   L2   |    ----    |   全表示   | フィルター解除
■使用条件
・ディスプレイの拡大を100%（デスクトップ上で右クリック > ディスプレイ設定 > 拡大と縮小 : 100%）
・外部ディスプレイ使用していて、以下の2項目が該当している場合、想定している動作にならないため、ディスプレイ配置(ディスプレイ設定)を変更すること！
  ➀外部モニタが主モニタの左側に配置
  ➁外部モニタ上端が主モニタ上端よりも上部に配置
  (理由)マウスの位置決めを行う際に、マウスを強制的に斜め左45°に移動させ、そこを基準座標としている。
'''

# パラメータ ####################################################################
MYDELAY = 0.1       #遅延時間[秒]　※特に問題なければ触る必要なし！
MYSHIFT = 0         #フィルターボタン位置の右方向への移動(左方向は負にする)
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ

mus = Mouse(usb_hid.devices)          #マウス
kbd = Keyboard(usb_hid.devices)       #キーボード


''' 原点復帰 '''
  # 移動量を指数のカウントダウンとすることで少ない手数で基準座標(左上)に移動
  # 【注意】サブモニタを左上に設置は×
def MoveOrigin(  ):
  for ii in range( 11, 0, -1 ): mus.move( -2**ii, -2**ii, 0 ) # 2^11(=2048px) -> 2^0(=1px) で各移動量=全移動量(4097px:大画面にも対応であろう)



''' All '''
def Allxx( FLAG ) :
  MoveOrigin( )                     #原点復帰
  if   FLAG==0 : mus.move( 322, 38, 0 ) #ALL△
  elif FLAG==1 : mus.move( 278, 38, 0 ) #All○
  elif FLAG==2 : mus.move( 366, 38, 0 ) #ALLｘ
  elif FLAG==3 : mus.move( 410, 38, 0 ) #ALL--
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )
  myPush( Keycode.TAB )



''' Filter '''
def Fltxx( FLAG ) :
  MoveOrigin( )                     #原点復帰
  if   FLAG==0 : mus.move( 338 + MYSHIFT, 76, 0 ) ; nn = 8  #Filter△
  elif FLAG==1 : mus.move( 325 + MYSHIFT, 76, 0 ) ; nn = 9  #Filter○
  elif FLAG==2 : mus.move( 351 + MYSHIFT, 76, 0 ) ; nn = 7  #Filterｘ
  elif FLAG==3 : mus.move( 364 + MYSHIFT, 76, 0 ) ; nn = 6  #Filter未
  elif FLAG==4 : mus.move( 312 + MYSHIFT, 76, 0 ) ; nn = 10 #FilterCancel
  elif FLAG==9 : return
  mus.click( Mouse.LEFT_BUTTON )  #右クリ
  myPush( Keycode.ENTER )         #Enter
  for ii in range( nn ):
    myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)
  return FLAG #Filter状態を戻す



''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' ボタンの割り当て '''
myKey = [ [ board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ],
          []]  #空リスト
myFile = open ( 'CodeTable.txt', 'r' )  #ファイルを読み込みモードで開く
DataList = myFile.readlines() #各行ごとに読み込み
for ii in range( len(DataList) ) :  #読み込んだ行数で繰り返し
  myKey[1] += [ int( DataList[ ii ][ DataList[ii].find(',')+1: ].strip() ) ]  #コンマ以降の文字を抽出(空白削除、テキスト→数値化)
myFile.close()  #ファイルを閉じる



''' SW用GPIOの初期設定(プルアップ) '''
GPIO =  []  #空リスト(≒配列)定義
for ii in myKey[0] : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
  GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)



''' Main Loop '''
FlagAll = False		#R2の状態　※ブロック用
FlagFlt = False		#L2の状態
MODE = 4 #Filter解除
while True:
  for ii in range( len( GPIO ) ): #ボタンの数で繰り返し　

    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell and FlagAll==False and FlagFlt==False: #ボタン「押」 ※フラグはブロック
     
      if   myKey[1][0]==ii  : myPush( Keycode.UP_ARROW )    #上
      elif myKey[1][1]==ii  : myPush( Keycode.LEFT_ARROW )  #左
      elif myKey[1][2]==ii  : myPush( Keycode.DOWN_ARROW )  #下
      elif myKey[1][3]==ii  : myPush( Keycode.RIGHT_ARROW ) #右
      elif myKey[1][4]==ii  : myPush( Keycode.C )  #△
      elif myKey[1][5]==ii  : myPush( Keycode.Z )  #〇
      elif myKey[1][6]==ii  : myPush( Keycode.X )  #✕
      elif myKey[1][7]==ii  : myPush( Keycode.P ) ; MODE = Fltxx( MODE ) #戻
      elif myKey[1][8]==ii  : pass #Filter(L2)
      elif myKey[1][9]==ii  : myPush( Keycode.N ) ; MODE = Fltxx( MODE ) #次
      elif myKey[1][10]==ii : pass #ALL(R2)

  
  # Allxx(R2+a)
  if GPIO[ myKey[1][10] ].fell: FlagAll = True	#R2押でフラフ立てる
  if GPIO[ myKey[1][10] ].rose: FlagAll = False	#R2戻でフラフ下ろす
  if FlagAll==True and GPIO[ myKey[1][4] ].fell : Allxx( 0 ) #All△
  if FlagAll==True and GPIO[ myKey[1][5] ].fell : Allxx( 1 ) #All〇
  if FlagAll==True and GPIO[ myKey[1][6] ].fell : Allxx( 2 ) #All×
  # if FlagAll==True and GPIO[ myKey[1][ ] ].fell : Allxx( 3 ) #All--
  if FlagAll==True and GPIO[ myKey[1][8] ].fell : MODE = Fltxx( 4 ) #Filter解除


  # FilterXX(L2+a)
  if GPIO[ myKey[1][8] ].fell: FlagFlt = True	#L2押でフラフ立てる
  if GPIO[ myKey[1][8] ].rose: FlagFlt = False	#L2戻でフラフ下ろす
  if FlagFlt==True and GPIO[ myKey[1][4] ].fell  : MODE = Fltxx( 0 ) #Filter△
  if FlagFlt==True and GPIO[ myKey[1][5] ].fell  : MODE = Fltxx( 1 ) #Filter〇
  if FlagFlt==True and GPIO[ myKey[1][6] ].fell  : MODE = Fltxx( 2 ) #Filter×
  #if FlagFlt==True and GPIO[ myKey[1][--] ].fell : MODE = Fltxx( 3 ) #Filter--
  if FlagFlt==True and GPIO[ myKey[1][10] ].fell : MODE = Fltxx( 4 ) #Filter解除
