from kivymd.uix.screen import MDScreen
from kivy.logger import Logger

from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import CategoryController

from models.category import Category
from models.category_list import CategoryList
from models.task_repository import TaskRepository

from views.task_widget import TaskItem
from views.deadline_selector import DeadlineSelector
from views.dialogs import AddTaskContent, EditTaskContent
from views.category_creator import CategoryCreator

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.uix.popup import Popup

from datetime import date, datetime


class MainWindow(MDScreen):
    """
    MAIN WINDOW
    """

    def __init__(self, repo: TaskRepository = None, catlist: CategoryList = None, **kwargs):
        super().__init__(**kwargs)

        self.repo = repo
        self.catlist = catlist

        if self.repo and self.catlist:
            self.controller = MainWindowController(self.repo)
            self.task_controller = TaskController(self.repo)
            self.cat_controller = CategoryController(self.catlist)

    """
    UNIVERSAL DEADLINE PICKER
    """
    def open_deadline_for_field(self, field):
        def _set_date(date_str):
            field.text = date_str
        DeadlineSelector(_set_date).open()

    def _divider(self):
        return {
            "viewclass": "MDBoxLayout",
            "size_hint_y": None,
            "height": 1,
            "md_bg_color": (0.7, 0.7, 0.7, 1),
        }

    """
    NAV MENU + INITIAL LOAD
    """
    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: (self.load_existing_tasks(), self.update_dashboard()), 0)

        root = self.parent.parent

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Switch View",
                "on_release": lambda: self.open_view_submenu(),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.1, 0.1, 1),
            },
            self._divider(),
            {
                "viewclass": "OneLineListItem",
                "text": "Create Category",
                "on_release": lambda: self.open_category_creator(source="nav"),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.1, 0.1, 1),
            },
            self._divider(),
            {
                "viewclass": "OneLineListItem",
                "text": "Manage Categories",
                "on_release": lambda: self.open_category_manager(),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.1, 0.1, 1),
            },
        ]

        self.nav_menu = MDDropdownMenu(
            caller=root.ids.nav_button,
            items=menu_items,
            width_mult=4,
            md_bg_color=(0.97, 0.97, 0.97, 1),
            border_margin=8,
            radius=[12, 12, 12, 12],
            elevation=4,
        )

    def open_nav_menu(self):
        if hasattr(self, "nav_menu"):
            self.nav_menu.open()

    """
    SWITCH VIEW SUBMENU
    """
    def open_view_submenu(self):
        submenu_items = [
            {
                "text": "Dashboard",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.switch_view("Dashboard"),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.1, 0.1, 1),
            },
            self._divider(),
            {
                "text": "Task View",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.switch_view("Task View"),
                "theme_text_color": "Custom",
                "text_color": (0.1, 0.1, 0.1, 1),
            },
            self._divider(),
        ]

        root = self.parent.parent

        self.view_submenu = MDDropdownMenu(
            caller=root.ids.nav_button,
            items=submenu_items,
            width_mult=4,
            md_bg_color=(0.94, 0.94, 0.94, 1),
            border_margin=8,
            radius=[12, 12, 12, 12],
            elevation=4,
        )

        if hasattr(self, "nav_menu"):
            self.nav_menu.dismiss()

        self.view_submenu.open()

    def switch_view(self, name):
        self.ids.screen_manager.current = name

        if hasattr(self, "view_submenu"):
            self.view_submenu.dismiss()
        if hasattr(self, "nav_menu"):
            self.nav_menu.dismiss()

    """
    CATEGORY CREATOR ENTRY
    """
    def open_category_creator(self, source="nav"):
        creator = CategoryCreator(self, source=source)
        popup = Popup(
            title="Create Category",
            content=creator,
            size_hint=(0.8, 0.6),
            auto_dismiss=True,
        )

        creator.popup = popup
        popup.open()

        if hasattr(self, "nav_menu"):
            self.nav_menu.dismiss()

    """
    MANAGE CATEGORIES
    """
    def populate_category_manager(self):
        """Populate the Manage Categories screen."""
        if "category_list" not in self.ids:
            return

        self.ids.category_list.clear_widgets()

        categories = self.cat_controller.load_categories()

        from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

        for cat in categories:
            item = OneLineIconListItem(
                text=f"{cat.name} ({cat.color})",
                on_release=lambda inst, c=cat: Logger.info(f"Selected category: {c.name}"),
            )
            icon = IconLeftWidget(icon="folder")
            item.add_widget(icon)
            self.ids.category_list.add_widget(item)

    def open_category_manager(self):
        self.populate_category_manager()
        self.ids.screen_manager.current = "ManageCategories"

    """
    UNIFIED CATEGORY CREATION (OPTION C)
    """
    def create_category(self, name, color_key, *, source="nav"):
        result = self.cat_controller.add_category(name, color_key)

        if not result.success:
            self.show_error(result.error)
            return

        new_cat = result.return_val

        # Refresh UI
        self.load_existing_tasks()
        self.update_dashboard()

        # Refresh category menus
        if hasattr(self, "category_menu"):
            self.category_menu.dismiss()
        if hasattr(self, "edit_category_menu"):
            self.edit_category_menu.dismiss()

        # Behavior depends on source
        if source == "nav":
            self.populate_category_manager()
            self.ids.screen_manager.current = "ManageCategories"

        elif source == "add_task":
            self.selected_category = new_cat
            self.category_field.text = new_cat.name

        elif source == "edit_task":
            self.edit_selected_category = new_cat
            self.edit_category_field.text = new_cat.name

        Logger.info(f"MainWindow: Created category '{name}' ({color_key}) from {source}")

    """
    LOAD EXISTING TASKS
    """
    def load_existing_tasks(self):
        try:
            tasks = self.controller.load_tasks()

            if "task_list" in self.ids:
                self.ids.task_list.clear_widgets()

            if "dashboard_task_list" in self.ids:
                self.ids.dashboard_task_list.clear_widgets()

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
                            focused_widget = TaskItem(
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
                            self.ids.dashboard_task_list.add_widget(focused_widget)
                    except Exception:
                        pass

        except Exception as e:
            self.show_error(str(e))

    """
    ADD TASK
    """
    def add_todo_item(self, task_name, text, deadline, category):
        cat_id = category.id if category else None
        result = self.controller.add_task(task_name, text, deadline, cat_id)

        if not result.success:
            self.show_error(result.error)
            return

        task_id = result.return_val

        task_widget = TaskItem(
            main_window=self,
            controller=self.task_controller,
            item_id=task_id,
            task_name=task_name,
            description=text,
            category=category,
            cat_controller=self.cat_controller,
            done=False,
            deadline=deadline,
        )

        if "task_list" in self.ids:
            self.ids.task_list.add_widget(task_widget)

        if deadline:
            try:
                d = datetime.strptime(deadline, "%m/%d/%Y").date()
                if d == date.today() and "dashboard_task_list" in self.ids:
                    self.ids.dashboard_task_list.add_widget(task_widget)
            except Exception:
                pass

    """
    REMOVE TASK
    """
    def remove_task_widget(self, item_id):
        if "task_list" in self.ids:
            for widget in list(self.ids.task_list.children):
                if isinstance(widget, TaskItem) and widget.item_id == item_id:
                    self.ids.task_list.remove_widget(widget)
                    break

        if "dashboard_task_list" in self.ids:
            for widget in list(self.ids.dashboard_task_list.children):
                if isinstance(widget, TaskItem) and widget.item_id == item_id:
                    self.ids.dashboard_task_list.remove_widget(widget)
                    break

        self.update_dashboard()

    """
    ERROR POPUP
    """
    def show_error(self, message):
        Popup(
            title="Error",
            content=MDLabel(text=message),
            size_hint=(0.6, 0.3),
        ).open()

    """
    DASHBOARD STATS
    """
    def update_dashboard(self):
        try:
            tasks = self.controller.load_tasks()

            if "stat_total_tasks" in self.ids:
                self.ids.stat_total_tasks.text = str(len(tasks))

            today = date.today()
            due_today = []

            for t in tasks:
                if getattr(t, "deadline", None):
                    try:
                        d = datetime.strptime(t.deadline, "%m/%d/%Y").date()
                        if d == today:
                            due_today.append(t)
                    except Exception:
                        pass

            if "stat_due_today_header" in self.ids:
                if due_today:
                    self.ids.stat_due_today_header.text = f"{len(due_today)} due today"
                else:
                    self.ids.stat_due_today_header.text = "No tasks due today"

        except Exception as e:
            self.show_error(f"Dashboard update failed: {e}")

    """
    ADD TASK DIALOG
    """
    def open_add_dialog(self):
        content = AddTaskContent()

        self.add_task_name = content.ids.task_name
        self.add_description = content.ids.description
        self.add_deadline = content.ids.deadline
        self.category_field = content.ids.category

        categories = self.catlist.load_categories()
        menu_items = []
        for row in categories:
            cat = Category(id=row[0], name=row[1], color=row[2])
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_add_category(c),
            })

        self.selected_category = None
        self.category_menu = MDDropdownMenu(
            caller=self.category_field,
            items=menu_items,
            width_mult=4,
        )

        self.category_field.on_focus = (
            lambda inst, val: self.category_menu.open() if val else None
        )

        self.add_dialog = MDDialog(
            title="Create Task",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.add_dialog.dismiss()),
                MDRaisedButton(text="Create", on_release=lambda x: self.submit_add_task()),
            ],
        )

        self.add_dialog.open()

    def set_add_category(self, category):
        self.selected_category = category
        self.category_field.text = category.name
        self.category_menu.dismiss()

    def submit_add_task(self):
        name = self.add_task_name.text.strip()
        desc = self.add_description.text.strip()
        deadline = self.add_deadline.text.strip()
        category = self.selected_category

        if not name:
            self.show_error("Task name is required.")
            return

        self.add_todo_item(name, desc, deadline, category)

        self.add_dialog.dismiss()

        self.load_existing_tasks()
        self.update_dashboard()

    """
    EDIT TASK DIALOG
    """
    def open_edit_dialog(self, task_widget):
        self.edit_target = task_widget

        content = EditTaskContent()

        self.edit_task_name = content.ids.task_name
        self.edit_description = content.ids.description
        self.edit_deadline = content.ids.deadline
        self.edit_category_field = content.ids.category

        self.edit_task_name.text = task_widget.task_name
        self.edit_description.text = task_widget.description
        self.edit_deadline.text = task_widget.deadline

        categories = self.catlist.load_categories()
        menu_items = []
        for row in categories:
            cat = Category(id=row[0], name=row[1], color=row[2])
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_edit_category(c),
            })

        self.edit_selected_category = (
            task_widget.cat_controller.get_category(task_widget.cat_id).return_val
            if task_widget.cat_id else None
        )

        self.edit_category_menu = MDDropdownMenu(
            caller=self.edit_category_field,
            items=menu_items,
            width_mult=4,
        )

        self.edit_category_field.on_focus = (
            lambda inst, val: self.edit_category_menu.open() if val else None
        )

        self.edit_dialog = MDDialog(
            title="Edit Task",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.edit_dialog.dismiss()),
                MDRaisedButton(text="Save", on_release=lambda x: self.submit_edit_task()),
            ],
        )

        self.edit_dialog.open()

    def set_edit_category(self, category):
        self.edit_selected_category = category
        self.edit_category_field.text = category.name
        self.edit_category_menu.dismiss()

    def submit_edit_task(self):
        name = self.edit_task_name.text.strip()
        desc = self.edit_description.text.strip()
        deadline = self.edit_deadline.text.strip()
        category = self.edit_selected_category

        if not name:
            self.show_error("Task name is required.")
            return

        result = self.task_controller.update_task(
            self.edit_target.item_id,
            name,
            desc,
            deadline,
            category.id if category else None,
        )

        if not result.success:
            self.show_error(result.error)
            return

        self.edit_target.task_name = name
        self.edit_target.description = desc
        self.edit_target.deadline = deadline

        if category:
            self.edit_target.cat_id = category.id
            self.edit_target.cat_name = category.name
            self.edit_target.color = (
                self.edit_target.cat_controller.get_category(category.id).return_val.color
            )
        else:
            self.edit_target.change_to_none()

        self.edit_dialog.dismiss()

        self.load_existing_tasks()
        self.update_dashboard()
