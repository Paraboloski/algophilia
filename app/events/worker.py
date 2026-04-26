import threading
from queue import Queue
from app.models import Log
from typing import Callable, Optional


class Worker:
    def __init__(self):
        self._queue: Queue[Optional[Log]] = Queue()
        self._subscribers: list[Callable[[Log], None]] = []

        self._thread = threading.Thread(
            target=self._process_queue, daemon=True)
        self._thread.start()

    def subscribe(self, callback: Callable[[Log], None]):
        self._subscribers.append(callback)

    def dispatch(self, log: Log):
        self._queue.put(log)

    def _process_queue(self):
        while True:
            log = self._queue.get()

            if log is None:
                self._queue.task_done()
                break

            for sub in self._subscribers:
                threading.Thread(target=sub, args=(log,), daemon=True).start()

            self._queue.task_done()

    def shutdown(self):
        self._queue.put(None)
        self._queue.join()
