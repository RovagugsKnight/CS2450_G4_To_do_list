from views.spacer import Spacer
from kivymd.uix.gridlayout import GridLayout

def normalize_grid(layout:GridLayout, cols:int =3):
    """pad last row with spacer objects to keep
    task widet size consistent"""
    # Only pad with spacers so that len(children) % cols == 0
    remainder = len(layout.children) % cols
    if remainder != 0:
        needed = cols - remainder
        for _ in range(needed):
            layout.add_widget(Spacer())
