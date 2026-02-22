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

    def remove_item(self, item_id):
        for widget in list(self.todoitems.children):
            if widget.item_id == item_id:
                self.todoitems.remove_widget(widget)
                break

    def mark_item_done(self, item_id):
        for widget in self.todoitems.children:
            if widget.item_id == item_id:
                widget.mark_done_button.disabled = True
                break