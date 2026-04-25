from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from app.config import settings

class Level(Enum):
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Theme:
    border_color: str
    bg_light:     str
    bg_dark:      str
    icon:         Path
    duration_s:   Optional[int]


CLASSES: dict[Level, Theme] = {
    Level.INFO: Theme(
        border_color=settings.APP_PAGE_INFO_LIGHT_COLOR,
        bg_light=settings.APP_PAGE_BG_LIGHT_COLOR,
        bg_dark=settings.APP_PAGE_INFO_DARK_COLOR,
        icon=settings.APP_PAGE_INFO_ICON,
        duration_s=4,
    ),
    Level.WARNING: Theme(
        border_color=settings.APP_PAGE_WARNING_LIGHT_COLOR,
        bg_light=settings.APP_PAGE_BG_LIGHT_COLOR,
        bg_dark=settings.APP_PAGE_WARNING_DARK_COLOR,
        icon=settings.APP_PAGE_WARNING_ICON,
        duration_s=7,
    ),
    Level.ERROR: Theme(
        border_color=settings.APP_PAGE_ERROR_LIGHT_COLOR,
        bg_light=settings.APP_PAGE_BG_LIGHT_COLOR,
        bg_dark=settings.APP_PAGE_ERROR_DARK_COLOR,
        icon=settings.APP_PAGE_ERROR_ICON,
        duration_s=None,
    ),
}
