'''
2022年8月20日
■■■ ABC-Z専用の入力キーボード　for PS用コントローラ(アナログなし動作確認) ■■■
  プレステのコントローラを採点ソフトABC用にチューニング
  〇、△、☓、次の問題、前の問題、十字キーだけでなく、一括やフィルタにも対応
  ※アナログなしモデルでもフルカラーLEDの点灯が見えないため、それに関わるソースをコメントアウトしている
  

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
   L2   |    ----    |   全表示   |



■使用条件
・外部ディスプレイ使用していて、以下の2項目が該当している場合、想定している動作にならないため、ディスプレイ配置(ディスプレイ設定)を変更すること！
  ➀外部モニタが主モニタの左側に配置
  ➁外部モニタ上端が主モニタ上端よりも上部に配置
  (理由)マウスの位置決めを行う際に、マウスを強制的に斜め左45°に移動させ、そこを基準座標としている。

 
■RGB(フルカラー)LEDについて
  ※コントローラ筐体でLEDが見えないため、関係プログラムはコメントアウト
      [フルカラーLED]で検索
  [単色(変更なし)にしたい場合]
  以下()内のRRGGBBを変更することで、各256段階のため約1677万色表現できる(明るさ別、黒は消灯で再現)
  設定方法は、134行目付近の
    RGBLED.fill( colorwheel( ( time.monotonic()*15 )%255 ) )
    #RGBLED.fill( 0xRRGGBB )
  を
    #RGBLED.fill( colorwheel( ( time.monotonic()*15 )%255 ) )
    RGBLED.fil( 0xRRGGBB )
  と行先頭の「#」を書き換える。ここで、
    RR(赤) : 00, 01, ・・・, 09, 0A, 0B, ・・・, 0f, 10, ・・・, ff の256段階
    GG(緑) : 同上
    BB(青) : 同上
  と 00 から ff までの16進数のため、 RRGGBB の前に 0x (ゼロエックス)を付ける必要がある。
    例)
      赤 : 0xff0000
      紫 : 0xff00ff
'''


# パラメータ ####################################################################
NumTAB = 34         #MailSkip時のShift+TABキーを押す回数　【注意】学校や所属、部署などによって回数が異なる場合あり
NumSKIPMAIL = 5     #未使用(SkipMailで使用)   MailSkip時に一度に既読にするメール数
ExDsply = 1.0      #未使用(SkipMailで使用)   学習系の拡大@ディスプレイ設定(default : 100%=1.0, 125%=1.25, 150%=1.5)
MYDELAY = 0.1       #遅延時間[秒]　※特に問題なければ触る必要なし！
#################################################################################

import time       #for sleep
import board      #for #GP
import usb_hid    #for hid
import digitalio  #set gpio
from adafruit_hid.keyboard import Keyboard  #HIDのキーボード
from adafruit_hid.keycode import Keycode    #HIDのキー宣言
from adafruit_hid.mouse   import Mouse      #HIDのマウス
from adafruit_debouncer import Debouncer    #GPIOの設定で必要なヤツ
# import neopixel   #フルカラーLED

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
  if   FLAG==0 : mus.move( 366, 38, 0 ) #ALLｘ
  elif FLAG==1 : mus.move( 278, 38, 0 ) #All○
  elif FLAG==2 : mus.move( 322, 38, 0 ) #ALL△
  elif FLAG==3 : mus.move( 410, 38, 0 ) #ALL--
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )
  myPush( Keycode.TAB )



''' Filter '''
def Fltxx( FLAG ) :
  MoveOrigin( )                     #原点復帰
  if   FLAG==0 : mus.move( 323, 76, 0 ) ; nn = 7  #Filterｘ
  elif FLAG==1 : mus.move( 297, 76, 0 ) ; nn = 9  #Filter○
  elif FLAG==2 : mus.move( 310, 76, 0 ) ; nn = 8  #Filter△
  elif FLAG==3 : mus.move( 336, 76, 0 ) ; nn = 6  #Filter未
  elif FLAG==4 : mus.move( 285, 76, 0 ) ; nn = 10 #FilterCancel
  mus.click( Mouse.LEFT_BUTTON )    #右クリ
  myPush( Keycode.ENTER )
  for ii in range( nn ):
    myPush( Keycode.TAB ) #TABを押離	※自然な挙動用(カーソル移動)
    


''' KxxSの通知回答に既読をつけるヤツ '''
def SkipMail(  ):
  MoveOrigin(  )  # マウスを左上(基準)に移動

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


