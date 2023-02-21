'''
2023年2月21日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログなし動作確認) ■■■
  プレステのコントローラを採点ソフトABC用にチューニング
  〇、△、☓、次の問題、前の問題、十字キーだけでなく、一括やフィルタにも対応
  解答欄の拡大/縮小機能を追加（2023/02/03）
  
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
   L2   |    ----    |   全表示   | フィルター解除
   上   |    ----    |   拡大x1   |
   下   |    ----    |   縮小x1   |
   右   |    ----    |   拡大x5   |
   左   |    ----    |   縮小x5   |


■使用条件
・「マウスポインタの速度」が「10(デフォルト)」
・ディスプレイの拡大を100%（デスクトップ上で右クリック > ディスプレイ設定 > 拡大と縮小 : 100%）
・外部ディスプレイ使用していて、以下の2項目が該当している場合、想定している動作にならないため、ディスプレイ配置(ディスプレイ設定)を変更すること！
  ➀外部モニタが主モニタの左側に配置
  ➁外部モニタ上端が主モニタ上端よりも上部に配置
  (理由)マウスの位置決めを行う際に、マウスを強制的に斜め左45°に移動させ、そこを基準座標としている。
'''

# パラメータ ####################################################################
MYDELAY = 0.0       #遅延時間[秒]　※特に問題なければ触る必要なし！
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ
from myConf import posiall                  #ABC-Zのボタン[一括]位置の読み込み
from myConf import posifilter               #ABC-Zのボタン[フィルタ]位置の読み込み
from myConf import zoom                     #Zoom使用時のカーソル移動
from myConf import disply                   #ディスプレイサイズの読み込み


mus = Mouse(usb_hid.devices)          #マウス
kbd = Keyboard(usb_hid.devices)       #キーボード


''' 原点復帰 '''
  # 移動量を指数のカウントダウンとすることで少ない手数で基準座標(左上)に移動
  # 【注意】サブモニタを左上に設置は×
def MoveOrigin(  ):
  for ii in range( disply['Size'], 0, -1 ): mus.move( -2**ii, -2**ii, 0 ) # 2^11(=2048px) -> 2^0(=1px) で各移動量=全移動量(4097px:大画面にも対応であろう)



''' All '''
def Allxx( FLAG ) :
  MoveOrigin( ) #原点復帰
  if   FLAG==0 : mus.move( posiall['X.T'], posiall['Y'], 0 ) #ALL△
  elif FLAG==1 : mus.move( posiall['X.o'], posiall['Y'], 0 ) #All○
  elif FLAG==2 : mus.move( posiall['X.x'], posiall['Y'], 0 ) #ALLｘ
  elif FLAG==3 : mus.move( posiall['X.-'], posiall['Y'], 0 ) #ALL--
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )   #一括操作確認のポップアップ[はい/いいえ]を「はい」
  myPush( Keycode.TAB )     #解答欄にカーソルを戻す



''' Filter '''
def Fltxx( FLAG ) :
  MoveOrigin( ) #原点復帰
  if   FLAG==0 : mus.move( posifilter['X.T'], posifilter['Y'], 0 ) ; nn = 8  #Filter△
  elif FLAG==1 : mus.move( posifilter['X.o'], posifilter['Y'], 0 ) ; nn = 9  #Filter○
  elif FLAG==2 : mus.move( posifilter['X.x'], posifilter['Y'], 0 ) ; nn = 7  #Filterｘ
  elif FLAG==3 : mus.move( posifilter['X.-'], posifilter['Y'], 0 ) ; nn = 6  #Filter□
  elif FLAG==4 : mus.move( posifilter['X.C'], posifilter['Y'], 0 ) ; nn = 10 #FilterCancel
  elif FLAG==9 : return
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )
  for ii in range( nn ): myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)
  return FLAG



''' Zoom '''
def Zoom( FLAG ):
  #拡大/縮小のコントールにカーソル移動
  kbd.press( Keycode.SHIFT )
  for ii in range( zoom['Start'] ):  myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)
  kbd.release( Keycode.SHIFT )
  
  #拡大/縮小操作
  if   FLAG==0 : myPush( Keycode.UP_ARROW )   #1拡大
  elif FLAG==1 : myPush( Keycode.DOWN_ARROW ) #1縮小
  elif FLAG==2 :
    for ii in range( zoom['Repeat'] ) : myPush( Keycode.UP_ARROW )   #5拡大
  elif FLAG==3 :
    for ii in range( zoom['Repeat'] ) : myPush( Keycode.DOWN_ARROW ) #5縮小

  #カーソルを解答欄に戻す
  for ii in range( zoom['Return'] ): myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)



