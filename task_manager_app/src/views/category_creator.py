from kivymd.uix.boxlayout import MDBoxLayout
from views.buttons import YellowButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from views.color_selector import ColorSelector
from views.colors import color_dict
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.logger import Logger
Builder.load_file('views/category_creator.kv')

class CategoryCreator(MDBoxLayout):
    def __init__(self, mainwindow, popup: Popup | None = None, **kwargs):
        super().__init__(**kwargs)

        self.mainwindow = mainwindow

        self.popup = popup

        self.col_selector = ColorSelector(color_dict)

        self.add_widget(self.col_selector)

        self.submit_button = YellowButton(text="Submit", size_hint_y= None, height="50dp")
        self.add_widget(self.submit_button)

        self.submit_button.bind(on_release= self.end_creation)
    
    def end_creation(self, instance):
        cat_name = self.ids.cat_name.text
        color = self.col_selector.get_selected_color()
        self.popup.dismiss()
        Logger.info("DEBUG: cat_name={self.cat_name}, color={self.color}")
        self.mainwindow.add_cat_option(cat_name, color)
