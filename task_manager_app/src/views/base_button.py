from kivymd.uix.button import MDRaisedButton
from views.colors import get_color


class BaseButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        """# Remove default Kivy textures
        self.background_normal = ""
        self.background_down = ""

        # Remove border artifacts
        self.border = (0, 0, 0, 0)"""

        # Default text color
        self.text_color = get_color('White')
   