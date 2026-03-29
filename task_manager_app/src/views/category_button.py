from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.lang import Builder

Builder.load_file("views/category_button.kv")

class CategoryButton(MDFillRoundFlatIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)