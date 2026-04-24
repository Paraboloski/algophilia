import flet as ft
from pathlib import Path
from app.core.exception import Error
from app.view.fallback import Fallback
from app.config import logger, settings
from app.services.registry import load_all
from app.domain.data.database import Database

_DIR = Path(__file__).parent
logger.init(_DIR)

async def init_app() -> Database:
    load_all()

    db = Database(
        db=settings.DATABASE_PATH,
        schema=settings.SCHEMA_PATH
    )

    (await db.connect()).unwrap()
    (await db.seed()).unwrap()

    return db


def main(page: ft.Page) -> None:

    async def start() -> None:
        try:
            db = await init_app()
            page.session.store.set("db", db)
            logger.info("init OK")
        except Error as e:
            Fallback(page, "Errore applicativo", str(e))
        except Exception as e:
            Fallback(page, "Errore critico", str(e))

    page.run_task(start)
    page.on_close = lambda _: logger.shutdown()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
