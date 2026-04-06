from kivy.uix.button import Button  
from views.colors import Black_transparent, get_color
from kivy.metrics import dp 

class YellowButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = '' 
        self.background_color = get_color('Yellow')
        self.text_color = 'black'    
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


