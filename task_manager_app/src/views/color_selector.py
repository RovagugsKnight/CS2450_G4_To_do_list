from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.properties import StringProperty
from kivy.logger import Logger

"""
COLOR SELECTOR
"""

class ColorSelector(MDBoxLayout):
    """
    A simple color selection widget that displays color swatches
    based on the provided color dictionary. Returns the selected
    color key (string).
    """

    selected_color_key = StringProperty(None)

    def __init__(self, color_dict: dict, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = "8dp"
        self.padding = "8dp"

        self.color_dict = color_dict
        self._build_swatches()

    def _build_swatches(self):
        """Create a button for each color in the palette."""
        for key, data in self.color_dict.items():

            # Skip white so users cannot select it
            if key == "white":
                continue

            rgba = data["rgba"]

            btn = MDRaisedButton(
                text=data["label"],
                md_bg_color=rgba,
                size_hint=(None, None),
                width="90dp",
                height="40dp",
                radius=[10, 10, 10, 10],
            )

            btn.bind(on_release=lambda inst, k=key: self._select_color(k))
            self.add_widget(btn)


    def _select_color(self, key: str):
        """Store the selected color key."""
        Logger.info(f"ColorSelector: Selected color key = {key}")
        self.selected_color_key = key

    def get_selected_color_key(self) -> str:
        """Return the selected color key."""
        return self.selected_color_key
