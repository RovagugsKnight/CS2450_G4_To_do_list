from kivy.uix.boxlayout import BoxLayout
from views.buttons import YellowButton, LightTealButton


class TaskItem(BoxLayout):
    size_hint = (1, None)
    spacing = 5

    def __init__(self, main_window, item_id, todo_item, done=False, **kwargs):
        super().__init__(**kwargs)

        self.height = 40
        self.item_id = item_id

        item_display_box = LightTealButton(
            text=todo_item,
            size_hint=(0.6, 1)
        )

        self.mark_done_button = YellowButton(
            text="Done",
            size_hint=(None, 1),
            width=100,
            disabled=done
        )
        self.mark_done_button.bind(
            on_release=lambda *args: main_window.mark_as_done(item_id)
        )

        remove_button = YellowButton(
            text="-",
            size_hint=(None, 1),
            width=40
        )
        remove_button.bind(
            on_release=lambda *args: main_window.delete_todo_item(item_id)
        )

        self.add_widget(item_display_box)
        self.add_widget(self.mark_done_button)
        self.add_widget(remove_button)