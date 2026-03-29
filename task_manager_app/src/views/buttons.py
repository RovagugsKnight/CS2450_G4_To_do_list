from kivymd.uix.button import MDRaisedButton
from views.colors import get_color

class YellowButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color('Yellow')
        self.text_color = get_color('Black')

class RedButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color('Red')

class LightTealButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color('Light Teal')