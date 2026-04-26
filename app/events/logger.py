import os
import inspect
from app.utils import Dir
from app.models import Log, LogLevel
from app.events.worker import Worker
from typing import Any, Callable, Optional


class Logger:
    def __init__(self, dir: Dir, worker: Worker):
        self._directory = dir
        self._worker = worker
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

    def info(self, msg: str):
        self._log(LogLevel.INFO, msg)

    def debug(self, msg: str):
        self._log(LogLevel.DEBUG, msg)

    def warn(self, msg: str):
        self._log(LogLevel.WARNING, msg)

    def error(self, msg: str, err: Optional[Any] = None):
        self._log(LogLevel.ERROR, msg, err)

    def subscribe(self, callback: Callable[[Log], None]):
        self._worker.subscribe(callback)
