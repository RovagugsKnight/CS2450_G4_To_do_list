from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from views.inputs import InputFrame
from views.scrollable_list import ScrollableList
from views.task_widget import TaskItem
from models.task_repository import TaskRepository
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from views.grid_layout import normalize_grid
from views.spacer import Spacer
from models.category_list import CategoryList
from models.category import Category
from controller.category_controller import CategoryController

class MainWindow(FloatLayout):
    """Main window veiw. Has a title, input box, and scrollable list of tasks"""
    def __init__(self, repo: TaskRepository, catlist: CategoryList,**kwargs):
        super().__init__(**kwargs)
        #task repo
        self.repo = repo
        #category list
        self.catlist = catlist
        #controllers
        self.controller = MainWindowController(self.repo)
        self.task_controller = TaskController(self.repo)
        self.cat_controller = CategoryController(self.catlist)

        #task list container
        todo_list_container = BoxLayout(
            orientation="vertical",
            size_hint=(0.90, 0.90),
            height=350,
            pos_hint={"center_x": 0.5, "top": 0.85},
            spacing=10
        )

        #Title label
        title_label = Label(
            font_size=35,
            text="[b]Todo App[/b]",
            size_hint=(1, None),
            markup=True
        )

        #task input
        self.inputframe = InputFrame(self)
        #scrollable task list
        self.scrollablelist = ScrollableList()
        #task list tasks
        self.todoitems = self.scrollablelist.todoitems

        todo_list_container.add_widget(title_label)
        todo_list_container.add_widget(self.inputframe)
        todo_list_container.add_widget(self.scrollablelist)

        self.add_widget(todo_list_container)

        #load tasks from data base
        self.load_existing_tasks()

    def show_popup(self, message):
        """Creates popup for errors"""
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def load_existing_tasks(self) -> None:
        """Controller grabs tasks from db which are used
         to create taskitem widgets. Widgets are added
         to task list and spaced with spacer widgets."""
        try:
            tasks = self.controller.load_tasks()
            for task in reversed(tasks):
                cat = self.cat_controller.get_category(task.catid)
                widget = TaskItem(self, self.task_controller, task.task_id, task.task_name, task.text, cat, task.done)
                self.todoitems.add_widget(widget)

            # pad with invisible spacers
            normalize_grid(self.todoitems, 3)
        except ValueError as e:
            self.show_popup(e.value)

    def add_todo_item(self, task_name: str, text: str, category: Category) -> None:
        """task input is sent to controller to check and add to db.
        New task widget is added to task list and evenly spaced with
        spacer widgets."""
        result = self.controller.add_task(task_name, text)
        if not result.success:
            self.show_popup(result.error)
        
        else:
            task_id = result.return_val
            widget = TaskItem(self, self.task_controller, task_id, task_name, text, category)

            #grab last row
            last_row = self.todoitems.children[:self.todoitems.cols]

            # Remove spacers
            for child in reversed(last_row):
                if isinstance(child, Spacer):
                    self.todoitems.remove_widget(child)
            
            #add widget
            self.todoitems.add_widget(widget)

            #clear input frame
            self.inputframe.ids.task_name.text = ""
            self.inputframe.ids.description.text = ""

            # add spacers if needed
            normalize_grid(self.todoitems, 3)

    def remove_task_widget(self, item_id: int) -> None:
        """Task widget is removed from task list"""
        self.scrollablelist.remove_item(item_id)


    
