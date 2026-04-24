import aiosqlite
from pathlib import Path
from app.config.logger import logger
from app.domain.data.seeder import DataSeeder
from app.domain.data.executor import QueryExecutor
from app.domain.data.connection import DatabaseConnect

class Database(DataSeeder, QueryExecutor, DatabaseConnect):
    def __init__(self, db: str | Path, schema: str | Path):
        self.db     = Path(db)
        self.schema = Path(schema)
        self._conn: aiosqlite.Connection | None = None
        logger.info(f"Database inizializzato — db={self.db.name}, schema={self.schema.name}")

    @property
    def connection(self) -> aiosqlite.Connection | None:
        return self._conn