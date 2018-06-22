# JapaneseWordSeparator
Sublime Text 3における日本語の単語選択機能を強化するプラグイン。

現在のSublime Textでは、日本語の単語を選択しようとダブルクリックしても、文章全部が選択されてしまったり、段落全てが丸々選択されてしまったりします。
一応「Preferences.sublime-settings」にて「word_separator」という値をいじることで、分割単位をある程度小さくすることはできますが、単語レベルでの分割はやはりできません。

このプラグインは、その単語レベルでの分割を可能にします。

# 使い方
基本的には、今まで通り**選択したい単語の上でダブルクリックする**だけです。
![JapaneseWordSeparatorの動作例](http://ashija.net/img/JapaneseWordSeparator_demo.gif "JapaneseWordSeparatorの動作例")

注意点として、**ダブルクリック後にドラッグして選択範囲を拡張したい場合、動作に遅延が生じます。**
GIFを見て分かる通り、任意の場所までポインタを移動させたらマウスを静止させ、選択範囲が拡張するまで待つ必要があります。
これは、Sublime TextのAPIにマウスの動きを追随してくれるようなメソッドがなく、代わりにon_hoverという、マウスがホバーした時に呼び出されるメソッドを用いているためです。
> Called when the user's mouse hovers over a view for a short period.
> [API Reference – Sublime Text 3 Documentation](http://www.sublimetext.com/docs/3/api_reference.html#sublime_plugin.EventListener)

マウス操作だけでなく、キーボードでの範囲選択にも対応しています。

| 入力 　　　　　　　　　　　　　　　　　|　　　　　　　 機能 　　　　　　　|
|:-----------|------------:|
| **Ctrl+左右の矢印キー**       | 単語レベルでのカーソル移動 |
| **Ctrl+Shift+左右の矢印キー** | 単語レベルでの範囲選択 |

## インストール方法
### Gitからインストール
[Preferences]>[Browse Packages...]で出てきたフォルダにこのリポジトリをクローンしてください。
```bash
$ git clone https://github.com/ASHIJANKEN/JapaneseWordSeparator.git
```
これだけでインストールは完了です。

### Package Controlからインストール
1. Command Palleteを開く(**Ctrl/Cmd+Shift+P**)。
1. `Package Controll: Install Package`を選択。
1. `JapaneseWordSeparator`と検索してインストール。これで完了です。

Package ControlはSublime Text用プラグインの管理ツールです("apt-get"のSublime Text版みたいなもの)。インストールしていない場合は[ここ](https://packagecontrol.io/installation)からインストールしてください。

## 確認できている不具合など
- Find Resultsページにおいて、ダブルクリックで当該箇所にジャンプできない。
- ~~最初に選択した単語より前に選択範囲を拡張していく場合、正常に動作しない。選択範囲を広く取りすぎたから少し縮めよう、と思ってマウスの位置を戻しても拡張されっぱなしになる。
(最初に選択した単語より後ろに選択範囲を拡張していく場合は正常に動作する)~~(2018/04/22修正)

- ctrl+ダブルクリックで選択範囲を追加する時、ctrlを押したままでは追加した選択範囲の拡張ができない。
ctrl+ダブルクリックで選択範囲を追加した後、ctrlを離してドラッグするとうまくいく。
ctrlを押したままではon_hoverが呼び出されないらしい。
- alt+ダブルクリックでの選択範囲を縮める動作が実装されていない。
(自分の動作環境ではalt+ダブルクリックしても何も起こらず、正しい動作がどのようなものなのか確認できなかったので未実装。確認でき次第実装予定。)
