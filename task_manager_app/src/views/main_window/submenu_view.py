from kivy.app import App
from kivy.clock import Clock

from views.main_window.nav_menu_helpers import make_nav_dropdown, nav_menu_item_style


def open_view_submenu(self):
    def _after_layout(_dt):
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        item_style = nav_menu_item_style(is_dark)
        submenu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Dashboard",
                "on_release": lambda: self.nav_submenu_switch_view("Dashboard"),
                **item_style,
            },
            {"viewclass": "MDSeparator", "height": 1},
            {
                "viewclass": "OneLineListItem",
                "text": "Task View",
                "on_release": lambda: self.nav_submenu_switch_view("Task View"),
                **item_style,
            },
        ]

        caller = self.nav_submenu_anchor_caller("view")
        self.view_submenu = make_nav_dropdown(caller, submenu_items, submenu=True)
        self.view_submenu.open()
        # KivyMD may dismiss the parent menu on tap; reopen next frame only if needed (see MainWindow).
        Clock.schedule_once(self._reopen_nav_menu_if_dismissed, 0)

    # Defer one frame so ``nav_menu`` layout/geometry is valid after any synchronous ``open()``.
    Clock.schedule_once(_after_layout, 0)


def open_manage_categories_submenu(self):
    def _after_layout(_dt):
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        item_style = nav_menu_item_style(is_dark)
        submenu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Create Category",
                "on_release": lambda: self.nav_submenu_open_category_creator(),
                **item_style,
            },
            {"viewclass": "MDSeparator", "height": 1},
            {
                "viewclass": "OneLineListItem",
                "text": "Category View",
                "on_release": lambda: self.nav_submenu_open_category_manager(),
                **item_style,
            },
        ]

        caller = self.nav_submenu_anchor_caller("manage")
        self.manage_categories_submenu = make_nav_dropdown(caller, submenu_items, submenu=True)
        self.manage_categories_submenu.open()
        Clock.schedule_once(self._reopen_nav_menu_if_dismissed, 0)

    Clock.schedule_once(_after_layout, 0)
