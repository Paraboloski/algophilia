import flet as ft
from app.config import Container
from app.view.components.ui.toast import ToastManager
from app.view.style import settings

class App:
    def __init__(self, page: ft.Page, container: Container):
        self.page = page
        self.container = container
        
        self.toast = ToastManager(page, safe_area_top=40)
        
        self.page.title = settings._app_name
        self.page.window.width = settings._main_width
        self.page.window.height = settings._main_height
        self.page.padding = 0
        self.page.bgcolor = settings._main_colors["bg_dark"]
        
        self.page.fonts = {
            name: str(path) for name, path in settings._main_fonts.items()
        }

    async def build(self):
        bg_image = ft.Image(
            src=str(settings._main_images["bg_fallback"]),
            fit=ft.BoxFit.COVER,
            width=self.page.width,
            height=self.page.height,
            opacity=0.3,
        )

        content = ft.Column(
            controls=[
                ft.Text(
                    settings._app_name,
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=settings._main_colors["bg_light"],
                    font_family="cinzel_bold",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.page.add(ft.Stack(
            controls=[
                ft.Container(
                    content=bg_image,
                    expand=True,
                ),
                ft.Container(
                    content=content,
                    alignment=ft.alignment.Alignment(0, 0),
                    expand=True,
                ),
            ],
            expand=True,
            alignment=ft.alignment.Alignment(0, 0),
        ))

        self.toast.info("Benvenuto in Algophilia!")
        self.page.update()