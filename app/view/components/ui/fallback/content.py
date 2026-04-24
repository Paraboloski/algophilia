import flet as ft
from typing import cast
from app.config import settings

from app.view.components.common import (
    Label,
    Title,
    Divider
)

def Content(title: str, message: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=cast(list, [
                Title(title, settings.APP_PAGE_MAIN_COLOR, "Cinzel Black", 50, ft.TextAlign.CENTER),
                Divider(settings.APP_PAGE_MAIN_COLOR, 4, 80),
                Label(message, settings.APP_PAGE_MAIN_COLOR,"Cinzel Medium", 10, 4, ft.TextAlign.CENTER),
            ]),
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30
        ),
        alignment=ft.Alignment(0, 0)
    )
