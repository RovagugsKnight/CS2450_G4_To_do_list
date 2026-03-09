from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from views.inputs import InputFrame
from views.scrollable_list import ScrollableList
from views.task_widget import TaskItem
from models.sqllite_repository import SqliteRepo
from controller.task_controller import TaskController
from controller.main_window_controller import main_window_controller
from controller.grid_layout import normalize_grid
from views.spacer import Spacer

class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.controller = TaskController()

        self.true_controller = main_window_controller(SqliteRepo())

        todo_list_container = BoxLayout(
            orientation="vertical",
            size_hint=(0.90, 0.90),
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
        tasks = self.true_controller.load_tasks()
        for task in reversed(tasks):
            widget = TaskItem(self, task.task_id, task.task_name, task.text, task.done)
            self.todoitems.add_widget(widget)

        # pad with invisible spacers
        normalize_grid(self.todoitems, 3)


    def add_todo_item(self, task_name, text):
        
        result = self.true_controller.add_task(task_name, text)
        if not result.success:
            self.show_popup(result.error)
        
        else:
            task_id = result.task_id
            widget = TaskItem(self, task_id, task_name, text)

            last_row = self.todoitems.children[:self.todoitems.cols]

            # Remove spacers
            for child in reversed(last_row):
                if isinstance(child, Spacer):
                    self.todoitems.remove_widget(child)
                    
            self.todoitems.add_widget(widget)

            self.inputframe.ids.task_name.text = ""
            self.inputframe.ids.description.text = ""

            # add spacers if needed
            normalize_grid(self.todoitems, 3)

    def delete_todo_item(self, item_id):
        self.controller.delete_task(item_id)
        self.scrollablelist.remove_item(item_id)

    def mark_todo_item_done(self, item_id):
        self.controller.mark_done(item_id)

    
