from enum import Enum as _Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

class Level(str, _Enum):
    INFO = "info"
    ERROR = "error"
    DEBUG = "debug"
    WARNING = "warning"

@dataclass(frozen=True)
class Log:
    line: int
    origin: str
    message: str
    level: Level
    exception: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return (
            f"[{self.timestamp.isoformat()}] {self.level.upper()} "
            f"[{self.origin}:{self.line}] {self.message}"
            f"{f' | EXCEPTION: {self.exception}' if self.exception else ''}"
        )
