import flet as ft


def Title(value: str, color: str, font_family: str, size: int, text_align: ft.TextAlign) -> ft.Container:
    return ft.Container(
        content=ft.Text(
            value=value,
            size=size,
            weight=ft.FontWeight.BOLD,
            color=color,
            font_family=font_family,
            text_align=text_align
        ),
    )
