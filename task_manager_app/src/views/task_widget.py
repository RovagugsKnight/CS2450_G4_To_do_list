from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty, ListProperty

from controller.task_controller import TaskController
from controller.category_controller import CategoryController
from models.category import Category
from views.colors import get_color


class TaskItem(MDBoxLayout):
    """
    Dribbble-style task card.
    UI is defined entirely in task_widget.kv.
    This class only handles logic and controller interaction.
    """

    done = BooleanProperty(False)
    task_name = StringProperty("")
    description = StringProperty("")
    deadline = StringProperty("")
    color = ListProperty([1, 1, 1, 1])  # category accent color

    def __init__(
        self,
        main_window=None,
        controller: TaskController = None,
        item_id=None,
        task_name="",
        description="",
        category: Category | None = None,
        cat_controller: CategoryController = None,
        done=False,
        deadline="",
        **kwargs
    ):
        super().__init__(**kwargs)

        # Allow KV to instantiate safely
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

    """
    CATEGORY HANDLING
    """

    def change_to_none(self):
        """Set category to None and use neutral accent color."""
        self.cat_id = None
        self.cat_name = "None"
        self.color = get_color("white")

    """
    ERROR POPUP
    """

    def show_popup(self, message: str):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label

        Popup(
            title="Error",
            content=Label(text=str(message)),
            size_hint=(0.6, 0.3),
        ).open()

    """
    TASK ACTIONS
    """

    def mark_done(self, *args):
        """Mark task as done in DB and refresh UI."""
        if not self.controller or not self.main_window:
            return

        result = self.controller.mark_done(self.item_id)
        if result.success:
            self.main_window.load_existing_tasks()
            self.main_window.update_dashboard()
        else:
            self.show_popup(result.error)

    def remove(self, *args):
        """Delete task from DB and remove widget from UI."""
        if not self.controller or not self.main_window:
            return

        result = self.controller.delete_task(self.item_id)
        if result.success:
            self.main_window.remove_task_widget(self.item_id)
        else:
            self.show_popup(result.error)

    def edit_task(self, *args):
        """Open edit dialog."""
        if self.main_window and hasattr(self.main_window, "open_edit_dialog"):
            self.main_window.open_edit_dialog(self)
        else:
            self.show_popup("Edit dialog not implemented yet.")
