import flet as ft
from pathlib import Path

def Icon(path: Path, size: int) -> ft.Image:
    return ft.Image(
        src=str(path),
        width=size,
        height=size,
    )