from kivymd.uix.button import MDFillRoundFlatIconButton
from models.category import Category
from views.colors import get_color
from kivy.properties import ListProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior

Builder.load_file("views/category_button.kv")

class CategoryButton(MDFillRoundFlatIconButton, ToggleButtonBehavior):

    color = ListProperty([1,1,1,1])
    name = StringProperty("None")

    def __init__(self, category: Category | None = None, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        if self.category:
            self.cat_id = self.category.id
            self.color = get_color(self.category.color)
            self.name = self.category.name
            self.bind(state=self.keep_color) # keep color after toggle
    
    def keep_color(self, *args):
        """change color back to original color"""
        self.md_bg_color = self.color
    
    def get_category(self):
        return self.category
    
    def show_selection(self, instance, value):
        """Show which button is selected with outline"""
        if value == "down":
            self.line_width = 2
            self.line_color = (0.7, 0.7, 0.7, 1)
        else:
            self.line_color = self.color