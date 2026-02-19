from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from views.buttons import YellowButton


class InputFrame(BoxLayout):
    def __init__(self, main_window, **kwargs):
        super().__init__(orientation="horizontal", size_hint=(1, None), height=40, **kwargs)

        self.todo_input_widget = TextInput(
            multiline=False,
            size_hint=(0.8, 1)
        )

        add_button = YellowButton(
            text="+",
            size_hint=(0.2, 1)
        )
        add_button.bind(on_release=lambda *args: main_window.add_todo_item(self.todo_input_widget.text))

        self.add_widget(self.todo_input_widget)
        self.add_widget(add_button)