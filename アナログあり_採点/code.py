'''
2022年12月09日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ ■■■
  採点ソフトABC用にチューニングしたコントローラで、〇、△、☓、次の問題、前の問題、十字キーだけでなく、一括〇などにも対応している。


■動作と対応ボタン
[シングル]
    ボタン   |     機能     
------------------------------
  上下左右   |   そのまま ※アナログ左
  〇×△□   |   そのまま
     L1      |   戻
     R1      |   次
   Select    |   機能なし
   Start     |   通知回答Skip


[コンビネーション] ※L2/R2を先に押す！
        |     L2     |     R2     |
-----------------------------------
   ○   |   一括〇   |   〇のみ   |
   ☓   |   一括×   |   ×のみ   |
   △   |   一括△   |   △のみ   |
   □   |   一括未   |   未のみ   |
   L2   |    ----    |   全表示   |



■使用条件
・外部ディスプレイ使用していて、以下の2項目が該当している場合、想定している動作にならないため、ディスプレイ配置(ディスプレイ設定)を変更すること！
  ➀外部モニタが主モニタの左側に配置
  ➁外部モニタ上端が主モニタ上端よりも上部に配置
  (理由)マウスの位置決めを行う際に、マウスを強制的に斜め左45°に移動させ、そこを基準座標としている。

 
■RGB(フルカラー)LEDについて
  動作モードのインジゲータとして使用しており、
      起動     : 青点滅
      通常     : 白
      All      : 赤
      Filter   : 緑
      通知回答 : 紫     に点灯する。
    
  プログラム中の色指定は、
    赤 : 00, 01, ・・・, 09, 0A, 0B, ・・・, 0F, 10, ・・・, FF の256段階
    緑 : 同上
    青 : 同上
  で3原色を赤緑青の順で16進数で指定するため
    0xFF0000 : 赤100%のみ
    0xFF00FF : 赤100%+青100%=紫
  となる。なお、数値先頭の0x (ゼロエックス)は16進数であることを示している。
'''


# パラメータ #####################################################################
NumTAB = 34         #MailSkip時のShift+TABキーを押す回数
NumSKIPMAIL = 5     #未使用(SkipMailで使用)   MailSkip時に一度に既読にするメール数
ExDsply = 1.0       #未使用(SkipMailで使用)   学習系の拡大@ディスプレイ設定(default : 100%=1.0, 150%=1.5)
MYDELAY = 0.0       #遅延時間[秒]　※特に問題なければ触る必要なし！
MYSHIFT = 0         #フィルターボタン位置の右方向への移動(左方向は負にする)
ANALOG = 60         #アナログ入力の動作しきい値(大:大きく倒して反応  小:僅かな傾きで反応　※理論値：0 <= ANALOG <= 127 )
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio(Digital)
import analogio   #set gpio(Anallog)
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ
import neopixel   #フルカラーLED

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
  elif FLAG==3 : mus.move( 410, 38, 0 ) #ALL□
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )
  myPush( Keycode.TAB )



''' Filter '''
def Fltxx( FLAG ) :

  if ( FLAG == MODE[1] ) and ( FLAG == 4 ) :
    pass  #初期設定 & 変更なし :なにもしない
  else: 
    MoveOrigin( )                     #原点復帰
    if   FLAG==0 : mus.move( 338 + MYSHIFT, 76, 0 ) ; nn = 8  #Filter△
    elif FLAG==1 : mus.move( 325 + MYSHIFT, 76, 0 ) ; nn = 9  #Filter○
    elif FLAG==2 : mus.move( 351 + MYSHIFT, 76, 0 ) ; nn = 7  #Filterｘ
    elif FLAG==3 : mus.move( 364 + MYSHIFT, 76, 0 ) ; nn = 6  #Filter□
    elif FLAG==4 : mus.move( 312 + MYSHIFT, 76, 0 ) ; nn = 10 #FilterCancel
    elif FLAG==9 : return
    mus.click( Mouse.LEFT_BUTTON )    #右クリ
    myPush( Keycode.ENTER )
    for ii in range( nn ):
      myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)

  MODE[1] = FLAG  #過去状態の更新
  return FLAG



