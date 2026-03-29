from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from views.buttons import YellowButton, LightTealButton
from kivymd.uix.card import MDCard
from kivy.properties import BooleanProperty, StringProperty, ColorProperty
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from controller.task_controller import TaskController
from models.category import Category
from views.colors import get_color

Builder.load_file("views/task_widget.kv")

class TaskItem(MDBoxLayout):
    """Task widget with card layout and done, delete, and edit buttons on the side"""
    done = BooleanProperty(False)
    task_name = StringProperty(" ")
    description = StringProperty(" ")
    color = ColorProperty(get_color('Light Teal'))
    deadline = StringProperty(" ")

    def __init__(self, main_window, controller:TaskController, item_id:int, task_name:str, description:str, category:Category,done=False, deadline:str="",**kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id
        self.main_window = main_window
        self.done = done
        self.task_name = task_name
        self.description = description
        self.deadline = deadline
        self.controller = controller
        self.cat_name = category.name
        self.color = get_color(category.color)
        self.cat_id = category.id

    def show_popup(self, message:str) -> None:
        """Creates popup for errors"""
        popup = Popup(
            title="Error",
            content=Label(text=str(message)),
            size_hint=(0.6, 0.3)
        )
        popup.open()
  
    def mark_done(self) -> None:
        """disables done button and tells controller 
        to mark task done"""
        result = self.controller.mark_done(self.item_id)
        if result.success:
            self.done = True
        else:
            self.show_popup(result.error)
    
    def remove(self) -> None:
        """tells main window to remove task widget and 
        tells controller to delete task from repository"""
        result = self.controller.delete_task(self.item_id)
        if result.success:
            self.main_window.remove_task_widget(self.item_id)
        else:
            self.show_popup(result.error)

    def edit_task(self) -> None:
        """Pulls up edit popup that lets user edit task name and description
        calls controller to update database info"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        task_box = TextInput(text=self.task_name, multiline=False)
        layout.add_widget(task_box)

        deadline_box = TextInput(text=self.deadline, multiline=False)
        layout.add_widget(deadline_box)

        input_box = TextInput(text=self.description, multiline=True)
        layout.add_widget(input_box)

        save_button = YellowButton(text="Save")
        layout.add_widget(save_button)

        popup = Popup(title="Edit Task", content=layout, size_hint=(0.8, 0.4))

        def save_changes(instance:Button) -> None:
            """Saves task to repository with controller.
            Shows popup on failure"""
            new_name = task_box.text.strip()
            new_text = input_box.text.strip()
            new_deadline = deadline_box.text.strip()

            if new_text and new_name:
                result = self.controller.update_task(self.item_id, new_name, new_text, new_deadline, self.color)
                if result.success:
                    self.task_name = new_name
                    self.description = new_text
                    self.deadline = new_deadline
                    popup.dismiss()
                else:
                    self.show_popup(result.error)
                    input_box.text = self.description
                    task_box.text = self.task_name
                    deadline_box.text = self.deadline

        save_button.bind(on_release=save_changes)
        popup.open()
