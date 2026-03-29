from kivy.uix.button import Button  
from views.colors import Black_transparent, get_color
from kivy.metrics import dp 

class YellowButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = '' 
        self.background_color = get_color('Yellow')
        self.color = get_color('Black')        
        self.md_bg_color = get_color('Yellow')     
        self._md_bg_color = get_color('Yellow')   
        self.line_color = Black_transparent
        self._line_color = Black_transparent
        self._line_color_disabled = Black_transparent
        self.line_width = 1
        self.radius = [0, 0, 0, 0]
        self._radius = 0

    def collide_point(self, x, y):
        pad = dp(20) 
        return (self.x - pad <= x <= self.right + pad and
                self.y - pad <= y <= self.top + pad)

class RedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color('Red')
        self.color = get_color('White')
        
        self.md_bg_color = get_color('Red')
        self._md_bg_color = get_color('Red')
        self.line_color = Black_transparent
        self._line_color = Black_transparent
        self._line_color_disabled = Black_transparent
        self.line_width = 1
        self.radius = [0, 0, 0, 0]
        self._radius = 0

class LightTealButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color('Light_teal')
        self.color = get_color('White')
        
        self.md_bg_color = get_color('Light_teal')
        self._md_bg_color = get_color('Light_teal')
        self.line_color = get_color('Black_transparent')
        self._line_color = get_color('Black_transparent')
        self._line_color_disabled = get_color('Black_transparent')
        self.line_width = 1
        self.radius = [0, 0, 0, 0]
        self._radius = 0