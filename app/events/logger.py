import os
import inspect
from app.utils import Dir
from app.models import Log, LogLevel
from app.events.worker import Worker
from typing import Any, Callable, Optional


class Logger:
    def __init__(self, directory: Dir, worker: Worker):
        self._worker = worker
        self._directory = directory
        self._worker.subscribe(self._write)

    def _write(self, log: Log):
        self._directory.write(f"{log.level.value}.log", str(log))

    def _origin(self) -> tuple[str, int]:
        info = inspect.stack()[3]
        return os.path.basename(info.filename), info.lineno

    def _log(self, level: LogLevel, message: str, error: Optional[Any] = None):
        origin, line = self._origin()

        log = Log(
            level=level,
            message=message,
            line=line,
            origin=origin,
            exception=str(error) if error else None,
        )

        self._worker.dispatch(log)

    def info(self, message: str):
        self._log(LogLevel.INFO, message)

    def debug(self, message: str):
        self._log(LogLevel.DEBUG, message)

    def warn(self, message: str):
        self._log(LogLevel.WARNING, message)

    def error(self, message: str, err: Optional[Any] = None):
        self._log(LogLevel.ERROR, message, err)

    def subscribe(self, f: Callable[[Log], Any]):
        self._worker.subscribe(f)
