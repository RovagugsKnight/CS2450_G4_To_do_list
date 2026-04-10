from kivymd.uix.button import MDToggleButton
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from models.category import Category
from views.colors import get_color


class CategoryButton(MDToggleButton):
    """
    A toggleable button representing a category.
    Works with CategorySelector to choose a category.
    """

    category = ObjectProperty(None)
    text = StringProperty("")
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, category: Category, **kwargs):
        super().__init__(**kwargs)

        self.category = category
        self.text = category.name

        # category.color is a string key ("teal", "gray", etc.)
        color_data = get_color(category.color)
        self.color = color_data["rgba"]

        # Style
        self.size_hint = (None, None)
        self.height = "40dp"
        self.width = "110dp"
        self.radius = [10, 10, 10, 10]
        self.md_bg_color = self.color
        self.theme_text_color = "Custom"
        self.text_color = (0.1, 0.1, 0.1, 1)

    def get_category(self):
        return self.category