''' KICSの通知回答に既読をつけるヤツ '''
def SkipMail(  ):
  #SkipMail
  RGBLED.fill( 0xFF00FF ) #紫
  
  # マウスを左上(基準)に移動
  MoveOrigin(  )

  ### [通知回答] ###
  if   ExDsply==1.00 : mus.move( 305, 75, 0 )  #移動
  elif ExDsply==1.25 : mus.move( 250, 62, 0 )
  elif ExDsply==1.50 : mus.move( 216, 55, 0 )

  time.sleep( 1*MYDELAY )             #適当な時間待ち  
  mus.click( Mouse.LEFT_BUTTON )      #右クリ
  time.sleep( 30*MYDELAY )            #適当な時間待ち

  ### メール ###
  if   ExDsply==1.00 : mus.move( -110, 155, 0 )  #移動
  elif ExDsply==1.25 : mus.move(  -85, 118, 0 )
  elif ExDsply==1.50 : mus.move(  -70,  95, 0 )
  time.sleep( 5*MYDELAY )             #適当な時間待ち
  for ii in range( NumSKIPMAIL ):     #NumSKIPMAIL通のメールを既読に！
    mus.click( Mouse.LEFT_BUTTON )    #メール表示
    time.sleep( 30*MYDELAY )          #適当な時間待ち

    ### [既読]ボタンへ移動 ###
    kbd.press( Keycode.LEFT_SHIFT )   #逆方向にフォーカス移動のため
    for jj in range( NumTAB ) :       #TABキーでカーソル移動する回数
      myPush( Keycode.TAB )    
    kbd.release( Keycode.LEFT_SHIFT ) #押したら戻す

    ### [既読]ボタン ###
    myPush( Keycode.ENTER )

    ### [ok]ボタン ###
    myPush( Keycode.ENTER )
    time.sleep( 20*MYDELAY )          #適当な表示待ち
  
  #通常モード色
  if MODE[0]==4 : RGBLED.fill( 0xFFFFFF ) #白
  else          : RGBLED.fill( 0x00FF00 ) #緑


''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 0*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' ボタンの割り当て読み込み '''
myKey = [ [ board.A0, board.A1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 ],
          [] ]  #空リスト
myFile = open ( 'CodeTable.txt', 'r' )  #ファイルを読み込みモードで開く
DataList = myFile.readlines() #各行ごとに読み込み
for ii in range( len(DataList) ) :  #読み込んだ行数で繰り返し
  myKey[1] += [ int( DataList[ ii ][ DataList[ii].find(',')+1: ].strip() ) ]  #コンマ以降の文字を抽出(空白削除、テキスト→数値化)
myFile.close()  #ファイルを閉じる



''' SW用GPIOの初期設定(Digital=プルアップ, Analog=初期値) '''
GPIO =  []          #空リスト(≒配列)定義
Axis = [ 0, 0 ]     #アナログ軸の値
AxisInit = [ 0, 0 ] #アナログ軸の初期値
for idx, ii in enumerate( myKey[1] ): #ボタンの数で繰り返し
  if ii>1: #デジタル入力のみの設定
    tmp = digitalio.DigitalInOut( myKey[0][ii] )  #GPIO(ii)を使用
    tmp.pull = digitalio.Pull.UP        #プルアップで使用
    GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)
  else:
    if ii == 0: Axis[0] = analogio.AnalogIn( myKey[0][ii] ) #X軸
    else:       Axis[1] = analogio.AnalogIn( myKey[0][ii] ) #Y軸
    tmp = 0
    for jj in range( 100 ): tmp = tmp + Axis[ii].value // 255 #アナログ信号を1/255で取得
    AxisInit[ii] = tmp // 100  #初期値の読み込み(1000回平均値)



''' NeoPix(RGB-LED)の設定 '''
#フルカラーLED
NeoPwr = digitalio.DigitalInOut( board.NEOPIXEL_POWER )   #NeoPix Power
NeoPwr.direction = digitalio.Direction.OUTPUT   #動作モード：出力
NeoPwr.value = True #動作スタート
RGBLED = neopixel.NeoPixel( board.NEOPIXEL, 1, brightness=1.0 ) #NeoPix Date, LED数, 明るさ



