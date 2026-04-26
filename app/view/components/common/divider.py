import flet as ft


def Divider(color: str, height: int, width: int) -> ft.Container:
    return ft.Container(
        bgcolor=color,
        height=height,
        width=width,
        border_radius=ft.BorderRadius.all(4),
    )
