import sys
import flet as ft
from app.view.app import App
from app.config import Container
from app.middleware import Result, Ok, Err
from app.middleware.exception import AppError

async def bootstrap(container: Container) -> Result:
    logger = container.logger()
    telegram = container.telegram()
    
    logger.subscribe(telegram.send)
    
    db = container.database()
    result = await db.start()
    
    if isinstance(result, Err):
        logger.error("Bootstrap: Errore inizializzazione DB", result.error)
        return result

    return Ok(True)

async def main(page: ft.Page):
    container = Container()
    
    def cleanup():
        container.worker().shutdown()
        container.logger()._directory._rmdir()

    page.on_disconnect = lambda _: cleanup()
    page.on_close = lambda _: cleanup()

    try:
        await bootstrap(container)
        app = App(page, container)
        await app.build()
    except AppError:
        sys.exit(1)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ft.run(
        main, 
        assets_dir="app/assets"
    )
