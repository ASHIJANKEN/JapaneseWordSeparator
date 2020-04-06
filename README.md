# JapaneseWordSeparator
Sublime Text 3における日本語の単語選択機能を強化するプラグイン。

現在のSublime Textでは、日本語の単語を選択しようとダブルクリックしても、文章全部が選択されてしまったり、段落全てが丸々選択されてしまったりします。
一応「Preferences.sublime-settings」にて「word_separator」という値をいじることで、分割単位をある程度小さくすることはできますが、単語レベルでの分割はやはりできません。

このプラグインは、その単語レベルでの分割を可能にします。

## 使い方
基本的には、今まで通り**選択したい単語の上でダブルクリックする**だけです。
![JapaneseWordSeparatorの動作例](http://ashija.net/img/JapaneseWordSeparator_demo.gif "JapaneseWordSeparatorの動作例")

注意点として、**ダブルクリック後にドラッグして選択範囲を拡張したい場合、動作に遅延が生じます。**
GIFを見て分かる通り、任意の場所までポインタを移動させたらマウスを静止させ、選択範囲が拡張するまで待つ必要があります。
これは、Sublime TextのAPIにマウスの動きを追随してくれるようなメソッドがなく、代わりにon_hoverという、マウスがホバーした時に呼び出されるメソッドを用いているためです。
> Called when the user's mouse hovers over a view for a short period.
> [API Reference – Sublime Text 3 Documentation](http://www.sublimetext.com/docs/3/api_reference.html#sublime_plugin.EventListener)

マウス操作だけでなく、キーボードでの範囲選択にも対応しています。

### Windows/Linux

| 入力 　　　　　　　　　　　　　　　　　|　　　　　　　 機能 　　　　　　　|
|:-----------|------------:|
| **Ctrl+左右の矢印キー**       | 単語レベルでのカーソル移動 |
| **Ctrl+Shift+左右の矢印キー** | 単語レベルでの範囲選択 |

### OSX

| 入力 　　　　　　　　　　　　　　　　　|　　　　　　　 機能 　　　　　　　|
|:-----------|------------:|
| **Alt+左右の矢印キー**       | 単語レベルでのカーソル移動 |
| **Alt+Shift+左右の矢印キー** | 単語レベルでの範囲選択 |

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
