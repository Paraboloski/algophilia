import flet as ft
from app.view.components.ui.fallback.fallback_content import Content

def Page(title: str, message: str) -> ft.Container:
    return ft.Container(
        content=Content(title, message),
        alignment=ft.Alignment(0, 0),
        expand=True
    )