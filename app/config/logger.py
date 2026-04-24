import inspect
from enum import Enum
from typing import IO
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

class Level(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    WARNING = "WARNING"

@dataclass
class Log:
    message:   str
    level:     Level
    target_class:    str = ""
    line_of_code:      int = 0
    exception: BaseException | None = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        loc = f"{self.target_class}:{self.line_of_code}" if self.target_class else "?"
        exc = f"\n  ↳ {type(self.exception).__name__}: {self.exception}" if self.exception else ""
        return f"[{ts}] [{self.level.value:<7}] [{loc}] {self.message}{exc}"


class Logger:
    def __init__(self):
        self._i:     int = 0
        self._flush_every: int = 10
        self._logs:     list[Log] = []
        self._max_log_number: int = 200
        self._levels:     dict[Level, IO[str]] = {}
        
    def init(self, base_dir: Path) -> None:
        _dir = base_dir / "logs"
        _dir.mkdir(exist_ok=True)

        for level in Level:
            path = _dir / f"{level.value.lower()}.log"
            self._levels[level] = path.open("a", encoding="utf-8", buffering=1)

    def shutdown(self) -> None:
        for level in self._levels.values():
            try:
                level.flush()
                level.close()
            except Exception:
                pass
        self._levels.clear()

    def debug(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.DEBUG, message, exc)

    def info(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.INFO, message, exc)

    def warning(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.WARNING, message, exc)

    def error(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.ERROR, message, exc)

    def _log(self, level: Level, message: str, exc: BaseException | None) -> None:
        root = inspect.stack()[2]
        target_class = self._resolve_target_class(root)
        line_of_code = root.lineno

        log = Log(level=level, message=message, target_class=target_class,
                         line_of_code=line_of_code, exception=exc)

        self._logs.append(log)
        if len(self._logs) > self._max_log_number:
            self._logs.pop(0)

        print(log)
        self._write(log)

    def _write(self, log: Log) -> None:
        level = self._levels.get(log.level)
        if level is None:
            return
        try:
            level.write(str(log) + "\n")
            self._i += 1
            if log.level == Level.ERROR or self._i >= self._flush_every:
                level.flush()
                self._i = 0
        except Exception as e:
            print(f"[Logger] Scrittura fallita: {e}")

    def _resolve_target_class(self, root: inspect.FrameInfo) -> str:
        local_self = root.frame.f_locals.get("self")

        local_cls = root.frame.f_locals.get("cls")

        if local_self is not None:
            cls_name = type(local_self).__name__

        elif local_cls is not None:
            cls_name = local_cls.__name__
        else:
            cls_name = root.frame.f_globals.get("__name__", "?")

        return f"{cls_name}.{root.function}"

    def all(self) -> list[Log]:
        return list(self._logs)

    def filter(self, level: Level) -> list[Log]:
        return [e for e in self._logs if e.level == level]

    def errors(self) -> list[Log]:
        return self.filter(Level.ERROR)

    def clear(self) -> None:
        self._logs.clear()

    def __len__(self) -> int:
        return len(self._logs)


logger = Logger()
