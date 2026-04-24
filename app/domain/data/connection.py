import aiosqlite
from pathlib import Path
from app.config.logger import logger
from app.core.result import Ok, Err, Result
from app.core.exception import SchemaNotFound, ConnectionError

class DatabaseConnect:
    db: Path
    schema: Path
    _conn: aiosqlite.Connection | None

    async def connect(self) -> Result[None]:
        logger.info(f"Connessione a {self.db.name}")
        try:
            self._conn = await aiosqlite.connect(self.db)
            self._conn.row_factory = aiosqlite.Row
            result = await self._populate()
            if not result.is_ok():
                await self.close()
            else:
                logger.info(f"Connesso a {self.db.name}")
            return result
        except Exception as e:
            logger.error(f"Connessione a {self.db.name} fallita", exc=e)
            return Err(ConnectionError(f"Connessione fallita: {e}"))

    async def _populate(self) -> Result[None]:
        if self._conn is None:
            return Err(ConnectionError("Non connesso"))
        if not self.schema.exists():
            logger.error(f"Schema non trovato: {self.schema}")
            return Err(SchemaNotFound(self.schema))
        try:
            logger.debug(f"Applicazione schema: {self.schema.name}")
            await self._conn.executescript(self.schema.read_text(encoding="utf-8"))
            await self._conn.commit()
            logger.debug("Schema applicato")
            return Ok(None)
        except Exception as e:
            logger.error("Applicazione schema fallita", exc=e)
            return Err(ConnectionError(f"Schema: {e}"))

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
            logger.info(f"Connessione a {self.db.name} chiusa")

    async def commit(self) -> Result[None]:
        if self._conn is None:
            return Err(ConnectionError("Non connesso"))
        try:
            await self._conn.commit()
            logger.debug("Commit eseguito")
            return Ok(None)
        except Exception as e:
            logger.error("Commit fallito", exc=e)
            return Err(ConnectionError(f"Commit fallito: {e}"))