''' 任意キーを押して放すヤツ '''
def myPush( key ):
  kbd.press( key )        #ボタンを押す
  time.sleep( 1*MYDELAY ) #適当な表示待ち
  kbd.release( key )      #押したら戻す



''' NeoPixを虹色に変化させるヤツ(本家ライブラリから抽出) '''
"""
#フルカラーLED
def colorwheel( pos ):
  if pos < 0 or pos > 255: return (0), (0), (0)
  if pos < 85:             return (255-pos*3), (pos*3), (0)
  if pos < 170:
      pos -= 85
      return (0), (255-pos*3), (pos*3)
  pos -= 170
  return (pos*3), (0), (255-pos*3)
"""



''' ボタンの割り当て '''
#  ii in Loop : 0         1         2         3         4         5         6         7         8         9         10  
#         ABC : 左        下        右        上        ✕        〇        △        戻        Filter    次        ALL
#         BTN : 左        下        右        上        ✕        〇        △        L1        L2        R1        R2
myKey = ( board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7, board.D8, board.D9, board.D10 )


''' SW用GPIOの初期設定(プルアップ) '''
GPIO =  []  #空リスト(≒配列)定義
for ii in myKey : #ボタンの数で繰り返し
  tmp = digitalio.DigitalInOut( ii )  #GPIO(ii)を使用
  tmp.pull = digitalio.Pull.UP        #プルアップで使用
  GPIO.append( Debouncer( tmp ) )     #リスト(GPIO)にリスト登録(追加)


''' NeoPix(RGB-LED)の設定 '''
"""
#フルカラーLED
NeoPwr = digitalio.DigitalInOut( board.NEOPIXEL_POWER )   #NeoPix Power
NeoPwr.direction = digitalio.Direction.OUTPUT   #動作モード：出力
NeoPwr.value = True #動作スタート
RGBLED = neopixel.NeoPixel( board.NEOPIXEL, 1, brightness=0.08 ) #NeoPix Date, LED数, 明るさ
"""



''' Main Loop '''
FlagAll = False		#R2の状態　※ブロック用
FlagFlt = False		#L2の状態
while True:
  for ii in range( len( GPIO ) ): #ボタンの数で繰り返し　
    # RGBLED.fill( colorwheel( ( time.monotonic()*15 )%255 ) ) #NeoPixを時間で虹色に変化 #フルカラーLED
    # RGBLED.fill( 0xFF00FF ) #単色 #フルカラーLED

    GPIO[ii].update() #スイッチ状態アップデート
    if GPIO[ii].fell and FlagAll==False and FlagFlt==False: #ボタン「押」 ※フラグはブロック
      if   ii==0  : myPush( Keycode.LEFT_ARROW )  #左
      elif ii==1  : myPush( Keycode.DOWN_ARROW )  #下
      elif ii==2  : myPush( Keycode.RIGHT_ARROW ) #右
      elif ii==3  : myPush( Keycode.UP_ARROW )    #上
      elif ii==4  : myPush( Keycode.X )  #✕
      elif ii==5  : myPush( Keycode.Z )  #〇
      elif ii==6  : myPush( Keycode.C )  #△
      elif ii==7  : myPush( Keycode.P )  #戻
      # elif ii==8  : #Filter(L2)
      elif ii==9  : myPush( Keycode.N )  #次
      # elif ii==10 : #ALL(R2)
  
  
  # Allxx(R2+a)
  if GPIO[10].fell: FlagAll = True	#R2押でフラフ立てる
  if GPIO[10].rose: FlagAll = False	#R2戻でフラフ下ろす
  if FlagAll==True and GPIO[4].fell: Allxx( 0 ) #All×
  if FlagAll==True and GPIO[5].fell: Allxx( 1 ) #All〇
  if FlagAll==True and GPIO[6].fell: Allxx( 2 ) #All△


  #SkipMail(R2+下)
  if GPIO[10].fell and GPIO[1].fell :SkipMail(  ) 


  # FilterXX(L2+a)
  if GPIO[8].fell: FlagFlt = True	#L2押でフラフ立てる
  if GPIO[8].rose: FlagFlt = False	#L2戻でフラフ下ろす
  if FlagFlt==True and GPIO[4].fell  : Fltxx( 0 ) #Filter×
  if FlagFlt==True and GPIO[5].fell  : Fltxx( 1 ) #Filter〇
  if FlagFlt==True and GPIO[6].fell  : Fltxx( 2 ) #Filter△
  if FlagFlt==True and GPIO[10].fell : Fltxx( 4 ) #Filter解除
  
