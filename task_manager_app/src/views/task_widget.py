from kivymd.uix.boxlayout import MDBoxLayout
from views.buttons import YellowButton, LightTealButton
from kivymd.uix.card import MDCard
from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from controller.task_controller import TaskController

Builder.load_file("views/task_widget.kv")

class TaskItem(MDBoxLayout):
    done = BooleanProperty(False)
    task_name = StringProperty(" ")
    description = StringProperty(" ")
    def __init__(self, main_window, controller:TaskController, item_id:int, task_name:str, description:str, done=False, **kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id
        self.main_window = main_window
        self.done = done
        self.task_name = task_name
        self.description = description
        self.controller = controller
  
    
    def mark_done(self):
        self.controller.mark_done(self.item_id)
        self.done = True
    
    def remove(self):
        self.main_window.delete_todo_item(self.item_id)

    def edit_task(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        input_box = TextInput(text=self.description, multiline=False)
        layout.add_widget(input_box)

        save_button = YellowButton(text="Save")
        layout.add_widget(save_button)

        popup = Popup(title="Edit Task", content=layout, size_hint=(0.8, 0.4))

        def save_changes(instance):
            new_text = input_box.text.strip()
            if new_text:
                self.main_window.controller.update_task(self.item_id, new_text)
                self.description = new_text
            popup.dismiss()

        save_button.bind(on_release=save_changes)
        popup.open()
