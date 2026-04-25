from __future__ import annotations

import uuid
from typing import Optional
from dataclasses import dataclass
from app.view.components.ui.toast.toast_classes import Level

@dataclass
class Toast:
    id:      str
    message: str
    level:   Level
    title:   Optional[str]

    @staticmethod
    def make(message: str, level: Level, title: Optional[str] = None) -> "Toast":
        return Toast(id=str(uuid.uuid4()), message=message, level=level, title=title)
