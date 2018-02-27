import sublime
import sublime_plugin


#TextCommandクラスよりもこっちが先に呼び出される
class JapaneseDragSelectCommand(sublime_plugin.EventListener):
  def on_text_command(self, view, command_name, args):
    if command_name == "drag_select_jp":
      print("drag_select_called")
      # view.run_command("drag_select", {"by": "words"})

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
    print(self.view.sel()[0])
    point = self.view.sel()[0].b
    self.view.sel().clear()
    region = sublime.Region(point - 1, point + 3)
    self.view.sel().add(region)
    print(self.view.sel()[0])