from kivy.uix.popup import Popup
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from views.colors import get_color
from views.category_creator import CategoryCreator


class ManageCategoriesPopup(Popup):
    """
    Popup that lists all categories with Edit/Delete controls.
    """

    def __init__(self, mainwindow, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = mainwindow
        self.title = "Manage Categories"
        self.size_hint = (0.9, 0.9)

        root = MDBoxLayout(orientation="vertical", spacing="12dp", padding="12dp")
        self.content = root

        # Scrollable list area
        self.list_area = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
        )
        self.list_area.bind(minimum_height=self.list_area.setter("height"))

        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(do_scroll_y=True)
        scroll.add_widget(self.list_area)

        root.add_widget(scroll)

        # Close button
        root.add_widget(
            MDRaisedButton(
                text="Close",
                size_hint_y=None,
                height="48dp",
                on_release=lambda inst: self.dismiss(),
            )
        )

        self.refresh()

    def _delete_and_refresh(self, category):
        """Delete category, refresh popup, refresh main UI."""
        self.mainwindow.delete_category(category)
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
                md_bg_color=(1, 1, 1, 1),
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
                )
            )

            # Edit button
            row.add_widget(
                MDIconButton(
                    icon="pencil",
                    on_release=lambda inst, c=cat: self.mainwindow.open_edit_category(c),
                )
            )

            # Delete button
            row.add_widget(
                MDIconButton(
                    icon="trash-can",
                    on_release=lambda inst, c=cat: self._delete_and_refresh(c),
                )
            )

            self.list_area.add_widget(row)
