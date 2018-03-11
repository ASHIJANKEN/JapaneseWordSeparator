# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sublime
import sublime_plugin
from tinysegmenter_python import segment
import re

# We can't detect a mouse release event, so we use "pressing" "to detect it.
# "pressing" is True when we press the button, and "pressing" is False when we release the button.
pressing = False
point_hover = 0

jp_pattern = u'[一-龠々〆ヵヶぁ-んァ-ヴｱ-ﾝﾞ]'
reg = re.compile(jp_pattern)

# This class detects mouse move while dragging.
# It finds the closest point in the view to the mouse location, then expands a region you selecting now.
class MouseMoveListener(sublime_plugin.EventListener):
  # find the point
  def on_hover(self, view, point, hover_zone):
    global point_hover
    point_hover = point
    print("point : {}".format(point))

    if pressing == True:
      self.expand_region(view, point)

  def expand_region(self, view, point):
    regions = [r for r in view.sel()]
    # print(regions)

    new_canditate = view.word(point)
    new_seg = find_seg_en_jp(view, new_canditate, point)

    if(regions[-1].begin() <= new_seg.end()):
      new_region = sublime.Region(regions[-1].begin(), new_seg.end())
    else:
      new_region = sublime.Region(new_seg.begin(), regions[-1].end())

    regions[-1] = new_region
    view.sel().clear()
    view.sel().add_all(regions)
    view.add_regions("override", view.sel())

# Find a region
class DragSelectJp(sublime_plugin.TextCommand):
  def run(self, edit, additive=False, subtractive=False):
    global pressing
    pressing = True

    point = self.view.sel()[-1].b

    if additive == False:
      self.view.sel().clear()

    # sleect a word using API
    # With this way, we can use "word_separators" in "Preferences.sublime-settings."
    canditate_region = self.view.word(point)
    # print("({}) ({})".format(canditate_region.a, canditate_region.b))

    point_seg = find_seg_en_jp(self.view, canditate_region, point)

    self.view.sel().add(point_seg)

class Released(sublime_plugin.TextCommand):
  def run(self, edit):
    global pressing
    pressing = False


def find_seg_en_jp(view, canditate_region, point):

  canditate_str = view.substr(canditate_region)

  # If there aren't any Japanese words
  if not reg.search(canditate_str):
    return canditate_region

  # Fing a segment using tinysegmenter from the Japanese sentence.
  segs = segment(canditate_str)

  # If canditate_region contain only one word
  if len(segs) == 1:
    return canditate_region

  sum_chars = 0
  for seg in segs:
    print(seg)
    sum_chars += len(seg)
    if sum_chars >= point - canditate_region.begin():
      point_seg = sublime.Region((sum_chars - len(seg)) + canditate_region.begin(), canditate_region.begin() + sum_chars)
      # print("({}) ({})".format((sum_chars - len(seg)) + canditate_region.a, point - canditate_region.a + sum_chars))
      return point_seg