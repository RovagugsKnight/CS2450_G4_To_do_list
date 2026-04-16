from models.category import Category
from models.theme_preference import save_theme_style
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
from views.main_window.submenu_view import (
    open_view_submenu,
    open_manage_categories_submenu,
)

from models.task_repository import TaskRepository
from models.category_list import CategoryList
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import (
    CategoryController,
    DEFAULT_CATEGORY_NAME,
    DONE_CATEGORY_NAME,
    is_system_category_name,
)
from controller.result import Result
from views.deadline_selector import DeadlineSelector
from views.category_creator import CategoryCreator
from views.task_widget import TaskItem

import sqlite3

from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.app import App
from kivymd.uix.label import MDLabel

from views.main_window.nav_menu_helpers import (
    DEFAULT_MENU_ROW_HALF_HEIGHT_DP,
    ESTIMATED_MENU_WIDTH_DP,
    FALLBACK_MANAGE_ROW_OFFSET_FROM_BTN_BOTTOM_DP,
    FALLBACK_VIEW_ROW_OFFSET_FROM_BTN_BOTTOM_DP,
    MANAGE_ROW_CENTER_FROM_BOTTOM_DP,
    MIN_NAV_HEIGHT_FOR_ANCHOR_DP,
    NAV_SUBMENU_ANCHOR_HEIGHT_DP,
    NAV_SUBMENU_ANCHOR_WIDTH_DP,
    RIGHT_EDGE_FRACTION,
)


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
            self.refresh_ui()

        elif name == "Task View":
            build_kanban_board(self)

    def load_existing_tasks(self):
        try:
            tasks = self.controller.load_tasks()
            populate_task_lists(self, tasks)
        except (sqlite3.Error, IndexError, TypeError, ValueError) as e:
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
            ln = c.name.lower()
            if ln == DEFAULT_CATEGORY_NAME.lower():
                return (0, ln)
            if ln == DONE_CATEGORY_NAME.lower():
                return (1, ln)
            return (2, ln)

        self.categories = sorted(categories, key=sort_key)

    def show_error(self, message):
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        Popup(
            title="Error",
            content=MDLabel(
                text=message,
                theme_text_color="Custom",
                text_color=(0.92, 0.92, 0.92, 1) if is_dark else (0.1, 0.1, 0.1, 1),
            ),
            size_hint=(0.6, 0.3),
            background="",
            background_color=(0.14, 0.14, 0.14, 1) if is_dark else (0.98, 0.98, 0.98, 1),
        ).open()

    def open_deadline_for_field(self, field):
        def _set_date(date_str):
            field.text = date_str
        DeadlineSelector(_set_date).open()

    def update_dashboard(self):
        """Delegate to the dashboard view function."""
        dashboard_update(self)

    # --- Category manager (popup) ---

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
            if isinstance(result, Result) and not result.success:
                self.show_error(result.error)
                return

            popup.dismiss()

            self.refresh_ui(reload_categories=True, refresh_category_popup=True)

        creator.submit_button.unbind(on_release=creator.end_creation)
        creator.submit_button.bind(on_release=save_changes)

        popup.content = creator
        popup.open()

    def delete_category(self, category):
        if is_system_category_name(category.name):
            return

        # 1. Reassign tasks
        self.task_controller.reassign_tasks_from_category(category.id)

        # 2. Delete category
        result = self.cat_controller.delete_category(category.id)
        if not result.success:
            self.show_error(result.error)
            return

        self.refresh_ui(reload_categories=True, refresh_category_popup=True)

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

    def _ensure_nav_submenu_anchor(self) -> Widget:
        """Invisible Window child used as MDDropdownMenu caller for cascade alignment."""
        w = getattr(self, "_nav_submenu_anchor_widget", None)
        if w is None:
            self._nav_submenu_anchor_widget = Widget(
                size=(dp(NAV_SUBMENU_ANCHOR_WIDTH_DP), dp(NAV_SUBMENU_ANCHOR_HEIGHT_DP)),
                opacity=0,
                size_hint=(None, None),
            )
            Window.add_widget(self._nav_submenu_anchor_widget)
        return self._nav_submenu_anchor_widget

    def _ensure_nav_menu_open_for_submenu(self) -> None:
        """Tap can dismiss the main menu before the cascade runs; reopen for layout."""
        nav = getattr(self, "nav_menu", None)
        if nav is not None and nav.parent is None:
            nav.open()

    def _nav_submenu_anchor_fallback_xy(self, kind: str):
        """Estimate window coords when the main menu is unavailable."""
        root = App.get_running_app().root
        nb = root.ids.nav_button
        ncx, btn_bottom_y = nb.to_window(nb.width * 0.5, 0)
        menu_w = float(dp(ESTIMATED_MENU_WIDTH_DP))
        wx = ncx + RIGHT_EDGE_FRACTION * menu_w
        if kind == "view":
            wy = btn_bottom_y - dp(FALLBACK_VIEW_ROW_OFFSET_FROM_BTN_BOTTOM_DP)
        else:
            wy = btn_bottom_y - dp(FALLBACK_MANAGE_ROW_OFFSET_FROM_BTN_BOTTOM_DP)
        return wx, wy

    def nav_submenu_anchor_caller(self, kind: str) -> Widget:
        """
        Place an invisible Window child so ``MDDropdownMenu``'s caller center matches the
        chevron row. Uses ``nav_menu``'s ``x``/``y``/``width``/``height`` (it is a
        ``Window`` child when open) instead of ``inner.to_window``, which can mis-map
        for recycle/menu content.
        """
        self._ensure_nav_menu_open_for_submenu()
        anchor = self._ensure_nav_submenu_anchor()
        nav = getattr(self, "nav_menu", None)
        wx, wy = None, None
        if nav is not None and nav.parent is not None and nav.height > dp(MIN_NAV_HEIGHT_FOR_ANCHOR_DP):
            ax = nav.x + nav.width * RIGHT_EDGE_FRACTION
            if kind == "view":
                ay = nav.y + nav.height - dp(DEFAULT_MENU_ROW_HALF_HEIGHT_DP)
            else:
                ay = nav.y + dp(MANAGE_ROW_CENTER_FROM_BOTTOM_DP)
            wx, wy = ax, ay
        if wx is None:
            wx, wy = self._nav_submenu_anchor_fallback_xy(kind)
        anchor.pos = (wx - anchor.width * 0.5, wy - anchor.height * 0.5)
        return anchor

    def dismiss_all_menus(self):
        """Close nav and any open cascading dropdown menus."""
        for attr in ("manage_categories_submenu", "view_submenu", "nav_menu"):
            menu = getattr(self, attr, None)
            dismiss = getattr(menu, "dismiss", None) if menu is not None else None
            if callable(dismiss):
                dismiss()

    def nav_submenu_switch_view(self, name: str):
        """Used from cascade submenus: apply choice and close all menus."""
        self.dismiss_all_menus()
        self.switch_view(name)

    def nav_submenu_open_category_creator(self):
        self.dismiss_all_menus()
        self.open_category_creator(source="nav")

    def nav_submenu_open_category_manager(self):
        self.dismiss_all_menus()
        self.open_category_manager()

    def _reopen_nav_menu_if_dismissed(self, dt):
        """After opening a submenu, reopen main nav only if KivyMD dismissed it."""
        nav = getattr(self, "nav_menu", None)
        if nav is not None and nav.parent is None:
            nav.open()

    def toggle_theme(self):
        app = App.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"

        save_theme_style(app.theme_cls.theme_style)

        if hasattr(self, "nav_menu"):
            self.nav_menu.dismiss()
        self.build_nav_menu()
        if self.ids.screen_manager.current == "Task View":
            self.refresh_kanban()

    def refresh_ui(self, reload_categories=False, refresh_category_popup=False):
        """
        Centralized post-action UI refresh to keep screens in sync.
        """
        if reload_categories:
            self.load_categories()

        self.load_existing_tasks()
        self.update_dashboard()
        self.refresh_kanban()

        if refresh_category_popup and self.category_popup:
            self.category_popup.refresh()

    # --- Delegated UI actions (module functions bound as methods) ---

    open_add_dialog = open_add_dialog
    set_add_category = set_add_category
    submit_add_task = submit_add_task
    open_edit_dialog = open_edit_dialog
    set_edit_category = set_edit_category
    submit_edit_task = submit_edit_task
    open_nav_menu = open_nav_menu
    build_nav_menu = build_nav_menu
    open_view_submenu = open_view_submenu
    open_manage_categories_submenu = open_manage_categories_submenu
