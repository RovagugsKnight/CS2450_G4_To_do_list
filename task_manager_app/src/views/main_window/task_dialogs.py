from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.app import App

from controller.category_controller import DEFAULT_CATEGORY_NAME, DONE_CATEGORY_NAME
from models.category import Category
from views.dialogs import AddTaskContent, EditTaskContent
from views.colors import category_rgba_for_theme, get_color
from views.task_widget import TaskItem


"""
ADD TASK DIALOG
"""


def open_add_dialog(self):
    is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
    dialog_bg = (0.18, 0.18, 0.18, 1) if is_dark else (0.98, 0.98, 0.98, 1)

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
        # "Done" is for completed work items, not a create target — use checkbox to complete.
        if cat.name.strip().lower() == DONE_CATEGORY_NAME.lower():
            continue
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
        md_bg_color=dialog_bg,
    )

    self.add_dialog = MDDialog(
        title="Create Task",
        type="custom",
        content_cls=content,
        md_bg_color=dialog_bg,
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

    if category and category.name.strip().lower() == DONE_CATEGORY_NAME.lower():
        self.show_error("Choose a category other than Done. Mark the task complete when it is finished.")
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

    self.refresh_ui()

    self.add_dialog.dismiss()


"""
EDIT TASK DIALOG
"""


def open_edit_dialog(self, task_widget: TaskItem):
    is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
    dialog_bg = (0.18, 0.18, 0.18, 1) if is_dark else (0.98, 0.98, 0.98, 1)

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
        if cat.name.strip().lower() == DONE_CATEGORY_NAME.lower():
            continue
        menu_items.append({
            "text": cat.name,
            "on_release": lambda c=cat: self.set_edit_category(c),
        })

    self.edit_category_menu = MDDropdownMenu(
        caller=content,
        items=menu_items,
        width_mult=4,
        md_bg_color=dialog_bg,
    )

    self.edit_dialog = MDDialog(
        title="Edit Task",
        type="custom",
        content_cls=content,
        md_bg_color=dialog_bg,
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

    if category and category.name.strip().lower() == DONE_CATEGORY_NAME.lower():
        self.show_error("Choose a category other than Done. Mark the task complete when it is finished.")
        return

    # Enforce Todo fallback instead of null category.
    if not category:
        rows = self.catlist.load_categories()
        for row in rows:
            cat_id, cat_name, cat_color = row
            if cat_name.lower() == DEFAULT_CATEGORY_NAME.lower():
                category = Category(id=cat_id, name=cat_name, color=cat_color)
                break

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
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        self.edit_target.color = category_rgba_for_theme(
            get_color(category.color)["rgba"],
            is_dark=is_dark,
        )
    else:
        self.edit_target.change_to_none()

    self.edit_dialog.dismiss()

    self.refresh_ui()
