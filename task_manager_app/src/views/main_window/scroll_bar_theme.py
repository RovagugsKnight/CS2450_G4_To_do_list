"""ScrollView scrollbar colors: high-contrast thumbs for dark / light UI."""
from __future__ import annotations

# Active (while dragging / focused) vs idle — both stay fairly opaque so bars remain visible.
BAR_ACTIVE_DARK = (0.80, 0.80, 0.90, 1.0)
BAR_INACTIVE_DARK = (0.55, 0.56, 0.65, 0.94)

BAR_ACTIVE_LIGHT = (0.20, 0.26, 0.36, 1.0)
BAR_INACTIVE_LIGHT = (0.42, 0.46, 0.55, 0.94)


def scroll_bar_pair(is_dark: bool) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    """Return ``(bar_color, bar_inactive_color)`` for the current theme."""
    if is_dark:
        return (BAR_ACTIVE_DARK, BAR_INACTIVE_DARK)
    return (BAR_ACTIVE_LIGHT, BAR_INACTIVE_LIGHT)


# Kivy's default scroll_timeout (~55ms) is short: if the finger has not moved
# scroll_distance yet, the touch is handed to children (MDCards, ButtonBehavior
# task rows), which blocks parent scrolling. Longer window + slightly lower
# threshold makes drags over interactive content register as scroll reliably.
SCROLL_TIMEOUT_MS = 200
SCROLL_DISTANCE_DP = 12


def scroll_gesture_kwargs() -> dict:
    """Keyword args for ``ScrollView`` touch tuning (Python-built views)."""
    from kivy.metrics import dp

    return {
        "scroll_timeout": SCROLL_TIMEOUT_MS,
        "scroll_distance": dp(SCROLL_DISTANCE_DP),
    }


# Stronger tuning for scroll areas full of ``TaskItem`` / controls (Today's Tasks, Kanban columns).
LIST_SCROLL_TIMEOUT_MS = 350
LIST_SCROLL_DISTANCE_DP = 8


def scroll_list_gesture_kwargs() -> dict:
    """Touch tuning for list-heavy ``ScrollView``s (task cards steal touches easily)."""
    from kivy.metrics import dp

    return {
        "scroll_timeout": LIST_SCROLL_TIMEOUT_MS,
        "scroll_distance": dp(LIST_SCROLL_DISTANCE_DP),
    }
