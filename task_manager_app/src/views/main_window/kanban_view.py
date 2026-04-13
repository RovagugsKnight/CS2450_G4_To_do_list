from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from views.task_widget import TaskItem
from views.colors import get_color, pastelize


def build_kanban_board(self):
    """Build a Kanban board with clean solid pastel columns (no fades, no shadows)."""
    if "board_columns" not in self.ids:
        return

    container = self.ids.board_columns
    container.clear_widgets()

    categories = self.cat_controller.load_categories()
    tasks = self.controller.load_tasks()

    for cat in categories:
        # cat.color is the key ("teal", "gray", etc.)
        color_data = get_color(cat.color)
        base_color = color_data["rgba"]
        pastel = pastelize(base_color)

        col = MDCard(
            orientation="vertical",
            radius=18,
            padding=[16, 16, 16, 16],
            size_hint=(None, 1),
            width=dp(300),
            elevation=0,
            md_bg_color=pastel,
        )

        col.add_widget(
            MDLabel(
                text=cat.name,
                font_style="H6",
                size_hint_y=None,
                height="32dp",
                theme_text_color="Custom",
                text_color=(0.1, 0.1, 0.1, 1),
            )
        )

        task_list = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
        )
        task_list.bind(minimum_height=task_list.setter("height"))

        for t in tasks:
            if cat.name.lower() == "done":
                if t.done:
                    task_list.add_widget(
                        TaskItem(
                            main_window=self,
                            controller=self.task_controller,
                            item_id=t.task_id,
                            task_name=t.task_name,
                            description=t.text,
                            category=cat,
                            cat_controller=self.cat_controller,
                            done=t.done,
                            deadline=t.deadline,
                        )
                    )
            else:
                if (t.catid == cat.id) and (not t.done):
                    task_list.add_widget(
                        TaskItem(
                            main_window=self,
                            controller=self.task_controller,
                            item_id=t.task_id,
                            task_name=t.task_name,
                            description=t.text,
                            category=cat,
                            cat_controller=self.cat_controller,
                            done=t.done,
                            deadline=t.deadline,
                        )
                    )

        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, bar_width="6dp")
        scroll.add_widget(task_list)

        col.add_widget(scroll)
        container.add_widget(col)
