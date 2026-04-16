from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from views.color_selector import ColorSelector
from views.colors import color_dict
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.app import App
from views.main_window.dashboard_view import update_dashboard
from kivymd.uix.label import MDLabel
from controller.category_controller import is_system_category_name

Builder.load_file('views/category_creator.kv')


class CategoryCreator(MDBoxLayout):
    """
    CATEGORY CREATOR POPUP
    """

    def __init__(self, mainwindow, source="nav", popup: Popup | None = None, **kwargs):
        super().__init__(**kwargs)

        self.mainwindow = mainwindow
        self.source = source
        self.popup = popup
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        self._primary_button_bg = (0.35, 0.35, 0.35, 1) if is_dark else (0.25, 0.45, 0.85, 1)

        # Color selector widget
        self.col_selector = ColorSelector(color_dict)
        self.ids.color_area.add_widget(self.col_selector)

        # Submit button
        self.submit_button = MDRaisedButton(
            text="Submit",
            size_hint=(1, None),
            height="50dp",
            md_bg_color=self._primary_button_bg,
        )
        self.ids.submit_area.add_widget(self.submit_button)

        self.submit_button.bind(on_release=self.end_creation)

    def end_creation(self, instance):
        cat_name = self.ids.cat_name.text.strip()
        color_key = self.col_selector.get_selected_color_key()

        Logger.info(f"DEBUG: cat_name={cat_name}, color_key={color_key}")

        if not cat_name:
            Logger.error("CategoryCreator: No category name provided")
            return

        # Auto-capitalize every word (but not all letters)
        cat_name = " ".join(word.capitalize() for word in cat_name.split())

        # Prevent creating system categories
        if is_system_category_name(cat_name):
            Logger.error("CategoryCreator: Cannot create system category names")
            return

        # Ensure a color is selected
        if not color_key:
            Logger.error("CategoryCreator: No color selected")
            return

        # Prevent white from being used as a category color
        if color_key == "white":
            Logger.error("CategoryCreator: White cannot be used as a category color")
            return

        # CREATE CATEGORY DIRECTLY THROUGH CONTROLLER
        result = self.mainwindow.cat_controller.add_category(cat_name, color_key)

        if not result.success:
            is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
            Popup(
                title="Error",
                content=MDLabel(
                    text=result.error,
                    theme_text_color="Custom",
                    text_color=(0.92, 0.92, 0.92, 1) if is_dark else (0.1, 0.1, 0.1, 1),
                ),
                size_hint=(0.6, 0.3),
                background="",
                background_color=(0.14, 0.14, 0.14, 1) if is_dark else (0.98, 0.98, 0.98, 1),
            ).open()
            return

        new_cat = result.return_val

        # Refresh UI
        self.mainwindow.refresh_kanban()
        update_dashboard(self.mainwindow)

        # Handle context (Add Task / Edit Task)
        if self.source == "add_task":
            self.mainwindow.selected_category = new_cat
            self.mainwindow.category_field.text = new_cat.name

        elif self.source == "edit_task":
            self.mainwindow.edit_selected_category = new_cat
            self.mainwindow.edit_category_field.text = new_cat.name

        # Close popup
        if self.popup:
            self.popup.dismiss()
