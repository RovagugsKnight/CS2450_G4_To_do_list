from models.category import Category
from views.main_window.dashboard_view import update_dashboard as dashboard_update
from views.main_window.kanban_view import build_kanban_board, populate_task_lists
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
        self.category_popup = None  # track popup if open

        if self.repo and self.catlist:
            self.controller = MainWindowController(self.repo)
            self.task_controller = TaskController(self.repo)
            self.cat_controller = CategoryController(self.catlist)

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: (
            self.load_existing_tasks(),
            self.update_dashboard(),
            self.build_nav_menu()
        ), 0)

    def switch_view(self, name):
        self.ids.screen_manager.current = name

        if name == "Dashboard":
            self.load_existing_tasks()
            self.update_dashboard()

        elif name == "Task View":
            build_kanban_board(self)

    def load_existing_tasks(self):
        try:
            tasks = self.controller.load_tasks()
            populate_task_lists(self, tasks)
        except Exception as e:
            self.show_error(str(e))

    def load_categories(self):
        """
        Loads all categories from the database into self.categories.
        Ensures system categories appear first.
        """
        rows = self.catlist.load_categories()

        categories = []
        for row in rows:
            cat_id, name, color = row
            categories.append(Category(cat_id, name, color))

        def sort_key(c):
            if c.name.lower() == "todo":
                return (0, c.name.lower())
            if c.name.lower() == "done":
                return (1, c.name.lower())
            return (2, c.name.lower())

        self.categories = sorted(categories, key=sort_key)

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

    def update_dashboard(self):
        """Delegate to the dashboard view function."""
        dashboard_update(self)

    """
    CATEGORY MANAGER (POPUP)
    """

    def open_category_manager(self):
        popup = ManageCategoriesPopup(self)
        self.category_popup = popup
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

            if not new_name:
                self.show_error("Category name cannot be empty.")
                return

            if not new_color:
                self.show_error("Please select a color.")
                return

            # Auto-capitalize every word (but not all letters)
            new_name = " ".join(word.capitalize() for word in new_name.split())

            result = self.cat_controller.update_category(category.id, new_name, new_color)
            if hasattr(result, "success") and not result.success:
                self.show_error(result.error)
                return

            popup.dismiss()

            # Refresh categories, Kanban, and dashboard
            self.load_categories()
            self.refresh_kanban()
            self.update_dashboard()

            # Refresh category manager popup if open
            if self.category_popup:
                self.category_popup.refresh()

        creator.submit_button.unbind(on_release=creator.end_creation)
        creator.submit_button.bind(on_release=save_changes)

        popup.content = creator
        popup.open()

    def delete_category(self, category):
        if category.name.lower() in ("todo", "done"):
            return

        # 1. Reassign tasks
        self.task_controller.reassign_tasks_from_category(category.id)

        # 2. Delete category
        result = self.cat_controller.delete_category(category.id)
        if not result.success:
            self.show_error(result.error)
            return

        # 3. Refresh internal category list
        self.load_categories()

        # 4. Refresh Kanban
        self.refresh_kanban()

        # 5. Refresh dashboard
        self.update_dashboard()

        # 6. Refresh popup if open
        if self.category_popup:
            self.category_popup.refresh()

    def open_category_creator(self, source="nav"):
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

    """
    DELEGATED UI ACTIONS
    """

    open_add_dialog = open_add_dialog
    set_add_category = set_add_category
    submit_add_task = submit_add_task
    open_edit_dialog = open_edit_dialog
    set_edit_category = set_edit_category
    submit_edit_task = submit_edit_task
    open_nav_menu = open_nav_menu
    build_nav_menu = build_nav_menu
    open_view_submenu = open_view_submenu
