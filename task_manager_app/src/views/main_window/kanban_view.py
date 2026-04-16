from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.factory import Factory

from views.task_widget import TaskItem
from views.colors import category_rgba_for_theme, get_color, pastelize
from views.main_window.scroll_bar_theme import scroll_bar_pair, scroll_list_gesture_kwargs

from datetime import date, datetime


def _parse_deadline(deadline: str):
    """Parse app deadline format (MM/DD/YYYY) into a date."""
    if not deadline:
        return None
    try:
        return datetime.strptime(deadline, "%m/%d/%Y").date()
    except (TypeError, ValueError):
        return None


def _build_task_widget(mainwindow, task, category):
    return TaskItem(
        main_window=mainwindow,
        controller=mainwindow.task_controller,
        item_id=task.task_id,
        task_name=task.task_name,
        description=task.text,
        category=category,
        cat_controller=mainwindow.cat_controller,
        done=task.done,
        deadline=task.deadline,
    )


def build_kanban_board(self):
    """Trello-style columns: full viewport height, vertical list scroll inside each column."""
    if "board_columns" not in self.ids:
        return

    container = self.ids.board_columns
    container.clear_widgets()

    categories = self.cat_controller.load_categories()
    tasks = self.controller.load_tasks()
    tasks_by_cat = {}
    done_tasks = []

    for task in tasks:
        if task.done:
            done_tasks.append(task)
            continue
        tasks_by_cat.setdefault(task.catid, []).append(task)

    is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
    bar_color, bar_inactive_color = scroll_bar_pair(is_dark)

    for cat in categories:
        color_data = get_color(cat.color)
        base_color = color_data["rgba"]
        if is_dark:
            col_bg = category_rgba_for_theme(base_color, is_dark=True)
        else:
            col_bg = pastelize(base_color)

        col = MDCard(
            orientation="vertical",
            radius=18,
            padding=[16, 16, 16, 16],
            size_hint=(None, 1),
            width=dp(300),
            elevation=0,
            md_bg_color=col_bg,
        )

        # Column title
        col.add_widget(
            MDLabel(
                text=cat.name,
                font_style="H6",
                size_hint_y=None,
                height="32dp",
                theme_text_color="Custom",
                text_color=(0.92, 0.92, 0.92, 1)
                if is_dark
                else (0.1, 0.1, 0.1, 1),
            )
        )

        separator = Factory.MDSeparator(
            height="1dp",
            size_hint_y=None,
            color=(0.35, 0.35, 0.38, 1)
            if is_dark
            else (0.60, 0.60, 0.60, 1),
        )
        col.add_widget(separator)

        task_list = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding=[0, dp(8), 0, 0],
            size_hint_y=None,
        )
        task_list.bind(minimum_height=task_list.setter("height"))

        column_tasks = done_tasks if cat.name.lower() == "done" else tasks_by_cat.get(cat.id, [])
        for t in column_tasks:
            task_list.add_widget(_build_task_widget(self, t, cat))

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint_y=1,
            bar_width="14dp",
            scroll_type=["bars", "content"],
            bar_color=bar_color,
            bar_inactive_color=bar_inactive_color,
            **scroll_list_gesture_kwargs(),
        )
        scroll.add_widget(task_list)
        col.add_widget(scroll)
        container.add_widget(col)


def populate_task_lists(mainwindow, tasks):
    """
    Populate the main task list and dashboard task list
    from a list of Task objects.
    """
    ids = mainwindow.ids

    if "task_list" in ids:
        ids.task_list.clear_widgets()

    if "dashboard_task_list" in ids:
        ids.dashboard_task_list.clear_widgets()

    today = date.today()
    done_category = None
    for cat in mainwindow.cat_controller.load_categories():
        if cat.name.lower() == "done":
            done_category = cat
            break

    for task in reversed(tasks):
        category = None
        if task.done and done_category:
            category = done_category
        elif task.catid:
            cat_result = mainwindow.cat_controller.get_category(task.catid)
            if cat_result.success:
                category = cat_result.return_val

        widget = TaskItem(
            main_window=mainwindow,
            controller=mainwindow.task_controller,
            item_id=task.task_id,
            task_name=task.task_name,
            description=task.text,
            category=category,
            cat_controller=mainwindow.cat_controller,
            done=task.done,
            deadline=task.deadline,
        )

        if "task_list" in ids:
            ids.task_list.add_widget(widget)
            ids.task_list.add_widget(MDBoxLayout(size_hint_y=None, height="10dp"))

        if "dashboard_task_list" in ids:
            d = _parse_deadline(task.deadline)
            if d == today:
                ids.dashboard_task_list.add_widget(widget)
                ids.dashboard_task_list.add_widget(MDBoxLayout(size_hint_y=None, height="10dp"))
