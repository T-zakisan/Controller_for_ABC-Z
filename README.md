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


![image](https://user-images.githubusercontent.com/43605763/208617930-e2527756-ff21-485f-a371-8c3d41a6aba6.png)



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
1. 上記の***Code▼*** をクリック
2. ***Download ZIP*** をクリック

![image](https://user-images.githubusercontent.com/43605763/186346284-155919a4-edf8-4373-bf9f-97778d5a4871.png)

3. ダウンロードしたzipファイルを解凍


## インストール
以下、コントローラが ***アナログなし*** であることを想定して説明する。


### 設定ファイル用のソースコード書き込み

**ソースコードの入手とインストール** で解凍したディレクトリ内の`アナログなし_初期設定/` の



- **code.py**
- **CodeTable.txt**
 
を`CIRCUITPY`にドラッグ＆ドロップする


### 設定ファイル出力
各ボタンとSeeed XIAO RP2040 の端子の接続関係をテキスト出力し、初期設定ファイル（CodeTable.txt）を完成させる。

ボタンと端子間の接続の個体差をこの設定ファイルで吸収できる。

また、簡易的であるが動作確認にもなる。


1. **CodeTable.txt** をメモ帳で開く
2. カーソルを **,(カンマ)** の右側に移動
3. 表記通りのボタンを押して、数字が入力されていることを確認
4. 上書き保存して、終了

※もし数字が出力されなければ、物理的あるいは電気的な接続不良を疑う

![image](https://user-images.githubusercontent.com/43605763/191004226-fe6582ee-8994-4adc-a3c8-10d8aae47128.png)




### 採点用ソースコードの書き込み
**ソースコードの入手とインストール** で解凍したディレクトリ内の `アナログなし_採点/` の
- **code.py**
 
を`CIRCUITPY`にドラッグ＆ドロップする



# 既知の対象コントローラ
プレステにこだわっているわけではないが、
- 安定した持ちやすさ（30年間基本形状に変更がない理由とは）
- ボタンの表記（慣れたらなんでもよいかもしれないが、、、）
- 初期型を今でも使える品質の良さ
- 歴史がタマ数と相関がある

などからここではPSシリーズを記載。

ちなみに、 ***可能*** となっているモノは、専用基板があるため、数日中の納品が可能となっている。

下表の型番は下図左下、可能/不可能の文字は、下図右型の刻印を示す。

![image](https://user-images.githubusercontent.com/43605763/208640654-2430f79a-6930-4b08-bae1-1c9bb8c2eebc.png)


|  | 型番 | 可能 | 不可 | 備考 |
|:---:|:---:|:---|:---|:---|
| アナログなし | SCPH-1010 | 無印, A, H, M, F | ? | いわゆるPS1 |
| ↑ | SCPH-1080 | 無印, A, H, M | ？ | ↑ |
| ↑ | SCPH-1000R | △ | ？ | 時間を要する |
| アナログ | SCPH-1150 | A | ？ | 別刻印については不明 |
| DUALSHOCK | SCPH-1200 | 無印, A, H | M | --- |
| DUALSHOCK2 | SCPH-10010 | なし | 全て | --- |
| ↑ | DESR-10 | ？ | ？ | --- |
| DUALSHOCK3 | CECH-ZC2J | 可能性あり | ？ | 基板構想中 |
| SIXAXIS| CECH-ZC1J | なし | 全て | --- |
| DUALSHOCK4 | CUH-ZCT1J | ？ | ？ | --- |
| ↑ | CUH-ZCT2J | ？ | ？ | --- |
| DualSense | CFI-ZCT1J | ？ | ？ | --- |


以上


