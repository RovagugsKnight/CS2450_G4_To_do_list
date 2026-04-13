from views.main_window.dashboard_view import update_dashboard
from views.main_window.kanban_view import build_kanban_board
from views.main_window.category_view import (
    populate_category_manager,
    open_category_manager,
    create_category,
)
from views.main_window.task_dialogs import (
    open_add_dialog,
    set_add_category,
    submit_add_task,
    open_edit_dialog,
    set_edit_category,
    submit_edit_task,
)

from models.task_repository import TaskRepository
from models.category_list import CategoryList
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import CategoryController

from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel

class MainWindow(MDScreen):
    """
    MAIN WINDOW — now clean and minimal.
    Handles:
        - screen switching
        - high-level orchestration
        - delegating to view modules
    """

    def __init__(self, repo: TaskRepository = None, catlist: CategoryList = None, **kwargs):
        super().__init__(**kwargs)

        self.repo = repo
        self.catlist = catlist

        if self.repo and self.catlist:
            self.controller = MainWindowController(self.repo)
            self.task_controller = TaskController(self.repo)
            self.cat_controller = CategoryController(self.catlist)

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: (
            self.load_existing_tasks(),
            update_dashboard(self),
        ), 0)

    def switch_view(self, name):
        self.ids.screen_manager.current = name

        if name == "Dashboard":
            self.load_existing_tasks()
            update_dashboard(self)

        if name == "Task View":
            build_kanban_board(self)

    def load_existing_tasks(self):
        """Existing logic stays — this is fine here."""
        try:
            tasks = self.controller.load_tasks()

            if "task_list" in self.ids:
                self.ids.task_list.clear_widgets()

            if "dashboard_task_list" in self.ids:
                self.ids.dashboard_task_list.clear_widgets()

            from views.task_widget import TaskItem
            from datetime import date, datetime

            today = date.today()

            for task in reversed(tasks):
                category = None
                if task.catid:
                    cat_result = self.cat_controller.get_category(task.catid)
                    category = cat_result.return_val

                task_widget = TaskItem(
                    main_window=self,
                    controller=self.task_controller,
                    item_id=task.task_id,
                    task_name=task.task_name,
                    description=task.text,
                    category=category,
                    cat_controller=self.cat_controller,
                    done=task.done,
                    deadline=task.deadline,
                )

                if "task_list" in self.ids:
                    self.ids.task_list.add_widget(task_widget)

                if task.deadline and "dashboard_task_list" in self.ids:
                    try:
                        d = datetime.strptime(task.deadline, "%m/%d/%Y").date()
                        if d == today:
                            self.ids.dashboard_task_list.add_widget(task_widget)
                    except Exception:
                        pass

        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        Popup(
            title="Error",
            content=MDLabel(text=message),
            size_hint=(0.6, 0.3),
        ).open()

    # Delegate UI actions to modules
    open_add_dialog = open_add_dialog
    open_edit_dialog = open_edit_dialog
    populate_category_manager = populate_category_manager
    open_category_manager = open_category_manager
    create_category = create_category
    # Attach modular functions to MainWindow so KV + main.py still work
    update_dashboard = update_dashboard
    build_kanban_board = build_kanban_board

    populate_category_manager = populate_category_manager
    open_category_manager = open_category_manager
    create_category = create_category

    open_add_dialog = open_add_dialog
    set_add_category = set_add_category
    submit_add_task = submit_add_task

    open_edit_dialog = open_edit_dialog
    set_edit_category = set_edit_category
    submit_edit_task = submit_edit_task
