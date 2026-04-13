from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu

def open_view_submenu(self):
    submenu_items = [
        {
            "viewclass": "OneLineListItem",
            "text": "Dashboard",
            "on_release": lambda: self.switch_view("Dashboard"),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
        {"viewclass": "MDSeparator", "height": 1},
        {
            "viewclass": "OneLineListItem",
            "text": "Task View",
            "on_release": lambda: self.switch_view("Task View"),
            "theme_text_color": "Custom",
            "text_color": (0.1, 0.1, 0.1, 1),
        },
    ]

    # Attach submenu to the header nav_button in app.kv
    root = App.get_running_app().root
    caller = root.ids.nav_button

    self.view_submenu = MDDropdownMenu(
        caller=caller,
        items=submenu_items,
        width_mult=4,
        md_bg_color=(0.94, 0.94, 0.94, 1),
        radius=[12, 12, 12, 12],
        elevation=4,
    )

    # Close main menu if open
    if hasattr(self, "nav_menu"):
        self.nav_menu.dismiss()

    self.view_submenu.open()