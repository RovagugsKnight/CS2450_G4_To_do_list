from kivymd.uix.stacklayout import MDStackLayout
from kivy.properties import StringProperty
from controller.category_controller import CategoryController
from models.category import Category
from kivy.logger import Logger
from kivy.lang import Builder
from category_button import CategoryButton

Builder.load_file('views/category_selector.kv')


class CategorySelector(MDStackLayout):
    """Category selection widget with buttons."""
    groupname = StringProperty("categories")

    def __init__(self, controller: CategoryController,
                 groupname: str = "categories", **kwargs):
        super().__init__(**kwargs)
        self.groupname = groupname
        self.controller = controller

        self.refresh()

    def refresh(self):
        """Clear and reload all category buttons."""
        self.clear_widgets()
        self.load_categories()

    def get_selected_category(self) -> Category | None:
        for child in self.children:
            if getattr(child, "state", None) == "down":
                return child.get_category()
        return None

    def check_selected(self) -> bool:
        for child in self.children:
            if getattr(child, "state", None) == "down":
                return True
        return False

    def load_categories(self) -> None:
        """Load categories from DB."""
        categories = self.controller.load_categories()

        # Sort so Todo and Done appear first
        categories.sort(key=lambda c: (c.is_system is False, c.name.lower()))

        for category in categories:
            btn = CategoryButton(category)
            btn.group = self.groupname
            self.add_widget(btn)
