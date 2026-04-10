from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from views.color_selector import ColorSelector
from views.colors import color_dict
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.logger import Logger

Builder.load_file('views/category_creator.kv')


class CategoryCreator(MDBoxLayout):
    """
    CATEGORY CREATOR
    """

    def __init__(self, mainwindow, popup: Popup | None = None, **kwargs):
        super().__init__(**kwargs)

        self.mainwindow = mainwindow
        self.popup = popup

        # Color selector widget
        self.col_selector = ColorSelector(color_dict)
        self.add_widget(self.col_selector)

        # Submit button (replaces YellowButton)
        self.submit_button = MDRaisedButton(
            text="Submit",
            size_hint_y=None,
            height="50dp",
            md_bg_color=(0.2, 0.2, 0.2, 1),  # neutral dark gray
            radius=[10, 10, 10, 10],
        )
        self.add_widget(self.submit_button)

        self.submit_button.bind(on_release=self.end_creation)
    
    """
    END CREATION
    """
    def end_creation(self, instance):
        cat_name = self.ids.cat_name.text.strip()
        color_key = self.col_selector.get_selected_color_key()

        Logger.info(f"DEBUG: cat_name={cat_name}, color_key={color_key}")

        if not cat_name:
            Logger.error("CategoryCreator: No category name provided")
            return

        # Prevent creating system categories
        if cat_name.lower() in ("todo", "done"):
            Logger.error("CategoryCreator: Cannot create system category names")
            return

        # Prevent white from being used as a category color
        if color_key == "white":
            Logger.error("CategoryCreator: White cannot be used as a category color")
            return

        self.mainwindow.create_category(cat_name, color_key)

        if self.popup:
            self.popup.dismiss()
