"""Persist KivyMD theme style (Light / Dark) under ``src/data``."""
from __future__ import annotations

import json
import pathlib

_DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
_PREFERENCE_FILE = _DATA_DIR / "theme_style.json"

_DEFAULT = "Light"
_VALID = frozenset({"Light", "Dark"})

# Light mode: explicitly darker blue. Dark mode: keep bluish-teal behavior.
_PRIMARY_HUE_LIGHT_BLUE = "700"
_PRIMARY_HUE_DARK_TEAL = "600"
_LIGHT_BLUE_MUTE_BLEND = 0.03
_DARK_TEAL_MUTE_BLEND = 0.18
_TEAL_TOWARD_CYAN = 0.30
# Light mode only: nudge Blue toward Indigo for a more royal-blue cast.
_LIGHT_BLUE_TOWARD_INDIGO = 0.28


def _mix_hex(a: str, b: str, t: float) -> str:
    """Linear mix of two ``RRGGBB`` strings (no ``#``), ``t`` in ``[0, 1]``."""
    ar = int(a[0:2], 16) / 255.0
    ag = int(a[2:4], 16) / 255.0
    ab = int(a[4:6], 16) / 255.0
    br = int(b[0:2], 16) / 255.0
    bg = int(b[2:4], 16) / 255.0
    bb = int(b[4:6], 16) / 255.0
    r = ar * (1.0 - t) + br * t
    g = ag * (1.0 - t) + bg * t
    bl = ab * (1.0 - t) + bb * t
    return f"{int(r * 255):02X}{int(g * 255):02X}{int(bl * 255):02X}"


def _lighten_hex_six(hex_six: str, *, toward_white: float) -> str:
    """Return 6 hex chars (no ``#``), blending RGB toward white."""
    r = int(hex_six[0:2], 16) / 255.0
    g = int(hex_six[2:4], 16) / 255.0
    b = int(hex_six[4:6], 16) / 255.0
    t = toward_white
    r = r + (1.0 - r) * t
    g = g + (1.0 - g) * t
    b = b + (1.0 - b) * t
    return f"{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"


def sync_primary_theme(app) -> None:
    """
    Light mode: darker Blue (700). Dark mode: bluish Teal (Teal mixed toward Cyan).
    Rebuilds from KivyMD defaults so toggling theme does not accumulate drift.
    """
    from kivymd.color_definitions import colors as md

    dest = app.theme_cls.colors
    if app.theme_cls.theme_style == "Dark":
        app.theme_cls.primary_palette = "Teal"
        base = dict(md["Teal"])
        cyan = md["Cyan"]
        merged: dict[str, str] = {}
        for k, v in base.items():
            if k in cyan:
                v = _mix_hex(v, cyan[k], _TEAL_TOWARD_CYAN)
            merged[k] = _lighten_hex_six(v, toward_white=_DARK_TEAL_MUTE_BLEND)
        dest["Teal"] = merged
        app.theme_cls.primary_hue = _PRIMARY_HUE_DARK_TEAL
    else:
        app.theme_cls.primary_palette = "Blue"
        base = dict(md["Blue"])
        indigo = md["Indigo"]
        dest["Blue"] = {
            k: _lighten_hex_six(
                _mix_hex(v, indigo[k], _LIGHT_BLUE_TOWARD_INDIGO),
                toward_white=_LIGHT_BLUE_MUTE_BLEND,
            )
            for k, v in base.items()
        }
        app.theme_cls.primary_hue = _PRIMARY_HUE_LIGHT_BLUE


def load_theme_style() -> str:
    """Return ``\"Light\"`` or ``\"Dark\"``; default Light if missing or invalid."""
    try:
        raw = _PREFERENCE_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        v = data.get("theme_style", _DEFAULT)
        return v if v in _VALID else _DEFAULT
    except (OSError, json.JSONDecodeError, TypeError, AttributeError):
        return _DEFAULT


def save_theme_style(theme_style: str) -> None:
    """Write preference; invalid values are stored as Light."""
    if theme_style not in _VALID:
        theme_style = _DEFAULT
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        _PREFERENCE_FILE.write_text(
            json.dumps({"theme_style": theme_style}, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass
