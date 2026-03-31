color_dict = {'black' : (0, 0, 0, 1),
'yellow' : (0.90, 0.82, 0.35, 1),
'red' : (0.8, 0.1, 0.1, 1),
'light teal' : (0, 0.41, 0.41, 1.0),
'white' : (1, 1, 1, 1),
}

def get_color(color: str):
    if color.lower() in color_dict:
        return color_dict[color.lower()]
    else:
        raise ValueError('Color not available')

Black_transparent = (0, 0, 0, 0)

