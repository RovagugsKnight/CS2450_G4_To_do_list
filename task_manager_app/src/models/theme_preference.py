"""Persist KivyMD theme style (Light / Dark) under ``src/data``."""
from __future__ import annotations

import json
import pathlib

_DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
_PREFERENCE_FILE = _DATA_DIR / "theme_style.json"

_DEFAULT = "Light"
_VALID = frozenset({"Light", "Dark"})


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
