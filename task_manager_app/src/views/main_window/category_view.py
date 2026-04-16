from kivy.uix.popup import Popup
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.factory import Factory
from views.colors import get_color
from views.category_creator import CategoryCreator


class ManageCategoriesPopup(Popup):
    """
    Popup that lists all categories with Edit/Delete controls.
    """

    def __init__(self, mainwindow, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = mainwindow
        # Hide native popup title bar; use custom in-card header instead.
        self.title = ""
        self.title_size = 0
        self.separator_height = 0
        self.size_hint = (0.9, 0.9)
        is_dark = App.get_running_app().theme_cls.theme_style == "Dark"
        popup_bg = (0.14, 0.14, 0.14, 1) if is_dark else (0.98, 0.98, 0.98, 1)
        surface_bg = (0.20, 0.20, 0.20, 1) if is_dark else (1, 1, 1, 1)
        primary_text = (0.92, 0.92, 0.92, 1) if is_dark else (0.12, 0.12, 0.12, 1)
        icon_text = (0.92, 0.92, 0.92, 1) if is_dark else (0.20, 0.20, 0.20, 1)
        delete_text = (1.0, 0.45, 0.45, 1) if is_dark else (0.75, 0.05, 0.05, 1)
        self._surface_bg = surface_bg
        self._primary_text = primary_text
        self._icon_text = icon_text
        self._delete_text = delete_text
        # Remove default popup texture so edge/border follows theme color cleanly.
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.title_color = primary_text

        # Rounded popup body to match the rest of the app styling.
        body = MDCard(
            orientation="vertical",
            radius=[16, 16, 16, 16],
            padding="12dp",
            spacing="12dp",
            md_bg_color=popup_bg,
        )
        self.content = body

        body.add_widget(
            MDLabel(
                text="Manage Categories",
                size_hint_y=None,
                height="28dp",
                halign="left",
                valign="middle",
                theme_text_color="Custom",
                text_color=self._primary_text,
                bold=True,
            )
        )

        body.add_widget(
            Factory.MDSeparator(
                height="1dp",
                size_hint_y=None,
                color=(0.35, 0.35, 0.35, 1) if is_dark else (0.80, 0.80, 0.80, 1),
            )
        )

        # Scrollable list area
        self.list_area = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
        )
        self.list_area.bind(minimum_height=self.list_area.setter("height"))

        from kivy.metrics import dp
        from kivy.uix.scrollview import ScrollView

        from views.main_window.scroll_bar_theme import scroll_bar_pair, scroll_list_gesture_kwargs

        bar_color, bar_inactive_color = scroll_bar_pair(is_dark)
        scroll = ScrollView(
            do_scroll_y=True,
            do_scroll_x=False,
            bar_width=dp(14),
            scroll_type=["bars", "content"],
            bar_color=bar_color,
            bar_inactive_color=bar_inactive_color,
            **scroll_list_gesture_kwargs(),
        )
        scroll.add_widget(self.list_area)

        body.add_widget(scroll)

        # Close button
        body.add_widget(
            MDRaisedButton(
                text="Close",
                size_hint_y=None,
                height="48dp",
                md_bg_color=(0.35, 0.35, 0.35, 1) if is_dark else (0.25, 0.45, 0.85, 1),
                on_release=lambda inst: self.dismiss(),
            )
        )

        self.refresh()

    def _delete_and_refresh(self, category):
        """Delete category, refresh popup, refresh main UI."""
        self.mainwindow.delete_category(category)
        self.refresh()

    def _move_and_refresh(self, category, direction: str):
        if direction == "up":
            result = self.mainwindow.cat_controller.move_category_up(category.id)
        else:
            result = self.mainwindow.cat_controller.move_category_down(category.id)
        if hasattr(result, "success") and not result.success:
            self.mainwindow.show_error(result.error)
            return
        self.mainwindow.refresh_ui(reload_categories=True, refresh_category_popup=False)
        self.refresh()

    def refresh(self):
        """Rebuild the category list."""
        self.list_area.clear_widgets()
        categories = self.mainwindow.cat_controller.load_categories()

        for cat in categories:
            # Skip system categories
            if cat.name.lower() in ("todo", "done"):
                continue

            rgba = get_color(cat.color)["rgba"]

            row = MDCard(
                orientation="horizontal",
                padding="8dp",
                radius=12,
                size_hint_y=None,
                height="60dp",
                md_bg_color=self._surface_bg,
            )

            # Color swatch
            row.add_widget(
                MDCard(
                    size_hint=(None, None),
                    width="40dp",
                    height="40dp",
                    radius=8,
                    md_bg_color=rgba,
                    elevation=2,
                )
            )

            # Category name (display‑side capitalization)
            row.add_widget(
                MDLabel(
                    text=" ".join(word.capitalize() for word in cat.name.split()),
                    halign="left",
                    valign="middle",
                    theme_text_color="Custom",
                    text_color=self._primary_text,
                )
            )

            # Edit button
            row.add_widget(
                MDIconButton(
                    icon="pencil",
                    theme_text_color="Custom",
                    text_color=self._icon_text,
                    on_release=lambda inst, c=cat: self.mainwindow.open_edit_category(c),
                )
            )

            # Move up button
            row.add_widget(
                MDIconButton(
                    icon="chevron-up",
                    theme_text_color="Custom",
                    text_color=self._icon_text,
                    on_release=lambda inst, c=cat: self._move_and_refresh(c, "up"),
                )
            )

            # Move down button
            row.add_widget(
                MDIconButton(
                    icon="chevron-down",
                    theme_text_color="Custom",
                    text_color=self._icon_text,
                    on_release=lambda inst, c=cat: self._move_and_refresh(c, "down"),
                )
            )

            # Delete button
            row.add_widget(
                MDIconButton(
                    icon="trash-can",
                    theme_text_color="Custom",
                    text_color=self._delete_text,
                    on_release=lambda inst, c=cat: self._delete_and_refresh(c),
                )
            )

            self.list_area.add_widget(row)
