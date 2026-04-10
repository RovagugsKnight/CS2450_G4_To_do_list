"""
Modern, minimal, light‑mode friendly palette
"""

color_dict = {
    "white": {
    "label": "White",
    "rgba": (1, 1, 1, 1)
    },
    "amber": {
        "label": "Amber",
        "rgba": (0.98, 0.82, 0.40, 1),
    },
    "rose": {
        "label": "Rose",
        "rgba": (0.94, 0.55, 0.55, 1),
    },
    "teal": {
        "label": "Teal",
        "rgba": (0.35, 0.70, 0.70, 1),
    },
    "blue": {
        "label": "Blue",
        "rgba": (0.55, 0.70, 0.90, 1),
    },
    "mint": {
        "label": "Mint",
        "rgba": (0.70, 0.90, 0.70, 1),
    },
    "lavender": {
        "label": "Lavender",
        "rgba": (0.78, 0.70, 0.90, 1),
    },
    "gray": {
        "label": "Gray",
        "rgba": (0.85, 0.85, 0.85, 1),
    },
}

"""
Utility: get RGBA from palette key
"""
def get_color(key: str):
    """Return RGBA for a palette key."""
    key = key.lower().replace(" ", "_")
    if key in color_dict:
        return color_dict[key]
    raise ValueError(f"Color '{key}' not available")


"""
Semantic defaults for your app
"""
DEFAULT_CATEGORY_COLOR = "teal"   # main todo
DONE_CATEGORY_COLOR = "gray"      # auto-done
