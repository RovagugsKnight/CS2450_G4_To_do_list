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
        self._buttons = []
        self._build_swatches()

        # Default to first non-white color if nothing selected
        if self.selected_color_key is None and self._buttons:
            first_key = self._buttons[0][0]
            self._select_color(first_key)

    def _build_swatches(self):
        """
        Build a row of color buttons based on the color_dict.
        Skips 'white' because it's not allowed as a category color.
        """
        for key, data in self.color_dict.items():
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

            btn.bind(on_release=lambda inst, k=key: self._select_color(k))
            self.add_widget(btn)
            self._buttons.append((key, btn))

    def _select_color(self, key: str):
        Logger.info(f"ColorSelector: Selected color key = {key}")
        self.selected_color_key = key

    def get_selected_color_key(self) -> str:
        return self.selected_color_key
