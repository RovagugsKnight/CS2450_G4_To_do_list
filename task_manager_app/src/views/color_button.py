from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.properties import ListProperty
from views.colors import get_color
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.lang import Builder

Builder.load_file("views/color_button.kv")

class ColorButton(MDFillRoundFlatIconButton, MDToggleButton):

    color = ListProperty([1,1,1,1])

    def __init__(self, color: str, **kwargs):
        super().__init__(**kwargs)
        self.color_val = color
        self.color = get_color(color)
        self.bind(state=self.keep_color) # keep color after toggle
    
    def keep_color(self, *args):
        """change color back to original color"""
        self.md_bg_color = self.color
    
    def show_selection(self, instance, value):
        """Show which button is selected with outline"""
        if value == "down":
            self.line_width = 2
            self.line_color = (0.7, 0.7, 0.7, 1)
        else:
            self.line_color = self.color