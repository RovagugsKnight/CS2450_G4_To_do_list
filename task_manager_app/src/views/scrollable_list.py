from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout


class ScrollableList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.todoitems = MDGridLayout(
            cols = 3,
            size_hint_y=None
        )
        self.todoitems.bind(minimum_height=self.todoitems.setter("height"))

        self.add_widget(self.todoitems)

    def remove_item(self, item_id):
        for widget in list(self.todoitems.children):
            if widget.item_id == item_id:
                self.todoitems.remove_widget(widget)
                break
    

