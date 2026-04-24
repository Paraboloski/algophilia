import flet as ft

def Label(value: str, color: str, font_family: str, size: int, letter_spacing: int, text_align) -> ft.Text:
    return ft.Text(
        value=value.upper(),
        size=size,
        color=color,
        font_family=font_family,
        text_align=text_align,
        style=ft.TextStyle(
            letter_spacing=letter_spacing,
        )
    )