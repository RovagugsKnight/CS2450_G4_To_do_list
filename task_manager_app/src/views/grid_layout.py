from views.spacer import Spacer

def normalize_grid(layout, cols=3):
    # Only pad with spacers so that len(children) % cols == 0
    remainder = len(layout.children) % cols
    if remainder != 0:
        needed = cols - remainder
        for _ in range(needed):
            layout.add_widget(Spacer())
