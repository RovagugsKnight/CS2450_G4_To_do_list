from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from views.inputs import InputFrame
from views.scrollable_list import ScrollableList
from views.task_widget import TaskItem
from controller.task_controller import TaskController


class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.controller = TaskController()

        todo_list_container = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, None),
            height=350,
            pos_hint={"center_x": 0.5, "top": 0.85},
            spacing=10
        )

        title_label = Label(
            font_size=35,
            text="[b]Todo App[/b]",
            size_hint=(1, None),
            markup=True
        )

        self.inputframe = InputFrame(self)
        self.scrollablelist = ScrollableList()
        self.todoitems = self.scrollablelist.todoitems

        todo_list_container.add_widget(title_label)
        todo_list_container.add_widget(self.inputframe)
        todo_list_container.add_widget(self.scrollablelist)

        self.add_widget(todo_list_container)

        self.load_existing_tasks()

    def show_popup(self, message):
        popup = Popup(
            title="Invalid Task",
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def load_existing_tasks(self):
        tasks = self.controller.load_tasks()
        for task in reversed(tasks):
            widget = TaskItem(self, task.id, task.text, task.done)
            self.todoitems.add_widget(widget)

    def add_todo_item(self, text):
        text = text.strip()

        # Empty check
        if not text:
            self.show_popup("Task cannot be empty.")
            return

        # Length check
        if len(text) > 150:
            self.show_popup("Task is too long. Maximum length is 150 characters.")
            return

        task_id = self.controller.add_task(text)
        widget = TaskItem(self, task_id, text)
        self.todoitems.add_widget(widget)

        self.inputframe.todo_input_widget.text = ""

    def delete_todo_item(self, item_id):
        self.controller.delete_task(item_id)

        for widget in list(self.todoitems.children):
            if widget.item_id == item_id:
                self.todoitems.remove_widget(widget)
                break

    def mark_as_done(self, item_id):
        self.controller.mark_done(item_id)

        for widget in self.todoitems.children:
            if widget.item_id == item_id:
                widget.mark_done_button.disabled = True
                break
    
