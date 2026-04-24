import aiosqlite
from pathlib import Path
from typing import Literal
from app.config.logger import logger
from app.core.exception import DataError
from app.core.result import Ok, Err, Result

class Database:
    def __init__(self, db: str | Path, schema: str | Path):
        self.db = Path(db)
        self.schema = Path(schema)
        self.db.parent.mkdir(parents=True, exist_ok=True)
        self.connection: aiosqlite.Connection | None = None
        logger.info(f"Database inizializzato — db={self.db.name}, schema={self.schema.name}")

    async def connect(self) -> Result[None]:
        logger.info(f"Connessione a {self.db.name}")
        try:
            self.connection = await aiosqlite.connect(self.db)
            self.connection.row_factory = aiosqlite.Row
            result = await self._populate()
            if not result.is_ok():
                await self.close()
            else:
                logger.info(f"Connesso a {self.db.name}")
            return result
        except Exception as e:
            logger.error(f"Connessione a {self.db.name} fallita", exc=e)
            return Err(DataError(f"Connessione fallita: {e}"))

    async def _populate(self) -> Result[None]:
        if self.connection is None:
            return Err(DataError("Non connesso"))
            
        async with self.connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' LIMIT 1"
            ) as q:
            if await q.fetchone() is not None:
                return Ok(None)
                
        if not self.schema.exists():
            logger.error(f"Schema non trovato: {self.schema}")
            return Err(DataError(f"Schema non trovato: '{self.schema}'"))
        try:
            logger.debug(f"Applicazione schema: {self.schema.name}")
            await self.connection.executescript(self.schema.read_text(encoding="utf-8"))
            await self.connection.commit()
            logger.debug("Schema applicato")
            return Ok(None)
        except Exception as e:
            logger.error("Applicazione schema fallita", exc=e)
            return Err(DataError(f"Schema: {e}"))

    async def execute(
        self,
        sql: str,
        params: tuple = (),
        fetch: Literal["all", "one", "none"] = "none",
    ) -> Result[list[aiosqlite.Row] | aiosqlite.Row | None | int]:
        if self.connection is None:
            logger.error("Esecuzione query senza connessione attiva")
            return Err(DataError("Non connesso"))
        try:
            logger.debug(f"[{fetch.upper()}] {sql.strip()} | params={params}")
            async with self.connection.execute(sql, params) as cursor:
                if fetch == "all":
                    rows = list(await cursor.fetchall())
                    logger.debug(f"{len(rows)} righe restituite")
                    return Ok(rows)
                if fetch == "one":
                    row = await cursor.fetchone()
                    logger.debug(f"{'1 riga restituita' if row else 'Nessuna riga trovata'}")
                    return Ok(row)
                await self.connection.commit()
                logger.debug(f"Scrittura completata — lastrowid={cursor.lastrowid or 0}")
                return Ok(cursor.lastrowid or 0)
        except Exception as e:
            logger.error(f"Query fallita: {sql.strip()}", exc=e)
            return Err(DataError(f"Query fallita: {e}"))

    async def commit(self) -> Result[None]:
        if self.connection is None:
            return Err(DataError("Non connesso"))
        try:
            await self.connection.commit()
            logger.debug("Commit eseguito")
            return Ok(None)
        except Exception as e:
            logger.error("Commit fallito", exc=e)
            return Err(DataError(f"Commit fallito: {e}"))

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            self.connection = None
            logger.info(f"Connessione a {self.db.name} chiusa")