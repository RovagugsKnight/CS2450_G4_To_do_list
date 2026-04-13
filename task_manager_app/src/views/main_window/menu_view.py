from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App

def build_nav_menu(self):
    menu_items = [
        {
            "viewclass": "OneLineListItem",
            "text": "Switch View",
            "on_release": lambda: self.open_view_submenu(),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
        {"viewclass": "MDSeparator", "height": 1},
        {
            "viewclass": "OneLineListItem",
            "text": "Create Category",
            "on_release": lambda: self.open_category_creator(source="nav"),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
        {"viewclass": "MDSeparator", "height": 1},
        {
            "viewclass": "OneLineListItem",
            "text": "Manage Categories",
            "on_release": lambda: self.open_category_manager(),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
    ]

    root = App.get_running_app().root
    caller = root.ids.nav_button

    self.nav_menu = MDDropdownMenu(
        caller=caller,
        items=menu_items,
        width_mult=4,
        md_bg_color=(0.97, 0.97, 0.97, 1),
        radius=[12, 12, 12, 12],
        elevation=4,
    )

def open_nav_menu(self):
    if hasattr(self, "nav_menu"):
        self.nav_menu.open()