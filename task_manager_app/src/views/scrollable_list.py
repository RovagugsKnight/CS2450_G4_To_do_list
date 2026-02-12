from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout


class ScrollableList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.todoitems = BoxLayout(
            orientation="vertical",
            size_hint_y=None
        )
        self.todoitems.bind(minimum_height=self.todoitems.setter("height"))

        self.add_widget(self.todoitems)