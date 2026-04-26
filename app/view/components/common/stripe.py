import flet as ft


def Stripe(color: str) -> ft.Container:
    return ft.Container(
        width=12,
        bgcolor=color,
        border_radius=ft.border_radius.only(top_left=8, bottom_left=8),
    )
