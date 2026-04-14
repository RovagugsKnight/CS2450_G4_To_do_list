from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty, ListProperty

from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton

from controller.task_controller import TaskController
from controller.category_controller import CategoryController, DEFAULT_CATEGORY_NAME
from models.category import Category
from views.colors import get_color
from views.dialogs import AddTaskContent, EditTaskContent


class TaskItem(ButtonBehavior, MDBoxLayout):
    """
    Task card widget.
    UI is defined in task_widget.kv.
    Handles logic and controller interaction only.
    """

    done = BooleanProperty(False)
    task_name = StringProperty("")
    description = StringProperty("")
    deadline = StringProperty("")
    color = ListProperty([1, 1, 1, 1])
    cat_name = StringProperty("None")

    is_expanded = BooleanProperty(False)

    def __init__(
        self,
        main_window,
        controller: TaskController,
        item_id: int,
        task_name: str,
        description: str,
        category: Category | None,
        cat_controller: CategoryController,
        done: bool = False,
        deadline: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.main_window = main_window
        self.controller = controller
        self.cat_controller = cat_controller

        self.item_id = item_id
        self.done = done
        self.task_name = task_name
        self.description = description
        self.deadline = deadline

        if category:
            self.cat_id = category.id
            self.cat_name = category.name
            self.color = get_color(category.color)
        else:
            self.change_to_none()

    def change_to_none(self):
        self.cat_id = None
        self.cat_name = "None"
        self.color = get_color("white")

    def toggle_expand(self):
        self.is_expanded = not self.is_expanded

    def toggle_done(self, checkbox, value):
        if value:
            result = self.controller.mark_done(self.item_id)
        else:
            result = self.controller.mark_undone(self.item_id)

        if not result.success:
            self.show_popup(result.error)
            return

        self.done = value

        # Refresh UI
        self.main_window.load_existing_tasks()
        self.main_window.update_dashboard()
        self.main_window.refresh_kanban()

    def delete_task(self):
        result = self.controller.delete_task(self.item_id)
        if not result.success:
            self.show_popup(result.error)
            return

        # Refresh UI instead of broken call
        self.main_window.load_existing_tasks()
        self.main_window.update_dashboard()
        self.main_window.refresh_kanban()

    def edit_task(self):
        if hasattr(self.main_window, "open_edit_dialog"):
            self.main_window.open_edit_dialog(self)
        else:
            self.show_popup("Edit dialog not implemented yet.")


"""
ADD TASK DIALOG
"""


def open_add_dialog(self):
    content = AddTaskContent()

    # Keep references for submit_add_task
    self.add_task_name = content.ids.task_name
    self.add_description = content.ids.description
    self.add_deadline = content.ids.deadline

    # Store content so we can update it from menu callbacks
    self.add_content = content

    # Default selected category (matches KV default "Todo")
    content.selected_category = "Todo"
    content.ids.category_label.text = "Category: Todo"

    categories = self.catlist.load_categories()
    menu_items = []
    for row in categories:
        cat = Category(id=row[0], name=row[1], color=row[2])
        menu_items.append({
            "text": cat.name,
            "on_release": lambda c=cat: self.set_add_category(c),
        })

    self.selected_category = None
    # Menu exists; caller is set from KV chevron button via .caller if you want,
    # but we don't rely on caller for logic here.
    self.category_menu = MDDropdownMenu(
        caller=content,
        items=menu_items,
        width_mult=4,
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


def set_add_category(self, category: Category):
    # Update dialog content (KV-bound label + property)
    if hasattr(self, "add_content") and self.add_content:
        self.add_content.selected_category = category.name
        self.add_content.ids.category_label.text = f"Category: {category.name}"

    # Store for submit_add_task
    self.selected_category = category

    # Close menu
    if hasattr(self, "category_menu") and self.category_menu:
        self.category_menu.dismiss()


def submit_add_task(self):
    name = self.add_task_name.text.strip()
    desc = self.add_description.text.strip()
    deadline = self.add_deadline.text.strip()
    category = self.selected_category

    if not name:
        self.show_error("Task name is required.")
        return

    # Resolve category id, defaulting to the system "Todo" category if none selected
    if category:
        category_id = category.id
    else:
        category_id = None
        rows = self.catlist.load_categories()
        for row in rows:
            cat_id, cat_name, _ = row
            if cat_name.lower() == DEFAULT_CATEGORY_NAME.lower():
                category_id = cat_id
                break

    result = self.task_controller.add_task(
        name,
        desc,
        deadline,
        category_id,
    )

    if not result.success:
        self.show_error(result.error)
        return

    self.load_existing_tasks()
    self.update_dashboard()
    self.refresh_kanban()

    self.add_dialog.dismiss()


"""
EDIT TASK DIALOG
"""


def open_edit_dialog(self, task_widget: TaskItem):
    self.edit_target = task_widget

    content = EditTaskContent()

    # Keep references for submit_edit_task
    self.edit_task_name = content.ids.task_name
    self.edit_description = content.ids.description
    self.edit_deadline = content.ids.deadline

    # Store content so we can update it from menu callbacks
    self.edit_content = content

    # Populate fields
    self.edit_task_name.text = task_widget.task_name
    self.edit_description.text = task_widget.description
    self.edit_deadline.text = task_widget.deadline

    # Current category from task
    self.edit_selected_category = (
        task_widget.cat_controller.get_category(task_widget.cat_id).return_val
        if task_widget.cat_id else None
    )

    # Initialize selected_category + label in dialog content
    if self.edit_selected_category:
        content.selected_category = self.edit_selected_category.name
        content.ids.category_label.text = f"Category: {self.edit_selected_category.name}"
    else:
        content.selected_category = "Todo"
        content.ids.category_label.text = "Category: Todo"

    categories = self.catlist.load_categories()
    menu_items = []
    for row in categories:
        cat = Category(id=row[0], name=row[1], color=row[2])
        menu_items.append({
            "text": cat.name,
            "on_release": lambda c=cat: self.set_edit_category(c),
        })

    self.edit_category_menu = MDDropdownMenu(
        caller=content,
        items=menu_items,
        width_mult=4,
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


def set_edit_category(self, category: Category):
    # Update dialog content (KV-bound label + property)
    if hasattr(self, "edit_content") and self.edit_content:
        self.edit_content.selected_category = category.name
        self.edit_content.ids.category_label.text = f"Category: {category.name}"

    # Store for submit_edit_task
    self.edit_selected_category = category

    # Close menu
    if hasattr(self, "edit_category_menu") and self.edit_category_menu:
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

    # Update widget fields
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
    self.refresh_kanban()
