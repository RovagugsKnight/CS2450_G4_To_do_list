from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from views.category_button import CategoryButton
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.lang import Builder

Builder.load_file('views/category_selector.kv')

class CategorySelector(MDStackLayout):
    groupname = StringProperty("categories")
    def __init__(self, groupname: str = "categories", **kwargs):
        super().__init__(**kwargs)
        self.groupname = groupname
    
    def get_selected_category(self):
        """grab category from selected button"""
        for child in self.children:
            if getattr(child, "state", None) == "down":
                cat = child.get_category()
                Logger.info("DEBUG: category={cat}")
                return child.get_category()
            
        return None

