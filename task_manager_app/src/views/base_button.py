from kivy.uix.button import Button
from views.colors import White


class BaseButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Remove default Kivy textures
        self.background_normal = ""
        self.background_down = ""

        # Remove border artifacts
        self.border = (0, 0, 0, 0)

        # Default text color
        self.color = White
   