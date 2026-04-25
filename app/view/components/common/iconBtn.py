import flet as ft
from pathlib import Path
from typing import Callable
from app.view.components.common.icon import Icon


def IconButton(
    icon: Path,
    color: str,
    icon_size: int,
    on_click: Callable,
    overlay_opacity: float
) -> ft.IconButton:
    return ft.IconButton(
        icon=Icon(
            path=icon,
            size=icon_size,
        ),
        on_click=on_click,
        style=ft.ButtonStyle(
            padding=ft.padding.all(2),
            overlay_color=ft.Colors.with_opacity(overlay_opacity, color)
        ),
    )
