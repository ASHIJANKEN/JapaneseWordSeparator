# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from .tinysegmenter_python import segment
import re

# We can't detect a mouse release event, so we use "pressing" "to detect it.
# "pressing" is True when we press the button, and "pressing" is False when we release the button.
pressing = False
point_hover = 0
start_region = sublime.Region(0, 0)

jp_pattern = u'[一-龠々〆ヵヶぁ-んァ-ヴｱ-ﾝﾞ]'
reg = re.compile(jp_pattern)

# This class detects mouse move while dragging.
# It finds the closest point in the view to the mouse location, then expands a region you selecting now.
class MouseMoveListener(sublime_plugin.EventListener):
  # find the point
  def on_hover(self, view, point, hover_zone):
    global point_hover
    point_hover = point
    # print("point : {}".format(point))
    # print("pressing : {}".format(pressing))

    if pressing == True:
      self.expand_region(view, point)

  def expand_region(self, view, point):
    # Use list comprehension to convert regions from a sel object into an array.
    regions = [r for r in view.sel()]

    new_canditate = view.word(point)
    new_seg = find_seg_en_jp(view, new_canditate, point)

    if regions[-1].end() < new_seg.end():
      new_region = sublime.Region(start_region.begin(), new_seg.end())
    elif new_seg.begin() < regions[-1].begin():
      new_region = sublime.Region(new_seg.begin(), start_region.end())
    elif regions[-1].begin() < new_seg.end() < regions[-1].end():
      if start_region.begin() < new_seg.begin():
        new_region = sublime.Region(start_region.begin(), new_seg.end())
      else:
        new_region = sublime.Region(new_seg.begin(), start_region.end())
    elif new_seg.begin() == regions[-1].begin() or new_seg.end() == regions[-1].end():
      new_region = start_region

    regions[-1] = new_region
    view.sel().clear()
    view.sel().add_all(regions)
    view.add_regions("override", view.sel())

# Find a region
class DragSelectJp(sublime_plugin.TextCommand):
  def run(self, edit, additive=False, subtractive=False):
    global pressing, start_region
    pressing = True

    point = self.view.sel()[-1].b

    if additive == False:
      self.view.sel().clear()

    # Select a word using API
    # With this way, we can use "word_separators" in "Preferences.sublime-settings."
    canditate_region = self.view.word(point)
    point_seg = find_seg_en_jp(self.view, canditate_region, point)
    start_region = point_seg
    self.view.sel().add(point_seg)

# Find region, move cursor by arrow keys.
class KeySelectJp(sublime_plugin.TextCommand):
  def run(self, edit, additive=False, subtractive=False, key='none'):

    # Handle every caret one at a time.
    regions = [r for r in self.view.sel()]
    for index, region in enumerate(regions):

      # Move mouse cursor
      if key == 'left':
        tmp_cursor_pos = max(region.b - 1, 0)
      elif key == 'right':
        tmp_cursor_pos = min(region.b + 1, self.view.size())

      # Sleect a word using API
      # With this way, we can use "word_separators" in "Preferences.sublime-settings."
      canditate_region = self.view.word(tmp_cursor_pos)

      point_seg = find_seg_en_jp(self.view, canditate_region, tmp_cursor_pos)

      # if aditive is true, expand/shrink selected regions.
      if additive == True:

        if key == 'left':
          region.b -= abs(point_seg.a - region.b)
        elif key == 'right':
          region.b += abs(point_seg.b - region.b)

      # Set cursor position to edge of a new region
      else:

        if key == 'left':
          regions[index] = sublime.Region(point_seg.a, point_seg.a)
        elif key == 'right':
          regions[index] = sublime.Region(point_seg.b, point_seg.b)

    # Clear and reset regions
    self.view.sel().clear()
    self.view.sel().add_all(regions)
    self.view.add_regions("override", self.view.sel())

# This is called when a mouse button is released.
class Released(sublime_plugin.TextCommand):
  def run(self, edit):
    global pressing
    pressing = False

# This method finds a segment which cursor position is within, and return it.
def find_seg_en_jp(view, canditate_region, point):

  canditate_str = view.substr(canditate_region)

  # If there aren't any Japanese words
  if not reg.search(canditate_str):
    return canditate_region

  # Fing segments using tinysegmenter from the Japanese sentence.
  segs = segment(canditate_str)

  # If canditate_region contain only one word
  if len(segs) == 1:
    return canditate_region

  # find a segment
  sum_chars = 0
  for seg in segs:
    # print(seg)
    sum_chars += len(seg)
    if sum_chars >= point - canditate_region.begin():
      point_seg = sublime.Region((sum_chars - len(seg)) + canditate_region.begin(), canditate_region.begin() + sum_chars)
      return point_seg