''' Main Loop '''
FlagAll = False
FlagFlt = False
FlagAlg = False
MODE = [ 4, -1 ] #Filter解除
for ii in range( 3 ):
  RGBLED.fill( 0x0000FF ) #青：起動中
  time.sleep( 1*MYDELAY )
  RGBLED.fill( 0x000000 ) #黒：点滅用
  time.sleep( 1*MYDELAY )

RGBLED.fill( 0xFFFFFF ) #白：通常
while True:
  
  #アナログ入力の処理
  if FlagAlg==False:  #傾いている時の処理
    #X軸
    if   (Axis[0].value // 255 - AxisInit[0] ) > +1 * ANALOG : myPush( Keycode.LEFT_ARROW )  ; FlagAlg = True
    elif (Axis[0].value // 255 - AxisInit[0] ) < -1 * ANALOG : myPush( Keycode.RIGHT_ARROW ) ; FlagAlg = True
    #Y軸
    if   (Axis[1].value // 255 - AxisInit[1] ) > +1 * ANALOG : myPush( Keycode.UP_ARROW )   ; FlagAlg = True
    elif (Axis[1].value // 255 - AxisInit[1] ) < -1 * ANALOG : myPush( Keycode.DOWN_ARROW ) ; FlagAlg = True
  else:  #傾きが足りない時の処理
    if ( abs( Axis[0].value //255 - AxisInit[0] ) < ANALOG // 2  ) and \
       ( abs( Axis[1].value //255 - AxisInit[1] ) < ANALOG // 2  ) :FlagAlg = False


  #デジタル入力の処理
  for ii in  range( len( GPIO ) ) : #ボタンの数で繰り返し 
    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell and FlagAll==False and FlagFlt==False: #ボタン「押」 ※フラグはブロック
      if   ii==0 : myPush( Keycode.C )  #△
      elif ii==1 : myPush( Keycode.Z )  #〇
      elif ii==2 : myPush( Keycode.X )  #✕
      elif ii==3 : pass                 #□ 
      elif ii==4 : myPush( Keycode.P ) ; MODE[0] = Fltxx( MODE[0] ) #戻
      elif ii==5 : pass #Filter(L2)
      elif ii==6 : myPush( Keycode.N ) ; MODE[0] = Fltxx( MODE[0] ) #次
      elif ii==7 : pass #ALL(R2)
      elif ii==8 : SkipMail #as you like
    
  # Allxx(R2+a)
  if GPIO[ 7 ].fell: FlagAll = True   ; RGBLED.fill( 0xFF0000 ) #赤：Allモード
  if GPIO[ 7 ].rose: FlagAll = False  ; RGBLED.fill( 0xFFFFFF )
  if FlagAll==True and GPIO[ 0 ].fell : Allxx( 0 ) #All△
  if FlagAll==True and GPIO[ 1 ].fell : Allxx( 1 ) #All〇
  if FlagAll==True and GPIO[ 2 ].fell : Allxx( 2 ) #All×
  if FlagAll==True and GPIO[ 3 ].fell : Allxx( 3 ) #All□
  if FlagAll==True and GPIO[ 5 ].fell : MODE[0] = Fltxx( 4 ) #Filter解除
 

  # FilterXX(L2+a)
  if GPIO[ 5 ].fell: FlagFlt = True   ; RGBLED.fill( 0x00FF00 ) #緑：Filterモード
  if GPIO[ 5 ].rose: FlagFlt = False  ; RGBLED.fill( 0xFFFFFF )
  if FlagFlt==True and GPIO[ 0 ].fell : MODE[0] = Fltxx( 0 ) #Filter△
  if FlagFlt==True and GPIO[ 1 ].fell : MODE[0] = Fltxx( 1 ) #Filter〇
  if FlagFlt==True and GPIO[ 2 ].fell : MODE[0] = Fltxx( 2 ) #Filter×
  if FlagFlt==True and GPIO[ 3 ].fell : MODE[0] = Fltxx( 3 ) #Filter□
  if FlagFlt==True and GPIO[ 7 ].fell : MODE[0] = Fltxx( 4 ) #Filter解除
  if MODE[0] != 4 : RGBLED.fill( 0x00FF00 )  #Filter解除以外(何かしらFilterモード)であれば、緑
