from pathlib import Path

import flet as ft
from app.config import settings
from app.view.components.common import FONTS
from app.view.components.ui.fallback import Page


def Fallback(page: ft.Page, title: str, message: str, width: int, height: int, bgImg: str | None = None) -> None:
    page.padding = 0
    page.window.width = width
    page.window.height = height
    page.window.resizable = False
    page.title = settings.APP_NAME
    page.window.maximizable = False
    page.bgcolor = settings.APP_PAGE_BG_DARK_COLOR
    
    page.fonts = FONTS

    page.clean()
    
    page.add(ft.Container(
        content=Page(title, message),        
        expand=True,                          
        bgcolor=settings.APP_PAGE_BG_DARK_COLOR,
        image=ft.DecorationImage(
            src=bgImg, 
            fit=ft.BoxFit.COVER,
            opacity=1.0
        ),
    ))