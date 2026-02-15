from kivy.uix.boxlayout import BoxLayout
from views.buttons import YellowButton, LightTealButton


class TaskItem(BoxLayout):
    size_hint = (1, None)
    spacing = 5

    def __init__(self, main_window, item_id, todo_item, done=False, **kwargs):
        super().__init__(**kwargs)

        self.height = 40
        self.item_id = item_id
        self.main_window = main_window

        self.item_display_box = LightTealButton(
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

        self.add_widget(self.item_display_box)
        self.add_widget(self.mark_done_button)
        self.add_widget(remove_button)
        

        edit_button = YellowButton(text="Edit", size_hint=(None, 1), width=60)
        edit_button.bind(on_release=self.edit_task)
        self.add_widget(edit_button)

    def edit_task(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        input_box = TextInput(text=self.item_display_box.text, multiline=False)
        layout.add_widget(input_box)

        save_button = YellowButton(text="Save")
        layout.add_widget(save_button)

        popup = Popup(title="Edit Task", content=layout, size_hint=(0.8, 0.4))

        def save_changes(instance):
            new_text = input_box.text.strip()
            if new_text:
                self.main_window.controller.update_task(self.item_id, new_text)
                self.item_display_box.text = new_text
            popup.dismiss()

        save_button.bind(on_release=save_changes)
        popup.open()
