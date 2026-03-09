from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from views.buttons import YellowButton
from kivy.lang import Builder

Builder.load_file("views/Input.kv")

class InputFrame(MDBoxLayout):
    """Input boxes for task name and description with button
    to add task."""
    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)
        self.main_window = main_window
    
    def add_task(self) -> None:
        """Sends name and description to main window"""
        name = self.ids.task_name.text
        desc = self.ids.description.text
        self.main_window.add_todo_item(name, desc)