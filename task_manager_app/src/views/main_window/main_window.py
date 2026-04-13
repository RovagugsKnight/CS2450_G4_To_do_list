from dataclasses import field

from views.main_window.dashboard_view import update_dashboard
from views.main_window.kanban_view import build_kanban_board
from views.main_window.category_view import ManageCategoriesPopup
from views.main_window.task_dialogs import (
    open_add_dialog,
    set_add_category,
    submit_add_task,
    open_edit_dialog,
    set_edit_category,
    submit_edit_task,
)
from views.main_window.menu_view import build_nav_menu, open_nav_menu
from views.main_window.submenu_view import open_view_submenu

from models.task_repository import TaskRepository
from models.category_list import CategoryList
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import CategoryController
from views.deadline_selector import DeadlineSelector
from views.category_creator import CategoryCreator
from views.task_widget import TaskItem

from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel


class MainWindow(MDScreen):
    """
    MAIN WINDOW — clean and minimal.
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
            self.build_nav_menu()
        ), 0)

    def switch_view(self, name):
        self.ids.screen_manager.current = name

        if name == "Dashboard":
            self.load_existing_tasks()
            update_dashboard(self)

        if name == "Task View":
            build_kanban_board(self)

    def load_existing_tasks(self):
        try:
            tasks = self.controller.load_tasks()

            if "task_list" in self.ids:
                self.ids.task_list.clear_widgets()

            if "dashboard_task_list" in self.ids:
                self.ids.dashboard_task_list.clear_widgets()

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

    def open_deadline_for_field(self, field):
        def _set_date(date_str):
            field.text = date_str
        DeadlineSelector(_set_date).open()

    #
    # CATEGORY MANAGER (POPUP)
    #

    def open_category_manager(self):
        popup = ManageCategoriesPopup(self)
        popup.open()

    def open_edit_category(self, category):
        popup = Popup(
            title=f"Edit Category: {category.name}",
            size_hint=(0.9, 0.6),
        )

        creator = CategoryCreator(
            mainwindow=self,
            source="edit",
            popup=popup,
        )

        creator.ids.cat_name.text = category.name
        creator.col_selector._select_color(category.color)

        def save_changes(*args):
            new_name = creator.ids.cat_name.text.strip()
            new_color = creator.col_selector.get_selected_color_key()

            self.cat_controller.update_category(category.id, new_name, new_color)
            popup.dismiss()
            self.refresh_kanban()

        creator.submit_button.unbind(on_release=creator.end_creation)
        creator.submit_button.bind(on_release=save_changes)

        popup.content = creator
        popup.open()

    def delete_category(self, category):
        if category.name.lower() in ("todo", "done"):
            return

        self.task_controller.reassign_tasks_from_category(category.id)
        self.cat_controller.delete_category(category.id)
        self.refresh_kanban()

    def open_category_creator(self, source="nav"):
        """Open the CategoryCreator popup for creating a new category."""
        popup = Popup(
            title="Create Category",
            size_hint=(0.9, 0.6),
        )

        creator = CategoryCreator(
            mainwindow=self,
            source=source,
            popup=popup,
        )

        popup.content = creator
        popup.open()

    def refresh_kanban(self):
        build_kanban_board(self)

    #
    # DELEGATED UI ACTIONS
    #

    open_add_dialog = open_add_dialog
    set_add_category = set_add_category
    submit_add_task = submit_add_task
    open_edit_dialog = open_edit_dialog
    set_edit_category = set_edit_category
    submit_edit_task = submit_edit_task
    open_nav_menu = open_nav_menu
    build_nav_menu = build_nav_menu
    open_view_submenu = open_view_submenu
    update_dashboard = update_dashboard
    build_kanban_board = build_kanban_board