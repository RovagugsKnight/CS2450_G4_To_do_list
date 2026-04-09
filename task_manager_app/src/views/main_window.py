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

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from datetime import date, datetime


class MainWindow(MDScreen):
    """
    Main window for the Dribbble-style UI.
    """

    def __init__(self, repo: TaskRepository = None, catlist: CategoryList = None, **kwargs):
        super().__init__(**kwargs)

        self.repo = repo
        self.catlist = catlist

        if self.repo and self.catlist:
            self.controller = MainWindowController(self.repo)
            self.task_controller = TaskController(self.repo)
            self.cat_controller = CategoryController(self.catlist)

        self.deadline_mode = None
        self.add_deadline = None
        self.edit_deadline = None

    """
    DROPDOWN MENU
    """
    def on_kv_post(self, base_widget):
        root = self.parent.parent

        menu_items = [
            {
                "text": "Dashboard",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.switch_view("Dashboard"),
                "theme_text_color": "Custom",
                "text_color": (0.20, 0.20, 0.20, 1)
            },
            {
                "text": "Task View",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.switch_view("Task View"),
                "theme_text_color": "Custom",
                "text_color": (0.20, 0.20, 0.20, 1)
            }
        ]

        self.nav_menu = MDDropdownMenu(
            caller=root.ids.nav_button,
            items=menu_items,
            width_mult=4,
            md_bg_color=(0.94, 0.94, 0.94, 1),
            border_margin=8,
            radius=[12, 12, 12, 12],
            elevation=4
        )

    def open_nav_menu(self):
        if hasattr(self, "nav_menu"):
            self.nav_menu.open()

    def switch_view(self, name):
        self.ids.screen_manager.current = name
        self.nav_menu.dismiss()

    """
    SCREEN ENTER
    """
    def on_pre_enter(self):
        self.load_existing_tasks()
        self.update_dashboard()

    """
    TASK LOADING
    """
    def load_existing_tasks(self):
        try:
            tasks = self.controller.load_tasks()

            if hasattr(self.ids, "task_list"):
                self.ids.task_list.clear_widgets()

            for task in reversed(tasks):
                category = None
                if task.catid:
                    cat_result = self.cat_controller.get_category(task.catid)
                    category = cat_result.return_val

                task_widget = TaskItem(
                    main_window=self,
                    controller=self.task_controller,
                    item_id=task.id,
                    task_name=task.task_name,
                    description=task.text,
                    category=category,
                    cat_controller=self.cat_controller,
                    done=task.done,
                    deadline=task.deadline
                )

                self.ids.task_list.add_widget(task_widget)

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
            deadline=deadline
        )

        self.ids.task_list.add_widget(task_widget)

    """
    REMOVE TASK
    """
    def remove_task_widget(self, item_id):
        if not hasattr(self.ids, "task_list"):
            return

        for widget in list(self.ids.task_list.children):
            if isinstance(widget, TaskItem) and widget.item_id == item_id:
                self.ids.task_list.remove_widget(widget)
                break

        self.update_dashboard()

    """
    KANBAN COLUMN
    """
    def build_column(self, category):
        return MDCard(
            orientation="vertical",
            size_hint=(None, None),
            width="280dp",
            height=self.ids.board_columns.height,
            padding="12dp",
            radius=[12, 12, 12, 12],
            children=[
                MDLabel(
                    text=category.name,
                    halign="center",
                    bold=True
                )
            ]
        )

    """
    ERROR POPUP
    """
    def show_error(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label

        Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        ).open()

    """
    DEADLINE PICKER
    """
    def open_deadline_selector(self, mode):
        self.deadline_mode = mode
        DeadlineSelector(self.on_deadline_selected).open()

    def on_deadline_selected(self, date_str):
        if self.deadline_mode == "add" and self.add_deadline:
            self.add_deadline.text = date_str
        elif self.deadline_mode == "edit" and self.edit_deadline:
            self.edit_deadline.text = date_str

    """
    ADD TASK DIALOG
    """
    def open_add_dialog(self):
        content = AddTaskContent()

        self.add_task_name = content.ids.task_name
        self.add_description = content.ids.description
        self.add_deadline = content.ids.deadline
        self.category_field = content.ids.category

        self.add_deadline.on_focus = (
            lambda inst, val: self.open_deadline_selector("add") if val else None
        )

        categories = self.catlist.load_categories()
        menu_items = []
        for row in categories:
            cat = Category(id=row[0], name=row[1], color=row[2])
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_add_category(c)
            })

        self.selected_category = None
        self.category_menu = MDDropdownMenu(
            caller=self.category_field,
            items=menu_items,
            width_mult=4
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
                MDRaisedButton(text="Create", on_release=lambda x: self.submit_add_task())
            ]
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

        self.edit_deadline.on_focus = (
            lambda inst, val: self.open_deadline_selector("edit") if val else None
        )

        categories = self.catlist.load_categories()
        menu_items = []
        for row in categories:
            cat = Category(id=row[0], name=row[1], color=row[2])
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_edit_category(c)
            })

        self.edit_selected_category = (
            task_widget.cat_controller.get_category(task_widget.cat_id).return_val
            if task_widget.cat_id else None
        )

        self.edit_category_menu = MDDropdownMenu(
            caller=self.edit_category_field,
            items=menu_items,
            width_mult=4
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
                MDRaisedButton(text="Save", on_release=lambda x: self.submit_edit_task())
            ]
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
            category.id if category else None
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
        self.update_dashboard()

    """
    KANBAN BOARD
    """
    def load_board(self):
        container = self.ids.board_columns
        container.clear_widgets()

        for row in self.catlist.load_categories():
            cat = Category(id=row[0], name=row[1], color=row[2])
            column = self.build_column(cat)
            container.add_widget(column)

    """
    DASHBOARD
    """
    def update_dashboard(self):
        try:
            tasks = self.controller.load_tasks()

            total = len(tasks)
            if "stat_total_tasks" in self.ids:
                self.ids.stat_total_tasks.text = str(total)

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

            if "stat_due_today" in self.ids:
                self.ids.stat_due_today.text = str(len(due_today))

            if "dashboard_today_list" in self.ids:
                lst = self.ids.dashboard_today_list
                lst.clear_widgets()

                if not due_today:
                    lst.add_widget(
                        MDLabel(
                            text="No tasks due today",
                            theme_text_color="Hint",
                            halign="left",
                            padding=(16, 16)
                        )
                    )
                else:
                    for task in due_today:
                        lst.add_widget(
                            MDLabel(
                                text=task.task_name,
                                theme_text_color="Primary",
                                halign="left"
                            )
                        )

        except Exception as e:
            self.show_error(f"Dashboard update failed: {e}")
