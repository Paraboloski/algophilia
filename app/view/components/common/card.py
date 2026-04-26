import flet as ft


def Card(
    content: ft.Control,
    border_radius: ft.BorderRadius,
    blur_radius: int,
    shadow_color: str,
    shadow_offset: ft.Offset
) -> ft.Container:

    return ft.Container(
        content=content,
        border_radius=border_radius,
        shadow=ft.BoxShadow(
            blur_radius=blur_radius,
            color=shadow_color,
            offset=shadow_offset,
        ),
    )
