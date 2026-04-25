from typing import cast

import flet as ft
from pathlib import Path
from app.view.fallback import Fallback
from app.data.database import Database
from app.core.exception import AppError
from app.services.registry import load_all
from app.config import logger, Log, LoggingLevel, settings
from app.view.components.ui.toast import ToastLevel, ToastManager

logger.init(Path(__file__).parent)

_LEVEL_MAP = {
    LoggingLevel.INFO:    ToastLevel.INFO,
    LoggingLevel.WARNING: ToastLevel.WARNING,
    LoggingLevel.ERROR:   ToastLevel.ERROR,
}


async def init_app() -> Database:
    load_all()

    db = Database(
        db=settings.DATABASE_PATH,
        schema=settings.SCHEMA_PATH
    )

    (await db.connect()).unwrap()
    from app.data.seeder import seed_database
    (await seed_database(db)).unwrap()

    return db


class PageWithToast(ft.Page):
    toast: "ToastManager"


def main(page: ft.Page) -> None:
    bgIMG = str(settings.APP_PAGE_BG_FALLBACK_IMG)
    width = int(settings.APP_PAGE_WIGHT)
    height = int(settings.APP_PAGE_HEIGHT)
    
    page.window.width = width
    page.window.height = height
    page = cast(PageWithToast, page)
    page.toast = ToastManager(page, 20)
    
    def _on_log(log: Log) -> None:
        toast_level = _LEVEL_MAP.get(log.level)
        if toast_level is None:
            return
        page.toast.show(log.message, toast_level)

    logger.subscribe(_on_log)

    async def start() -> None:
        try:
            db = await init_app()
            page.session.store.set("db", db)
            logger.info("init OK")
            Fallback(
                page,
                "OK",
                "DB seeded",
                width,
                height,
                bgIMG
            )
        except AppError as e:
            Fallback(
                page,
                "Errore applicativo",
                str(e),
                width,
                height,
                bgIMG
            )

    page.run_task(start)
    page.on_close = lambda _: logger.shutdown()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
