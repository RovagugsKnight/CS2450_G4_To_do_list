# views/main_window/task_dialogs.py

from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton

from models.category import Category
from views.dialogs import AddTaskContent, EditTaskContent


# -------------------------
# ADD TASK DIALOG
# -------------------------

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

    from views.main_window.dashboard_view import update_dashboard
    update_dashboard(self)

    from views.main_window.kanban_view import build_kanban_board
    build_kanban_board(self)


# -------------------------
# EDIT TASK DIALOG
# -------------------------

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

    from views.main_window.dashboard_view import update_dashboard
    update_dashboard(self)

    from views.main_window.kanban_view import build_kanban_board
    build_kanban_board(self)
