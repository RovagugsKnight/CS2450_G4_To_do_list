from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from views.task_widget import TaskItem
from views.grid_layout import normalize_grid    

class ScrollableList(ScrollView):
    """Creates a scrollable list to hold
    tasks"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.todoitems = MDGridLayout(
            cols = 3,
            size_hint_y=None
        )

        #matches children widgets combined height
        self.todoitems.bind(minimum_height=self.todoitems.setter("height"))

        self.add_widget(self.todoitems)

    def remove_item(self, item_id:int) -> None:
        """looks for task id in widgets and removes
        widget when found."""
        # look for widget with task id
        for widget in list(self.todoitems.children):
            if isinstance(widget, TaskItem) and widget.item_id == item_id:
                self.todoitems.remove_widget(widget)
                break
        
        # make sure task size is consistent with spacers
        normalize_grid(self.todoitems)

    

