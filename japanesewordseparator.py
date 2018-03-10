# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sublime
import sublime_plugin
from tinysegmenter_python import segment
import re

#TextCommandクラスよりもこっちが先に呼び出される
class JapaneseDragSelectCommand(sublime_plugin.EventListener):
  def on_text_command(self, view, command_name, args):
    if command_name == "drag_select_jp":
      print("drag_select_called")
      view.run_command("drag_select", {"by": "words"})

      # self.view.sel().clear()
      # print(view.sel()[0])
      # point = view.sel()[0].b
      # view.sel().clear()
      # region = sublime.Region(point - 1, point + 1)
      # view.sel().add(region)
      # print(view.sel()[0])
      # self.view.sel().add([region])
    elif command_name == "drag_select_additive_jp":
      print("drag_select_additive_called")
    elif command_name == "drag_select_subtractive_jp":
      print("drag_select_subtractive_called")
      # expand_by_class(point, classes, <separators>) 
      print(view.substr(self.view.sel()[0]))
      # self.view.insert(edit, 0, self.view.sel())

class DragSelectJp(sublime_plugin.TextCommand):
  def run(self, edit):
    point = self.view.sel()[0].b
    self.view.sel().clear()

    # STの機能で単語選択
    canditate_region = self.view.word(point)
    canditate_str = self.view.substr(canditate_region)

    # 選択範囲に日本語がなければregionの確定
    if not re.search(u'[一-龠々〆ヵヶぁ-んァ-ヴｱ-ﾝﾞ]', canditate_str):
      self.view.sel().add(canditate_region)
      return

    # 日本語があったらsegmenterをsegmentを見つける
    segs = segment(canditate_str)
    # print(segs)
    if len(segs) == 1:
      self.view.sel().add(canditate_region)
      return
    sum_chars = 0
    for seg in segs:
      print(seg)
      sum_chars += len(seg)
      if sum_chars >= point - canditate_region.a:
        point_seg = sublime.Region((sum_chars - len(seg)) + canditate_region.a, canditate_region.a + sum_chars)
        # print("({}) ({})".format((sum_chars - len(seg)) + canditate_region.a, point - canditate_region.a + sum_chars))
        break

    self.view.sel().add(point_seg)
