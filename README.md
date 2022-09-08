# Controller for ABC-Z
定評のあるインターフェースを使って、採点ソフトABC-Zを使用することで、更に採点業務が快適に！！

一括機能やフィルター機能をマウスに持ち直すことなく操作可能。

そのため、目線がモニタから離れることがないため、操作効率が高まります。

※フィルター機能は、ボタンが特に小さく押しにくい！

※フィルター機能は、問題移動（次/前の問題）しても維持される（採点ミス確認時に重宝）

https://user-images.githubusercontent.com/43605763/186742775-77fb4bad-561c-4811-a063-ccfca45388b2.mp4



# 準備
## Seeed XIAO PR2040 を入手
以下の販売店等から入手しておくこと！
- [SWITCHSCIENCE](https://www.switch-science.com/catalog/7634/)
- [秋月電子通称](https://akizukidenshi.com/catalog/g/gM-17044/)
- [マルツオンライン](https://www.marutsu.co.jp/pc/i/2229736/)


## ファームウェアを入手とインストール
 [本家WebSiteの説明](https://wiki.seeedstudio.com/XIAO-RP2040-with-CircuitPython/)
- ファームウェア(.uf2)は、[CircuitPython本家](https://circuitpython.org/board/seeeduino_xiao_rp2040/)から入手
- 上記説明サイトの"LED Flash Tutorial"以降は不要
- PC上で、Seeed XIAO PR2040 が "CIRCUITPY"と表示されたらok


## ライブラリの入手とインストール　
1. [CircuitPython本家のライブラリ配布場所](https://circuitpython.org/libraries)アクセスし、下図からライブラリをダウンロード

![image](https://user-images.githubusercontent.com/43605763/185802350-7a6c4999-844f-4b76-9860-59f934375b84.png)

2. ダウンロードしたライブラリを解凍

下図のディレクトリとファイルが生成される。

![image](https://user-images.githubusercontent.com/43605763/185802707-b66e42cc-9f02-4a70-8974-5c61c6941ead.png)

3. パソコンにSeeed XAIO PR2040 を接続（***CIRCUITPY***が出現）し、直下に***lib***を作成（***CIRCUITPY/lib***）

4. 解凍した ***/lib*** から以下のディレクトリとファイルをSeeed XAIO PR2040（***CIRCUITPY/lib***）に貼り付け
  ※adafruit_hid はディレクトリ丸ごと
 
![image](https://user-images.githubusercontent.com/43605763/185802888-962c7d67-b286-45b4-8abc-6b16a9cc2b04.png)



# ソースコードの入手とインストール
## 入手
1. 上記の***Code▼***をクリック
2. ***Download ZIP***をクリック

![image](https://user-images.githubusercontent.com/43605763/186346284-155919a4-edf8-4373-bf9f-97778d5a4871.png)

3. ダウンロードしたzipファイルを解凍
4. 以下フォルダ内にそれぞれ***code.py***があるか念のため確認
 - アナログなし_動作確認
 - アナログなし_ABC-Z
 - アナログあり_動作確認
 - アナログなし_ABC-Z


## インストール
***CIRCUITPY***に必要に応じた***code.py***をドラッグ＆ドロップする

※事前に、各ボタンとSeeed XIAO PR2040 の端子をはんだ付けし、それに合わせてソースコードを調整すること！

![image](https://user-images.githubusercontent.com/43605763/186352581-a76f5442-3beb-4440-bfcb-bcfb411125ad.png)
