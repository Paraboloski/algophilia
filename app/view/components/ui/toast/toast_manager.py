from __future__ import annotations

import time
import threading
import flet as ft
from typing import Optional
from app.view.components.ui.toast.toast_card import Toast
from app.view.components.ui.toast.toast_card import ToastCard
from app.view.components.ui.toast.toast_classes import Level, CLASSES

class ToastManager:
    def __init__(self, page: ft.Page, safe_area_top: int) -> None:
        self._page    = page
        self._active: list[Toast]                = []
        self._queue:  list[Toast]                = []
        self._timers: dict[str, threading.Timer] = {}

        self._col = ft.Column(
            controls=[],
            spacing =8,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        page.overlay.append(ft.Container(
            content=self._col,
            top    =safe_area_top,
            left   =12,
            right  =12,
        ))

    def info(self, message: str, title: Optional[str] = None) -> None:
        self.show(message, Level.INFO, title)

    def warning(self, message: str, title: Optional[str] = None) -> None:
        self.show(message, Level.WARNING, title)

    def error(self, message: str, title: Optional[str] = None) -> None:
        self.show(message, Level.ERROR, title)

    def show(self, message: str, level: Level, title: Optional[str] = None) -> None:
        toast = Toast.make(message, level, title)
        if len(self._active) < 3:
            self._mount(toast)
        else:
            self._queue.append(toast)

    def _mount(self, toast: Toast) -> None:
        self._active.append(toast)
        theme   = CLASSES[toast.level]

        self._col.controls.append(ToastCard(toast=toast, page=self._page, on_dismiss=self._dismiss))
        self._page.update()

        if theme.duration is not None:
            def auto_dismiss():
                time.sleep(float(theme.duration or 0))
                self._dismiss(toast.id)
            
            self._page.run_thread(auto_dismiss)

    def _dismiss(self, toast_id: str) -> None:
        timer = self._timers.pop(toast_id, None)
        if timer:
            timer.cancel()

        self._active = [t for t in self._active if t.id != toast_id]
        self._col.controls = [
            c for c in self._col.controls
            if getattr(c, "data", None) != toast_id
        ]

        if self._queue:
            self._mount(self._queue.pop(0))

        try:
            self._page.update()
        except Exception:
            pass