# views/main_window/category_view.py

from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel


def populate_category_manager(self):
    """Populate the Manage Categories screen."""
    if "category_list" not in self.ids:
        return

    self.ids.category_list.clear_widgets()

    categories = self.cat_controller.load_categories()

    for cat in categories:
        item = OneLineIconListItem(
            text=f"{cat.name} ({cat.color})",
            on_release=lambda inst, c=cat: print(f"Selected category: {c.name}"),
        )
        icon = IconLeftWidget(icon="folder")
        item.add_widget(icon)
        self.ids.category_list.add_widget(item)


def open_category_manager(self):
    """Switch to the Manage Categories screen."""
    populate_category_manager(self)
    self.ids.screen_manager.current = "ManageCategories"


def create_category(self, name, color_key, *, source="nav"):
    """Create a new category and update UI depending on source."""
    result = self.cat_controller.add_category(name, color_key)

    if not result.success:
        Popup(
            title="Error",
            content=MDLabel(text=result.error),
            size_hint=(0.6, 0.3),
        ).open()
        return

    new_cat = result.return_val

    # Refresh dashboard + tasks
    self.load_existing_tasks()
    from views.main_window.dashboard_view import update_dashboard
    update_dashboard(self)

    # Close dropdowns if open
    if hasattr(self, "category_menu"):
        self.category_menu.dismiss()
    if hasattr(self, "edit_category_menu"):
        self.edit_category_menu.dismiss()

    # Handle context
    if source == "nav":
        populate_category_manager(self)
        self.ids.screen_manager.current = "ManageCategories"

    elif source == "add_task":
        self.selected_category = new_cat
        self.category_field.text = new_cat.name

    elif source == "edit_task":
        self.edit_selected_category = new_cat
        self.edit_category_field.text = new_cat.name
