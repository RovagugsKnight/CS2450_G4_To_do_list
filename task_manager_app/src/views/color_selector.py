from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.properties import StringProperty
from kivy.logger import Logger


class ColorSelector(MDBoxLayout):
    """
    Displays color swatches and returns selected color key.
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
        """
        Build a row of color buttons based on the color_dict.
        Skips 'white' because it's not allowed as a category color.
        """
        for key, data in self.color_dict.items():

            # Skip white — not allowed for categories
            if key == "white":
                continue

            rgba = data["rgba"]

            btn = MDRaisedButton(
                text=data["label"],
                md_bg_color=rgba,
                size_hint=(None, None),
                width="90dp",
                height="40dp",
            )

            # Bind selection
            btn.bind(on_release=lambda inst, k=key: self._select_color(k))
            self.add_widget(btn)

    def _select_color(self, key: str):
        Logger.info(f"ColorSelector: Selected color key = {key}")
        self.selected_color_key = key

    def get_selected_color_key(self) -> str:
        return self.selected_color_key
