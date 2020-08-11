# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from .tinysegmenter_python import segment
import re

# We can't detect a mouse release event, so we use "pressing" "to detect it.
# "pressing" is True when we press the button, and "pressing" is False when we release the button.
pressing = False
point_hover = 0
editing_region = sublime.Region(0, 0)

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

    if pressing is True:
      self.expand_region(view, point)

  def expand_region(self, view, point):
    global editing_region

    # Use list comprehension to convert regions from a sel object into an array.
    regions = [r for r in view.sel()]

    target_index = regions.index(editing_region)

    new_canditate = view.word(point)
    new_seg = find_seg_en_jp(view, new_canditate, point)

    if regions[target_index].end() < new_seg.end():
      new_region = sublime.Region(editing_region.begin(), new_seg.end())
    elif new_seg.begin() < regions[target_index].begin():
      new_region = sublime.Region(new_seg.begin(), editing_region.end())
    elif regions[target_index].begin() < new_seg.end() < regions[target_index].end():
      if editing_region.begin() < new_seg.begin():
        new_region = sublime.Region(editing_region.begin(), new_seg.end())
      else:
        new_region = sublime.Region(new_seg.begin(), editing_region.end())
    elif new_seg.begin() == regions[target_index].begin() or new_seg.end() == regions[target_index].end():
      new_region = editing_region

    regions[target_index] = new_region
    editing_region = new_region
    view.sel().clear()
    view.sel().add_all(regions)
    view.add_regions("override", view.sel())


# Find a region
class DragSelectJp(sublime_plugin.TextCommand):
  def run(self, edit, additive=False, subtractive=False):
    global pressing, start_region, firepoint

    global pressing, editing_region, firepoint

    # suppress in Find Result
    if self.view.name() == "Find Results" and (not additive) and (not subtractive):
      self.view.run_command("double_click_at_caret")
      return

    # safety check
    if firepoint is None:
      # print("firepoint is None! what's up?")
      return

    pressing = True

    if additive is False:
      self.view.sel().clear()

    # Select a word using API
    # With this way, we can use "word_separators" in "Preferences.sublime-settings."
    canditate_region = self.view.word(firepoint)
    point_seg = find_seg_en_jp(self.view, canditate_region, firepoint)
    editing_region = point_seg
    self.view.sel().add(point_seg)

    # safety lock
    firepoint = None


# Keeping text point on command fired, to global variable "firepoint"
class LastCaretListener(sublime_plugin.EventListener):
  def on_text_command(self, view, command_name, args):
    global firepoint
    if command_name == "drag_select_jp":
      firepoint = view.window_to_text((args["event"]["x"], args["event"]["y"]))


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

      # Select a word using API
      # With this way, we can use "word_separators" in "Preferences.sublime-settings."
      canditate_region = self.view.word(tmp_cursor_pos)

      point_seg = find_seg_en_jp(self.view, canditate_region, tmp_cursor_pos)

      # if additive is true, expand/shrink selected regions.
      if additive is True:

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
    sum_chars += len(seg)
    if sum_chars >= point - canditate_region.begin():
      point_seg = sublime.Region((sum_chars - len(seg)) + canditate_region.begin(), canditate_region.begin() + sum_chars)
      return point_seg


# Shooting a double-click at the caret position
class DoubleClickAtCaretCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        view = self.view
        window_offset = view.window_to_layout((0, 0))
        vectors = []
        for sel in view.sel():
            vector = view.text_to_layout(sel.begin())
            vectors.append((vector[0] - window_offset[0], vector[1] - window_offset[1]))
        for idx, vector in enumerate(vectors):
            view.run_command('drag_select', {'event': {'button': 1, 'count': 2, 'x': vector[0], 'y': vector[1]}, 'by': 'words', 'additive': idx > 0 or kwargs.get('additive', False)})
