from views.base_button import BaseButton
from views.colors import Yellow, Red, Light_teal, Black, White

class YellowButton(BaseButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Yellow
        self.color = Black

class RedButton(BaseButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Red

class LightTealButton(BaseButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Light_teal