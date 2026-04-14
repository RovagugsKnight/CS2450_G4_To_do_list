from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty, ListProperty

from controller.task_controller import TaskController
from controller.category_controller import CategoryController
from models.category import Category
from views.colors import get_color


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

        # FIX: remove broken call and refresh UI instead
        self.main_window.load_existing_tasks()
        self.main_window.update_dashboard()
        self.main_window.refresh_kanban()

    def edit_task(self):
        if hasattr(self.main_window, "open_edit_dialog"):
            self.main_window.open_edit_dialog(self)
        else:
            self.show_popup("Edit dialog not implemented yet.")
