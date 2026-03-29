from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from views.category_button import CategoryButton
from kivy.lang import Builder
from views.color_button import ColorButton

Builder.load_file('views/color_selector.kv')

class ColorSelector(MDStackLayout):
    """Selection menu for colors"""
    def __init__(self, colors: dict, group_name="colors", **kwargs):
        super().__init__(**kwargs)
        self.group_name = group_name
    
        for color in colors:
            btn = ColorButton(color=color)
            btn.group = self.group_name  # assign color buttons group
            self.add_widget(btn)
    
    def get_selected_color(self):
        for child in self.children:
            if getattr(child, "state", None) == "down":
                return getattr(child, "color_val", None)
        return None