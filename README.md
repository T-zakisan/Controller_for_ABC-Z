# Controller for ABC-Z
ABC-Zをゲーム機のコントローラで使用するためのソースコード(CircuitPython)を配布、解説

# 準備
## Seeed XIAO PR2040 を入手
以下の販売店等から入手しておくこと！
- [SWITCHSCIENCE](https://www.switch-science.com/catalog/7634/)
- [秋月電子通称](https://akizukidenshi.com/catalog/g/gM-17044/)
- [マルツオンライン](https://www.marutsu.co.jp/pc/i/2229736/)
　

## ファームウェアを入手とインストール
 [WebSiteの説明](https://wiki.seeedstudio.com/XIAO-RP2040-with-CircuitPython/)
- google翻訳を活用すると良い
- ファームウェア(.uf2)は、[CircuitPython本家](https://circuitpython.org/board/seeeduino_xiao_rp2040/)から入手
- "Step4(ステップ4)"までで良い
- Seeed XIAO PR2040 が "CIRCUITPY"と表示されたらok
　

## ライブラリの入手とインストール　
1. [CircuitPython本家のライブラリ配布場所](https://circuitpython.org/libraries)の下図からライブラリをダウンロード

![image](https://user-images.githubusercontent.com/43605763/185802350-7a6c4999-844f-4b76-9860-59f934375b84.png)

2. ダウンロードしたライブラリを解凍
下図のディレクトリとファイルが生成される。

![image](https://user-images.githubusercontent.com/43605763/185802707-b66e42cc-9f02-4a70-8974-5c61c6941ead.png)

3. ***/lib*** から以下のディレクトリとファイルをディレクトリ***lib***に抽出(コピー)しておく
  - [dir] adafruit_hid ※ディレクトリ丸ごと
  - [file] adafruit_debouncer.mpy
  - [file] adafruit_pixelbuf.mpy
  - [file] adafruit_pypixelbuf.py
  - [file] adafruit_ticks.mpy
  - [file] neopixel.mpy

![image](https://user-images.githubusercontent.com/43605763/185802888-962c7d67-b286-45b4-8abc-6b16a9cc2b04.png)


4. 3のディレクトリ ***/lib*** を ***CIRCUITPY*** の直下に放り込む

# ソースコードの入手とインストール
***CIRCUITPY***に必要に応じた***code.py***()をドラッグ＆ドロップする
