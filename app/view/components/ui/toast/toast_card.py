from __future__ import annotations

import flet as ft
from app.config import logger, settings
from typing import Any, Callable
from app.view.components.ui.toast.toast import Toast
from app.view.components.ui.toast.toast_classes import CLASSES
from app.view.components.common import Icon, IconButton, Card, Title, Stripe, Label

def ToastCard(toast: Toast, bg: str, on_dismiss: Callable[[str], None]) -> ft.Container:
    theme = CLASSES[toast.level]

    stripe = Stripe(color=theme.border_color)

    icon = Icon(path=theme.icon, size=18)

    close_btn = IconButton(
        icon=settings.APP_PAGE_CLOSE_ICON,
        color=theme.border_color,
        icon_size=14,
        overlay_opacity=0.10,
        on_click=lambda _, tid=toast.id: on_dismiss(tid),
    )

    text_controls: list[ft.Control] = []
    if toast.title:
        text_controls.append(Title(
            value=toast.title,
            color=theme.border_color,
            font_family="default",
            size=12,
            text_align=ft.TextAlign.LEFT,
        ))
    text_controls.append(Label(
        value=toast.message,
        color=ft.Colors.ON_SURFACE,
        font_family="default",
        size=13,
        letter_spacing=0,
        text_align=ft.TextAlign.LEFT,
    ))

    body = ft.Row(
        controls=[
            icon,
            ft.Column(controls=text_controls, spacing=2,
                      expand=True, tight=True),
            close_btn,
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    inner = ft.Container(
        content=body,
        expand=True,
        padding=ft.padding.symmetric(horizontal=10, vertical=9),
        bgcolor=bg,
        border_radius=ft.border_radius.only(top_right=8, bottom_right=8),
    )

    row = ft.Row(controls=[stripe, inner], spacing=0)

    card = Card(
        content=row,
        border_radius=ft.border_radius.all(8),
        blur_radius=10,
        shadow_color=ft.Colors.with_opacity(0.14, ft.Colors.BLACK),
        shadow_offset=ft.Offset(0, 3),
    )

    _drag_x = [0.0]
    
    def _on_update(e: ft.DragUpdateEvent) -> None:
        dx = getattr(e, "delta_x", 0.0) or 0.0
        _drag_x[0] += dx

        card.offset = ft.Offset(_drag_x[0] / 100, 0)
        card.update()

    def _on_end(e: ft.DragEndEvent, tid: str = toast.id) -> None:
        velocity = getattr(e, "velocity_x", 0.0) or 0.0
        distance = _drag_x[0]
        _drag_x[0] = 0.0

        if abs(velocity) > 400 or abs(distance) > 64:
            on_dismiss(tid)

            if abs(velocity) > 400 or abs(distance) > 64:
                on_dismiss(tid)

    return ft.Container(
        data=toast.id,
        animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
        content=ft.GestureDetector(
            on_pan_update=_on_update,
            on_pan_end=_on_end,
            drag_interval=1,
            content=card,
        ),
    )