from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivymd.uix.button import MDIconButton      
from kivymd.uix.menu import MDDropdownMenu      

from views.inputs import InputFrame
from views.scrollable_list import ScrollableList
from views.task_widget import TaskItem
from models.task_repository import TaskRepository
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from views.grid_layout import normalize_grid
from views.spacer import Spacer

class MainWindow(FloatLayout):
    """Main window veiw. Has a title, input box, and scrollable list of tasks"""
    def __init__(self, repo:TaskRepository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo
        self.controller = MainWindowController(self.repo)
        self.task_controller = TaskController(self.repo)

        # --- HAMBURGER MENU SETUP ---
        # Create the button 
        self.hamburger_button = MDIconButton(
            icon="menu",
            pos_hint={"top": 0.98, "x": 0.02}
        )
        self.hamburger_button.bind(on_release=lambda x: self.menu.open())

        # Options inside the dropdown
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Create Category",
                "on_release": lambda x="Create Category": self.menu_click(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Edit Category",
                "on_release": lambda x="Edit Category": self.menu_click(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Remove Category",
                "on_release": lambda x="Remove Category": self.menu_click(x),
            }
        ]

        # 3. Create the actual dropdown menu
        self.menu = MDDropdownMenu(
            caller=self.hamburger_button,
            items=menu_items,
            width_mult=4,
        )

        # Add the button to the main window
        self.add_widget(self.hamburger_button)

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
        todo_list_container.add_widget(Widget(size_hint_y=None, height=30)) 
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

    def load_existing_tasks(self):
        """Controller grabs tasks from db which are used
         to create taskitem widgets. Widgets are added
         to task list and spaced with spacer widgets."""
        try:
            tasks = self.controller.load_tasks()
            for task in reversed(tasks):
                widget = TaskItem(self, self.task_controller, task.task_id, task.task_name, task.text, task.done, task.deadline)
                self.todoitems.add_widget(widget)

            normalize_grid(self.todoitems, 3)
        except Exception as e:
            self.show_popup(str(e))

    def add_todo_item(self, task_name, text, deadline):
        """task input is sent to controller to check and add to db.
        New task widget is added to task list and evenly spaced with
        spacer widgets."""
        result = self.controller.add_task(task_name, text, deadline)
        if not result.success:
            self.show_popup(result.error)
        
        else:
            task_id = result.task_id
            widget = TaskItem(self, self.task_controller, task_id, task_name, text, False, deadline)

            last_row = self.todoitems.children[:self.todoitems.cols]


            for child in reversed(last_row):
                if isinstance(child, Spacer):
                    self.todoitems.remove_widget(child)
            

            self.todoitems.add_widget(widget)
            self.inputframe.ids.task_name.text = ""
            self.inputframe.ids.description.text = ""
            self.inputframe.ids.deadline.text = ""
            normalize_grid(self.todoitems, 3)

    def remove_task_widget(self, item_id):
        """Task widget is removed from task list"""
        self.scrollablelist.remove_item(item_id)

    # Hamburger menu test function
    def menu_click(self, text_item):
        """Closes the menu and prints the clicked item to the terminal"""
        self.menu.dismiss()
        print(f"Hamburger Menu Clicked: {text_item}")