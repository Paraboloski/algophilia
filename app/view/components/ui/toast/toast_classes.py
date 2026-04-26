from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional
from app.view.style import settings
from dataclasses import dataclass


class Level(Enum):
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Theme:
    border_color: str
    bg_light: str
    bg_dark: str
    icon: Path
    duration: Optional[int]


CLASSES: dict[Level, Theme] = {
    Level.INFO: Theme(
        border_color=settings._main_colors["info_light"],
        bg_light=settings._main_colors["bg_light"],
        bg_dark=settings._main_colors["info_dark"],
        icon=settings._main_icons["info"],
        duration=4,
    ),
    Level.WARNING: Theme(
        border_color=settings._main_colors["warning_light"],
        bg_light=settings._main_colors["bg_light"],
        bg_dark=settings._main_colors["warning_dark"],
        icon=settings._main_icons["warning"],
        duration=7,
    ),
    Level.ERROR: Theme(
        border_color=settings._main_colors["error_light"],
        bg_light=settings._main_colors["bg_light"],
        bg_dark=settings._main_colors["error_dark"],
        icon=settings._main_icons["error"],
        duration=None,
    ),
}
