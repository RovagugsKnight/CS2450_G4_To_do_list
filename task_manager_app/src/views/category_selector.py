from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from views.category_button import CategoryButton
from kivy.lang import Builder

Builder.load_file('views/category_selector.kv')

class CategorySelector(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    

