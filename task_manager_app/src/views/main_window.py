from kivymd.uix.screen import MDScreen
from kivy.logger import Logger

from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import CategoryController

from models.category import Category
from models.category_list import CategoryList
from models.task_repository import TaskRepository

from views.task_widget import TaskItem

from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class MainWindow(MDScreen):
    """
    Main window for the Dribbble-style UI.
    UI layout is defined in main_window.kv.
    This class handles logic, controllers, and modal dialogs.
    """
    def __init__(self, repo: TaskRepository = None, catlist: CategoryList = None, **kwargs):
        super().__init__(**kwargs)

        self.repo = repo
        self.catlist = catlist

        # Only initialize controllers if repo/catlist were provided
        if self.repo and self.catlist:
            self.controller = MainWindowController(self.repo)
            self.task_controller = TaskController(self.repo)
            self.cat_controller = CategoryController(self.catlist)


    # ---------------------------------------------------------
    #  SCREEN LIFECYCLE
    # ---------------------------------------------------------

    def on_pre_enter(self):
        """Called automatically when the screen becomes visible."""
        self.load_existing_tasks()

    # ---------------------------------------------------------
    #  TASK MANAGEMENT
    # ---------------------------------------------------------

    def load_existing_tasks(self):
        """Load tasks from DB and display them using TaskItem cards."""
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
                    deadline=task.deadline,
                )

                self.ids.task_list.add_widget(task_widget)

        except Exception as e:
            self.show_error(str(e))

    def add_todo_item(self, task_name: str, text: str, deadline: str, category: Category | None):
        """Add a new task to DB and UI."""
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

        self.ids.task_list.add_widget(task_widget)

    def remove_task_widget(self, item_id: int):
        """Remove a task card from the UI."""
        if not hasattr(self.ids, "task_list"):
            return

        for widget in list(self.ids.task_list.children):
            if isinstance(widget, TaskItem) and widget.item_id == item_id:
                self.ids.task_list.remove_widget(widget)
                break

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
                    bold=True,
                )
                # then add TaskItem widgets for tasks in this category
            ],
        )

    # ---------------------------------------------------------
    #  CATEGORY MANAGEMENT (UI will be replaced with MDDialog)
    # ---------------------------------------------------------

    def delete_category(self):
        Logger.info("DEBUG: delete_category called (UI pending)")

    def create_category(self):
        Logger.info("DEBUG: create_category called (UI pending)")

    # ---------------------------------------------------------
    #  ERROR HANDLING
    # ---------------------------------------------------------

    def show_error(self, message: str):
        """Temporary error popup (will be replaced with MDDialog)."""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label

        Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.6, 0.3),
        ).open()

    # ---------------------------------------------------------
    #  EDIT TASK DIALOG HOOK
    # ---------------------------------------------------------

    def open_edit_dialog(self, task_widget: TaskItem):
        """Called by TaskItem when user taps Edit."""
        Logger.info(f"DEBUG: open_edit_dialog for task {task_widget.item_id}")
        # Will be implemented next (MDDialog)

    # ---------------------------------------------------------
    #  ADD TASK DIALOG
    # ---------------------------------------------------------

    def open_add_dialog(self):
        """Open the Add Task modal dialog."""
        # Text fields
        self.add_task_name = MDTextField(
            hint_text="Task Name",
            helper_text="Required",
            helper_text_mode="on_focus",
        )
        self.add_description = MDTextField(
            hint_text="Description",
            multiline=True,
        )
        self.add_deadline = MDTextField(
            hint_text="Deadline (optional)",
        )

        # Category dropdown menu
        menu_items = []
        for cat in self.catlist.categories:
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_add_category(c),
            })

        self.selected_category = None
        self.category_menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4,
        )

        self.category_field = MDTextField(
            hint_text="Category",
            on_focus=lambda inst, val: self.category_menu.open() if val else None
        )
        self.category_menu.caller = self.category_field

        # Build dialog
        self.add_dialog = MDDialog(
            title="Create Task",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                padding="12dp",
                children=[
                    self.add_task_name,
                    self.add_description,
                    self.add_deadline,
                    self.category_field,
                ],
            ),
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.add_dialog.dismiss()),
                MDRaisedButton(text="Create", on_release=lambda x: self.submit_add_task()),
            ],
        )

        self.add_dialog.open()

    def set_add_category(self, category):
        """Called when user selects a category from dropdown."""
        self.selected_category = category
        self.category_field.text = category.name
        self.category_menu.dismiss()

    def submit_add_task(self):
        """Validate and create the task."""
        name = self.add_task_name.text.strip()
        desc = self.add_description.text.strip()
        deadline = self.add_deadline.text.strip()
        category = self.selected_category

        if not name:
            self.show_error("Task name is required.")
            return

        self.add_todo_item(name, desc, deadline, category)
        self.add_dialog.dismiss()
    # ---------------------------------------------------------
    #  EDIT TASK DIALOG
    # ---------------------------------------------------------

    def open_edit_dialog(self, task_widget: TaskItem):
        """Open the Edit Task modal dialog with pre-filled values."""
        self.edit_target = task_widget

        # Pre-filled text fields
        self.edit_task_name = MDTextField(
            text=task_widget.task_name,
            hint_text="Task Name",
            helper_text="Required",
            helper_text_mode="on_focus",
        )
        self.edit_description = MDTextField(
            text=task_widget.description,
            hint_text="Description",
            multiline=True,
        )
        self.edit_deadline = MDTextField(
            text=task_widget.deadline,
            hint_text="Deadline (optional)",
        )

        # Category dropdown
        menu_items = []
        for cat in self.catlist.categories:
            menu_items.append({
                "text": cat.name,
                "on_release": lambda c=cat: self.set_edit_category(c),
            })

        self.edit_selected_category = task_widget.cat_controller.get_category(
            task_widget.cat_id
        ).return_val if task_widget.cat_id else None

        self.edit_category_menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4,
        )

        self.edit_category_field = MDTextField(
            text=self.edit_selected_category.name if self.edit_selected_category else "",
            hint_text="Category",
            on_focus=lambda inst, val: self.edit_category_menu.open() if val else None
        )
        self.edit_category_menu.caller = self.edit_category_field

        # Build dialog
        self.edit_dialog = MDDialog(
            title="Edit Task",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                padding="12dp",
                children=[
                    self.edit_task_name,
                    self.edit_description,
                    self.edit_deadline,
                    self.edit_category_field,
                ],
            ),
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.edit_dialog.dismiss()),
                MDRaisedButton(text="Save", on_release=lambda x: self.submit_edit_task()),
            ],
        )

        self.edit_dialog.open()

    def set_edit_category(self, category):
        """Called when user selects a category from dropdown."""
        self.edit_selected_category = category
        self.edit_category_field.text = category.name
        self.edit_category_menu.dismiss()

    def submit_edit_task(self):
        """Validate and update the task."""
        name = self.edit_task_name.text.strip()
        desc = self.edit_description.text.strip()
        deadline = self.edit_deadline.text.strip()
        category = self.edit_selected_category

        if not name:
            self.show_error("Task name is required.")
            return

        # Update DB
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

        # Update UI card live
        self.edit_target.task_name = name
        self.edit_target.description = desc
        self.edit_target.deadline = deadline

        if category:
            self.edit_target.cat_id = category.id
            self.edit_target.cat_name = category.name
            self.edit_target.color = self.edit_target.cat_controller.get_category(
                category.id
            ).return_val.color
        else:
            self.edit_target.change_to_none()

        self.edit_dialog.dismiss()

    # ---------------------------------------------------------
    #  Board Loading
    # ---------------------------------------------------------

    def load_board(self):
        container = self.ids.board_columns
        container.clear_widgets()

        for category in self.catlist.categories:
            column = self.build_column(category)
            container.add_widget(column)
    # ---------------------------------------------------------
    #  DASHBOARD DYNAMIC STATS
    # ---------------------------------------------------------

    def update_dashboard(self):
        """Update Dashboard stats and today's task preview."""
        try:
            tasks = self.controller.load_tasks()

            # --- Total Tasks ---
            total = len(tasks)
            if "stat_total_tasks" in self.ids:
                self.ids.stat_total_tasks.text = str(total)

            # --- Due Today ---
            from datetime import date
            today = date.today()

            due_today = []
            for t in tasks:
                if hasattr(t, "deadline") and t.deadline:
                    try:
                        if t.deadline == today:
                            due_today.append(t)
                    except Exception:
                        pass

            if "stat_due_today" in self.ids:
                self.ids.stat_due_today.text = str(len(due_today))

            # --- Today's Tasks List ---
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