from kivymd.uix.menu import MDDropdownMenu

def build_nav_menu(self):
    """Build the hamburger menu (clean, modular, no shadows)."""

    menu_items = [
        {
            "viewclass": "OneLineListItem",
            "text": "Switch View",
            "on_release": lambda: self.open_view_submenu(),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
        {"viewclass": "MDSeparator", "height": "1dp"},
        {
            "viewclass": "OneLineListItem",
            "text": "Create Category",
            "on_release": lambda: self.open_category_creator(source="nav"),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
        {"viewclass": "MDSeparator", "height": "1dp"},
        {
            "viewclass": "OneLineListItem",
            "text": "Manage Categories",
            "on_release": lambda: self.open_category_manager(),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
    ]

    self.nav_menu = MDDropdownMenu(
        caller=self.ids.nav_button,
        items=menu_items,
        width_mult=4,
        md_bg_color=(0.97, 0.97, 0.97, 1),
        radius=[12, 12, 12, 12],
        elevation=4,
    )


def open_nav_menu(self):
    if hasattr(self, "nav_menu"):
        self.nav_menu.open()