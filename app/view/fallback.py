import flet as ft
from app.config import settings
from app.view.components.ui.fallback import Page


def Fallback(page: ft.Page, title: str, message: str) -> None:
    page.padding = 0
    page.window.resizable = False
    page.title = settings.APP_NAME
    page.window.maximizable = False
    page.bgcolor = settings.APP_PAGE_BG_COLOR
    page.window.width = settings.APP_PAGE_WIGHT
    page.window.height = settings.APP_PAGE_HEIGHT
    
    page.fonts = {
        "Cinzel Bold":      settings.FONT_CINZEL_BOLD,
        "Cinzel Black":     settings.FONT_CINZEL_BLACK,
        "Cinzel Medium":    settings.FONT_CINZEL_MEDIUM,
        "Cinzel Regular":   settings.FONT_CINZEL_REGULAR,
        "Cinzel SemiBold":  settings.FONT_CINZEL_SEMIBOLD,
        "Cinzel ExtraBold": settings.FONT_CINZEL_EXTRABOLD,
    }

    page.clean()
    
    page.add(ft.Container(
        content=Page(title, message),        
        expand=True,                          
        bgcolor=settings.APP_PAGE_BG_COLOR,
        image=ft.DecorationImage(
            src=settings.APP_PAGE_BG_FALLBACK_IMG, 
            fit=ft.BoxFit.COVER,
            opacity=1.0
        ),
    ))