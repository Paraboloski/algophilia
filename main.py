import flet as ft
from pathlib import Path
from app.view.fallback import Fallback
from app.data.database import Database
from app.core.exception import AppError
from app.config import logger, settings
from app.services.registry import load_all

logger.init(Path(__file__).parent)

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


def main(page: ft.Page) -> None:

    async def start() -> None:
        try:
            db = await init_app()
            page.session.store.set("db", db)
            logger.info("init OK")
        except AppError as e:
            Fallback(page, "Errore applicativo", str(e))

    page.run_task(start)
    page.on_close = lambda _: logger.shutdown()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
