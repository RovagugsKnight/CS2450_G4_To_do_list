from kivymd.uix.button import MDToggleButton
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from models.category import Category
from kivy.app import App

from views.colors import category_rgba_for_theme, get_color


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
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        self.color = category_rgba_for_theme(color_data["rgba"], is_dark=is_dark)

        # Style
        self.size_hint = (None, None)
        self.height = "40dp"
        self.width = "110dp"
        self.radius = [10, 10, 10, 10]
        self.md_bg_color = self.color
        self.theme_text_color = "Custom"
        self.text_color = (0.92, 0.92, 0.92, 1) if is_dark else (0.1, 0.1, 0.1, 1)

    def get_category(self):
        return self.category