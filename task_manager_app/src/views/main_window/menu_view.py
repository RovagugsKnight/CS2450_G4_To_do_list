from kivy.app import App

from views.main_window.nav_menu_helpers import make_nav_dropdown, nav_menu_item_style


def build_nav_menu(self):
    is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
    item_style = nav_menu_item_style(is_dark)
    theme_toggle_text = (
        "Dark Mode" if App.get_running_app().theme_cls.theme_style == "Light" else "Light Mode"
    )

    menu_items = [
        {
            "viewclass": "OneLineListItem",
            "text": "Switch View  >",
            "on_release": lambda: self.open_view_submenu(),
            **item_style,
        },
        {"viewclass": "MDSeparator", "height": 1},
        {
            "viewclass": "OneLineListItem",
            "text": "Manage Categories  >",
            "on_release": lambda: self.open_manage_categories_submenu(),
            **item_style,
        },
        {"viewclass": "MDSeparator", "height": 1},
        {
            "viewclass": "OneLineListItem",
            "text": theme_toggle_text,
            "on_release": lambda: self.toggle_theme(),
            **item_style,
        },
    ]

    root = App.get_running_app().root
    caller = root.ids.nav_button

    self.nav_menu = make_nav_dropdown(caller, menu_items, submenu=False)


def open_nav_menu(self):
    if hasattr(self, "nav_menu"):
        self.nav_menu.open()
