"""
Shared theme, layout constants, and factories for the hamburger menu and cascade submenus.
"""
from __future__ import annotations

from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu

# --- Shared MDDropdownMenu chrome (matches prior hardcoded values) ---
NAV_DROPDOWN_WIDTH_MULT = 4
NAV_DROPDOWN_RADIUS = (12, 12, 12, 12)
NAV_DROPDOWN_ELEVATION = 4

# --- Cascade anchor math (KivyMD default row height is typically 48dp; separators 1dp in menu data) ---
# Center of the top list row: half a row down from the panel top.
DEFAULT_MENU_ROW_HALF_HEIGHT_DP = 24
# Main nav order from bottom: Theme row · sep · "Manage Categories" row center ≈ 48 + 1 + 24.
MANAGE_ROW_CENTER_FROM_BOTTOM_DP = 73
# Horizontal: align with the ">" column near the right edge of the panel.
RIGHT_EDGE_FRACTION = 0.94
# Fallback when the main menu was not measurable (width_mult menus often end up ~240dp wide).
ESTIMATED_MENU_WIDTH_DP = 240
# Invisible Window anchor used as MDDropdownMenu caller for positioning.
NAV_SUBMENU_ANCHOR_WIDTH_DP = 2
NAV_SUBMENU_ANCHOR_HEIGHT_DP = 40
MIN_NAV_HEIGHT_FOR_ANCHOR_DP = 24
# Fallback vertical offsets from the hamburger bottom (window coords) when geometry is missing.
FALLBACK_VIEW_ROW_OFFSET_FROM_BTN_BOTTOM_DP = 36
FALLBACK_MANAGE_ROW_OFFSET_FROM_BTN_BOTTOM_DP = 96


def _is_app_dark() -> bool:
    return App.get_running_app().theme_cls.theme_style == "Dark"


def nav_menu_text_color(is_dark: bool | None = None) -> tuple[float, float, float, float]:
    if is_dark is None:
        is_dark = _is_app_dark()
    return (0.92, 0.92, 0.92, 1) if is_dark else (0.1, 0.1, 0.1, 1)


def nav_menu_surface_bg(is_dark: bool | None = None, *, submenu: bool = False) -> tuple[float, float, float, float]:
    if is_dark is None:
        is_dark = _is_app_dark()
    if is_dark:
        return (0.18, 0.18, 0.18, 1)
    return (0.94, 0.94, 0.94, 1) if submenu else (0.97, 0.97, 0.97, 1)


def nav_menu_item_style(is_dark: bool | None = None) -> dict:
    """Merge into each ``OneLineListItem`` menu item dict."""
    if is_dark is None:
        is_dark = _is_app_dark()
    return {
        "theme_text_color": "Custom",
        "text_color": nav_menu_text_color(is_dark),
    }


def make_nav_dropdown(caller, items: list, *, submenu: bool = False, **extra) -> MDDropdownMenu:
    """Build a themed :class:`~kivymd.uix.menu.MDDropdownMenu` with shared chrome."""
    is_dark = _is_app_dark()
    kwargs = {
        "caller": caller,
        "items": items,
        "width_mult": NAV_DROPDOWN_WIDTH_MULT,
        "md_bg_color": nav_menu_surface_bg(is_dark, submenu=submenu),
        "radius": list(NAV_DROPDOWN_RADIUS),
        "elevation": NAV_DROPDOWN_ELEVATION,
    }
    kwargs.update(extra)
    return MDDropdownMenu(**kwargs)
