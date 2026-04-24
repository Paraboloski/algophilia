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
class LogEntry:
    message:   str
    level:     Level
    line:      int = 0
    caller:    str = ""
    exception: BaseException | None = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        loc = f"{self.caller}:{self.line}" if self.caller else "?"
        exc = f"\n  ↳ {type(self.exception).__name__}: {self.exception}" if self.exception else ""
        return f"[{ts}] [{self.level.value:<7}] [{loc}] {self.message}{exc}"


class Logger:
    def __init__(self, max_entries: int = 200, flush_every: int = 10):
        self._entries:     list[LogEntry] = []
        self._max_entries: int = max_entries
        self._flush_every: int = flush_every
        self._pending:     int = 0
        self._handles:     dict[Level, IO[str]] = {}

    def init(self, base_dir: Path) -> None:
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        for level in Level:
            path = logs_dir / f"{level.value.lower()}.log"
            self._handles[level] = path.open("a", encoding="utf-8", buffering=1)

    def shutdown(self) -> None:
        for handle in self._handles.values():
            try:
                handle.flush()
                handle.close()
            except Exception:
                pass
        self._handles.clear()

    def debug(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.DEBUG, message, exc)

    def info(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.INFO, message, exc)

    def warning(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.WARNING, message, exc)

    def error(self, message: str, exc: BaseException | None = None) -> None:
        self._log(Level.ERROR, message, exc)

    def _log(self, level: Level, message: str, exc: BaseException | None) -> None:
        frame = inspect.stack()[2]
        caller = self._resolve_caller(frame)
        line = frame.lineno

        entry = LogEntry(level=level, message=message,caller=caller, line=line, exception=exc)

        self._entries.append(entry)
        if len(self._entries) > self._max_entries: self._entries.pop(0)

        print(entry)
        self._write(entry)

    def _write(self, entry: LogEntry) -> None:
        handle = self._handles.get(entry.level)
        if handle is None:
            return
        try:
            handle.write(str(entry) + "\n")
            self._pending += 1
            if entry.level == Level.ERROR or self._pending >= self._flush_every:
                handle.flush()
                self._pending = 0
        except Exception as e:
            print(f"[Logger] Scrittura fallita: {e}")

    def _resolve_caller(self, frame: inspect.FrameInfo) -> str:
        local_self = frame.frame.f_locals.get("self")
        local_cls = frame.frame.f_locals.get("cls")
        if local_self is not None: cls_name = type(local_self).__name__
        elif local_cls is not None: cls_name = local_cls.__name__
        else: cls_name = frame.frame.f_globals.get("__name__", "?")
        return f"{cls_name}.{frame.function}"

    def all(self) -> list[LogEntry]:
        return list(self._entries)

    def filter(self, level: Level) -> list[LogEntry]:
        return [e for e in self._entries if e.level == level]

    def errors(self) -> list[LogEntry]:
        return self.filter(Level.ERROR)

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)

logger = Logger()
