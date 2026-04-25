import flet as ft
from pathlib import Path
from app.core.result import Err
from app.data.database import Database
from app.core.exception import AppError
from app.data.seeder import seed_database
from app.services.registry import load_all
from app.config import logger, Log, LoggingLevel, settings, Panic
from app.view.components.ui.toast import ToastLevel, ToastManager

logger.init(Path(__file__).parent)

_LEVEL_MAP = {
    LoggingLevel.INFO:    ToastLevel.INFO,
    LoggingLevel.WARNING: ToastLevel.WARNING,
    LoggingLevel.ERROR:   ToastLevel.ERROR,
}

class AppContext:
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast = ToastManager(page, 20)

async def init_app() -> Database:
    load_all()

    db = Database(
        db=settings.DATABASE_PATH,
        schema=settings.SCHEMA_PATH
    )

    _conn = await db.connect()
    if isinstance(_conn, Err):
        Panic._panic(f"Impossibile connettersi al database: {_conn.error}")

    _seed = await seed_database(db)
    if isinstance(_seed, Err):
        Panic._panic(f"Inizializzazione dati (seeding) fallita: {_seed.error}")

    return db

def main(page: ft.Page) -> None:
    ctx = AppContext(page)

    def _on_log(log: Log) -> None:
        toast_level = _LEVEL_MAP.get(log.level)
        if toast_level is None:
            return
        ctx.toast.show(log.message, toast_level)

    logger.subscribe(_on_log)

    async def start() -> None:
        try:
            db = await init_app()
            page.session.store.set("db", db)
            logger.info("init OK")
        except AppError as e:
            logger.error(f"init NOT OK: {str(e)}")

    page.run_task(start)
    page.on_close = lambda _: logger.shutdown()

if __name__ == "__main__":
    ft.run(main, assets_dir="app/assets")
