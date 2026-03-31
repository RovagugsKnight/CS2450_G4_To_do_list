from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from views.category_button import CategoryButton
from kivy.properties import StringProperty
from controller.category_controller import CategoryController
from models.category import Category
from kivy.logger import Logger
from kivy.lang import Builder

Builder.load_file('views/category_selector.kv')

class CategorySelector(MDStackLayout):
    """category selection widget with buttons and optional none value"""
    groupname = StringProperty("categories")
    def __init__(self, controller: CategoryController, none: bool = True, 
                 groupname: str = "categories", **kwargs):
        super().__init__(**kwargs)
        self.groupname = groupname
        self.controller = controller
        self.none = none
        self.give_none()
        self.load_categories()
    
    def get_selected_category(self) -> Category | None:
        Logger.info("DEBUG: get_selected_category called")
        """grab category from selected button"""
        for child in self.children:
            if getattr(child, "state", None) == "down":
                return child.get_category()
        return None
    
    def check_selected(self) -> bool:
        """check if a button is selected"""
        for child in self.children:
            if getattr(child, "state", None) == "down":
                return True
        return False

    def load_categories(self) -> None:
        """Load categories from db"""
        categories = self.controller.load_categories()

        for category in categories:
            btn = CategoryButton(category)
            btn.group = self.groupname
            self.add_widget(btn)
    
    def give_none(self) -> None:
        """Gives a none option for selection"""
        if self.none:
            btn = CategoryButton()
            btn.md_bg_color = "white"
            btn.text = "None"
            btn.group = self.groupname
            self.add_widget(btn)

        