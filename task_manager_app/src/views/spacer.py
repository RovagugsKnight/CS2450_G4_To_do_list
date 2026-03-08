from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_file("views/spacer.kv")

class Spacer(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    