''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' コントローラのボタンをマイコン端子のアサイン（割り当て） '''
myKey = [ [ board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ], [] ]  #空リスト
myFile = open ( 'CodeTable.txt', 'r' )  #ファイルを読み込みモードで開く
DataList = myFile.readlines() #各行ごとに読み込み
for ii in range( len(DataList) ) : myKey[1] += [ int( DataList[ ii ][ DataList[ii].find(',')+1: ].strip() ) ]  #コンマ以降の文字を抽出(空白削除、テキスト→数値化)
myFile.close()  #ファイルを閉じる



''' SW用GPIOの初期設定(プルアップ) '''
GPIO =  []  #空リスト(≒配列)定義
for ii in myKey[0] : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
  GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)



''' Main Loop '''
FlagR2 = False		#R2の状態　※ブロック用
FlagL2 = False		#L2の状態
MODE = 4 #Filter解除
while True:
  for ii in range( len( GPIO ) ): #ボタンの数で繰り返し　

    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell and FlagR2==False and FlagL2==False: #ボタン「押」 ※フラグはブロック
      if   myKey[1][0]==ii  : myPush( Keycode.UP_ARROW )    #上
      elif myKey[1][1]==ii  : myPush( Keycode.LEFT_ARROW )  #左
      elif myKey[1][2]==ii  : myPush( Keycode.DOWN_ARROW )  #下
      elif myKey[1][3]==ii  : myPush( Keycode.RIGHT_ARROW ) #右
      elif myKey[1][4]==ii  : myPush( Keycode.C )           #△
      elif myKey[1][5]==ii  : myPush( Keycode.Z )           #〇
      elif myKey[1][6]==ii  : myPush( Keycode.X )           #✕
      elif myKey[1][7]==ii  : myPush( Keycode.P ) ; MODE = Fltxx( MODE ) #戻
      elif myKey[1][8]==ii  : pass #Filter(L2)
      elif myKey[1][9]==ii  : myPush( Keycode.N ) ; MODE = Fltxx( MODE ) #次
      elif myKey[1][10]==ii : pass #ALL(R2)

  
  # Allxx(R2+a)
  if GPIO[ myKey[1][10] ].fell: FlagR2 = True	#R2押でフラフ立てる
  if GPIO[ myKey[1][10] ].rose: FlagR2 = False	#R2戻でフラフ下ろす
  if FlagR2==True and GPIO[ myKey[1][4] ].fell : Allxx( 0 ) #All△
  if FlagR2==True and GPIO[ myKey[1][5] ].fell : Allxx( 1 ) #All〇
  if FlagR2==True and GPIO[ myKey[1][6] ].fell : Allxx( 2 ) #All×
  # if FlagR2==True and GPIO[ myKey[1][ ] ].fell : Allxx( 3 ) #All--
  if FlagR2==True and GPIO[ myKey[1][8] ].fell : MODE = Fltxx( 4 ) #Filter解除


  # Zoom(R2+十字キー)
  if FlagR2==True and GPIO[ myKey[1][0] ].fell : Zoom( 0 ) #拡大 x1
  if FlagR2==True and GPIO[ myKey[1][2] ].fell : Zoom( 1 ) #縮小 x1
  if FlagR2==True and GPIO[ myKey[1][3] ].fell : Zoom( 2 ) #拡大 x5
  if FlagR2==True and GPIO[ myKey[1][1] ].fell : Zoom( 3 ) #縮小 x5


  # FilterXX(L2+a)
  if GPIO[ myKey[1][8] ].fell: FlagL2 = True	#L2押でフラフ立てる
  if GPIO[ myKey[1][8] ].rose: FlagL2 = False	#L2戻でフラフ下ろす
  if FlagL2==True and GPIO[ myKey[1][4] ].fell  : MODE = Fltxx( 0 ) #Filter△
  if FlagL2==True and GPIO[ myKey[1][5] ].fell  : MODE = Fltxx( 1 ) #Filter〇
  if FlagL2==True and GPIO[ myKey[1][6] ].fell  : MODE = Fltxx( 2 ) #Filter×
  #if FlagL2==True and GPIO[ myKey[1][--] ].fell : MODE = Fltxx( 3 ) #Filter--
  if FlagL2==True and GPIO[ myKey[1][10] ].fell : MODE = Fltxx( 4 ) #Filter解除