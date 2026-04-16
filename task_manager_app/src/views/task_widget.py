from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.vector import Vector

from controller.task_controller import TaskController
from controller.category_controller import (
    CategoryController,
    DEFAULT_CATEGORY_NAME,
    DEFAULT_CATEGORY_COLOR,
)
from models.category import Category
from views.colors import get_color

# Touch tuning: exclude right action column; max move to count as tap vs scroll.
ACTION_STRIP_WIDTH_DP = 88
TAP_VS_SCROLL_MAX_MOVE_DP = 15


class TaskItem(MDBoxLayout):
    """
    Task card: not ButtonBehavior (so ScrollView can scroll). Tap almost anywhere on the
    card toggles expand; a short drag is treated as scroll. The right action column is
    excluded so checkbox / edit / delete stay accurate.
    """

    done = BooleanProperty(False)
    task_name = StringProperty("")
    description = StringProperty("")
    deadline = StringProperty("")
    color = ListProperty([1, 1, 1, 1])
    cat_name = StringProperty(DEFAULT_CATEGORY_NAME)

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
            self.color = get_color(category.color)["rgba"]
        else:
            self.change_to_none()

    def _touch_on_action_strip(self, touch) -> bool:
        """Right-side controls column (~80dp); touches here should not toggle expand."""
        # touch / widget geometry are in window coordinates
        return touch.x >= self.right - dp(ACTION_STRIP_WIDTH_DP)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self._touch_on_action_strip(touch):
            return super().on_touch_down(touch)

        handled = super().on_touch_down(touch)
        if handled:
            return True

        # Candidate for tap-to-expand; cleared in on_touch_up if finger moved (scroll).
        touch.ud[f"_task_expand_{id(self)}"] = (touch.x, touch.y)
        return False

    def on_touch_up(self, touch):
        key = f"_task_expand_{id(self)}"
        start = touch.ud.pop(key, None)
        if start is not None:
            ax, ay = start
            # Slightly above ScrollView scroll_distance so a dragIntent scroll does not toggle.
            if Vector(touch.pos).distance((ax, ay)) <= dp(TAP_VS_SCROLL_MAX_MOVE_DP):
                self.toggle_expand()
        return super().on_touch_up(touch)

    def change_to_none(self):
        self.cat_id = None
        self.cat_name = DEFAULT_CATEGORY_NAME
        self.color = get_color(DEFAULT_CATEGORY_COLOR)["rgba"]

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

        self.main_window.refresh_ui()

    def delete_task(self):
        result = self.controller.delete_task(self.item_id)
        if not result.success:
            self.show_popup(result.error)
            return

        self.main_window.refresh_ui()

    def edit_task(self):
        if hasattr(self.main_window, "open_edit_dialog"):
            self.main_window.open_edit_dialog(self)
        else:
            self.show_popup("Edit dialog not implemented yet.")
