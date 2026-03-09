from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from views.buttons import YellowButton
from kivy.lang import Builder

Builder.load_file("views/box_layouts.kv")

class InputFrame(MDBoxLayout):

    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)
        self.main_window = main_window
    
    def add_task(self):
        name = self.ids.task_name.text
        print(name)
        desc = self.ids.description.text
        print(desc)
        self.main_window.add_todo_item(name, desc)