from kivymd.uix.button import MDFillRoundFlatIconButton
from models.category import Category
from views.colors import get_color
from kivy.properties import ListProperty, StringProperty
from kivy.lang import Builder

Builder.load_file("views/category_button.kv")

class CategoryButton(MDFillRoundFlatIconButton):

    color = ListProperty([1,1,1,1])
    name = StringProperty("None")

    def __init__(self, category: Category | None = None, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        if self.category:
            self.color = get_color(self.category.color)
            self.name = self.category.name
    
    def get_category(self):
        return self.category